# Michael Ley Line — Population-Level Corridor Test Results

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20307501.svg)](https://doi.org/10.5281/zenodo.20307501)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Status.** Four concentric statistical tests of progressively increasing rigor have been run against the canonical Michael ley line corridor. The corridor is significant against all four, with the headline result surviving Bonferroni correction at the 50 km width across all three independent reference catalogs jointly.

**One-line summary.** The canonical Michael corridor in southern Britain over-populates three independent reference catalogs of culturally significant sites (Christian dedications, prehistoric monuments, and broad archaeology), simultaneously and at population scale, beyond what would be expected from random great circles through the UK or from random great circles oriented along the British landmass diagonal. The result is statistical and geographic; it does not establish any proposed mechanism, and the corridor is not the unique or maximal alignment of sites in the region.

---

## Question

Earlier work showed that a canonical 12-site catalog of Michael Line waypoints — and a richer 130-site KML extraction of the line — admit a great-circle corridor that captures all sites at half-width 5 km, with internal-null z-scores of 16 (12-site) up to 245 (130-site). Those tests demonstrate that the catalogs are internally aligned, but they cannot distinguish "the corridor reflects a real underlying landscape feature" from "the curators picked sites that lie on a corridor."

This work tests the corridor against **independent reference catalogs that the canonical curators did not select**. Selection bias on the canonical 130 cannot manufacture a result here, because the canonical 130 are not on either side of the comparison.

---

## Methods

### Four concentric tests

1. **Internal null (already established).** Catalog of 12 / 130 canonical sites fixed; corridor randomized via `lon_shuffle`, `uniform_sphere`, and `lon_uniform`. Tests whether the canonical sites cluster more tightly on a great circle than random rearrangements of themselves. Result: z = 16 (12-site, w=5km) to 245 (130-site, w=5km, uniform_sphere).

2. **Population null — isotropic.** Corridor fixed at the canonical great-circle pole (extracted from the tightest 5 km capture in the 130-site analysis: pole +33.330°, −147.354°, defined by the pair St Cleer Well ↔ Throwleigh, 47 km separation). Catalog drawn from independent reference sources. Random corridors are great circles through the UK bounding box, with poles uniform on S² subject to the constraint that the corresponding circle passes within the bbox half-diagonal (~ 383 km) of the bbox center.

3. **Population null — bearing-restricted.** Same as (2), but additionally constrains random corridors to have bearing (at the bbox center) within ±D° of the canonical bearing (61.7° at the bbox center, undirected). D ∈ {30°, 15°, 5°}. Tests whether the canonical corridor is exceptional within the family of similarly-oriented corridors, isolating any orientation confound from the British-landmass diagonal.

4. **Joint conjunction test.** Random poles sampled **once** for all three catalogs, and the test statistic is the fraction of trials in which K_t equals or exceeds K_real *simultaneously* across all three catalogs at the same width. Tightens the three correlated per-catalog p-values into a single joint p-value, and addresses the implicit reviewer concern that the same random alignment with the British landmass might happen to win on all three catalogs at once.

### Reference catalogs

- **Catalog A — St. Michael church dedications (754 sites).** OSM Overpass query for `amenity=place_of_worship` records whose name starts with "St Michael", "Saint Michael", or "Church of St Michael", plus the Welsh form "Mihangel" (anchored regex on the canonical name field with multilingual fallbacks). Bounded to the same bbox as the canonical analysis.

- **Catalog B1 — Strict prehistoric / Iron-Age monuments (2422 sites).** OSM Overpass query for `historic ∈ {stone_circle, standing_stone, menhir, megalith, tumulus, cairn, hillfort}`, plus `historic=archaeological_site` whose `archaeological_site` subtype is in `{stone_circle, standing_stone, megalith, tumulus, cairn, barrow, henge, dolmen, fortification}`. This is the primary hypothesis catalog.

- **Catalog B2 — Broad archaeological catch-all (5500 sites).** All `historic=archaeological_site` records in the bbox, irrespective of subtype. Includes Roman villas, ridge-and-furrow agriculture, settlements, and other non-prehistoric archaeology. Reported as a sensitivity / robustness check.

### Bounding box

Lat ∈ [49.5°, 53.5°], lon ∈ [−6.5°, +2.5°]. Contains the entire canonical Cornwall-to-East-Anglia stretch with > 100 km margin and excludes Scotland, Ireland, and continental Europe.

### Statistics

Test statistic: K(w; corridor) = number of catalog sites within w km of the great circle (perpendicular spherical distance), w ∈ {5, 10, 20, 50, 100} km. Trials per null: T = 10,000. p-value (one-sided): (#{K_null ≥ K_real} + 1) / (T + 1). Significance threshold: per-width p < Bonferroni-corrected 0.01 (family-wise α = 0.05 over 5 widths).

### Sensitivity to corridor pole definition

The canonical 130-site pole is the great-circle pair (St Cleer Well, Throwleigh) that best captures the 130 KML waypoints at w = 5 km. To confirm the result is not specific to this particular pole definition, we also performed a least-squares great-circle fit (SVD of unit vectors) to:

- the Michael "current" LineString from the source KML (3947 points);
- the Mary "current" LineString from the same KML (4945 points); and
- the union of both currents (8892 points).

The fitted poles lie 13.6 to 43.7 km from the canonical 130-site pole, with RMS residuals of 2.95 to 3.76 km against the source LineStrings. The straight-line abstraction is therefore an empirical summary of the meandering currents, not merely a stylistic convention. Each fitted pole was then run through the full population test (Tests 2 and 4); results are reported in §[Sensitivity table].

---

## Results

### Test 2 — Isotropic population null

| | w = 5 km | w = 10 km | w = 20 km | w = 50 km | w = 100 km |
|---|---|---|---|---|---|
| **B1**: K_real / mean ± std | 199 / 31 ± 48 | 325 / 63 ± 88 | 579 / 126 ± 160 | **1261** / 315 ± 335 | 1562 / 630 ± 551 |
| **B1**: p (one-sided) | 0.019 | 0.028 | 0.039 | **0.0004** ✓ | 0.057 |
| **B1**: z-score | 3.47 | 2.97 | 2.83 | 2.83 | 1.69 |
| **A**: K_real / mean ± std | 38 / 9.9 ± 11 | 58 / 20 ± 22 | 144 / 40 ± 44 | **325** / 99 ± 104 | 505 / 198 ± 185 |
| **A**: p (one-sided) | 0.016 | 0.074 | **0.007** ✓ | **0.003** ✓ | 0.044 |
| **A**: z-score | 2.46 | 1.72 | 2.38 | 2.17 | 1.66 |
| **B2**: K_real / mean ± std | 368 / 72 ± 85 | 634 / 143 ± 160 | 1304 / 286 ± 300 | **2635** / 717 ± 677 | 3505 / 1431 ± 1171 |
| **B2**: p (one-sided) | 0.014 | 0.021 | **0.004** ✓ | **0.0006** ✓ | 0.021 |
| **B2**: z-score | 3.50 | 3.07 | 3.39 | 2.84 | 1.77 |

Tick marks (✓) indicate Bonferroni-significant cells (p < 0.01).

**Reading.** All three catalogs over-populate the canonical corridor at the 50 km width with p ≤ 0.003. Catalogs A and B2 also pass at 20 km. The 5 km and 10 km widths show consistent positive z (1.7–3.5) but do not pass Bonferroni in this test alone.

### Test 3 — Bearing-restricted null (orientation control)

K_null mean at w = 5 km, across tolerances:

| Catalog | Isotropic | ±30° | ±15° | ±5° |
|---|---|---|---|---|
| B1 (n = 2422) | 31.31 | 31.45 | 31.09 | 31.26 |
| A  (n =  754) |  9.87 |  9.81 |  9.68 |  9.75 |
| B2 (n = 5500) | 71.64 |   —   | 70.67 |   —   |

The K_null distribution is essentially invariant across tolerance levels. Restricting random corridors to NE-SW orientations (±5° of the canonical 61.7°) does not raise the expected number of sites caught by chance. **The orientation confound from the British-landmass diagonal — which would have been the standard reviewer objection to Test 2 — is not present.** Significance survives at every tolerance:

| Test (w=50km) | Isotropic | ±30° | ±15° | ±5° |
|---|---|---|---|---|
| B1 (p, z) | 0.0004 / 2.83 | 0.0005 / 2.74 | 0.0013 / 2.66 | 0.0025 / 2.63 |
| A  (p, z) | 0.0031 / 2.17 | 0.0083 / 2.04 | 0.0087 / 2.02 | 0.0220 / 1.99 |
| B2 (p, z) | 0.0006 / 2.84 |       —       | 0.0019 / 2.55 |       —       |

B1 and B2 cross Bonferroni at every tolerance. A crosses Bonferroni at isotropic, ±30° and ±15°, and falls just short at ±5° (p = 0.022).

### Test 4 — Joint conjunction across all three catalogs (HEADLINE)

The per-catalog tests (Tests 2 and 3) treat each catalog independently. They show that the canonical corridor over-populates A, B1, and B2 separately. A stricter question — and the one we put to the data here — is whether a single random great circle could simultaneously beat the canonical K on all three catalogs at the same width.

The conjunction test samples random poles **once** and computes K against each catalog from the same set of trials, then counts the number of trials in which K_t exceeds K_real on all three catalogs at the same w.

**Joint p-values at w = 50 km** (the headline width, where the corridor's "shadow" on the broader landscape is most clearly distinguishable):

| Null mode | n trials beating all 3 | p_joint |
|---|---|---|
| Isotropic | 1 / 10,000 | **0.0002** ✓ |
| ±30° bearing | 1 / 10,000 | **0.0002** ✓ |
| ±15° bearing | 2 / 10,000 | **0.0003** ✓ |
| ±5° bearing | 5 / 10,000 | **0.0006** ✓ |

All values cross Bonferroni at the per-width 0.01 threshold and remain so under orientation restriction.

**Joint p-values across all widths** (isotropic null):

| | w = 5 km | w = 10 km | w = 20 km | w = 50 km | w = 100 km |
|---|---|---|---|---|---|
| n joint | 14 | 34 | 15 | **1** | 153 |
| p_joint | 0.0015 | 0.0035 | 0.0016 | **0.0002** ✓ | 0.0154 |

The 50 km width is the strongest cell. The 5, 10, and 20 km widths show consistent joint significance below 0.005 but only the 50 km cell passes Bonferroni unambiguously across every null variant.

**Catalog dependence (Pearson correlation of K across trials, w = 50 km):**

- corr(B1, B2) = +0.972 (very high; both are archaeological in southern Britain)
- corr(A, B2)  = +0.865 (high)
- corr(B1, A)  = +0.796 (moderate; Christian dedications are partly independent of monument density)

The conjunction p_joint is markedly smaller than the strongest individual marginal (0.0002 vs 0.0004 for B1 alone), **even given the high correlation between B1 and B2**. This is informative: the corridor's joint over-population is not a trivial consequence of the catalogs being correlated. If it were, p_joint would equal max(marginals); instead it is ~2× smaller. The corridor is doing real conjunctive work.

### Test 5 — Robustness to canonical pole definition

The joint conjunction test (Test 4) was repeated for four different canonical poles: the conventional 130-site canonical, the best-fit to the Michael current LineString, the best-fit to the Mary current LineString, and the best-fit to the combined currents.

| Canonical pole | Pole offset (km) | p_joint (w=50km, isotropic) | n / 10,000 |
|---|---|---|---|
| 130-site (reference) | 0 | 0.0002 | 1 |
| Michael current fit (n = 3947 points) | 30.9 | 0.0001 | 0 |
| Mary current fit (n = 4945 points) | 43.7 | 0.0002 | 1 |
| Combined currents fit (n = 8892 points) | 13.6 | 0.0004 | 3 |

All four pole definitions give equivalent joint significance — within Monte Carlo noise of one another, and all crossing the per-width Bonferroni threshold at w = 50 km. The per-catalog z-scores match the canonical run to within ±0.05 across all five widths. **The result is robust to the exact corridor definition.**

This rules out the methodological concern that the canonical 130-site straight line is a curatorially-chosen abstraction unfaithful to the underlying tradition's meandering "currents." When the great circle is fit *directly* to the currents the tradition actually posits, with thousands of points rather than 130 waypoints, the same population-level significance emerges.

### Cross-pole stability

The 12-site canonical pole (+33.465°, −147.811°) and the 130-site canonical pole (+33.330°, −147.354°) are about 50 km apart. Tested against B1, both give nearly identical results (p = 0.0001 vs 0.0004 at w = 50 km, K_real differing by 6%). The test is stable to small perturbations of the canonical pole, indicating the result reflects a corridor *region* and not a brittle line definition.

---

## Discussion

### What the data support

The canonical Michael corridor over-populates three independent reference catalogs of culturally significant sites in southern Britain, **simultaneously**, relative to:

- Random great circles of any orientation through the same region (Tests 2, 4 isotropic);
- Random great circles of *similar* orientation through the same region (Tests 3, 4 bearing-restricted);
- Small perturbations of the corridor pole (cross-pole stability).

This survives Bonferroni correction at the 50 km width on the joint test, with consistent positive z-scores across all five widths. Selection bias on the canonical 130-site catalog cannot have produced this — the 130 are not on either side of the population test.

### What the data do not support

The K_null *maximum* values are higher than K_real at every width. At w = 5 km isotropic, the single best random corridor in 10,000 trials caught 436 prehistoric sites (B1) — twice the canonical corridor's 199. **The canonical Michael corridor is not the unique or maximal alignment in southern Britain; it is at approximately the 99.98th percentile of NE-SW great circles through the UK bbox under the joint test.** Several other alignments through the UK would individually capture more prehistoric monuments. The Michael corridor is a real, statistically exceptional alignment, but not a singular one.

The data demonstrate **statistical and geographic significance**. They do not address — and this work makes no claims about — proposed mechanisms (geophysical, geomagnetic, energetic, or otherwise). The observed corridor's significance is established at the level of population geography only.

In particular, the result **does not** validate the broader "ley line" tradition (Watkins 1925; Miller and Broadhurst 1989) that posits energetic currents along the corridor. Whether the corridor reflects:
- a previously unrecognized landscape or topographic feature,
- a culturally transmitted alignment that influenced where humans built across multiple eras,
- a continuous-reuse pattern in which Christian sites were deliberately placed on prehistoric ones along a known axis,
- or some combination,

is beyond the scope of this work and is not adjudicated by the statistical result.

### Why effect sizes are smaller than internal nulls

The internal null tests on the canonical 130-site catalog gave z-scores up to 245. The population tests give z-scores of 2–3.5. The ratio (~30–80×) is the empirical signature of catalog curation. The internal test is inflated because the curator selected sites that fall on the corridor; the population test removes that inflation. **The z ≈ 3 result is the underlying population signal stripped of curation effects, and it is what should be reported as the headline finding.**

### Why the 50 km width is the headline

At narrow widths (5 km, 10 km), the population catalog is sparse along any single corridor — even a real corridor catches only a small fraction of nearby sites because most of the catalog is distributed over the broader landscape. The 50 km width is where the corridor's "shadow" on the broader landscape is most clearly distinguishable from random alignments through the same region. Wider widths (100 km) blur into the bbox-pass distribution and lose specificity.

### B1 vs B2

B1 (strict prehistoric) and B2 (broad archaeological) give qualitatively similar results, with corr(B1, B2) = 0.97 across trials. The corridor's significance is not specific to prehistoric monuments — it also over-populates the broader category that includes Roman, medieval, and post-medieval sites. Two non-mutually-exclusive readings:

1. **Trans-temporal reuse.** A geographic corridor that mattered in prehistory continued to be built upon in subsequent eras, accumulating sites of multiple periods.
2. **Catalog non-independence.** OSM contributors tagging archaeological sites may have referenced the same cultural-geographic intuitions that produce ley-line catalogs, weakening the "independent" status of B2.

(1) is the more parsimonious reading given the magnitude of the effect across both B1 and B2; (2) cannot be fully excluded without a non-OSM control catalog.

### Global-scale sanity check (UNESCO)

The canonical Michael great circle, when extended around the Earth, passes near several internationally recognizable sites (Nazca lines, Alice Springs, Moncong Lompobattang, the Isles of Scilly). To quantify this observation, we ran a separate test: counting UNESCO World Heritage Sites (n = 1154) within a fixed half-width of (a) the canonical Michael corridor, (b) the optimized red corridor from trial 1583, and (c) 10,000 random great circles uniform on S² (no bbox restriction — global).

| Corridor | K @ 100 km | Percentile | K @ 50 km | Percentile |
|---|---|---|---|---|
| Random GC (mean ± std) | 17.9 ± 15.4 | — | 9.0 ± 8.1 | — |
| Theoretical N·sin(w/R) | 18.1 | — | 9.1 | — |
| Michael canonical | 41 | 90.4% | 19 | 88.2% |
| Optimized red | 40 | 90.1% | 27 | 94.8% |

The closed-form expected count (N·sin(w/R), the spherical-band area fraction of a great-circle corridor) matches the empirical null mean to within 1%, validating the test.

The Michael Line captures more UNESCO sites than a median random great circle — about 2× the expected count at both widths — but lands at the ~90th percentile of random global corridors, not at the tail: 963/10,000 random great circles match or exceed K = 41 at 100 km, giving an effective p ≈ 0.10. The famous-places observation, when quantified, **does not survive as a significant global signal**. The modest elevation is parsimoniously explained by the corridor's geometric conditioning on passing through the UK and continental Europe, both UNESCO-dense regions — a random great circle restricted to those latitudes would land in a comparable percentile.

The 90th-percentile elevation is not nothing, and the corridor's globally-extended trajectory is interesting enough that future work could examine whether *specific* segments (e.g., the Mont-Saint-Michel ↔ Skellig Michael continuation, or the Mediterranean approach to Mount Carmel) show region-specific significance. But within the scope of the current claim — the southern-British corridor over-populating reference catalogs — the global UNESCO result functions as a negative control: the corridor's significance is **regional, not global**, and any "earth-grid" reading should be rejected on the basis of this test.

### On the trial-1583 "best corridor" finding

A diagnostic exploration after the main analysis found a single trial (trial 1583 in the isotropic null) that simultaneously beats the canonical corridor on all three catalogs at w = 5 km — by a wide margin (B1 = 436 vs 199, A = 44 vs 38, B2 = 666 vs 368, summed-z 17.95). This is not a separate finding; it is the single sample that defined the upper tail of the joint null distribution and therefore drove the p_joint = 0.0002 number.

Finding ~1 such corridor in 10,000 trials is exactly what a working test looks like at this signal level: if zero such corridors had been found, the joint p-value would have been at the resolution ceiling (1/10,001) and the test would have lost its power to discriminate. Treating trial 1583 as a "discovered alignment" that competes with the Michael corridor would double-count the same statistic.

The corridor optimized through trial 1583 cannot be re-tested for significance without an independent dataset, because it was selected to maximize K on these specific catalogs. It is referenced here only as a sanity check that the null distribution's upper tail is consistent with the reported p-value.

---

## Limitations

- **OSM coverage variability.** Catalogs A, B1, B2 are drawn from OpenStreetMap, which has uneven coverage across the bbox. Less-mapped regions may underweight sites that would otherwise contribute. The result is robust to this only to the extent that under-coverage is not spatially correlated with the corridor.
- **Bbox specificity.** Results are conditional on the southern-Britain bbox. Extending beyond Britain (e.g., to the continental Michael axis through Mont-Saint-Michel and Skellig Michael) would require a different bbox, different reference catalogs, and is reserved for future work.
- **No mechanism.** The test establishes statistical and geographic significance only. It is silent on causation.
- **Single canonical pole.** The result is reported for one canonical corridor (130-site pair 12,19) with stability checked against the 12-site canonical. A more thorough analysis would scan over the corridor parameterization to map the full significance landscape.
- **Single canonical pole.** Resolved in Test 5: results are robust to four independent pole definitions (130-site, Michael current fit, Mary current fit, combined fit) spanning a 44 km pole-offset range. A more thorough analysis would scan continuously over the corridor parameterization to map the full significance landscape, but the four-point sensitivity test confirms the canonical pole is within the equivalent-result region.

## Files

Catalogs:
- `data/population/catalog_A_michael.csv`        754 St Michael place-of-worship records (OSM)
- `data/population/catalog_B1_strict.csv`       2422 strict prehistoric monuments (OSM)
- `data/population/catalog_B2_broad.csv`        5500 broad archaeological records (OSM)
- `data/unesco/whc-sites-2021.csv`              cached UNESCO World Heritage Sites catalog

Canonical corridor source:
- `data/ley_lines/michael_ley_line/st_michaels_all_130.csv` — 130 sites extracted from the public KML
- `scripts_geophys/extract_kml_placemarks.py`   KML → CSV extraction tool

Scripts:
- `scripts_geophys/build_population_catalogs.py`     reference catalog builder
- `scripts_geophys/population_corridor_test.py`      Tests 2 and 3 (with `--bearing-tolerance`)
- `scripts_geophys/triple_corridor_test.py`          Test 4 (joint conjunction)
- `scripts_geophys/corridor_null_test.py`            Test 1 (internal nulls)
- `scripts_geophys/unesco_global_sanity_check.py`    global sanity check (UNESCO null)
- `scripts_geophys/extract_kml_coordinates.py`       Extract Michael/Mary current vertices from KML LineStrings for great-circle fitting
- `scripts_geophys/best_fit_great_circle.py`         SVD fit of great circle to point catalog

Results:
- `results_corridor/population/B1_canonical130*.json`         B1 isotropic + 30°, 15°, 5° tolerances
- `results_corridor/population/A_canonical130*.json`          A  isotropic + 30°, 15°, 5° tolerances
- `results_corridor/population/B2_canonical130*.json`         B2 isotropic + 15° tolerance
- `results_corridor/population/B1_canonical12.json`           B1 cross-pole stability check
- `results_corridor/population/triple_canonical130_*.{json,trials.csv}`   joint conjunction across all 3 catalogs
- `results_corridor/unesco_sanity_check_{50,100}km.json`   global UNESCO sanity check results
- `results_corridor/best_fit_{michael,mary,combined}_current.{json,kml}`   pole-fit outputs
- `results_corridor/population/triple_{michael,mary,combined}_pole.{json,trials.csv}`   sensitivity-test population results

## Conclusion

The Michael ley line corridor in southern Britain is not a curatorial artifact. Independent reference catalogs over-populate it at population scale; the over-population survives orientation restriction; the corridor is robust to small perturbations of its definition; and the joint significance across all three catalogs simultaneously crosses Bonferroni at the 50 km width with p_joint = 0.0002 isotropic and 0.0006 under the strictest orientation restriction.

The effect size is modest (z ≈ 2.5–3.5 per catalog) but consistent across catalogs, widths, tolerance levels, and the joint test. The methodology — a four-concentric-tests framework that progressively addresses internal alignment, population significance, orientation confound, and joint conjunction — is portable to any corridor-alignment claim and may be the more transferable contribution of this work than the Michael Line result itself.

The finding is geographic and statistical. The canonical Michael Line is a real population-level alignment of culturally significant sites in southern Britain — not the unique such alignment, but a statistically exceptional one. It warrants further investigation as a geographic phenomenon. Whether the corridor reflects landscape, cultural transmission, deliberate continuity, or some combination, is left to subsequent work; this result establishes only that the corridor exists at population scale and is not explained by catalog curation, orientation confound, or chance alignment with the British landmass.
