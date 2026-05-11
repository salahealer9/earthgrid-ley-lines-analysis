#!/usr/bin/env python3
"""
corridor_null_test.py

Search-aware null test for great-circle corridor alignment of sites.

Question
--------
Do the sites cluster along any great-circle corridor more than would be
expected if their longitudes were randomly arranged at the same latitudes
(or under stronger nulls)?

Why not Haar SO(3)?
-------------------
The natural analog of Stage 3C — Haar-rotate the catalog, re-enumerate
candidate corridors, take the max count — is degenerate here. The corridor
statistic is rotation-invariant: if every p_k -> R p_k, then n_ij -> R n_ij
and (R n_ij) . (R p_k) = n_ij . p_k. The set of |n_ij . p_k| values is
preserved exactly under any rotation, so the max-count statistic cannot
change under any R in O(3). A non-isometric perturbation of the catalog
is required. Three options are offered.

Null modes
----------
  lon_shuffle   (default, recommended)
      Permute the longitudes among the sites (latitudes stay attached to
      their original index). Preserves the marginal latitude distribution
      exactly and breaks longitudinal correlations. Answers:
      "Given this latitude distribution, do these longitudes produce
       sharper great-circle corridors than random rearrangements would?"

  lon_uniform
      Replace each longitude with an independent uniform draw on
      [-180, 180]. Latitudes preserved. Looser than lon_shuffle (does
      not preserve the empirical longitude marginal at all).

  uniform_sphere
      Replace the entire catalog with N i.i.d. uniformly-distributed
      points on the sphere. Tests against pure spatial uniformity --
      most aggressive null, sensitive to the fact that sacred sites
      are not uniformly distributed on Earth's surface (they cluster
      in inhabited regions). A pass under this null does not by itself
      mean the sites have non-trivial corridor structure --- it might
      reflect concentration alone.

Method
------
- For each pair (i, j), the great circle through them has unit normal
  n_ij = normalize(p_i x p_j). Site k is in the corridor of half-width
  w iff |n_ij . p_k| <= sin(w / R_earth).
- Real statistic at width w: max over all C(N, 2) candidate corridors
  of the count of sites within w.
- Null trial: perturb the catalog per --null-mode, re-enumerate
  candidate corridors from the perturbed points, take the new max count.
- Sweep w in {2, 5, 10, 20} km.

Output
------
- JSON summary: per-width real count, null mean/std/range, p-value, z.
- Per-trial CSV log (resumable).

Usage
-----
  # Quick validation (5 trials)
  python corridor_null_test.py --sites <catalog.csv> \\
      --out results/corridor_smoke.json --smoke-test

  # Headline run: longitude shuffle, 1000 trials
  python corridor_null_test.py --sites <catalog.csv> \\
      --out results/corridor_lonshuffle.json \\
      --null-mode lon_shuffle --trials 1000 --seed 42

  # Comparison run: uniform sphere null
  python corridor_null_test.py --sites <catalog.csv> \\
      --out results/corridor_uniform.json \\
      --null-mode uniform_sphere --trials 1000 --seed 42
"""

import argparse
import csv
import json
import math
import time
from pathlib import Path

import numpy as np

EARTH_R_KM = 6371.0


# ──────────────────────────────────────────────────────────────────────────
# I/O
# ──────────────────────────────────────────────────────────────────────────

def load_sites(path):
    """Load lat/lon CSV -> (lats_deg, lons_deg, P_unit_vectors).

    Accepts column names lat/lon or latitude/longitude (case-insensitive).
    """
    lats, lons = [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        fieldmap = {name.lower(): name for name in reader.fieldnames}
        lat_key = fieldmap.get("lat") or fieldmap.get("latitude")
        lon_key = fieldmap.get("lon") or fieldmap.get("longitude")
        if lat_key is None or lon_key is None:
            raise ValueError(
                f"CSV must have lat/lon columns; got {reader.fieldnames}"
            )
        for row in reader:
            lats.append(float(row[lat_key]))
            lons.append(float(row[lon_key]))
    lats_deg = np.array(lats)
    lons_deg = np.array(lons)
    return lats_deg, lons_deg, latlon_to_unit(lats_deg, lons_deg)


def latlon_to_unit(lats_deg, lons_deg):
    lats = np.deg2rad(lats_deg)
    lons = np.deg2rad(lons_deg)
    x = np.cos(lats) * np.cos(lons)
    y = np.cos(lats) * np.sin(lons)
    z = np.sin(lats)
    P = np.stack([x, y, z], axis=1)
    return P / np.linalg.norm(P, axis=1, keepdims=True)


# ──────────────────────────────────────────────────────────────────────────
# Null perturbations
# ──────────────────────────────────────────────────────────────────────────

def perturb_lon_shuffle(lats_deg, lons_deg, rng):
    """Permute longitudes among sites; latitudes unchanged."""
    perm = rng.permutation(len(lons_deg))
    return lats_deg.copy(), lons_deg[perm]


def perturb_lon_uniform(lats_deg, lons_deg, rng):
    """Replace each longitude with U(-180, 180); latitudes unchanged."""
    new_lons = rng.uniform(-180.0, 180.0, size=lats_deg.shape[0])
    return lats_deg.copy(), new_lons


def perturb_uniform_sphere(lats_deg, lons_deg, rng):
    """Replace catalog with N i.i.d. uniform points on the sphere."""
    N = lats_deg.shape[0]
    # Uniform on sphere: lat = arcsin(2u - 1), lon = U(-180, 180).
    u = rng.uniform(0.0, 1.0, size=N)
    new_lats_deg = np.degrees(np.arcsin(2.0 * u - 1.0))
    new_lons_deg = rng.uniform(-180.0, 180.0, size=N)
    return new_lats_deg, new_lons_deg


PERTURB_FNS = {
    "lon_shuffle": perturb_lon_shuffle,
    "lon_uniform": perturb_lon_uniform,
    "uniform_sphere": perturb_uniform_sphere,
}


# ──────────────────────────────────────────────────────────────────────────
# Corridor enumeration
# ──────────────────────────────────────────────────────────────────────────

def best_corridor_counts(P, widths_rad, degenerate_tol=1e-12):
    """Best (max) corridor count per width.

    A "candidate corridor" is the great circle through some site pair (i, j).
    Its normal is n = normalize(p_i x p_j). A site k is in the corridor of
    half-width w iff |n . p_k| <= sin(w).

    Returns dict[w_rad] = (best_count, i, j) where (i, j) defines the
    corridor that achieved the maximum.
    """
    N = P.shape[0]
    i_idx, j_idx = np.triu_indices(N, k=1)
    cross = np.cross(P[i_idx], P[j_idx])             # (M, 3)
    norms = np.linalg.norm(cross, axis=1)            # (M,)
    valid = norms > degenerate_tol
    if not np.all(valid):
        cross = cross[valid]
        i_idx = i_idx[valid]
        j_idx = j_idx[valid]
        norms = norms[valid]
    cross = cross / norms[:, None]                   # unit normals (M, 3)

    abs_dots = np.abs(cross @ P.T)                   # (M, N)

    results = {}
    for w_rad in widths_rad:
        sin_w = math.sin(w_rad)
        counts = (abs_dots <= sin_w).sum(axis=1)
        best = int(np.argmax(counts))
        results[w_rad] = (int(counts[best]), int(i_idx[best]), int(j_idx[best]))
    return results


# ──────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--sites", required=True,
                    help="CSV with lat/lon columns")
    ap.add_argument("--widths-km", type=float, nargs="+",
                    default=[2.0, 5.0, 10.0, 20.0],
                    help="Half-widths in km (default: 2 5 10 20)")
    ap.add_argument("--null-mode",
                    choices=list(PERTURB_FNS.keys()),
                    default="lon_shuffle",
                    help="Perturbation for null trials (default: lon_shuffle)")
    ap.add_argument("--trials", type=int, default=1000,
                    help="Number of null trials (default: 1000)")
    ap.add_argument("--seed", type=int, default=42, help="RNG seed")
    ap.add_argument("--out", required=True, help="Output JSON summary path")
    ap.add_argument("--trial-log", default=None,
                    help="Per-trial CSV log path (default: <out>.trials.csv)")
    ap.add_argument("--resume", action="store_true",
                    help="Resume from existing trial log if present")
    ap.add_argument("--smoke-test", action="store_true",
                    help="Set trials=5 for a quick validation run")
    ap.add_argument("--progress-every", type=int, default=0,
                    help="Print progress every N trials (default: trials/50)")
    args = ap.parse_args()

    if args.smoke_test:
        args.trials = 5

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    trial_log_path = (Path(args.trial_log) if args.trial_log
                      else out_path.with_suffix(".trials.csv"))

    # ── Load ──
    print(f"Loading sites: {args.sites}")
    lats_deg, lons_deg, P = load_sites(args.sites)
    N = P.shape[0]
    print(f"  N = {N} sites")
    print(f"  Latitude  range: [{lats_deg.min():.2f}, {lats_deg.max():.2f}]")
    print(f"  Longitude range: [{lons_deg.min():.2f}, {lons_deg.max():.2f}]")
    print(f"Null mode: {args.null_mode}")

    widths_km = list(args.widths_km)
    widths_rad = [w / EARTH_R_KM for w in widths_km]
    print(f"Half-widths (km):  {widths_km}")

    # ── Real statistic ──
    print("\nReal best-corridor counts:")
    t0 = time.time()
    real = best_corridor_counts(P, widths_rad)
    t1 = time.time()
    print(f"  ({t1 - t0:.3f}s)")
    for w_km, w_rad in zip(widths_km, widths_rad):
        cnt, i, j = real[w_rad]
        baseline = math.sin(w_rad) * N
        print(f"  w = {w_km:5.1f} km : count = {cnt:4d}  pair = ({i}, {j})"
              f"   [random-circle baseline ~{baseline:.2f}]")

    # ── Trial log: resume or initialise ──
    null_counts = {w: [] for w in widths_rad}
    start_trial = 0
    width_keys = [f"count_w{w}km" for w in widths_km]

    if args.resume and trial_log_path.exists():
        with open(trial_log_path, newline="") as f:
            reader = csv.reader(f)
            header = next(reader)
            expected = ["trial"] + width_keys
            if header != expected:
                raise SystemExit(
                    f"Resume mismatch: log header {header} != expected {expected}.\n"
                    f"Either delete {trial_log_path} or adjust --widths-km."
                )
            for row in reader:
                t_idx = int(row[0])
                for k, w in enumerate(widths_rad):
                    null_counts[w].append(int(row[1 + k]))
                start_trial = t_idx + 1
        print(f"\nResuming from trial {start_trial} ({trial_log_path})")
        log_f = open(trial_log_path, "a", newline="")
        log_w = csv.writer(log_f)
    else:
        log_f = open(trial_log_path, "w", newline="")
        log_w = csv.writer(log_f)
        log_w.writerow(["trial"] + width_keys)
        log_f.flush()

    # ── Null trials ──
    rng = np.random.default_rng(args.seed + start_trial)
    perturb_fn = PERTURB_FNS[args.null_mode]

    n_to_run = args.trials - start_trial
    if n_to_run <= 0:
        print(f"\nAll {args.trials} trials already complete; aggregating.")
    else:
        print(f"\nRunning {n_to_run} null trials (mode: {args.null_mode})...")
    progress_every = (args.progress_every if args.progress_every > 0
                      else max(1, args.trials // 50))
    t_start = time.time()
    for trial in range(start_trial, args.trials):
        new_lats, new_lons = perturb_fn(lats_deg, lons_deg, rng)
        P_null = latlon_to_unit(new_lats, new_lons)
        null_res = best_corridor_counts(P_null, widths_rad)
        row = [trial]
        for w in widths_rad:
            null_counts[w].append(null_res[w][0])
            row.append(null_res[w][0])
        log_w.writerow(row)
        if (trial + 1 - start_trial) % progress_every == 0:
            elapsed = time.time() - t_start
            done = trial + 1 - start_trial
            eta = elapsed / done * (n_to_run - done) if done else 0.0
            print(f"  trial {trial + 1}/{args.trials}  "
                  f"elapsed {elapsed:.1f}s  ETA {eta:.1f}s")
            log_f.flush()
    log_f.close()

    # ── Aggregate ──
    print("\n" + "=" * 64)
    print(f"RESULTS  (null mode: {args.null_mode})")
    print("=" * 64)

    summary = {
        "sites_path": str(args.sites),
        "n_sites": N,
        "trials": args.trials,
        "seed": args.seed,
        "null_mode": args.null_mode,
        "widths_km": widths_km,
        "earth_radius_km": EARTH_R_KM,
        "per_width": {},
    }

    for w_km, w_rad in zip(widths_km, widths_rad):
        real_cnt, real_i, real_j = real[w_rad]
        null = np.asarray(null_counts[w_rad], dtype=np.int64)
        k_geq = int(np.sum(null >= real_cnt))
        p = (k_geq + 1) / (args.trials + 1)
        mu = float(null.mean())
        sd = float(null.std(ddof=0))
        z = (real_cnt - mu) / sd if sd > 0 else float("nan")
        summary["per_width"][f"{w_km}"] = {
            "real_count": real_cnt,
            "real_pair": [real_i, real_j],
            "null_mean": mu,
            "null_std": sd,
            "null_min": int(null.min()),
            "null_max": int(null.max()),
            "k_geq": k_geq,
            "p_value": p,
            "z_score": z,
        }
        print(f"\nw = {w_km} km")
        print(f"  Real best count : {real_cnt}  (pair {real_i}, {real_j})")
        print(f"  Null mean ± std : {mu:.2f} ± {sd:.2f}")
        print(f"  Null range      : [{null.min()}, {null.max()}]")
        print(f"  k(null >= real) : {k_geq} / {args.trials}")
        print(f"  p (one-sided)   : {p:.4f}")
        print(f"  z-score         : {z:.2f}")

    n_widths = len(widths_km)
    bonf_alpha = 0.05 / n_widths
    summary["bonferroni_alpha_per_width"] = bonf_alpha
    summary["bonferroni_n_widths"] = n_widths
    print(f"\nBonferroni-adjusted threshold (family-wise alpha = 0.05, "
          f"{n_widths} widths): per-width p < {bonf_alpha:.4f}")

    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary written to : {out_path}")
    print(f"Per-trial log      : {trial_log_path}")


if __name__ == "__main__":
    main()
