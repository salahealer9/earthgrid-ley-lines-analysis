#!/usr/bin/env python3
"""
triple_corridor_test.py

Joint population corridor test across multiple reference catalogs.

Generalizes population_corridor_test.py: instead of running one catalog at a
time, samples the random corridor poles ONCE and computes K per (trial, catalog,
width). This permits:

  - Per-catalog marginal p-values (reproduces the per-catalog tests)
  - CONJUNCTION p-value: fraction of random corridors whose K equals or exceeds
    the canonical K simultaneously on ALL catalogs at the same width.
  - Pairwise conjunctions: A & B1, A & B2, B1 & B2 (useful for discussion).
  - Pearson correlation of K across trials, per catalog pair (tells us how
    dependent the catalogs are; informs interpretation of the conjunction).

The conjunction test answers a stricter question than the per-catalog tests:
  "Could a single random great circle through the UK bbox match or beat the
   canonical Michael corridor's site count on prehistoric monuments AND
   Michael churches AND broad archaeology, all at once?"

It's not a replacement for the per-catalog tests — it tightens them into a
single statistic. The catalogs are correlated (corridors that catch many B1
sites tend to also catch many B2 sites), so the conjunction p-value lies
between the maximum marginal p-value and the (incorrect) product of marginals.

The same null sampling logic as population_corridor_test.py is used:
isotropic mode by default; --bearing-tolerance D activates the bearing-
restricted null at +/- D degrees of the canonical bearing.

Usage:
  python triple_corridor_test.py \\
    --catalog data/population/catalog_B1_strict.csv:B1 \\
    --catalog data/population/catalog_A_michael.csv:A \\
    --catalog data/population/catalog_B2_broad.csv:B2 \\
    --canonical-pole 33.330 -147.354 \\
    --bbox 49.5 -6.5 53.5 2.5 \\
    --widths-km 5 10 20 50 100 \\
    --bearing-tolerance 15 \\
    --trials 10000 \\
    --out-prefix results_corridor/population/triple_canonical130_bearing15

  Each --catalog is "PATH:LABEL" (label used in output column names).
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
# Geometry (shared with population_corridor_test.py)
# ============================================================================

def latlon_to_xyz(lat_deg, lon_deg):
    lat = np.radians(np.asarray(lat_deg, dtype=np.float64))
    lon = np.radians(np.asarray(lon_deg, dtype=np.float64))
    return np.stack([
        np.cos(lat) * np.cos(lon),
        np.cos(lat) * np.sin(lon),
        np.sin(lat),
    ], axis=-1)


def gc_bearing_at_point(pole_xyz, point_xyz):
    n = pole_xyz / np.linalg.norm(pole_xyz)
    p = point_xyz / np.linalg.norm(point_xyz)
    q_unnorm = p - np.dot(p, n) * n
    q = q_unnorm / np.linalg.norm(q_unnorm)
    t = np.cross(n, q); t /= np.linalg.norm(t)
    lat_q = np.arcsin(np.clip(q[2], -1.0, 1.0))
    lon_q = np.arctan2(q[1], q[0])
    east  = np.array([-np.sin(lon_q),                 np.cos(lon_q),                 0.0])
    north = np.array([-np.sin(lat_q) * np.cos(lon_q), -np.sin(lat_q) * np.sin(lon_q), np.cos(lat_q)])
    return float(np.degrees(np.arctan2(np.dot(t, east), np.dot(t, north))) % 180.0)


def gc_bearings_vectorized(poles_xyz, point_xyz):
    p = point_xyz / np.linalg.norm(point_xyz)
    n = poles_xyz
    dots = n @ p
    q_unnorm = p[None, :] - dots[:, None] * n
    q = q_unnorm / np.linalg.norm(q_unnorm, axis=1, keepdims=True)
    t = np.cross(n, q); t /= np.linalg.norm(t, axis=1, keepdims=True)
    lat_q = np.arcsin(np.clip(q[:, 2], -1.0, 1.0))
    lon_q = np.arctan2(q[:, 1], q[:, 0])
    east_x  = -np.sin(lon_q);                north_x = -np.sin(lat_q) * np.cos(lon_q)
    east_y  =  np.cos(lon_q);                north_y = -np.sin(lat_q) * np.sin(lon_q)
    t_e = t[:, 0] * east_x  + t[:, 1] * east_y
    t_n = t[:, 0] * north_x + t[:, 1] * north_y + t[:, 2] * np.cos(lat_q)
    return np.degrees(np.arctan2(t_e, t_n)) % 180.0


def undirected_bearing_diff(b1, b2):
    diff = np.abs(b1 - b2) % 180.0
    return np.minimum(diff, 180.0 - diff)


def sample_random_poles(n_trials, bbox_center_xyz, bbox_radius_km, rng,
                        bearing_constraint=None):
    poles = []
    points = []   # list of (lat1, lon1, lat2, lon2)
    n_proposed = 0
    n_passed_bbox = 0
    while len(poles) < n_trials:
        batch = max(n_trials - len(poles), 1000) * 3
        v = rng.standard_normal((batch, 3))
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        d_km = np.arcsin(np.clip(np.abs(v @ bbox_center_xyz), 0.0, 1.0)) * R_EARTH_KM
        bbox_keep = d_km <= bbox_radius_km
        v_pass = v[bbox_keep]
        n_proposed += batch
        n_passed_bbox += int(bbox_keep.sum())
        if bearing_constraint is not None and v_pass.shape[0] > 0:
            canon_bearing, tol = bearing_constraint
            bearings = gc_bearings_vectorized(v_pass, bbox_center_xyz)
            v_pass = v_pass[undirected_bearing_diff(bearings, canon_bearing) <= tol]
        for vk in v_pass:
            # Compute two points on the great circle: random orthogonal vectors
            pole = vk
            # Find a random orthogonal vector
            if abs(pole[0]) < 0.9:
                ref = np.array([1.0, 0.0, 0.0])
            else:
                ref = np.array([0.0, 1.0, 0.0])
            vec1 = np.cross(ref, pole)
            vec1 /= np.linalg.norm(vec1)
            vec2 = np.cross(pole, vec1)
            angle = 2 * np.pi * rng.random()
            p1 = vec1 * np.cos(angle) + vec2 * np.sin(angle)
            p2 = vec1 * np.cos(angle + np.pi/2) + vec2 * np.sin(angle + np.pi/2)
            def vec_to_latlon(v):
                lat = np.arcsin(np.clip(v[2], -1.0, 1.0)) * 180 / np.pi
                lon = np.arctan2(v[1], v[0]) * 180 / np.pi
                return lat, lon
            lat1, lon1 = vec_to_latlon(p1)
            lat2, lon2 = vec_to_latlon(p2)
            poles.append(pole.tolist())
            points.append((lat1, lon1, lat2, lon2))
            if len(poles) >= n_trials:
                break
    return (np.array(poles[:n_trials], dtype=np.float64),
            np.array(points[:n_trials], dtype=np.float64),
            n_trials / n_proposed,
            n_passed_bbox / n_proposed if n_proposed else 0.0)


def count_real(cat_xyz, pole_xyz, widths_km):
    d = np.arcsin(np.clip(np.abs(cat_xyz @ pole_xyz), 0.0, 1.0)) * R_EARTH_KM
    return [int(np.sum(d <= w)) for w in widths_km]


def count_null(cat_xyz, poles_xyz, widths_km, chunk=500):
    T = poles_xyz.shape[0]
    W = len(widths_km)
    out = np.zeros((T, W), dtype=np.int32)
    widths = np.asarray(widths_km, dtype=np.float64)
    for s in range(0, T, chunk):
        e = min(s + chunk, T)
        d = np.arcsin(np.clip(np.abs(poles_xyz[s:e] @ cat_xyz.T), 0.0, 1.0)) * R_EARTH_KM
        for wi, w in enumerate(widths):
            out[s:e, wi] = np.sum(d <= w, axis=1)
    return out


# ============================================================================
# I/O
# ============================================================================

def load_catalog(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "lat" not in reader.fieldnames or "lon" not in reader.fieldnames:
            raise ValueError(f"{path}: missing 'lat'/'lon' columns; have {reader.fieldnames}")
        for r in reader:
            try:
                rows.append((float(r["lat"]), float(r["lon"])))
            except (KeyError, ValueError, TypeError):
                continue
    if not rows:
        raise ValueError(f"{path}: no valid (lat, lon) rows")
    return np.array(rows, dtype=np.float64)


def parse_catalog_arg(s):
    if ":" in s:
        path, label = s.rsplit(":", 1)
    else:
        path = s
        label = os.path.splitext(os.path.basename(s))[0]
    return path, label


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--catalog", action="append", required=True,
                    help="PATH:LABEL of a reference catalog. May be specified "
                         "multiple times. Label is used in output columns.")
    ap.add_argument("--canonical-pole", nargs=2, type=float, required=True,
                    metavar=("LAT", "LON"))
    ap.add_argument("--bbox", nargs=4, type=float,
                    default=[49.5, -6.5, 53.5, 2.5],
                    metavar=("S", "W", "N", "E"))
    ap.add_argument("--widths-km", nargs="+", type=float,
                    default=[5, 10, 20, 50, 100])
    ap.add_argument("--trials", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--bearing-tolerance", type=float, default=None)
    ap.add_argument("--out-prefix", required=True,
                    help="Output prefix; writes <prefix>.summary.json and "
                         "<prefix>.trials.csv")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)

    # Catalogs
    cats = []  # list of (label, latlon, xyz)
    for arg in args.catalog:
        path, label = parse_catalog_arg(arg)
        latlon = load_catalog(path)
        xyz = latlon_to_xyz(latlon[:, 0], latlon[:, 1])
        cats.append({"label": label, "path": path, "N": xyz.shape[0],
                     "latlon": latlon, "xyz": xyz})
        print(f"[{label}] loaded {xyz.shape[0]} sites from {path}")

    # Geometry setup
    cp_lat, cp_lon = args.canonical_pole
    canonical_xyz = latlon_to_xyz(cp_lat, cp_lon)
    south, west, north, east = args.bbox
    cen_lat = (south + north) / 2
    cen_lon = (west + east) / 2
    bbox_center_xyz = latlon_to_xyz(cen_lat, cen_lon)
    dlat = (north - south) / 2.0
    dlon = (east - west) / 2.0
    cos_lat = np.cos(np.radians(cen_lat))
    half_diag_deg = np.sqrt(dlat**2 + (dlon * cos_lat) ** 2)
    bbox_radius_km = float(R_EARTH_KM * np.radians(half_diag_deg))
    canon_bearing = gc_bearing_at_point(canonical_xyz, bbox_center_xyz)
    print(f"\nCanonical pole : ({cp_lat:.4f}, {cp_lon:.4f})")
    print(f"BBox center    : ({cen_lat:.2f}, {cen_lon:.2f}); "
          f"half-diagonal {bbox_radius_km:.0f} km")
    print(f"Canonical bearing at bbox center: {canon_bearing:.2f} deg")

    bearing_constraint = None
    if args.bearing_tolerance is not None:
        bearing_constraint = (canon_bearing, args.bearing_tolerance)
        print(f"Bearing-restricted null: ±{args.bearing_tolerance:.1f} deg")
    else:
        print("Isotropic null.")

    # Real K per catalog
    K_real_by_label = {}
    print("\nReal corridor counts:")
    for c in cats:
        K_real = count_real(c["xyz"], canonical_xyz, args.widths_km)
        K_real_by_label[c["label"]] = K_real
        print(f"  [{c['label']}] N={c['N']}: " +
              ", ".join(f"w{w}={k}" for w, k in zip(args.widths_km, K_real)))

    # Null sampling — ONCE
    print(f"\nSampling {args.trials} corridors ...")
    t0 = time.time()
    poles, trial_points, accept_rate, bbox_pass_rate = sample_random_poles(
        args.trials, bbox_center_xyz, bbox_radius_km, rng,
        bearing_constraint=bearing_constraint)
    print(f"  sampled in {time.time()-t0:.1f}s; "
          f"bbox pass-rate ~ {bbox_pass_rate:.2%}, "
          f"final acceptance ~ {accept_rate:.2%}")

    # K_null for each catalog over the same poles
    K_null_by_label = {}
    for c in cats:
        t0 = time.time()
        K_null = count_null(c["xyz"], poles, args.widths_km)
        K_null_by_label[c["label"]] = K_null
        print(f"[{c['label']}] K_null computed in {time.time()-t0:.1f}s; "
              f"shape {K_null.shape}")

    # ----- Per-catalog marginals ------------------------------------------
    print("\n" + "=" * 60)
    print("PER-CATALOG MARGINALS  (sanity check vs the per-catalog runs)")
    print("=" * 60)
    marginals = {}
    for c in cats:
        label = c["label"]
        K_real = K_real_by_label[label]
        K_null = K_null_by_label[label]
        per_width = []
        print(f"\n[{label}] N={c['N']}")
        for wi, w in enumerate(args.widths_km):
            K_r = K_real[wi]
            K_n = K_null[:, wi]
            n_ge = int(np.sum(K_n >= K_r))
            p = (n_ge + 1) / (args.trials + 1)
            z = (K_r - np.mean(K_n)) / np.std(K_n) if np.std(K_n) > 0 else float("inf")
            per_width.append({
                "width_km": w, "K_real": K_r,
                "K_null_mean": float(np.mean(K_n)),
                "K_null_std": float(np.std(K_n)),
                "K_null_min": int(np.min(K_n)), "K_null_max": int(np.max(K_n)),
                "k_null_ge_real": n_ge, "p_oneside": p, "z_score": float(z),
            })
            print(f"  w={w:>5.1f}km  K_real={K_r:>4}  null={np.mean(K_n):.1f}±{np.std(K_n):.1f}  "
                  f"p={p:.4f}  z={z:.2f}")
        marginals[label] = per_width

    # ----- Conjunction p-values --------------------------------------------
    labels = [c["label"] for c in cats]
    print("\n" + "=" * 60)
    print("CONJUNCTION TESTS  (all catalogs simultaneously >= K_real)")
    print("=" * 60)
    conjunction = []
    for wi, w in enumerate(args.widths_km):
        # Build per-catalog "exceeds K_real" boolean vector
        masks = []
        thresholds = {}
        for label in labels:
            K_real = K_real_by_label[label][wi]
            K_null = K_null_by_label[label][:, wi]
            masks.append(K_null >= K_real)
            thresholds[label] = K_real
        joint_mask = np.all(np.stack(masks, axis=0), axis=0)
        n_joint = int(joint_mask.sum())
        p_joint = (n_joint + 1) / (args.trials + 1)
        # Pairwise conjunctions for diagnostic
        pairwise = {}
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                m_pair = masks[i] & masks[j]
                pairwise[f"{labels[i]}+{labels[j]}"] = {
                    "n": int(m_pair.sum()),
                    "p": float((int(m_pair.sum()) + 1) / (args.trials + 1)),
                }
        conjunction.append({
            "width_km": w,
            "thresholds": thresholds,
            "n_joint_ge_real_all": n_joint,
            "p_joint_all": p_joint,
            "pairwise": pairwise,
        })
        print(f"\nw={w:>5.1f} km, thresholds={thresholds}")
        print(f"  ALL {len(labels)} catalogs simultaneously: "
              f"{n_joint}/{args.trials} trials  ->  p_joint = {p_joint:.4f}")
        for pair, stats in pairwise.items():
            print(f"  {pair:>15} : {stats['n']:>4} trials  ->  p = {stats['p']:.4f}")

    # ----- Pairwise correlations of K across trials -----------------------
    print("\n" + "=" * 60)
    print("PEARSON CORRELATION of K across trials (catalog dependence)")
    print("=" * 60)
    correlations = {}
    for wi, w in enumerate(args.widths_km):
        per_w = {}
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                Ki = K_null_by_label[labels[i]][:, wi].astype(np.float64)
                Kj = K_null_by_label[labels[j]][:, wi].astype(np.float64)
                if Ki.std() > 0 and Kj.std() > 0:
                    r = float(np.corrcoef(Ki, Kj)[0, 1])
                else:
                    r = float("nan")
                per_w[f"{labels[i]}+{labels[j]}"] = r
        correlations[f"w_{w}"] = per_w
        print(f"\nw={w:>5.1f} km")
        for pair, r in per_w.items():
            print(f"  corr({pair}) = {r:+.3f}")

    # ----- Save outputs ----------------------------------------------------
    out_dir = os.path.dirname(args.out_prefix) or "."
    os.makedirs(out_dir, exist_ok=True)

    # Per-trial CSV
    csv_path = args.out_prefix + ".trials.csv"
    fields = ["trial", "lat1", "lon1", "lat2", "lon2"] + \
             [f"K_{label}_w{w}" for label in labels for w in args.widths_km]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(fields)
        for t in range(args.trials):
            lat1, lon1, lat2, lon2 = trial_points[t]   # <-- you need trial_points
            row = [t, lat1, lon1, lat2, lon2]
            for label in labels:
                for wi in range(len(args.widths_km)):
                    row.append(int(K_null_by_label[label][t, wi]))
            wr.writerow(row)
    print(f"\nPer-trial counts -> {csv_path}")

    # Summary JSON
    summary_path = args.out_prefix + ".summary.json"
    payload = {
        "catalogs": [{"label": c["label"], "path": c["path"], "N": c["N"]} for c in cats],
        "canonical_pole_lat_lon": [cp_lat, cp_lon],
        "canonical_bearing_at_bbox_center_deg": canon_bearing,
        "bearing_tolerance_deg": args.bearing_tolerance,
        "null_mode": "bearing_restricted" if args.bearing_tolerance is not None else "isotropic",
        "bbox_swne": [south, west, north, east],
        "bbox_radius_km": bbox_radius_km,
        "trials": args.trials,
        "seed": args.seed,
        "widths_km": list(args.widths_km),
        "K_real_by_catalog": {label: K_real_by_label[label] for label in labels},
        "marginals": marginals,
        "conjunction": conjunction,
        "correlations": correlations,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    with open(summary_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Summary          -> {summary_path}")

    # ----- Bonferroni reminder --------------------------------------------
    bonf = 0.05 / len(args.widths_km)
    print(f"\nBonferroni-adjusted threshold (alpha = 0.05, "
          f"{len(args.widths_km)} widths): per-width p < {bonf:.4f}")


if __name__ == "__main__":
    sys.exit(main() or 0)
