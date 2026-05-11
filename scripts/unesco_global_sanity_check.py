#!/usr/bin/env python3
"""
unesco_global_sanity_check.py

Quantifies the "the corridor passes through Nazca / Alice Springs / etc."
observation by counting how many UNESCO World Heritage Sites fall within a
fixed corridor width of (a) the canonical Michael Line corridor, (b) the
'optimized red line' corridor, and (c) a null distribution of 10,000
random great circles uniform on S^2.

Predicted result (the famous-places fallacy quantified):

  A 100-km wide great-circle corridor covers ~1.5% of Earth's surface area.
  With ~1150 UNESCO sites, a random great circle is expected to capture
  ~18 sites by chance, with a wide spread. The Michael Line and the
  optimized red line should land somewhere in the middle of that
  distribution — neither remarkable nor anti-remarkable.

If the Michael Line lands at the >99th percentile of UNESCO hits, the
"global alignment" reading deserves serious follow-up. If it lands near
the median, the famous-places observation is the standard ley-line
fallacy and should not appear in the paper.

Usage:
  python unesco_global_sanity_check.py \\
    --out results_corridor/unesco_sanity_check.json
"""

from __future__ import annotations
import argparse
import csv
import io
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

import numpy as np


R_EARTH_KM = 6371.0


# ============================================================================
# Geometry (mirrors triple_corridor_test.py)
# ============================================================================

def latlon_to_xyz(lat_deg, lon_deg):
    lat = np.radians(np.asarray(lat_deg, dtype=np.float64))
    lon = np.radians(np.asarray(lon_deg, dtype=np.float64))
    return np.stack([
        np.cos(lat) * np.cos(lon),
        np.cos(lat) * np.sin(lon),
        np.sin(lat),
    ], axis=-1)


def pole_from_two_points(lat1, lon1, lat2, lon2):
    """Compute the great-circle pole from two defining points."""
    p1 = latlon_to_xyz(lat1, lon1)
    p2 = latlon_to_xyz(lat2, lon2)
    pole = np.cross(p1, p2)
    return pole / np.linalg.norm(pole)


def count_within(catalog_xyz, pole_xyz, width_km):
    """Number of catalog points within width_km of the great circle (perp distance)."""
    d = np.arcsin(np.clip(np.abs(catalog_xyz @ pole_xyz), 0.0, 1.0)) * R_EARTH_KM
    return int(np.sum(d <= width_km))


def count_within_many_poles(catalog_xyz, poles_xyz, width_km, chunk=500):
    """Vectorized count for many poles. Returns shape (T,)."""
    T = poles_xyz.shape[0]
    out = np.zeros(T, dtype=np.int32)
    for s in range(0, T, chunk):
        e = min(s + chunk, T)
        d = np.arcsin(np.clip(np.abs(poles_xyz[s:e] @ catalog_xyz.T), 0.0, 1.0)) * R_EARTH_KM
        out[s:e] = np.sum(d <= width_km, axis=1)
    return out


# ============================================================================
# UNESCO data
# ============================================================================

UNESCO_GIST_URL = ("https://gist.githubusercontent.com/jawj/"
                   "01c21d04531570cf0206d67748f240d3/raw/"
                   "e5e2d7a847e5ca62a7d6050293cfe1e6af30ff06/whc-sites-2021.csv")


def fetch_unesco_sites(cache_path: str | None = None) -> np.ndarray:
    """Fetch UNESCO World Heritage Sites with coordinates.
    Returns (N, 2) array of (lat, lon) in degrees.

    The dataset (whc-sites-2021.csv from the UNESCO syndication feed,
    converted to CSV by jawj) contains ~1154 sites.
    """
    if cache_path and os.path.exists(cache_path):
        print(f"Using cached UNESCO data: {cache_path}")
        with open(cache_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        print(f"Fetching UNESCO data from {UNESCO_GIST_URL} ...")
        req = urllib.request.Request(UNESCO_GIST_URL,
                                      headers={"User-Agent": "michael-corridor-sanity-check"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            content = resp.read().decode("utf-8")
        if cache_path:
            os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Cached to {cache_path}")

    rows = []
    reader = csv.DictReader(io.StringIO(content))
    if "longitude" not in reader.fieldnames or "latitude" not in reader.fieldnames:
        raise ValueError(f"Unexpected UNESCO CSV columns: {reader.fieldnames}")
    for r in reader:
        try:
            lat = float(r["latitude"])
            lon = float(r["longitude"])
        except (KeyError, ValueError, TypeError):
            continue
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            rows.append((lat, lon, r.get("name_en", "?")))
    print(f"Loaded {len(rows)} UNESCO sites with valid coordinates")
    return rows


# ============================================================================
# Main
# ============================================================================

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width-km", type=float, default=100.0,
                    help="Corridor half-width in km (default 100)")
    ap.add_argument("--trials", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--cache",
                    default="data/unesco/whc-sites-2021.csv",
                    help="Local cache path for UNESCO data (default: data/unesco/...)")
    args = ap.parse_args()

    # ----- Load UNESCO catalog ---------------------------------------------
    sites = fetch_unesco_sites(cache_path=args.cache)
    latlons = np.array([[s[0], s[1]] for s in sites])
    cat_xyz = latlon_to_xyz(latlons[:, 0], latlons[:, 1])
    N = cat_xyz.shape[0]

    # ----- Define the two named corridors ----------------------------------
    # Canonical Michael corridor: 130-site analysis pole
    michael_pole = latlon_to_xyz(33.330, -147.354)

    # "Optimized red line" from trial 1583 of the user's previous run.
    # User reported defining points: (-11.619635, -72.235626) and (-52.201087, -177.608758).
    red_pole = pole_from_two_points(-11.619635, -72.235626,
                                     -52.201087, -177.608758)

    # ----- Real K for both corridors ---------------------------------------
    K_michael = count_within(cat_xyz, michael_pole, args.width_km)
    K_red     = count_within(cat_xyz, red_pole, args.width_km)
    print(f"\nUNESCO sites within {args.width_km:.0f} km of:")
    print(f"  Michael canonical corridor : {K_michael}")
    print(f"  'Optimized red' corridor   : {K_red}")

    # ----- Null distribution: random great circles uniform on S^2 ----------
    print(f"\nGenerating {args.trials} random global great circles ...")
    rng = np.random.default_rng(args.seed)
    t0 = time.time()
    v = rng.standard_normal((args.trials, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    K_null = count_within_many_poles(cat_xyz, v, args.width_km)
    print(f"  null computed in {time.time()-t0:.1f}s")

    mean_n = float(K_null.mean())
    std_n  = float(K_null.std())
    pct_michael = float((K_null < K_michael).mean()) * 100
    pct_red     = float((K_null < K_red).mean()) * 100
    n_ge_michael = int(np.sum(K_null >= K_michael))
    n_ge_red     = int(np.sum(K_null >= K_red))

    # ----- Theoretical expectation for sanity check ------------------------
    # The set of points within angular distance alpha = w/R of a great circle
    # is a spherical band of fraction sin(alpha) of the sphere's surface.
    # Expected hits = N * sin(w_km / R_earth_km).
    expected = N * np.sin(args.width_km / R_EARTH_KM)
    print(f"\nTheoretical expected hits (random GC, {args.width_km:.0f}km half-width):")
    print(f"  N * sin(w/R) = {N} * sin({args.width_km}/{R_EARTH_KM}) = {expected:.1f}")

    # ----- Report ----------------------------------------------------------
    print("\n" + "=" * 60)
    print("UNESCO GLOBAL CORRIDOR SANITY CHECK  RESULTS")
    print("=" * 60)
    print(f"Corridor half-width      : {args.width_km:.0f} km")
    print(f"UNESCO catalog size N    : {N}")
    print(f"Random GC trials         : {args.trials}")
    print()
    print(f"Null distribution K      : mean={mean_n:.2f}, std={std_n:.2f}, "
          f"min={K_null.min()}, max={K_null.max()}")
    print(f"Theoretical expected K   : {expected:.1f}  (sanity check; "
          f"should be close to null mean)")
    print()
    print(f"Michael canonical line   : K = {K_michael:>3}  "
          f"(percentile {pct_michael:5.1f}%, "
          f"#null >= K_michael = {n_ge_michael})")
    print(f"Optimized red line       : K = {K_red:>3}  "
          f"(percentile {pct_red:5.1f}%, "
          f"#null >= K_red     = {n_ge_red})")
    print()

    # ----- Honest interpretation ------------------------------------------
    if pct_michael < 90:
        print(f"INTERPRETATION: Michael corridor's UNESCO hit count ({K_michael}) is "
              f"unremarkable. It lands at the {pct_michael:.0f}th percentile of "
              f"random great circles, with {n_ge_michael}/{args.trials} random GCs "
              f"matching or exceeding it. The 'famous-places' observation is "
              f"the standard ley-line fallacy: any great-circle corridor through "
              f"populated regions hits comparable numbers of named sites.")
    elif pct_michael < 99:
        print(f"INTERPRETATION: Michael corridor lands at the {pct_michael:.1f}th "
              f"percentile of random global great circles' UNESCO hits — "
              f"elevated but not exceptional.")
    else:
        print(f"INTERPRETATION: Michael corridor lands at the {pct_michael:.1f}th "
              f"percentile — UNUSUAL. This deserves further investigation as "
              f"a global pattern, not just a southern-Britain corridor.")

    # ----- Save -----------------------------------------------------------
    payload = {
        "width_km": args.width_km,
        "unesco_catalog_size": N,
        "trials": args.trials,
        "seed": args.seed,
        "K_null_mean": mean_n,
        "K_null_std": std_n,
        "K_null_min": int(K_null.min()),
        "K_null_max": int(K_null.max()),
        "expected_hits_theory": expected,
        "michael_canonical": {
            "K": K_michael,
            "percentile": pct_michael,
            "n_null_ge_K": n_ge_michael,
        },
        "optimized_red": {
            "K": K_red,
            "percentile": pct_red,
            "n_null_ge_K": n_ge_red,
        },
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nSummary written to {args.out}")


if __name__ == "__main__":
    sys.exit(main() or 0)
