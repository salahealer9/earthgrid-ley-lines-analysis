#!/usr/bin/env python3
"""
population_corridor_test.py  (v2: with bearing-controlled null)

Population corridor test (Null 1 from POPULATION_CORRIDOR_PROTOCOL.md).

Inverts the original corridor null test:
  - Original test: catalog fixed, corridor randomized over the catalog's
    own structure (lon_shuffle / uniform_sphere / lon_uniform).
    Asks: are these specific N sites unusually well-aligned?
  - This test:  corridor fixed at the canonical pole, catalog comes from
    an exhaustive independent reference set; corridor is randomized
    by sampling uniform random great-circle poles whose great circle
    passes through the bounding box.
    Asks: does the canonical corridor over-populate this independent
    catalog more than a random great circle through the same region?

Two null modes:

  (default) "isotropic" — random pole uniform on S², subject only to the
  constraint that the corresponding great circle passes through the bbox.
  This was the original Null 1.

  --bearing-tolerance D  "bearing-restricted" — additionally constrains
  the random great circle's bearing at the bbox center to be within D
  degrees of the canonical great circle's bearing at the same point
  (undirected, so a 60-degree corridor and a 240-degree corridor are
  equivalent).
  This addresses the orientation confound: most random great circles
  through the UK bbox run E-W or N-S and miss the NE-SW British
  landmass diagonal, which inflates significance in the isotropic mode
  for any catalog of British sites. The bearing-restricted null compares
  the canonical corridor only against great circles oriented like
  Britain itself.

Test statistic:
  K_real(w) = number of catalog sites within w km of the canonical great
  circle (perpendicular spherical distance).

p-value (one-sided): (#{K_t >= K_real} + 1) / (T + 1)
z-score: (K_real - mean(K_t)) / std(K_t)

Math:
  Both the canonical and random "corridors" are great circles, each
  represented by its (unit) pole vector n. For a unit vector p (a site),
  the perpendicular spherical distance from p to the great circle is
  arcsin(|p . n|) * R_earth.

Usage:
  python population_corridor_test.py \\
    --catalog data/population/catalog_B1_strict.csv \\
    --canonical-pole 33.330 -147.354 \\
    --bbox 49.5 -6.5 53.5 2.5 \\
    --widths-km 5 10 20 50 100 \\
    --trials 10000 \\
    --out results_corridor/population/B1_canonical130.json
"""

from __future__ import annotations
import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np


R_EARTH_KM = 6371.0


# ============================================================================
# Geometry
# ============================================================================

def latlon_to_xyz(lat_deg, lon_deg):
    """Convert (lat, lon) in degrees to unit 3-vectors. Broadcasts."""
    lat = np.radians(np.asarray(lat_deg, dtype=np.float64))
    lon = np.radians(np.asarray(lon_deg, dtype=np.float64))
    return np.stack([
        np.cos(lat) * np.cos(lon),
        np.cos(lat) * np.sin(lon),
        np.sin(lat),
    ], axis=-1)


def perp_dist_km(points_xyz, pole_xyz):
    """Perpendicular spherical distance (km) from each point to the great
    circle whose pole is pole_xyz. Both inputs are unit vectors.
    points_xyz: (N, 3) or (3,);  pole_xyz: (3,) or (T, 3)."""
    dot = np.abs(np.einsum("...i,...i->...", points_xyz, pole_xyz)) \
        if points_xyz.ndim == 1 and pole_xyz.ndim == 1 \
        else np.abs(points_xyz @ pole_xyz.T) if pole_xyz.ndim == 2 \
        else np.abs(points_xyz @ pole_xyz)
    return np.arcsin(np.clip(dot, 0.0, 1.0)) * R_EARTH_KM


def gc_bearing_at_point(pole_xyz, point_xyz):
    """Undirected bearing in [0, 180) of the great circle (with pole = pole_xyz)
    at the closest point on that great circle to point_xyz.

    Bearing convention: 0 = north, 90 = east. Undirected because a corridor
    has no inherent direction (60-degree and 240-degree corridors are the same).
    """
    n = pole_xyz / np.linalg.norm(pole_xyz)
    p = point_xyz / np.linalg.norm(point_xyz)
    # Closest point on the GC to p
    q_unnorm = p - np.dot(p, n) * n
    q = q_unnorm / np.linalg.norm(q_unnorm)
    # Tangent direction along the GC at q
    t = np.cross(n, q)
    t = t / np.linalg.norm(t)
    # Local east-north basis at q
    lat_q = np.arcsin(np.clip(q[2], -1.0, 1.0))
    lon_q = np.arctan2(q[1], q[0])
    east  = np.array([-np.sin(lon_q),                 np.cos(lon_q),                 0.0])
    north = np.array([-np.sin(lat_q) * np.cos(lon_q), -np.sin(lat_q) * np.sin(lon_q), np.cos(lat_q)])
    bearing_rad = np.arctan2(np.dot(t, east), np.dot(t, north))
    return float(np.degrees(bearing_rad) % 180.0)


def gc_bearings_vectorized(poles_xyz, point_xyz):
    """Bearings (T,) for many great circles, evaluated at the closest point on each
    to a fixed location point_xyz. Returns degrees in [0, 180)."""
    p = point_xyz / np.linalg.norm(point_xyz)
    n = poles_xyz                                              # (T, 3) — already unit
    dots = n @ p                                               # (T,)
    q_unnorm = p[None, :] - dots[:, None] * n                  # (T, 3)
    q = q_unnorm / np.linalg.norm(q_unnorm, axis=1, keepdims=True)
    t = np.cross(n, q)
    t = t / np.linalg.norm(t, axis=1, keepdims=True)
    lat_q = np.arcsin(np.clip(q[:, 2], -1.0, 1.0))
    lon_q = np.arctan2(q[:, 1], q[:, 0])
    east_x  = -np.sin(lon_q);                north_x = -np.sin(lat_q) * np.cos(lon_q)
    east_y  =  np.cos(lon_q);                north_y = -np.sin(lat_q) * np.sin(lon_q)
    # east_z = 0;                            north_z =  np.cos(lat_q)
    t_e = t[:, 0] * east_x  + t[:, 1] * east_y
    t_n = t[:, 0] * north_x + t[:, 1] * north_y + t[:, 2] * np.cos(lat_q)
    return np.degrees(np.arctan2(t_e, t_n)) % 180.0


def undirected_bearing_diff(b1, b2):
    """Minimum undirected difference between two bearings in [0, 180) degrees.
    Returns values in [0, 90]."""
    diff = np.abs(b1 - b2) % 180.0
    return np.minimum(diff, 180.0 - diff)


# ============================================================================
# Sampling
# ============================================================================

def sample_random_poles(n_trials, bbox_center_xyz, bbox_radius_km, rng,
                        bearing_constraint=None):
    """Uniform random poles on S², rejection-sampled so the corresponding
    great circle passes within bbox_radius_km of the bbox center.

    If bearing_constraint is given as (canonical_bearing_deg, tolerance_deg),
    additionally reject poles whose great circle's bearing at the bbox center
    differs from canonical_bearing by more than tolerance (undirected, mod 180)."""
    poles = []
    n_proposed = 0
    n_passed_bbox = 0
    while len(poles) < n_trials:
        batch = max(n_trials - len(poles), 1000) * 3
        v = rng.standard_normal((batch, 3))
        v /= np.linalg.norm(v, axis=1, keepdims=True)

        # First gate: corridor passes through bbox
        d_km = np.arcsin(np.clip(np.abs(v @ bbox_center_xyz), 0.0, 1.0)) * R_EARTH_KM
        bbox_keep = d_km <= bbox_radius_km
        v_pass = v[bbox_keep]
        n_proposed += batch
        n_passed_bbox += int(bbox_keep.sum())

        # Second gate (optional): bearing within tolerance of canonical
        if bearing_constraint is not None and v_pass.shape[0] > 0:
            canon_bearing, tol = bearing_constraint
            bearings = gc_bearings_vectorized(v_pass, bbox_center_xyz)
            diffs = undirected_bearing_diff(bearings, canon_bearing)
            v_pass = v_pass[diffs <= tol]

        for vk in v_pass:
            poles.append(vk.tolist())
            if len(poles) >= n_trials:
                break

    poles = np.array(poles[:n_trials], dtype=np.float64)
    accept_rate = n_trials / n_proposed
    bbox_pass_rate = n_passed_bbox / n_proposed if n_proposed else 0.0
    return poles, accept_rate, bbox_pass_rate


# ============================================================================
# Counting
# ============================================================================

def count_real(catalog_xyz, pole_xyz, widths_km):
    """K_real for one canonical pole at multiple widths. Returns list[int]."""
    d = np.arcsin(np.clip(np.abs(catalog_xyz @ pole_xyz), 0.0, 1.0)) * R_EARTH_KM
    return [int(np.sum(d <= w)) for w in widths_km]


def count_null(catalog_xyz, poles_xyz, widths_km, chunk=500):
    """K_null for many random poles at multiple widths. Returns (T, W) int array."""
    T = poles_xyz.shape[0]
    W = len(widths_km)
    out = np.zeros((T, W), dtype=np.int32)
    widths = np.asarray(widths_km, dtype=np.float64)
    for s in range(0, T, chunk):
        e = min(s + chunk, T)
        # (chunk, N) distances
        d = np.arcsin(np.clip(np.abs(poles_xyz[s:e] @ catalog_xyz.T), 0.0, 1.0)) * R_EARTH_KM
        for wi, w in enumerate(widths):
            out[s:e, wi] = np.sum(d <= w, axis=1)
    return out


# ============================================================================
# I/O
# ============================================================================

def load_catalog(path):
    """Load (lat, lon) pairs from CSV with 'lat' and 'lon' columns. Skips bad rows."""
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "lat" not in reader.fieldnames or "lon" not in reader.fieldnames:
            raise ValueError(f"{path}: missing 'lat'/'lon' columns; have {reader.fieldnames}")
        for r in reader:
            try:
                lat = float(r["lat"])
                lon = float(r["lon"])
            except (KeyError, ValueError, TypeError):
                continue
            rows.append((lat, lon))
    if not rows:
        raise ValueError(f"{path}: no valid (lat, lon) rows")
    arr = np.array(rows, dtype=np.float64)
    return arr


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--catalog", required=True,
                    help="CSV with 'lat' and 'lon' columns")
    ap.add_argument("--canonical-pole", nargs=2, type=float, required=True,
                    metavar=("LAT", "LON"),
                    help="Canonical great-circle pole, lat lon in degrees")
    ap.add_argument("--bbox", nargs=4, type=float,
                    default=[49.5, -6.5, 53.5, 2.5],
                    metavar=("S", "W", "N", "E"),
                    help="Bounding box: south west north east (deg). Default UK box.")
    ap.add_argument("--widths-km", nargs="+", type=float,
                    default=[5, 10, 20, 50, 100])
    ap.add_argument("--trials", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--bearing-tolerance", type=float, default=None,
                    help="If set, restrict random corridors to those with bearing "
                         "(at bbox center) within this many degrees of the canonical "
                         "corridor's bearing (undirected, mod 180). Tests whether the "
                         "canonical corridor is exceptional WITHIN the family of "
                         "similarly-oriented corridors. Typical values: 5, 15, 30.")
    ap.add_argument("--out", required=True, help="Output JSON path")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)

    # Catalog
    print(f"Loading catalog from {args.catalog} ...")
    cat_latlon = load_catalog(args.catalog)
    cat_xyz = latlon_to_xyz(cat_latlon[:, 0], cat_latlon[:, 1])
    N = cat_xyz.shape[0]
    print(f"  {N} sites loaded")

    # Canonical pole
    cp_lat, cp_lon = args.canonical_pole
    canonical_xyz = latlon_to_xyz(cp_lat, cp_lon)
    print(f"Canonical pole : ({cp_lat:.4f}, {cp_lon:.4f})")

    # BBox geometry — center and half-diagonal in km
    south, west, north, east = args.bbox
    cen_lat = (south + north) / 2
    cen_lon = (west + east) / 2
    bbox_center_xyz = latlon_to_xyz(cen_lat, cen_lon)
    dlat = (north - south) / 2.0
    dlon = (east - west) / 2.0
    cos_lat = np.cos(np.radians(cen_lat))
    half_diag_deg = np.sqrt(dlat**2 + (dlon * cos_lat) ** 2)
    bbox_radius_km = float(R_EARTH_KM * np.radians(half_diag_deg))
    print(f"BBox center    : ({cen_lat:.2f}, {cen_lon:.2f}); "
          f"half-diagonal {bbox_radius_km:.0f} km (corridor-pass tolerance)")

    # Canonical bearing at bbox center (always computed for reporting; only
    # used as a constraint if --bearing-tolerance is set).
    canon_bearing = gc_bearing_at_point(canonical_xyz, bbox_center_xyz)
    print(f"Canonical bearing at bbox center: {canon_bearing:.2f} deg "
          f"(undirected, 0=N, 90=E)")

    bearing_constraint = None
    if args.bearing_tolerance is not None:
        bearing_constraint = (canon_bearing, args.bearing_tolerance)
        print(f"Bearing-restricted null: random corridors must have bearing "
              f"within +/-{args.bearing_tolerance:.1f} deg of canonical "
              f"(i.e. in [{(canon_bearing - args.bearing_tolerance) % 180:.1f}, "
              f"{(canon_bearing + args.bearing_tolerance) % 180:.1f}] deg)")
    else:
        print("Isotropic null: random corridors uniform on S^2 subject to bbox-pass.")

    # Real
    K_real = count_real(cat_xyz, canonical_xyz, args.widths_km)
    print("\nReal corridor counts:")
    for w, k in zip(args.widths_km, K_real):
        print(f"  w = {w:>5.1f} km : K_real = {k}  ({100*k/N:.1f}% of catalog)")

    # Null
    print(f"\nSampling {args.trials} random great-circle corridors through bbox ...")
    t0 = time.time()
    poles, accept_rate, bbox_pass_rate = sample_random_poles(
        args.trials, bbox_center_xyz, bbox_radius_km, rng,
        bearing_constraint=bearing_constraint)
    print(f"  sampled in {time.time()-t0:.1f}s; "
          f"bbox pass-rate ~ {bbox_pass_rate:.2%}, "
          f"final acceptance ~ {accept_rate:.2%}")

    print(f"Computing K_null over {args.trials} corridors x {N} sites x {len(args.widths_km)} widths ...")
    t0 = time.time()
    K_null = count_null(cat_xyz, poles, args.widths_km)
    print(f"  K_null computed in {time.time()-t0:.1f}s")

    # Stats
    results = []
    print("\n" + "=" * 60)
    print("RESULTS  (population null test, fixed canonical corridor)")
    print("=" * 60)
    for wi, w in enumerate(args.widths_km):
        K_r = K_real[wi]
        K_n = K_null[:, wi]
        mean_n = float(np.mean(K_n))
        std_n  = float(np.std(K_n))
        max_n  = int(np.max(K_n))
        min_n  = int(np.min(K_n))
        n_ge   = int(np.sum(K_n >= K_r))
        p      = (n_ge + 1) / (args.trials + 1)
        z      = (K_r - mean_n) / std_n if std_n > 0 else float("inf")
        results.append({
            "width_km": w,
            "K_real": K_r,
            "K_real_pct": 100.0 * K_r / N,
            "K_null_mean": mean_n,
            "K_null_std": std_n,
            "K_null_min": min_n,
            "K_null_max": max_n,
            "k_null_ge_real": n_ge,
            "p_oneside": p,
            "z_score": z,
        })
        print(f"\nw = {w} km")
        print(f"  K_real          : {K_r}  ({100*K_r/N:.2f}% of catalog)")
        print(f"  K_null mean±std : {mean_n:.2f} ± {std_n:.2f}")
        print(f"  K_null range    : [{min_n}, {max_n}]")
        print(f"  k(null >= real) : {n_ge} / {args.trials}")
        print(f"  p (one-sided)   : {p:.4f}")
        print(f"  z-score         : {z:.2f}")

    # Bonferroni line
    n_widths = len(args.widths_km)
    bonf_per_width = 0.05 / n_widths
    print(f"\nBonferroni-adjusted threshold (family-wise alpha = 0.05, "
          f"{n_widths} widths): per-width p < {bonf_per_width:.4f}")

    # Save
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    payload = {
        "catalog_path": args.catalog,
        "catalog_size": N,
        "canonical_pole_lat_lon": [cp_lat, cp_lon],
        "canonical_bearing_at_bbox_center_deg": canon_bearing,
        "bearing_tolerance_deg": args.bearing_tolerance,  # None if isotropic
        "null_mode": "bearing_restricted" if args.bearing_tolerance is not None else "isotropic",
        "bbox_swne": [south, west, north, east],
        "bbox_radius_km": bbox_radius_km,
        "trials": args.trials,
        "seed": args.seed,
        "widths_km": list(args.widths_km),
        "results": results,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nSummary written to : {args.out}")


if __name__ == "__main__":
    sys.exit(main() or 0)
