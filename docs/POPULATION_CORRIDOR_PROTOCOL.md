# POPULATION CORRIDOR — Scientific Protocol

**Purpose.** The `CORRIDOR_PROTOCOL.md` test established that the canonical 12-site St. Michael Line catalog admits a great-circle corridor (pair 0,3 — Carn Les Boel ↔ The Hurlers) that captures all 12 sites at half-width 5 km, with p ≈ 0.001 and z ≈ 16 against three independent nulls.

That result conditions on the catalog. The 12 sites were originally curated, in part, *because* they appeared aligned. The published p-value answers the well-defined question "given these 12 specific points, are their longitudinal arrangement and the corridor consistent with chance?" — but it does **not** address the prior question: "is the curated 12-site catalog itself an extremal subsample of a broader population that does not align?"

This protocol inverts the test. The corridor is now fixed; the catalog is varied. It asks whether an independent, exhaustive reference catalog over-populates the canonical Michael Line corridor relative to (a) random great circles over the same region and (b) random size-12 subsamples of the reference catalog.

---

## Question

> Does an independent reference catalog of culturally significant pre-modern sites in southern Britain over-populate the great-circle corridor through (Carn Les Boel, The Hurlers) more than:
> (i) random great-circle corridors over the same region, or
> (ii) random size-12 subsamples drawn from the same reference catalog reproduce the canonical 12-of-12 capture?

If both fail to reject, the canonical Michael Line is a curated subset of a population that does not align — the alignment is selection-driven. If either rejects, the alignment survives population-level scrutiny.

---

## Two reference catalogs

The two catalogs answer different sub-questions and are run independently. Reporting must keep them separate.

### Catalog A — St. Michael church dedications

Tests whether the **dedication pattern** is corridor-aligned. This is the closest population analogue of the canonical claim, since the Michael Line is defined by Michael dedications.

Primary source: **Wikidata** (clean, queryable, citable). Filter:

- `wdt:P31` (instance of) → church / chapel / subclass thereof (`wd:Q16970` church building, `wd:Q317557` parish church, etc.)
- `wdt:P825` (dedicated to) = `wd:Q47652` (Michael the Archangel)
- `wdt:P625` (coordinate location) inside the bounding box

Supplementary sources (added if Wikidata coverage looks sparse, with provenance flag preserved per record):

- **National Heritage List for England (NHLE)** — bulk CSV, grep `(?i)\bst\.?\s*michael\b` in the listed-building name field.
- **Canmore** (Historic Environment Scotland) — for completeness, though all 12 canonical sites are in England.
- **Coflein** (Royal Commission on the Ancient and Historical Monuments of Wales) — supplementary; the corridor barely clips Wales but a few coastal Welsh dedications could fall within wide widths.

If a candidate church appears in both Wikidata and NHLE, deduplicate by spatial proximity (< 100 m) on the (lat, lon) pair.

### Catalog B — prehistoric monuments

Tests whether **any class of culturally significant pre-Christian site** over-populates the corridor. This is the harder, selection-resistant test: if megaliths cluster on the corridor independent of any Christian framing, the alignment predates the dedications it was named for.

Primary source: **OpenStreetMap (Overpass API)**. Tags:

- `historic=stone_circle`
- `historic=standing_stone`
- `historic=megalith`
- `historic=tomb`
- `historic=tumulus`
- `historic=hillfort`
- `historic=archaeological_site` with `archaeological_site` ∈ {`megalith`, `tumulus`, `barrow`, `henge`, `tomb`}

Supplementary: **Historic England Pastscape** (authoritative monument inventory; bulk download via Heritage Gateway). The OSM-only first pass is enough to validate the protocol; Pastscape is only added if OSM coverage looks visibly thin.

Records with no coordinates, only addresses, are dropped (no geocoding — too noisy at the 5 km scale we care about).

---

## Bounding box

> lat ∈ [49.5°, 53.5°] N, lon ∈ [-6.5°, +2.5°] E

Rationale:

- Contains all 12 canonical Michael Line sites with > 100 km margin on each side.
- Contains the entire Cornwall–East Anglia stretch of the canonical corridor.
- Excludes Scotland, Ireland, and continental Europe — keeping the test focused on the region the canonical claim is about, and avoiding smuggling in unrelated geography that would dilute the population.
- Truncating the corridor at the box edges is acceptable: the test statistic counts catalog sites in the band, and we are not extrapolating the corridor beyond the data region.

Both catalogs are filtered to this box before any further processing.

---

## Test statistic

The corridor is **fixed** at the canonical (0,3) great circle from the original test:

- Pole: (+33.465°, -147.811°)
- Defining pair: Carn Les Boel (+50.0461, -5.7142) ↔ The Hurlers (+50.5160, -4.4582)
- Pair separation: 103.4 km (0.93°)

For each catalog C of size N(C):

> K(w; C) = #{ p ∈ C : d(p, n_canonical) ≤ w }

with d(p, n) = arcsin(|n · p|) · R_⊕, swept over w ∈ {5, 10, 20, 50, 100} km. This matches the width sweep used for the canonical 12-site test.

---

## Two nulls (run separately, both reported)

### Null 1 — random corridors over the bounding box (population-level)

Holds the catalog fixed at the real C; randomizes the corridor.

For trial t = 1 … T:

1. Sample a random great-circle pole **n_t** uniformly on S², subject to the constraint that the corresponding circle intersects the bounding box. (Implementation: reject poles whose great circle does not cross the box.)
2. Compute K_t(w) = #{ p ∈ C : d(p, n_t) ≤ w } for each w.
3. p₁(w) = (#{ K_t(w) ≥ K_real(w) } + 1) / (T + 1)

This is the population analogue of `uniform_sphere` from `CORRIDOR_PROTOCOL.md`, with the symmetry inverted: instead of "given a fixed corridor, are these specific 12 points exceptional?" we ask "given this exhaustive catalog, is this specific corridor exceptional?"

### Null 2 — random size-12 subsamples (selection-level)

Holds the corridor randomization aside; tests whether the canonical 12-of-12 count is reproducible by random draws from the broader catalog.

For trial t = 1 … T:

1. Draw a uniformly random size-12 subset C_t ⊂ C (without replacement).
2. Run the **best-pair search** from `CORRIDOR_PROTOCOL.md` on C_t — i.e. enumerate the C(12, 2) = 66 candidate normals, count sites within w of each, take the maximum over normals.
3. K_t^max(w) = max-over-normals count for C_t.
4. p₂(w) = (#{ K_t^max(w) ≥ 12 } + 1) / (T + 1)

This null asks: *if I randomly picked 12 sites from the same broader population, how often would a best-pair corridor through them capture all 12?*

If p₂ is small, the canonical 12 are selection-extremal — but that itself is consistent with either (a) the catalog was hand-curated to align (selection bias), or (b) the broader population genuinely has rare alignment structure that the canonical 12 happen to instantiate. p₂ alone cannot distinguish these. p₁ does the disentangling.

### How to read the joint outcome

| p₁ (random corridors) | p₂ (random subsamples) | Reading |
|---|---|---|
| significant | significant | Canonical corridor is exceptional **and** canonical 12 are an exceptional subsample. Strongest result: the alignment is real and the catalog reflects it. |
| significant | not significant | Canonical corridor is exceptional, but 12-of-12 capture is generic for size-12 subsamples in this region. The corridor matters; the specific 12 sites do not. |
| not significant | significant | Canonical corridor is unremarkable as a great circle through this region, but the 12 are an extremal subsample on it. Selection bias has not been ruled out — the curators picked an unusually tight 12 from a population that would not have produced this corridor on its own. |
| not significant | not significant | Population shows nothing at this corridor, and the canonical 12-of-12 capture is generic. The Michael Line is a curated artifact. |

The (sig, not-sig) cell — corridor matters, exact site list does not — is the most plausible "real and not just selection bias" outcome and is well worth distinguishing from the others.

---

## Pre-registration

Lock these before running:

1. **Bounding box.** lat ∈ [49.5°, 53.5°], lon ∈ [-6.5°, +2.5°].
2. **Catalogs.** Catalog A from Wikidata (with NHLE supplement if Wikidata count < 100). Catalog B from OSM Overpass with the tag list above. Both filtered to bounding box. Both deduplicated at 100 m.
3. **Corridor.** Fixed at canonical (0,3) pole = (+33.465°, -147.811°). No re-fitting.
4. **Widths.** {5, 10, 20, 50, 100} km. Headline finding is at w ≤ 20 km, where the canonical test was tightest.
5. **Nulls.** Both Null 1 and Null 2, run separately on each catalog.
6. **Trials.** T = 10,000 per null. (Cheap: each trial is a few-millisecond matmul.)
7. **Significance threshold.** Per-width raw p < 0.05; family-wise Bonferroni p < 0.01 across 5 widths. Both catalogs and both nulls reported regardless of outcome.
8. **Catalog snapshots.** Save Wikidata SPARQL response and Overpass response as on-disk artifacts with the query timestamp, so the test is reproducible against the same population state. Include in the Zenodo deposit.

---

## Files (planned)

- `scripts_geophys/build_population_catalogs.py` — fetches Wikidata + Overpass into `data/population/catalog_A_michael.csv` and `data/population/catalog_B_megaliths.csv`. Saves raw responses under `data/population/raw/`.
- `scripts_geophys/population_corridor_test.py` — runs Null 1 and Null 2 for a given catalog and corridor, with `--null-mode {random_corridor,random_subsample}` and `--resume`. Output schema parallel to `corridor_null_test.py`.
- `results_corridor/population/<catalog>_<null>.json` — summary.
- `results_corridor/population/<catalog>_<null>.trials.csv` — per-trial log.
- `POPULATION_CORRIDOR_PROTOCOL.md` — this file.

---

## Sanity checks

Before running on the real catalogs:

- **Validation against canonical 12.** Pass the canonical 12-site catalog through Null 2 (random size-12 subsamples drawn from itself, with replacement disabled and excluding the actual 12 — i.e. trivially 0 alternative draws). This should error out gracefully on the empty draw space. The check is that the script handles "subsample drawn from itself" sensibly.
- **Catalog A spot check.** St Michael's Mount must appear in Catalog A (it is dedicated to Michael, has a chapel on it, is in Wikidata). Burrow Mump and Brentor Church likewise. If any of the canonical sites with Michael dedications are missing from Catalog A, the catalog is incomplete and needs the NHLE supplement before the test runs.
- **Catalog B spot check.** Stonehenge, Avebury, The Hurlers, Boscawen-un must appear in Catalog B. Stonehenge is just outside the canonical 12 but inside the bounding box — its presence in Catalog B is a sanity check, not a test contamination.
- **Bounding-box integrity.** Plot the catalogs against the bounding box and the canonical corridor. Visual inspection should show: (a) catalogs filling the box, not concentrated at edges in a way that suggests geocoding artifacts; (b) the canonical 12 falling on the corridor as expected.

---

## Why this is enough

If the canonical Michael Line corridor over-populates an exhaustive, independently-sourced catalog of either Michael dedications **or** prehistoric monuments — relative to random corridors over the same region — that is a population-level result that selection bias on the canonical 12 cannot manufacture. The 12 were curated; Wikidata and OSM were not.

Conversely, if both catalogs come back null, the canonical alignment is best understood as a property of the curated catalog rather than the underlying landscape, and any further claims about the Michael Line should reflect that.

This is not the end of the question — a positive result here would naturally extend to the broader 160-site sacred-site catalog and the E8 alignment work — but it is the cleanest possible test of the selection issue raised by the original 12-site result, and it can be run end-to-end on the existing Hetzner infrastructure with no new dependencies beyond `requests` for the API calls.
