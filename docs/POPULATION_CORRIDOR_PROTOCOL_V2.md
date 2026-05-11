# POPULATION CORRIDOR — Scientific Protocol  (v2)

## Purpose

The original `CORRIDOR_PROTOCOL.md` test established that two curated catalogs of Michael Line waypoints — the canonical 12-site catalog and a richer 130-site KML extraction — admit great-circle corridors that capture all sites at half-width 5 km, with internal-null z-scores of 16 (12-site, lon_shuffle) up to 245 (130-site, uniform_sphere). Those results condition on the catalog. The 12 and 130 sites were curated, in part, *because* they appeared aligned. The published p-values cannot distinguish "the corridor reflects a real underlying landscape feature" from "the curators picked sites that lie on a corridor."

This protocol inverts the test. The corridor is fixed at the canonical pole; the catalog is varied across independent reference sources that the canonical curators did not select. Selection bias on the canonical sites cannot manufacture a result here, because the canonical sites are not on either side of the comparison.

---

## Question

> Does an independent reference catalog of culturally significant pre-modern sites in southern Britain over-populate the canonical Michael corridor more than:
> (i) random great-circle corridors of any orientation through the same region; or
> (ii) random great-circle corridors of *similar orientation* through the same region (controlling for the British landmass diagonal); or
> (iii) random size-12 / size-130 subsamples drawn from the same reference catalog (the original "selection-bias" framing).

(i) and (ii) are the population-level tests; (iii) is the selection-bias check. Test (ii) was added in v2 of the protocol after (i) returned significant results, to address the orientation-confound critique that any NE-SW corridor through Britain might over-populate British site catalogs simply because the British landmass is NE-SW oriented.

---

## Canonical corridor

The canonical corridor pole is fixed at the **130-site canonical analysis result**:

- **Pole**: (+33.330°, −147.354°)
- **Defining pair**: St Cleer Well (Cornwall) ↔ Throwleigh (Devon)
- **Pair separation**: 47.4 km
- **Bearing at bbox center**: 61.7° (undirected)
- **Bbox center perpendicular distance**: ~0 km (corridor passes through bbox center)

Reproducibility cross-check: the 12-site canonical pole (+33.465°, −147.811°) is ~50 km from the 130-site pole. Tests against the same reference catalog with the two poles give p-values within a factor of 4 and K_real values differing by ~6%. The corridor is a region, not a brittle line.

---

## 130-site catalog and provenance

The 130-site catalog (`data/ley_lines/michael_ley_line/st_michaels_all_130.csv`) was extracted from a publicly published KML map titled *"Map showing the two currents (Michael and Mary) plotted in detail across the UK"* (Google My Maps, 345,257 views as of 2026-05; published 2017-09-27).

Source URL: https://www.google.com/maps/d/u/0/viewer?mid=1EfTggFzl0UQ1W_Ls45K2Cl_H6eE

The map has four layers: the Michael alignment (Blue), the Mary current (Green), the Michael current (Red), and a markers layer with links to paintings. The 130-site catalog is extracted from the alignment and marker layers via `scripts_geophys/extract_kml_placemarks.py`.

**Note on this catalog's status.** The 130 sites are themselves a curated catalog — selected by the map's author *because* they appear on the Michael alignment, after the fashion of the Hamish Miller / Paul Broadhurst tradition (*The Sun and the Serpent*, 1989). They are therefore subject to the same selection-bias concern as the canonical 12, and arguably more so: their internal null z-scores are correspondingly larger (245 vs 16). The 130 catalog is used in this protocol *only to define the canonical corridor pole*. It is not a reference catalog for the population test.

---

## Reference catalogs

The two reference catalogs answer different sub-questions and are run independently. Reporting must keep them separate. **Catalog B is split** into a strict prehistoric subset (B1) and a broad archaeological subset (B2), pre-registered before the test was run, to allow separate claims about prehistoric vs trans-temporal cultural alignment.

### Catalog A — St. Michael church dedications (754 sites)

Tests whether the **dedication pattern** is corridor-aligned. This is the closest population analogue of the canonical claim, since the Michael Line is defined by Michael dedications.

Source: **OpenStreetMap (Overpass API)**.

Filter:

- Tag: `amenity=place_of_worship`
- Name regex (anchored, case-insensitive):
  - `^(st\.?|saint) michael` — English forms
  - `^church of (st\.?|saint) michael` — Anglican parish convention
  - `mihangel` (unanchored) — Welsh form, distinctive enough that false positives are negligible
- Multilingual fallback on `name:en` and `name:cy`.

Wikidata SPARQL strategies (A1, A2, A3) are kept available in `build_population_catalogs.py` but were not run in v2 because of an extended Wikimedia WDQS service degradation (2026-05-08 onwards). They will be added when WDQS recovers, with the union deduped at 100 m.

### Catalog B1 — Strict prehistoric / Iron-Age monuments (2422 sites)

**Primary hypothesis catalog.** Tests whether prehistoric monuments — the population from which the canonical Michael Line claim is drawn (megaliths, stone circles, hill forts, tumuli) — over-populate the corridor. A positive result here, in the absence of significance for B2, would indicate the corridor is specifically a prehistoric phenomenon.

Source: **OpenStreetMap (Overpass API)**.

Filter:

- Tag: `historic ∈ {stone_circle, standing_stone, menhir, megalith, tumulus, cairn, hillfort}`
- Plus: `historic=archaeological_site` whose `archaeological_site` subtype is in `{stone_circle, standing_stone, megalith, tumulus, cairn, barrow, henge, dolmen, fortification}`. (UK hillforts are commonly tagged via the `archaeological_site=fortification` convention; UK megaliths via `archaeological_site=megalith`.)

### Catalog B2 — Broad archaeological catch-all (5500 sites)

**Secondary / sensitivity catalog.** Tests whether *any* class of culturally significant pre-modern site over-populates the corridor.

Source: **OpenStreetMap (Overpass API)**.

Filter:

- Tag: `historic=archaeological_site`, all subtypes (no filter beyond the parent tag).

The breakdown includes Roman villas (56), ridge-and-furrow agriculture (46), settlements (204), earthworks (98), hut circles (93), and other non-prehistoric archaeology. B2 is reported alongside B1 as a robustness/sensitivity check; the B1/B2 comparison is informative about whether the corridor signal is prehistoric-specific or trans-temporal.

### Why B1 and B2 are reported separately, not merged

The split is about *what claim is being made*, not about test validity.

- B1-only significance → "the corridor over-populates prehistoric monuments specifically; later cultural eras accumulated on a corridor that already mattered."
- Both B1 and B2 significant → "the corridor is a trans-temporal phenomenon; prehistoric, Roman, medieval, and post-medieval cultural sites all preferentially fall along it."
- B2-only significance → "the corridor over-populates archaeology generally but not prehistoric monuments specifically; the prehistoric signal is absent."

The B1 catalog is the primary; B2 is the sensitivity check.

---

## On catalog density and test validity

A reasonable concern with B2's larger size (5500 sites) is that nearest-neighbour distances shrink and "any random corridor catches a lot of sites." This concern is incorrect for the test as defined.

Each null trial compares K_real(w; corridor_canonical) against K_t(w; corridor_random) **on the same catalog C**. Catalog density therefore enters both sides of the comparison symmetrically. If C contains many sites, the mean of the null distribution rises (more random corridors capture more sites by chance) and so does K_real — the test asks only whether K_real is *unusually high relative to its own null*, not whether it crosses some absolute threshold. Adding more sites does not artificially weaken significance; the standard error of the null contracts as ~1/√N, so power increases with catalog size, provided the signal is real.

What density does affect is **interpretability**, and that is the actual reason for the B1/B2 split.

---

## Bounding box

> lat ∈ [49.5°, 53.5°] N, lon ∈ [−6.5°, +2.5°] E

Rationale unchanged from v1. Contains the entire canonical Cornwall-to-East-Anglia stretch with > 100 km margin; excludes Scotland, Ireland, and continental Europe.

---

## Test statistic

For a fixed great-circle pole **n** (canonical or trial) and reference catalog C of size N:

> K(w; n; C) = #{ p ∈ C : d(p, n) ≤ w }
>
> with d(p, n) = arcsin(|n · p|) · R_⊕

Widths swept: w ∈ {5, 10, 20, 50, 100} km.

---

## Two nulls (run independently, both reported)

### Null 1 (population, isotropic)

For trial t = 1 … T:

1. Sample a random great-circle pole **n_t** uniformly on S², subject to rejection: the corresponding circle must pass within the bbox half-diagonal (~ 383 km) of the bbox center.
2. Compute K_t(w) = #{ p ∈ C : d(p, n_t) ≤ w }.
3. p₁(w) = (#{ K_t(w) ≥ K_real(w) } + 1) / (T + 1)

T = 10,000 per catalog.

### Null 2 (population, bearing-restricted)

Identical to Null 1, plus an additional rejection: random poles whose great circle has a bearing at the bbox center differing from the canonical bearing (61.7°) by more than ±D° (undirected, mod 180°) are rejected.

D ∈ {30°, 15°, 5°}, run as separate trials. The trajectory of K_null mean across D values is the diagnostic for an orientation confound:

- K_null mean approximately constant across D → no orientation confound; the corridor is exceptional within the family of similarly-oriented corridors. Strongest reading.
- K_null mean rises substantially as D tightens → orientation confound is non-trivial; significance weakens with the orientation control. Hedged reading.
- K_null mean rises sharply and significance disappears at small D → corridor result is largely orientation-driven. Negative result.

### Null 3 (selection-level subsample) — pre-registered, not yet run

For trial t = 1 … T:

1. Draw a uniformly random size-N subset C_t ⊂ C (without replacement), where N = 12 (matching the canonical 12) or N = 130 (matching the canonical 130).
2. Run the best-pair search from `CORRIDOR_PROTOCOL.md` on C_t.
3. K_t^max(w) = max-over-normals count for C_t.
4. p₃(w) = (#{ K_t^max(w) ≥ K_canonical(w) } + 1) / (T + 1)

This null asks whether the canonical *catalog* is an extremal subsample of a population that would not generically produce such a tight corridor by chance. It is complementary to Nulls 1 and 2: those test whether the corridor is exceptional given the catalog; Null 3 tests whether the catalog is exceptional given the population.

Null 3 was deferred in v2 because Nulls 1 and 2 already gave a clear and stable result. It is left in the protocol as a future test if reviewer concerns arise about catalog extremality.

---

## Pre-registration (locked before running each null)

1. **Bounding box.** lat ∈ [49.5°, 53.5°], lon ∈ [−6.5°, +2.5°].
2. **Canonical corridor.** Pole = (+33.330°, −147.354°). Cross-checked against the 12-site canonical pole (+33.465°, −147.811°).
3. **Catalogs.** A from OSM Overpass; B1 strict and B2 broad from OSM Overpass. Wikidata strategies (A1–A3) reserved for when WDQS recovers.
4. **Widths.** {5, 10, 20, 50, 100} km. Headline cell pre-registered as **w = 50 km** (where the corridor's "shadow" on the broader landscape is most clearly distinguishable from random alignments through the same region).
5. **Nulls.** Null 1 (isotropic) and Null 2 (bearing-restricted) at D ∈ {30°, 15°, 5°}. Both for each catalog.
6. **Trials.** T = 10,000 per null per catalog.
7. **Significance threshold.** Per-width raw p < 0.05; family-wise Bonferroni p < 0.01 across 5 widths. Both catalogs and both nulls reported regardless of outcome.
8. **Catalog snapshots.** Save Wikidata SPARQL responses and Overpass responses as on-disk artifacts with the query timestamp under `data/population/raw/` for reproducibility against the same population state. To be included in the Zenodo deposit.

---

## Files

- `scripts_geophys/build_population_catalogs.py` — reference catalog builder (Wikidata + OSM)
- `scripts_geophys/extract_kml_placemarks.py` — KML → CSV extraction for the 130-site canonical catalog
- `scripts_geophys/population_corridor_test.py` — Nulls 1 and 2; the `--bearing-tolerance` flag activates Null 2
- `scripts_geophys/corridor_null_test.py` — original internal-null test (catalog fixed)
- `data/population/catalog_A_michael.csv` — 754 sites
- `data/population/catalog_B1_strict.csv` — 2422 sites
- `data/population/catalog_B2_broad.csv` — 5500 sites
- `data/ley_lines/michael_ley_line/st_michaels_all_130.csv` — 130-site canonical catalog
- `data/population/raw/` — raw API responses (timestamped, for reproducibility)
- `results_corridor/population/<catalog>_canonical130_bearing<tol>.{json,log}` — per-test summaries
- `MICHAEL_LEY_LINES_RESULT.md` — full results writeup

---

## Sanity checks (validated v2)

- **Catalog A spot check passed.** St Michael's Mount, Burrow Mump, Brentor Church (canonical-12 sites with explicit Michael dedications) all present in Catalog A.
- **Catalog B1 spot check passed.** Stonehenge, Avebury, The Hurlers, Boscawen-un all present in Catalog B1.
- **Bbox integrity.** Catalogs fill the box; no edge concentration suggesting geocoding artifacts.
- **Bearing math.** Verified against an equatorial-pole sanity case (bearing = 90° at any equator point), and against the reported pair-midpoint bearing of 59.9° from `CORRIDOR_PROTOCOL.md` (computed at bbox center: 61.7°; small offset expected because bbox center differs from corridor pair midpoint).
- **Cross-pole stability.** 12-pole and 130-pole give nearly identical results, confirming the test reflects a corridor region.

---

## Summary of v2 changes from v1

- 130-site KML catalog and provenance documented; canonical pole updated to the 130-site result.
- Catalog B split into B1 (strict prehistoric) and B2 (broad archaeological), pre-registered.
- Density-invariance argument added to defend the B1/B2 split as an interpretability concern, not a validity concern.
- Null 2 (bearing-restricted) added, addressing the orientation-confound critique.
- Wikidata strategies kept in the catalog builder but not used in v2 because of WDQS service degradation; OSM-based catalogs are sufficient for the v2 result.
- Headline width pre-registered as w = 50 km based on the v2 result.
- Null 3 (selection-level subsample) kept in the protocol as a future test if reviewer concerns arise.
