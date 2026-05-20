#!/usr/bin/env python3
"""
best_fit_great_circle.py

Fit the best-fit great circle to a set of (lat, lon) points by SVD on the
matrix of unit vectors. The best-fit pole minimizes the sum of squared
perpendicular spherical distances from the points to the great circle.

Math: given unit vectors p_i, find unit n minimizing sum (n . p_i)^2. This
is the smallest eigenvector of M = sum_i p_i p_i^T, equivalently the
smallest singular vector of the (N, 3) stacked point matrix.

Use case in this project: fit a great circle to the Mary / Michael
meandering current points extracted from the canonical KML, then test
whether that data-derived corridor gives equivalent significance to the
canonical 130-site straight-line corridor.

Usage:
  python best_fit_great_circle.py \\
    --points data/ley_lines/michael_ley_line/mary_current_points.csv \\
              data/ley_lines/michael_ley_line/michael_current_points.csv \\
    --label "Mary+Michael currents combined" \\
    --canonical-pole 33.330 -147.354 \\
    --kml-out results_corridor/best_fit_mary_michael.kml \\
    --json-out results_corridor/best_fit_mary_michael.json

Pass --points multiple times to combine multiple input files (e.g. Mary and
Michael currents) into one best-fit. Each file must have lat,lon columns.

Output:
  - The fitted pole as (lat, lon)
  - Residual statistics (RMS, max, distribution)
  - Angular and km offset from the optional --canonical-pole
  - Optional KML of the fitted great circle for visual comparison
"""

from __future__ import annotations
import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np


R_EARTH_KM = 6371.0


# ============================================================================
# Geometry
# ============================================================================

def latlon_to_xyz(lat_deg, lon_deg):
    lat = np.radians(np.asarray(lat_deg, dtype=np.float64))
    lon = np.radians(np.asarray(lon_deg, dtype=np.float64))
    return np.stack([
        np.cos(lat) * np.cos(lon),
        np.cos(lat) * np.sin(lon),
        np.sin(lat),
    ], axis=-1)


def xyz_to_latlon(xyz):
    xyz = xyz / np.linalg.norm(xyz)
    lat = np.degrees(np.arcsin(np.clip(xyz[2], -1, 1)))
    lon = np.degrees(np.arctan2(xyz[1], xyz[0]))
    return float(lat), float(lon)


def fit_best_great_circle(points_xyz):
    """SVD fit: returns the unit pole minimizing sum_i (pole . p_i)^2.
    Equivalently the eigenvector of M = sum p_i p_i^T with the smallest
    eigenvalue, or the smallest right singular vector of the stacked
    points matrix."""
    # Use SVD on the (N, 3) matrix. The smallest singular vector is the
    # direction of least variance, i.e. the great-circle normal.
    U, S, Vt = np.linalg.svd(points_xyz, full_matrices=False)
    pole = Vt[-1]                           # last row = smallest singular vector
    pole = pole / np.linalg.norm(pole)
    # Sign convention: pick the hemisphere where pole's z >= 0 (cosmetic; any
    # pole and its antipode define the same great circle).
    if pole[2] < 0:
        pole = -pole
    # Residual stats
    residuals_rad = np.arcsin(np.clip(np.abs(points_xyz @ pole), 0, 1))
    residuals_km = residuals_rad * R_EARTH_KM
    rms = float(np.sqrt(np.mean(residuals_km ** 2)))
    return pole, residuals_km, rms


def angular_separation_km(pole_a, pole_b):
    """Angular distance between two great-circle poles, as a surface km."""
    # Poles are undirected (n and -n are the same great circle), so use
    # the acute angle.
    cos_ang = np.clip(np.abs(np.dot(pole_a, pole_b)), 0, 1)
    return float(np.arccos(cos_ang) * R_EARTH_KM)


# ============================================================================
# I/O
# ============================================================================

def load_points(paths):
    """Load (lat, lon) from one or more CSVs. Returns (N, 2) array."""
    all_rows = []
    for p in paths:
        n_before = len(all_rows)
        with open(p, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if "lat" not in reader.fieldnames or "lon" not in reader.fieldnames:
                raise ValueError(f"{p}: missing 'lat'/'lon' columns; have {reader.fieldnames}")
            for r in reader:
                try:
                    all_rows.append((float(r["lat"]), float(r["lon"])))
                except (KeyError, ValueError, TypeError):
                    continue
        print(f"  loaded {len(all_rows) - n_before} valid points from {p}")
    return np.array(all_rows, dtype=np.float64)


def write_gc_kml(pole_xyz, label, color_hex_aabbggrr, kml_path, n_samples=720):
    """Write a KML LineString sampling the great circle whose pole is pole_xyz.
    The line is traced as a full 360-degree loop around the sphere."""
    # Two orthogonal vectors in the great-circle plane
    n = pole_xyz / np.linalg.norm(pole_xyz)
    # Pick an arbitrary vector not parallel to n, then orthogonalize
    e1 = np.array([1.0, 0.0, 0.0]) if abs(n[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    u = e1 - np.dot(e1, n) * n
    u = u / np.linalg.norm(u)
    v = np.cross(n, u)
    coords = []
    for t in np.linspace(0, 2 * np.pi, n_samples):
        p = np.cos(t) * u + np.sin(t) * v
        lat = np.degrees(np.arcsin(np.clip(p[2], -1, 1)))
        lon = np.degrees(np.arctan2(p[1], p[0]))
        coords.append(f"{lon:.6f},{lat:.6f},0")
    kml = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>{label}</name>
  <Placemark>
    <name>{label}</name>
    <Style>
      <LineStyle>
        <color>{color_hex_aabbggrr}</color>
        <width>3</width>
      </LineStyle>
    </Style>
    <LineString>
      <tessellate>1</tessellate>
      <coordinates>{' '.join(coords)}</coordinates>
    </LineString>
  </Placemark>
</Document>
</kml>
"""
    os.makedirs(os.path.dirname(kml_path) or ".", exist_ok=True)
    with open(kml_path, "w", encoding="utf-8") as f:
        f.write(kml)


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--points", nargs="+", required=True,
                    help="One or more CSVs of (lat, lon) points. All are combined "
                         "into a single best-fit.")
    ap.add_argument("--label", default="best-fit great circle",
                    help="Label used in KML output")
    ap.add_argument("--canonical-pole", nargs=2, type=float, default=None,
                    metavar=("LAT", "LON"),
                    help="Optional canonical pole (lat lon, degrees) for "
                         "side-by-side comparison")
    ap.add_argument("--kml-out", default=None,
                    help="Optional KML output path for the fitted great circle")
    ap.add_argument("--json-out", required=True,
                    help="Output JSON path for the fitted pole and statistics")
    args = ap.parse_args()

    # Load
    print(f"Loading points from {len(args.points)} file(s) ...")
    latlons = load_points(args.points)
    N = latlons.shape[0]
    if N < 3:
        print(f"ERROR: need at least 3 points to fit a great circle, got {N}",
              file=sys.stderr)
        return 2
    print(f"Total: {N} points")
    xyz = latlon_to_xyz(latlons[:, 0], latlons[:, 1])

    # Fit
    print("\nFitting best-fit great circle (SVD on unit vectors) ...")
    pole_xyz, residuals_km, rms_km = fit_best_great_circle(xyz)
    pole_lat, pole_lon = xyz_to_latlon(pole_xyz)
    max_residual = float(residuals_km.max())
    median_residual = float(np.median(residuals_km))
    p95_residual = float(np.percentile(residuals_km, 95))

    print(f"\nFitted pole : ({pole_lat:.4f}, {pole_lon:.4f}) deg")
    print(f"Residuals (perpendicular distance from each point to the GC):")
    print(f"  RMS    : {rms_km:.3f} km")
    print(f"  median : {median_residual:.3f} km")
    print(f"  p95    : {p95_residual:.3f} km")
    print(f"  max    : {max_residual:.3f} km")

    # Compare to canonical pole (if given)
    comparison = None
    if args.canonical_pole is not None:
        canon_lat, canon_lon = args.canonical_pole
        canonical_xyz = latlon_to_xyz(canon_lat, canon_lon)
        offset_km = angular_separation_km(pole_xyz, canonical_xyz)
        # Distance between corresponding great circles at the bbox center:
        # this is approximately the pole offset projected onto the perpendicular
        # of the bbox-center direction. For most relevant cases (small offset),
        # offset between GCs at any point is bounded by the pole offset itself.
        comparison = {
            "canonical_pole_lat_lon": [canon_lat, canon_lon],
            "fitted_pole_lat_lon": [pole_lat, pole_lon],
            "pole_offset_km": offset_km,
            "pole_offset_deg": offset_km / R_EARTH_KM * 180.0 / np.pi,
        }
        print(f"\nComparison to canonical pole ({canon_lat:.4f}, {canon_lon:.4f}):")
        print(f"  pole-to-pole great-circle separation : {offset_km:.1f} km "
              f"({comparison['pole_offset_deg']:.3f} deg)")
        if offset_km < 100:
            print("  -> within cross-pole stability envelope (12-pole vs 130-pole "
                  "were 50 km apart with equivalent results)")

    # Save JSON
    payload = {
        "n_points": N,
        "input_files": args.points,
        "label": args.label,
        "fitted_pole_lat_lon": [pole_lat, pole_lon],
        "fitted_pole_xyz": pole_xyz.tolist(),
        "residuals_km": {
            "rms": rms_km,
            "median": median_residual,
            "p95": p95_residual,
            "max": max_residual,
        },
        "comparison_to_canonical": comparison,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    os.makedirs(os.path.dirname(args.json_out) or ".", exist_ok=True)
    with open(args.json_out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nFitted pole written to {args.json_out}")

    # KML
    if args.kml_out:
        # Red line for the fitted GC (matches the "best corridor" convention)
        write_gc_kml(pole_xyz, args.label, "ff0000ff", args.kml_out)
        print(f"KML written to {args.kml_out}")
        print("Tip: open in Google Earth alongside the original KML to overlay "
              "the fitted line on the Mary/Michael currents and the 130-site "
              "alignment for visual comparison.")

    # Reproducibility hint
    print(f"\nTo run the population test on this fitted corridor:")
    print(f"  python scripts_geophys/population_corridor_test.py \\")
    print(f"    --catalog data/population/catalog_B1_strict.csv \\")
    print(f"    --canonical-pole {pole_lat:.4f} {pole_lon:.4f} \\")
    print(f"    --widths-km 5 10 20 50 100 \\")
    print(f"    --trials 10000 \\")
    print(f"    --out results_corridor/population/B1_bestfit.json")
    print(f"\nOr the triple test:")
    print(f"  python scripts_geophys/triple_corridor_test.py \\")
    print(f"    --catalog data/population/catalog_B1_strict.csv:B1 \\")
    print(f"    --catalog data/population/catalog_A_michael.csv:A \\")
    print(f"    --catalog data/population/catalog_B2_broad.csv:B2 \\")
    print(f"    --canonical-pole {pole_lat:.4f} {pole_lon:.4f} \\")
    print(f"    --widths-km 5 10 20 50 100 \\")
    print(f"    --trials 10000 \\")
    print(f"    --out-prefix results_corridor/population/triple_bestfit_iso")


if __name__ == "__main__":
    sys.exit(main() or 0)
