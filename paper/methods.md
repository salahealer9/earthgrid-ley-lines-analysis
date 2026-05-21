# 2. Methods

We test the canonical Michael ley line corridor in southern Britain against six concentric Monte Carlo null tests, each progressively addressing a specific class of statistical confound. The framework is designed so that significance must survive *all* six tests for the corridor to be considered exceptional at the level of population geography. All catalogs, scripts, and per-trial outputs are archived at Zenodo under DOI [10.5281/zenodo.20307501](https://doi.org/10.5281/zenodo.20307501) (v0.1.0).

## 2.1 Test statistic and Monte Carlo framework

A great circle on the unit sphere is parameterized by its (unsigned) pole vector **n** ∈ S². The perpendicular spherical distance from a point **p** ∈ S² to the great circle is

> d(p, n) = arcsin(|p · n|) · R⊕,

where R⊕ = 6371 km. For a reference catalog C of N sites (each represented as a unit vector on the sphere) and a corridor half-width w, we define the test statistic

> K(w; n; C) = #{p ∈ C : d(p, n) ≤ w}.

For each null mode, T = 10,000 random poles {n_t} were drawn under the mode's sampling distribution and K_t(w) was computed for each. The one-sided p-value is

> p(w) = (#{t : K_t(w) ≥ K_real(w)} + 1) / (T + 1),

with the canonical corridor evaluated at K_real(w) = K(w; n_canonical; C). The z-score is reported as (K_real − E[K_null]) / SD[K_null].

Widths swept: w ∈ {5, 10, 20, 50, 100} km.

## 2.2 Reference catalogs

Three reference catalogs of culturally significant sites in southern Britain were assembled independently of any ley-line tradition. All three were filtered to the bounding box defined in Section 2.4 and deduplicated at a 100 m spatial threshold to remove near-coincident OSM duplicates.

**Catalog A — St. Michael church dedications (N = 754).** OSM Overpass query for `amenity=place_of_worship` records whose name begins with "St Michael", "Saint Michael", or "Church of St Michael" (anchored regex, case-insensitive), supplemented by the Welsh form "Mihangel" (unanchored) and multilingual fallbacks on the `name:en` and `name:cy` tags.

**Catalog B1 — Strict prehistoric and Iron-Age monuments (N = 2422).** OSM Overpass query for `historic ∈ {stone_circle, standing_stone, menhir, megalith, tumulus, cairn, hillfort}`, plus records tagged `historic=archaeological_site` whose `archaeological_site` subtype falls within `{stone_circle, standing_stone, megalith, tumulus, cairn, barrow, henge, dolmen, fortification}`. UK hillforts are commonly mapped under the latter convention; this filter ensures their inclusion.

**Catalog B2 — Broad archaeological catalog (N = 5500).** All OSM records tagged `historic=archaeological_site` in the bounding box, irrespective of subtype. Includes Roman villas, ridge-and-furrow agriculture, settlements, and other non-prehistoric material. B2 is reported as a sensitivity/robustness check on B1.

All three catalogs were verified against canonical sites: St Michael's Mount, Burrow Mump, and Brentor Church appear in A; Stonehenge, Avebury, the Hurlers, and Boscawen-un appear in B1. Catalog snapshots are stored with query timestamps under `data/population/raw/` to preserve reproducibility against the OSM state at the time of testing.

For the global sanity check (Section 2.5.6), a fourth catalog of N = 1154 UNESCO World Heritage Sites was retrieved from the WHC syndication feed.

## 2.3 Canonical corridor

The canonical Michael corridor is defined by the great circle through the pair (St Cleer Well, Throwleigh), the optimal site pair from a 130-site KML extraction of the alignment as published in the Miller–Broadhurst tradition (*The Sun and the Serpent*, 1989). The corresponding pole is

> **n**_canonical = (+33.330°, −147.354°),

with a bearing of 61.7° at the bounding-box center. The 130-site catalog is curated and is used in this work *only* to define the corridor geometry under test; Section 2.5.5 examines whether this curatorial choice is faithful to the underlying tradition's vertex data. The 130-site catalog is not used as a reference catalog in any test.

For cross-pole stability, a second canonical pole (+33.465°, −147.811°), defined by the equivalent best-pair search on the older 12-site catalog, was tested in parallel.

Both poles give equivalent population significance to within Monte Carlo noise (p_joint at w=50km differing by less than a factor of 2), establishing a cross-pole stability envelope of approximately 50 km within which the corridor's significance is robust.

## 2.4 Bounding box

Tests were conducted within a fixed bounding box covering southern Britain:

> latitude ∈ [49.5°, 53.5°] N, longitude ∈ [6.5° W, 2.5° E].

The box contains the entire Cornwall-to-East-Anglia stretch of the canonical alignment with > 100 km margin on all sides, and excludes Scotland, Ireland, and continental Europe. The bounding-box center is (51.5° N, 2.0° W) and its half-diagonal is approximately 383 km, used in Section 2.5.2 as the rejection-sampling tolerance for random corridors required to pass through the data region.

## 2.5 Six concentric tests

### 2.5.1 Test 1 — Internal null

The internal null fixes the catalog of canonical waypoints and randomizes the corridor by applying three rearrangement schemes to the catalog itself: `lon_shuffle` (longitudes permuted across fixed latitudes), `uniform_sphere` (positions resampled uniformly), and `lon_uniform` (longitudes resampled uniformly within the bbox). For each rearranged catalog, the best-pair search (enumerating C(N,2) candidate poles and taking the maximum K over all pairs) is rerun. This test asks whether the canonical sites cluster more tightly on *any* great circle than randomly arranged versions of themselves.

This test is internal to the curated catalog and cannot distinguish "the corridor is real" from "the curator chose sites that lie on a corridor." It is included for completeness and as a baseline that the subsequent population-level tests are designed to discriminate against.

### 2.5.2 Test 2 — Population null (isotropic)

The canonical corridor is fixed at **n**_canonical, and 10,000 random great-circle poles are sampled uniformly on S² subject to a single rejection criterion: a candidate pole is accepted if its minimum spherical distance to the bounding-box center is ≤ 383 km (the half-diagonal). This ensures the corresponding great circle traverses the data region. K is computed against each reference catalog independently.

This test addresses the curator-independence concern: the reference catalog is exhaustive within the bbox and independent of the 130-site KML curation.

### 2.5.3 Test 3 — Population null (bearing-restricted)

Identical to Test 2, but with an additional rejection: each random pole's bearing at the bbox center must lie within ±D° (undirected, mod 180°) of the canonical bearing (61.7°). Three tolerances were run independently: D ∈ {30°, 15°, 5°}. The bearing at a point on a great circle is computed as the angle between the great circle's tangent at that point and the local north direction, in the local east-north plane.

This test addresses the orientation-confound concern: any NE-SW great circle through Britain might over-populate British site catalogs simply because the British landmass is NE-SW oriented. If the canonical corridor's significance is driven by orientation alone, K_null mean should rise substantially as D tightens. If it is driven by the specific corridor location, K_null mean should remain approximately constant.

### 2.5.4 Test 4 — Joint conjunction

The per-catalog tests (Tests 2 and 3) treat the three reference catalogs independently. Test 4 samples random poles *once* and computes K against all three catalogs from the same set of trials. The joint test statistic at width w is

> n_joint(w) = #{t : K_t^{B1}(w) ≥ K_real^{B1}(w) ∧ K_t^A(w) ≥ K_real^A(w) ∧ K_t^{B2}(w) ≥ K_real^{B2}(w)},

with p_joint(w) = (n_joint(w) + 1) / (T + 1). The Bonferroni threshold from Section 2.6 applies to each width independently.

The Pearson correlation of K across trials between each catalog pair is also recorded, to quantify catalog dependence. A small p_joint that is markedly below the strongest individual marginal indicates that the corridor is doing genuine conjunctive work rather than merely reflecting correlated catalogs.

### 2.5.5 Test 5 — Pole sensitivity

The canonical 130-site pole is a curatorial choice: the KML on which it is based contains both the alignment (the straight line) and two meandering "current" LineStrings (the Mary and Michael currents in the Miller–Broadhurst tradition). To verify that the result is not specific to the straight-line abstraction, we fit a great circle directly to:

- the Michael current LineString (3947 vertices);
- the Mary current LineString (4945 vertices);
- the union of both (8892 vertices).

The fit minimizes the sum of squared perpendicular spherical distances from the points to the great circle. The minimizer is the eigenvector of M = Σᵢ pᵢpᵢᵀ associated with the smallest eigenvalue, equivalently the smallest right singular vector of the stacked unit-vector matrix. The residuals (perpendicular distances from each vertex to its fitted great circle) are reported as RMS, median, 95th percentile, and maximum, providing a geometric coherence metric for the meandering currents that is independent of the population tests. The full population test (Sections 2.5.2 and 2.5.4) was then run on each fitted pole.

If the canonical 130-site pole is an arbitrary or unfaithful summary of the underlying tradition, this test will fail: the fitted poles will differ from the canonical, and the population significance will not replicate. If the canonical pole is empirically a good summary, the fitted poles will land within the cross-pole stability envelope (established to be at least ~50 km in Section 2.3), and p_joint will replicate to within Monte Carlo noise.

### 2.5.6 Test 6 — Global sanity check

The canonical Michael corridor, when extended around the Earth, passes near several internationally recognizable sites. To quantify whether this constitutes a global signal or merely the standard "ley-line fallacy" — the observation that any 40,000 km great circle through populated regions will pass near comparable numbers of named sites — we count UNESCO World Heritage Sites within a fixed half-width of (a) the canonical Michael corridor, (b) the optimized corridor from Test 4 trial 1583 (the single random trial in the upper tail of the joint null distribution, which captured 436 B1 sites within 5 km), and (c) 10,000 random great circles uniform on S² with no bbox restriction.

The closed-form expected count for a random great circle at half-width w is N · sin(w/R⊕), the surface-area fraction of a spherical band. This is computed as a validation check on the empirical null mean.

This test deliberately uses a different null distribution (global, isotropic) than the population tests (UK bbox), because the question being asked is different: not "is the corridor exceptional within Britain?" but "is the corridor exceptional planet-wide?"

## 2.6 Significance threshold

Each test is reported across five widths. To control the family-wise Type I error rate, we apply Bonferroni correction at α = 0.05 across the five widths, giving a per-width threshold of p < 0.01. Cells crossing this threshold are reported as Bonferroni-significant. Cells with raw p < 0.05 but failing Bonferroni are reported as marginal.

Bonferroni is intentionally conservative given the strong positive correlation in K_t across widths within a single trial. We did not apply Holm–Bonferroni or false-discovery-rate control in order to keep the reporting transparent and the comparisons consistent across catalogs.

## 2.7 Software and reproducibility

All code and reference catalogs are open-source under Apache-2.0 (code) and CC-BY-4.0 (data and documentation), archived under DOI [10.5281/zenodo.20307501](https://doi.org/10.5281/zenodo.20307501) and additionally preserved in the Software Heritage long-term archive:

```
swh:1:dir:eacb8ff55520d38a30109b759eb302e2e43a9eaa
```

The implementation uses Python 3.10+ with NumPy as the only external dependency; data fetching is via the standard library. The Zenodo deposit includes timestamped snapshots of all reference catalogs (OSM Overpass and UNESCO WHC responses), so the tests are reproducible against the same catalog state even if the upstream data sources change.

The scripts implementing each test are:

| Test | Script |
|---|---|
| 1 — internal null | `scripts/corridor_null_test.py` |
| 2, 3 — population null (per catalog) | `scripts/population_corridor_test.py --bearing-tolerance D` |
| 4 — joint conjunction | `scripts/triple_corridor_test.py` |
| 5 — pole sensitivity (fit only) | `scripts/best_fit_great_circle.py` |
| 6 — global UNESCO | `scripts/unesco_global_sanity_check.py` |

Catalogs are rebuilt by `scripts/build_population_catalogs.py`, which fetches from the OpenStreetMap Overpass API and (when available) Wikidata SPARQL. The KML extraction of canonical sites and current LineStrings is performed by `scripts/extract_kml_coordinates.py`. All scripts accept `--seed` for deterministic reproduction. Per-trial outputs are saved as CSV alongside summary JSON for downstream inspection.

End-to-end runtime for all six tests on the catalogs reported here, on a single Hetzner cloud instance (Ubuntu, 8 GB RAM, no GPU), is under five minutes excluding the initial OSM Overpass and UNESCO catalog fetches.
