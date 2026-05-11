#!/usr/bin/env python3
"""
inspect_corridor.py

Given a sites CSV and a corridor definition (a pair of site indices), list
the sites that fall within specified half-widths of the great circle, with
their names (if available), coordinates, and exact angular distances.

Useful for interpreting results from corridor_null_test.py: once a
significant corridor is identified by its defining pair, this script tells
you which actual sites it contains.

Usage
-----
  python inspect_corridor.py --sites <catalog.csv> --pair 63 118
  python inspect_corridor.py --sites <catalog.csv> --pair 63 118 --widths-km 20
  python inspect_corridor.py --sites <catalog.csv> --pair 63 118 --show-all
"""

import argparse
import csv
import math

import numpy as np

EARTH_R_KM = 6371.0


def load_sites_with_metadata(path):
    """Load sites with all CSV metadata preserved.

    Returns a list of dicts with keys lat, lon, name, raw.
    """
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        fieldmap = {n.lower(): n for n in fieldnames}
        lat_key = fieldmap.get("lat") or fieldmap.get("latitude")
        lon_key = fieldmap.get("lon") or fieldmap.get("longitude")
        if lat_key is None or lon_key is None:
            raise SystemExit(f"CSV must have lat/lon columns; got {fieldnames}")
        # Identify a name column if one is present (case-insensitive).
        name_key = None
        for candidate in ("name", "site", "site_name", "label", "place"):
            if candidate in fieldmap:
                name_key = fieldmap[candidate]
                break
        for row in reader:
            rows.append({
                "lat": float(row[lat_key]),
                "lon": float(row[lon_key]),
                "name": row.get(name_key, "") if name_key else "",
                "raw": row,
            })
    return rows, name_key


def latlon_to_unit(lat_deg, lon_deg):
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    return np.array([
        math.cos(lat) * math.cos(lon),
        math.cos(lat) * math.sin(lon),
        math.sin(lat),
    ])


def describe_corridor(p_i, p_j, n):
    """Print geometric characterization of the corridor."""
    pole_lat = math.degrees(math.asin(np.clip(n[2], -1.0, 1.0)))
    pole_lon = math.degrees(math.atan2(n[1], n[0]))
    max_lat = 90.0 - abs(pole_lat)

    midpoint = p_i + p_j
    midpoint /= np.linalg.norm(midpoint)
    mid_lat = math.degrees(math.asin(np.clip(midpoint[2], -1.0, 1.0)))
    mid_lon = math.degrees(math.atan2(midpoint[1], midpoint[0]))

    # Bearing of the corridor at midpoint (direction of travel along great circle).
    tangent = np.cross(n, midpoint)
    tangent /= np.linalg.norm(tangent)
    east = np.array([-math.sin(math.radians(mid_lon)),
                     math.cos(math.radians(mid_lon)),
                     0.0])
    north = np.cross(midpoint, east)
    north /= np.linalg.norm(north)
    bearing_deg = math.degrees(math.atan2(np.dot(tangent, east),
                                          np.dot(tangent, north))) % 360.0

    # Angular separation of the defining pair (km along the corridor).
    sep_rad = math.acos(np.clip(np.dot(p_i, p_j), -1.0, 1.0))
    sep_km = sep_rad * EARTH_R_KM

    print("Corridor characterization:")
    print(f"  Great-circle pole       : ({pole_lat:+8.3f}°, {pole_lon:+8.3f}°)")
    print(f"  Max latitude on corridor: ±{max_lat:.2f}°")
    print(f"  Midpoint of defining pair: ({mid_lat:+8.3f}°, {mid_lon:+8.3f}°)")
    print(f"  Bearing at midpoint     : {bearing_deg:6.1f}°  (0=N, 90=E, 180=S, 270=W)")
    print(f"  Pair separation         : {sep_km:8.1f} km  ({math.degrees(sep_rad):.2f}°)")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--sites", required=True, help="CSV with lat/lon columns")
    ap.add_argument("--pair", type=int, nargs=2, required=True,
                    metavar=("I", "J"),
                    help="Indices of the two sites defining the corridor")
    ap.add_argument("--widths-km", type=float, nargs="+",
                    default=[2.0, 5.0, 10.0, 20.0],
                    help="Half-widths in km (default: 2 5 10 20)")
    ap.add_argument("--show-all", action="store_true",
                    help="List every site sorted by distance to corridor "
                         "(not just within widths)")
    ap.add_argument("--top-n", type=int, default=20,
                    help="With --show-all, limit to top N closest (default: 20)")
    args = ap.parse_args()

    rows, name_key = load_sites_with_metadata(args.sites)
    N = len(rows)
    print(f"Loaded {N} sites from {args.sites}")
    if name_key:
        print(f"Name column: {name_key!r}")
    else:
        print("No name column found; printing indices and coordinates only.")

    i, j = args.pair
    if not (0 <= i < N and 0 <= j < N) or i == j:
        raise SystemExit(f"Bad pair: ({i}, {j}) for N={N}")

    p_i = latlon_to_unit(rows[i]["lat"], rows[i]["lon"])
    p_j = latlon_to_unit(rows[j]["lat"], rows[j]["lon"])
    cross = np.cross(p_i, p_j)
    cross_norm = np.linalg.norm(cross)
    if cross_norm < 1e-12:
        raise SystemExit(f"Degenerate pair ({i}, {j}): coincident or antipodal.")
    n = cross / cross_norm

    name_w = max((len(r["name"]) for r in rows), default=0) if name_key else 0
    name_w = max(name_w, 4)
    name_fmt = f"{{:<{name_w}}}"

    print()
    describe_corridor(p_i, p_j, n)

    print(f"\nDefining pair:")
    for k in (i, j):
        nm = name_fmt.format(rows[k]["name"]) if name_key else ""
        print(f"  [{k:4d}] {nm}  ({rows[k]['lat']:+9.4f}, {rows[k]['lon']:+9.4f})")

    # Distance from every site to the corridor (in km).
    P = np.array([latlon_to_unit(r["lat"], r["lon"]) for r in rows])
    abs_dots = np.clip(np.abs(P @ n), 0.0, 1.0)
    dist_km = np.arcsin(abs_dots) * EARTH_R_KM

    if args.show_all:
        order = np.argsort(dist_km)[: args.top_n]
        print(f"\nClosest {len(order)} sites (sorted by distance to corridor):")
        for k in order:
            tag = "  <- defining" if k in (i, j) else ""
            nm = name_fmt.format(rows[k]["name"]) if name_key else ""
            print(f"  [{k:4d}] {dist_km[k]:8.3f} km  {nm}  "
                  f"({rows[k]['lat']:+9.4f}, {rows[k]['lon']:+9.4f}){tag}")
        return

    for w in sorted(args.widths_km):
        mask = dist_km <= w
        members = list(np.where(mask)[0])
        members.sort(key=lambda k: dist_km[k])
        print(f"\nSites within {w:.1f} km of corridor through pair "
              f"({i}, {j}):  {len(members)} sites")
        for k in members:
            tag = "  <- defining" if k in (i, j) else ""
            nm = name_fmt.format(rows[k]["name"]) if name_key else ""
            print(f"  [{k:4d}] {dist_km[k]:7.3f} km  {nm}  "
                  f"({rows[k]['lat']:+9.4f}, {rows[k]['lon']:+9.4f}){tag}")


if __name__ == "__main__":
    main()
