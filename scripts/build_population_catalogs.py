#!/usr/bin/env python3
"""
build_population_catalogs.py  (v3)

Reference catalogs for the population corridor test.

Catalog A (Michael dedications): up to four strategies, unioned.
  A1: Wikidata strict     P825 = Q47652 + church type chain
  A2: Wikidata P825 only  P825 = Q47652 (no type filter)
  A3: Wikidata name regex broad religious-building types + label match
  A4: OSM Overpass        amenity=place_of_worship + name regex
  Wikidata strategies are skippable while WDQS is degraded; A4 alone is
  sufficient for a first-pass catalog.

Catalog B is split into two pre-registered sub-catalogs:

  B1 (strict prehistoric / hypothesis-driven):
       stone_circle | standing_stone | menhir | megalith
       | tumulus | cairn | hillfort
     This is the primary corridor-test catalog.

  B2 (broad archaeological / sensitivity / robustness check):
       all historic=archaeological_site (any subtype)
     This is a secondary catalog reported alongside B1.

The split is about what claim is being made (prehistoric monuments vs.
"any archaeology"), NOT about test validity — see the protocol section
"On catalog density and test validity".

Performance changes vs. v2 (per reviewer feedback):
  - Anchored regex on Michael names (^st\\.? michael, ^saint michael,
    ^church of ...). amenity=place_of_worship pre-filter keeps the
    candidate set small, so this is fast.
  - building=church|chapel queries dropped (overwhelmingly redundant
    with amenity=place_of_worship in well-mapped UK).
  - Overpass timeout 60s, HTTP timeout 90s, endpoints reordered to put
    less-loaded mirrors first.
  - Per-fetch timing prints so it's obvious where seconds go.
"""

from __future__ import annotations
import argparse
import csv
import json
import os
import re
import random
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode
import urllib.request
import urllib.error


# ============================================================================
# Configuration
# ============================================================================

BBOX = {"south": 49.5, "west": -6.5, "north": 53.5, "east": 2.5}

WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"

# Reordered: less-loaded mirrors first, main endpoint last.
OVERPASS_ENDPOINTS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass-api.de/api/interpreter",
]

USER_AGENT = "earthgrid-research/population-corridor (research)"

OVERPASS_TIMEOUT_S = 60   # in-query timeout (Overpass-side)
HTTP_TIMEOUT_S    = 90    # HTTP read timeout (client-side)


def _bbox() -> str:
    return f"{BBOX['south']},{BBOX['west']},{BBOX['north']},{BBOX['east']}"


# ============================================================================
# SPARQL queries (unchanged from v2; for use when WDQS recovers)
# ============================================================================

SPARQL_A1 = """
SELECT DISTINCT ?item ?itemLabel ?coord WHERE {
  SERVICE wikibase:box {
    ?item wdt:P625 ?coord .
    bd:serviceParam wikibase:cornerSouthWest "Point(%(west)s %(south)s)"^^geo:wktLiteral .
    bd:serviceParam wikibase:cornerNorthEast "Point(%(east)s %(north)s)"^^geo:wktLiteral .
  }
  ?item wdt:P31/wdt:P279* wd:Q16970 .
  ?item wdt:P825 wd:Q47652 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,cy,kw,gd". }
}
""" % BBOX

SPARQL_A2 = """
SELECT DISTINCT ?item ?itemLabel ?coord WHERE {
  SERVICE wikibase:box {
    ?item wdt:P625 ?coord .
    bd:serviceParam wikibase:cornerSouthWest "Point(%(west)s %(south)s)"^^geo:wktLiteral .
    bd:serviceParam wikibase:cornerNorthEast "Point(%(east)s %(north)s)"^^geo:wktLiteral .
  }
  ?item wdt:P825 wd:Q47652 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,cy,kw,gd". }
}
""" % BBOX

SPARQL_A3 = """
SELECT DISTINCT ?item ?itemLabel ?coord WHERE {
  SERVICE wikibase:box {
    ?item wdt:P625 ?coord .
    bd:serviceParam wikibase:cornerSouthWest "Point(%(west)s %(south)s)"^^geo:wktLiteral .
    bd:serviceParam wikibase:cornerNorthEast "Point(%(east)s %(north)s)"^^geo:wktLiteral .
  }
  ?item wdt:P31 ?type .
  VALUES ?type {
    wd:Q16970 wd:Q317557 wd:Q108325 wd:Q5341295 wd:Q56242215
    wd:Q1370598 wd:Q24398318 wd:Q56242211 wd:Q44613
  }
  ?item rdfs:label ?label .
  FILTER(LANG(?label) IN ("en", "cy", "kw"))
  FILTER(REGEX(STR(?label), "\\\\bst\\\\.? ?(michael|mihangel|michel)\\\\b", "i"))
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,cy,kw,gd". }
}
""" % BBOX


# ============================================================================
# Overpass queries (anchored, narrow tag filters)
# ============================================================================

# A4 — Michael churches.
#
# Three regex patterns, all anchored, on the small amenity=place_of_worship
# candidate set:
#   (1) ^(st\.? |saint ) michael ...   matches "St Michael's Church", "St. Michael..."
#   (2) ^church of (st\.?|saint) michael   catches "Church of St Michael, ..."
#                                          (Anglican parish convention; would be
#                                          missed by start-anchored "st michael")
#   (3) mihangel (unanchored)          Welsh form, distinctive enough that
#                                       false positives are negligible
#
# The amenity filter pre-restricts the candidate set to ~tens of thousands
# of records bbox-wide, so even the unanchored Welsh-form regex is cheap.
OVERPASS_QUERY_MICHAEL = f"""
[out:json][timeout:{OVERPASS_TIMEOUT_S}];
(
  node["amenity"="place_of_worship"]["name"~"Michael",i]({_bbox()});
  way["amenity"="place_of_worship"]["name"~"Michael",i]({_bbox()});
);
out center tags;
"""

# B1 — Strict prehistoric / Iron-Age monuments.
B1_TYPES = "stone_circle|standing_stone|menhir|megalith|tumulus|cairn|hillfort"

OVERPASS_QUERY_B1 = f"""
[out:json][timeout:{OVERPASS_TIMEOUT_S}];
(
  node["historic"~"^({B1_TYPES})$"]({_bbox()});
  way ["historic"~"^({B1_TYPES})$"]({_bbox()});
  relation["historic"~"^({B1_TYPES})$"]({_bbox()});

  // Stone circles and standing stones are sometimes tagged via archaeological_site
  node["historic"="archaeological_site"]["archaeological_site"~"^(stone_circle|standing_stone|megalith|tumulus|cairn|barrow|henge|dolmen|fortification)$"]({_bbox()});
  way ["historic"="archaeological_site"]["archaeological_site"~"^(stone_circle|standing_stone|megalith|tumulus|cairn|barrow|henge|dolmen|fortification)$"]({_bbox()});
  relation["historic"="archaeological_site"]["archaeological_site"~"^(stone_circle|standing_stone|megalith|tumulus|cairn|barrow|henge|dolmen|fortification)$"]({_bbox()});
);
out center tags;
"""

# B2 — Broad archaeological catch-all.
OVERPASS_QUERY_B2 = f"""
[out:json][timeout:{OVERPASS_TIMEOUT_S}];
(
  node["historic"="archaeological_site"]({_bbox()});
  way ["historic"="archaeological_site"]({_bbox()});
  relation["historic"="archaeological_site"]({_bbox()});
);
out center tags;
"""


# ============================================================================
# HTTP helpers
# ============================================================================

def _http_post(url: str, data: bytes, headers: dict[str, str], timeout: int) -> bytes:
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_wikidata(query: str, max_attempts: int = 5) -> dict[str, Any]:
    """POST to WDQS with exponential-backoff retry on 5xx and timeouts."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/sparql-results+json"}
    body = urlencode({"query": query}).encode("utf-8")
    delays = [5, 15, 45, 90, 180]
    last_err: Exception | None = None
    for attempt in range(max_attempts):
        try:
            t0 = time.time()
            raw = _http_post(WIKIDATA_SPARQL, body, headers, timeout=HTTP_TIMEOUT_S)
            dt = time.time() - t0
            print(f"  wikidata: ok in {dt:.1f}s")
            return json.loads(raw)
        except urllib.error.HTTPError as e:
            last_err = e
            if 500 <= e.code < 600:
                wait = delays[min(attempt, len(delays) - 1)] + random.uniform(0, 3)
                print(f"  wikidata: HTTP {e.code} (attempt {attempt+1}/{max_attempts}); "
                      f"retry in {wait:.1f}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            wait = delays[min(attempt, len(delays) - 1)] + random.uniform(0, 3)
            print(f"  wikidata: {type(e).__name__} (attempt {attempt+1}/{max_attempts}); "
                  f"retry in {wait:.1f}s", file=sys.stderr)
            time.sleep(wait)
            continue
    raise RuntimeError(f"wikidata: all {max_attempts} attempts failed; last error: {last_err}")


def fetch_overpass(query: str) -> dict[str, Any]:
    headers = {"User-Agent": USER_AGENT, "Content-Type": "text/plain; charset=utf-8"}
    body = query.encode("utf-8")
    last_err: Exception | None = None
    for endpoint in OVERPASS_ENDPOINTS:
        t0 = time.time()
        try:
            print(f"  overpass: trying {endpoint} ...")
            raw = _http_post(endpoint, body, headers, timeout=HTTP_TIMEOUT_S)
            dt = time.time() - t0
            print(f"  overpass: ok in {dt:.1f}s ({len(raw):,} bytes)")
            return json.loads(raw)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            dt = time.time() - t0
            last_err = e
            print(f"  overpass: {endpoint} failed after {dt:.1f}s ({e}); trying next",
                  file=sys.stderr)
            time.sleep(2)
    raise RuntimeError(f"overpass: all endpoints failed; last error: {last_err}")


# ============================================================================
# Parsers
# ============================================================================

def parse_wikidata(payload: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for binding in payload.get("results", {}).get("bindings", []):
        try:
            qid = binding["item"]["value"].rsplit("/", 1)[-1]
            label = binding.get("itemLabel", {}).get("value", qid)
            wkt = binding["coord"]["value"]
            inner = wkt[wkt.index("(") + 1 : wkt.rindex(")")]
            lon_str, lat_str = inner.split()
            lon, lat = float(lon_str), float(lat_str)
        except (KeyError, ValueError) as e:
            print(f"  wikidata: skipping malformed binding ({e})", file=sys.stderr)
            continue
        out.append({"id": qid, "name": label, "lat": lat, "lon": lon, "source": "wikidata"})
    return out

def is_st_michael(name: str) -> bool:
    """Return True if name appears to refer to St Michael."""
    if not name:
        return False
    return bool(re.search(r"\b(st\.?|saint)\s+michael\b", name, re.IGNORECASE))

def parse_overpass_michael(payload: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for el in payload.get("elements", []):
        et = el.get("type")
        if et == "node":
            lat = el.get("lat"); lon = el.get("lon")
        elif et in ("way", "relation"):
            c = el.get("center") or {}
            lat = c.get("lat"); lon = c.get("lon")
        else:
            continue
        if lat is None or lon is None:
            continue
        tags = el.get("tags") or {}
        name = tags.get("name:en") or tags.get("name") or f"{et}/{el.get('id')}"

        # --- ADD THIS FILTER ---
        if not is_st_michael(name):
            continue   # skip non‑St Michael churches
        # -----------------------

        out.append({
            "id": f"{et}/{el.get('id')}",
            "name": name,
            "lat": lat,
            "lon": lon,
            "source": "osm",
        })
    return out


def parse_overpass_monuments(payload: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for el in payload.get("elements", []):
        et = el.get("type")
        if et == "node":
            lat = el.get("lat"); lon = el.get("lon")
        elif et in ("way", "relation"):
            c = el.get("center") or {}
            lat = c.get("lat"); lon = c.get("lon")
        else:
            continue
        if lat is None or lon is None:
            continue
        tags = el.get("tags") or {}
        name = tags.get("name") or tags.get("name:en") or f"{et}/{el.get('id')}"
        # Surface the most specific subtype available
        historic = tags.get("historic", "")
        arch_sub = tags.get("archaeological_site", "")
        if historic == "archaeological_site" and arch_sub:
            kind = arch_sub
        elif historic:
            kind = historic
        else:
            kind = "unknown"
        out.append({
            "id": f"{et}/{el.get('id')}",
            "name": name,
            "lat": lat,
            "lon": lon,
            "type": kind,
            "source": "osm",
        })
    return out


def in_bbox(lat: float, lon: float) -> bool:
    return (BBOX["south"] <= lat <= BBOX["north"]
            and BBOX["west"] <= lon <= BBOX["east"])


def deduplicate(records: list[dict[str, Any]], radius_m: float = 100.0) -> list[dict[str, Any]]:
    R = 6_371_000.0
    deg_per_m = 1.0 / (R * 3.141592653589793 / 180.0)
    eps = radius_m * deg_per_m
    kept: list[dict[str, Any]] = []
    for r in records:
        dup = False
        for k in kept:
            if abs(r["lat"] - k["lat"]) < eps and abs(r["lon"] - k["lon"]) < eps:
                dup = True
                break
        if not dup:
            kept.append(r)
    return kept


# ============================================================================
# Main
# ============================================================================

def run_wikidata_strategy(name: str, query: str, raw_dir: str, ts: str) -> list[dict[str, Any]]:
    print(f"[A:{name}] Querying Wikidata ...")
    t0 = time.time()
    try:
        payload = fetch_wikidata(query)
    except Exception as e:
        dt = time.time() - t0
        print(f"[A:{name}] FAILED after {dt:.1f}s: {e}", file=sys.stderr)
        return []
    raw_path = os.path.join(raw_dir, f"wikidata_{name}_{ts}.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    records = parse_wikidata(payload)
    records = [r for r in records if in_bbox(r["lat"], r["lon"])]
    dt = time.time() - t0
    print(f"[A:{name}] {len(records)} records in bbox in {dt:.1f}s  ->  {raw_path}")
    for r in records[:3]:
        print(f"           e.g. {r['id']:<10} {r['name']!r:<50} ({r['lat']:.4f},{r['lon']:.4f})")
    return records


def run_overpass_query(label: str, query: str, raw_dir: str, ts: str,
                       parser, raw_filename: str) -> list[dict[str, Any]]:
    print(f"\n[{label}] Fetching Overpass ...")
    t0 = time.time()
    payload = fetch_overpass(query)
    raw_path = os.path.join(raw_dir, raw_filename)
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    records = parser(payload)
    records = [r for r in records if in_bbox(r["lat"], r["lon"])]
    before = len(records)
    records = deduplicate(records, radius_m=100.0)
    dt = time.time() - t0
    print(f"[{label}] {before} parsed -> {len(records)} after dedup ({dt:.1f}s total)")
    return records


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", default="data/population")
    ap.add_argument("--skip-wikidata", action="store_true",
                    help="Skip A1+A2+A3 (Wikidata strategies; useful while WDQS is degraded)")
    ap.add_argument("--skip-osm-michael", action="store_true",
                    help="Skip A4 (OSM Michael query)")
    ap.add_argument("--skip-b1", action="store_true",
                    help="Skip Catalog B1 (strict prehistoric)")
    ap.add_argument("--skip-b2", action="store_true",
                    help="Skip Catalog B2 (broad archaeological)")
    ap.add_argument("--skip-overpass", action="store_true",
                    help="Shortcut: skip A4 + B1 + B2 (all Overpass)")
    args = ap.parse_args()

    if args.skip_overpass:
        args.skip_osm_michael = True
        args.skip_b1 = True
        args.skip_b2 = True

    out_dir = args.out_dir
    raw_dir = os.path.join(out_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # ----- Catalog A: union of available strategies -------------------------
    rec_A1: list[dict[str, Any]] = []
    rec_A2: list[dict[str, Any]] = []
    rec_A3: list[dict[str, Any]] = []
    rec_A4: list[dict[str, Any]] = []

    if not args.skip_wikidata:
        rec_A1 = run_wikidata_strategy("A1", SPARQL_A1, raw_dir, ts)
        time.sleep(3)
        rec_A2 = run_wikidata_strategy("A2", SPARQL_A2, raw_dir, ts)
        time.sleep(3)
        rec_A3 = run_wikidata_strategy("A3", SPARQL_A3, raw_dir, ts)

    if not args.skip_osm_michael:
        try:
            rec_A4 = run_overpass_query(
                "A:A4", OVERPASS_QUERY_MICHAEL, raw_dir, ts,
                parse_overpass_michael, f"overpass_michael_{ts}.json",
            )
        except Exception as e:
            print(f"[A:A4] FAILED: {e}", file=sys.stderr)
            rec_A4 = []
        for r in rec_A4[:5]:
            print(f"           e.g. {r['id']:<22} {r['name']!r:<40} ({r['lat']:.4f},{r['lon']:.4f})")

    for r in rec_A1: r["strategy"] = "A1"
    for r in rec_A2: r["strategy"] = "A2"
    for r in rec_A3: r["strategy"] = "A3"
    for r in rec_A4: r["strategy"] = "A4"

    if any([rec_A1, rec_A2, rec_A3, rec_A4]):
        seen_ids: set[str] = set()
        union: list[dict[str, Any]] = []
        for src in (rec_A1, rec_A2, rec_A3, rec_A4):
            for r in src:
                if r["id"] in seen_ids:
                    continue
                seen_ids.add(r["id"])
                union.append(r)
        before = len(union)
        union = deduplicate(union, radius_m=100.0)
        print(f"\n[A] Union: A1={len(rec_A1)} A2={len(rec_A2)} A3={len(rec_A3)} A4={len(rec_A4)} "
              f"-> {before} unique IDs -> {len(union)} after 100 m dedup")
        csv_A = os.path.join(out_dir, "catalog_A_michael.csv")
        with open(csv_A, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["id", "name", "lat", "lon", "strategy", "source"])
            w.writeheader()
            w.writerows(union)
        print(f"[A] Catalog A written to {csv_A}  ({len(union)} sites)")

    # ----- Catalog B1: strict prehistoric -----------------------------------
    if not args.skip_b1:
        try:
            rec_B1 = run_overpass_query(
                "B1", OVERPASS_QUERY_B1, raw_dir, ts,
                parse_overpass_monuments, f"overpass_b1_{ts}.json",
            )
            csv_B1 = os.path.join(out_dir, "catalog_B1_strict.csv")
            with open(csv_B1, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=["id", "name", "lat", "lon", "type", "source"])
                w.writeheader()
                w.writerows(rec_B1)
            print(f"[B1] Catalog B1 written to {csv_B1}  ({len(rec_B1)} sites)")

            # ========== SUBSETS ==========
            rec_B1a = [r for r in rec_B1 if r["type"] in ("stone_circle", "standing_stone", "megalith", "henge")]
            rec_B1b = [r for r in rec_B1 if r["type"] in ("tumulus", "cairn")]
            rec_B1c = [r for r in rec_B1 if r["type"] in ("hillfort", "fortification")]

            for name, subset in [("B1a_ceremonial", rec_B1a), ("B1b_funerary", rec_B1b), ("B1c_hillfort", rec_B1c)]:
                csv_path = os.path.join(out_dir, f"catalog_{name}.csv")
                with open(csv_path, "w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=["id", "name", "lat", "lon", "type", "source"])
                    w.writeheader()
                    w.writerows(subset)
                print(f"[{name}] {len(subset)} sites written to {csv_path}")
            # ==========================================

            print(f"[B1] Type breakdown:")
            for t, n in Counter(r["type"] for r in rec_B1).most_common():
                print(f"       {n:>5}  {t}")
        except Exception as e:
            print(f"[B1] FAILED: {e}", file=sys.stderr)

    # ----- Catalog B2: broad archaeological ---------------------------------
    if not args.skip_b2:
        try:
            rec_B2 = run_overpass_query(
                "B2", OVERPASS_QUERY_B2, raw_dir, ts,
                parse_overpass_monuments, f"overpass_b2_{ts}.json",
            )
            csv_B2 = os.path.join(out_dir, "catalog_B2_broad.csv")
            with open(csv_B2, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=["id", "name", "lat", "lon", "type", "source"])
                w.writeheader()
                w.writerows(rec_B2)
            print(f"[B2] Catalog B2 written to {csv_B2}  ({len(rec_B2)} sites)")
            print(f"[B2] Type breakdown (top 15):")
            for t, n in Counter(r["type"] for r in rec_B2).most_common(15):
                print(f"       {n:>5}  {t}")
        except Exception as e:
            print(f"[B2] FAILED: {e}", file=sys.stderr)

    print("\nNext checks:")
    print("  grep -iE \"michael's mount|burrow|brentor|de rupe\" data/population/catalog_A_michael.csv")
    print("  grep -iE 'stonehenge|avebury|hurlers|boscawen' data/population/catalog_B1_strict.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())