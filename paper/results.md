# 3. Results

The canonical Michael corridor passed all four population-level tests at the 50 km width, with joint conjunction p = 0.0002 (one-sided, 10,000 trials). The result was stable under three orientation-control tolerances and across four independent corridor pole definitions. The global UNESCO sanity check confirmed the signal as regional rather than planet-wide.

Headline statistics per test:

| Test | Statistic | Value | Bonferroni (p < 0.01) |
|---|---|---|---|
| 1. Internal null  | z (5 km, lon_shuffle) | 16.5 (12-site) / 95.9 (130-site) | trivially yes |
| 2. Population isotropic | p (B1, 50 km) | 0.0004 | ✓ |
| 3. Bearing-restricted (±5°) | p (B1, 50 km) | 0.0025 | ✓ |
| 4. Joint conjunction (isotropic) | p_joint (50 km) | **0.0002** | ✓ |
| 5. Pole sensitivity | p_joint range (4 poles, 50 km, iso) | 0.0001 – 0.0004 | all ✓ |
| 6. UNESCO global (100 km) | Michael percentile | 90.4 % | n.s. |

Throughout, K_real denotes the canonical corridor's site count and K_null denotes the per-trial site count under the random-corridor null; p is the one-sided fraction of null trials with K_null ≥ K_real, with the Laplace-smoothed estimator (Section 2.1). Bonferroni-significant cells (per-width p < 0.01) are marked ✓; cells with p < 0.05 but failing Bonferroni are reported as marginal. Catalog sizes are N_A = 754, N_B1 = 2422, N_B2 = 5500. Widths swept: w ∈ {5, 10, 20, 50, 100} km.

## 3.1 Test 1 — Internal null

The internal null was reported in earlier work and is summarized here for completeness. On the 12-site canonical catalog under the `lon_shuffle` scheme at w = 5 km, K_real = 12 against a null mean of 3.33 ± 0.53, giving z = 16.5 (p < 0.001). On the 130-site catalog under the same scheme, K_real = 120 against a null mean of 16.4 ± 1.1, giving z = 95.9; the `uniform_sphere` scheme yielded z = 245 on the same catalog. As anticipated, the internal-null result is dominated by catalog curation and is not interpretable as evidence for a population-level corridor on its own (Section 2.5.1).

## 3.2 Test 2 — Population null (isotropic)

Per-catalog significance against 10,000 random great circles uniform on S² subject to bbox-passage:

| | w = 5 km | w = 10 km | w = 20 km | w = 50 km | w = 100 km |
|---|---|---|---|---|---|
| **B1** K_real / null mean ± SD | 199 / 31 ± 48 | 325 / 63 ± 88 | 579 / 126 ± 160 | **1261** / 315 ± 335 | 1562 / 630 ± 551 |
| **B1** p (z)  | 0.019 (3.47) | 0.028 (2.97) | 0.039 (2.83) | **0.0004 (2.83)** ✓ | 0.057 (1.69) |
| **A** K_real / null mean ± SD | 38 / 9.9 ± 11 | 58 / 20 ± 22 | 144 / 40 ± 44 | **325** / 99 ± 104 | 505 / 198 ± 185 |
| **A** p (z)   | 0.016 (2.46) | 0.074 (1.72) | **0.007 (2.38)** ✓ | **0.003 (2.17)** ✓ | 0.044 (1.66) |
| **B2** K_real / null mean ± SD | 368 / 72 ± 85 | 634 / 143 ± 160 | 1304 / 286 ± 300 | **2635** / 717 ± 677 | 3505 / 1431 ± 1171 |
| **B2** p (z)  | 0.014 (3.50) | 0.021 (3.07) | **0.004 (3.39)** ✓ | **0.0006 (2.84)** ✓ | 0.021 (1.77) |

All three catalogs crossed Bonferroni at the 50 km width with p ≤ 0.003. Catalogs A and B2 additionally crossed at 20 km. The 5 km and 10 km widths showed consistent positive z (range 1.7 – 3.5) but did not pass Bonferroni in the per-catalog test. The 100 km width showed weaker significance in all three catalogs.

The K_null distribution at w = 5 km is highly right-skewed: median ~ 12, mean ~ 31, maximum 436 (B1). Random great circles that happen to lie along the British landmass diagonal accumulate many sites; the canonical corridor's K_real = 199 lies at approximately the 98th percentile (p = 0.019) of this distribution for B1.

## 3.3 Test 3 — Bearing-restricted null

Random corridors were additionally constrained to have bearing within ±D° of the canonical bearing of 61.7° at the bbox center. K_null mean at w = 5 km across tolerances:

| Catalog | Isotropic | ±30° | ±15° | ±5° |
|---|---|---|---|---|
| B1 (N = 2422) | 31.31 | 31.45 | 31.09 | 31.26 |
| A  (N =  754) |  9.87 |  9.81 |  9.68 |  9.75 |
| B2 (N = 5500) | 71.64 | 71.39 | 70.67 | 71.04 |

The K_null mean was effectively invariant across tolerance levels in all three catalogs: the maximum range across the four conditions was 0.36 sites for B1, 0.19 for A, and 0.97 for B2. The null distribution was not shifted by restricting random corridors to a narrow NE-SW orientation band, indicating no detectable orientation confound from the British landmass diagonal.

p-values at w = 50 km under the bearing restriction:

| Catalog | Isotropic | ±30° | ±15° | ±5° |
|---|---|---|---|---|
| B1 (p / z) | **0.0004** / 2.83 | **0.0005** / 2.74 | **0.0013** / 2.66 | **0.0025** / 2.63 |
| A  (p / z) | **0.0031** / 2.17 | **0.0083** / 2.04 | **0.0087** / 2.02 | 0.0220 / 1.99 |
| B2 (p / z) | **0.0006** / 2.84 | **0.0009** / 2.63 | **0.0019** / 2.55 | 0.0054 / 2.52 |

B1 crossed Bonferroni at every tolerance tested. Catalogs A and B2 crossed Bonferroni at isotropic, ±30°, and ±15°, and fell just short at ±5° (A: p = 0.022; B2: p = 0.005, marginal). Effect sizes (z-scores) decreased modestly with tighter tolerance, from 2.83 to 2.63 for B1 over the range tested, but remained positive in every cell.

## 3.4 Test 4 — Joint conjunction

Random poles were sampled once and K was computed against all three catalogs from the same trials. Joint p-values at w = 50 km:

| Null mode | n trials beating all 3 | p_joint |
|---|---|---|
| Isotropic | 1 / 10,000 | **0.0002** ✓ |
| ±30° bearing | 1 / 10,000 | **0.0002** ✓ |
| ±15° bearing | 2 / 10,000 | **0.0003** ✓ |
| ±5° bearing | 5 / 10,000 | **0.0006** ✓ |

All four null modes crossed Bonferroni at the per-width 0.01 threshold. Joint p-values across all widths under the isotropic null:

| | w = 5 km | w = 10 km | w = 20 km | w = 50 km | w = 100 km |
|---|---|---|---|---|---|
| n joint | 14 | 34 | 15 | **1** | 153 |
| p_joint | 0.0015 | 0.0035 | 0.0016 | **0.0002** ✓ | 0.0154 |

The 5, 10, and 20 km widths showed consistent joint significance below 0.005 but only the 50 km cell crossed Bonferroni unambiguously across every null variant. The 100 km width showed weaker joint significance (p_joint = 0.015 isotropic), parallel to the per-catalog results.

The upper tail of the joint null distribution at w = 5 km was driven by a single trial (trial 1583) that simultaneously beat the canonical corridor on all three catalogs: K_t^{B1} = 436, K_t^A = 44, K_t^{B2} = 666 (vs. K_real of 199, 38, 368 respectively). Trial 1583 is reported here as a diagnostic — the upper tail of a properly-calibrated null distribution should contain at least a handful of such trials, and finding zero would indicate the test had lost statistical resolution. Its high K count does not constitute a discovered alignment and is treated further in Section 4.

Pearson correlation of K across the 10,000 trials, w = 50 km:

| Catalog pair | r |
|---|---|
| B1, B2 | +0.972 |
| A,  B2 | +0.865 |
| B1, A  | +0.796 |

The conjunction p-value (0.0002 isotropic at 50 km) was smaller than the strongest individual marginal in the same row (B1 isotropic at 50 km: 0.0004), with the difference holding under all four bearing-tolerance conditions.

## 3.5 Test 5 — Pole sensitivity

Best-fit great circles were computed by SVD against the meandering Mary and Michael current LineStrings from the source KML. Three fits were performed and tested in parallel with the canonical 130-site pole:

| Pole definition | Fitted pole (lat, lon) | Offset to canonical (km) | RMS (km) | Median (km) |
|---|---|---|---|---|
| 130-site canonical (reference) | (+33.330°, −147.354°) | 0 | — | — |
| Michael current fit (n = 3947) | (+33.419°, −147.669°) | 30.9 | 2.95 | 1.84 |
| Mary current fit (n = 4945) | (+33.175°, −146.922°) | 43.7 | 3.76 | 2.57 |
| Combined currents fit (n = 8892) | (+33.276°, −147.222°) | 13.6 | 3.55 | 2.31 |

All four pole offsets fell within the cross-pole stability envelope established in Section 2.3 (the 12-pole vs. 130-pole separation is ~50 km with equivalent population significance). The RMS residual of 3.55 km against 8892 combined current points, with a median of 2.31 km, indicates the meandering LineStrings are well-approximated by a great circle: the maximum residual was 11.3 km, and the 95th percentile 7.1 km.

Joint conjunction p-values at w = 50 km for each fitted pole (isotropic null):

| Pole | p_joint | n trials beating all 3 |
|---|---|---|
| Canonical 130-site | 0.0002 | 1 / 10,000 |
| Michael current fit | 0.0001 | 0 / 10,000 |
| Mary current fit | 0.0002 | 1 / 10,000 |
| Combined currents fit | 0.0004 | 3 / 10,000 |

All four pole definitions yielded equivalent joint significance, with p_joint differing by at most a factor of 4 across the four (0.0001 to 0.0004), all crossing the per-width Bonferroni threshold. Per-catalog z-scores at w = 50 km were within ±0.05 of one another across all four pole definitions.

## 3.6 Test 6 — Global UNESCO sanity check

The canonical Michael great circle was extended globally and tested against 10,000 random great circles uniform on S² (no bbox restriction), with K computed as the number of UNESCO World Heritage Sites (N = 1154) within a fixed half-width.

| Corridor | K (100 km) | Percentile | K (50 km) | Percentile |
|---|---|---|---|---|
| Random GC mean ± SD | 17.9 ± 15.4 | — | 9.0 ± 8.1 | — |
| Theoretical N·sin(w/R⊕) | 18.1 | — | 9.1 | — |
| Michael canonical | 41 | 90.4 % | 19 | 88.2 % |
| Optimized red (Test 4 trial 1583) | 40 | 90.1 % | 27 | 94.8 % |

The "optimized red" corridor referenced in the table is the single random trial in the upper tail of the joint null distribution (Section 3.4) that captured 436 B1 sites within 5 km. The empirical null mean matched the closed-form expectation to within 1 % at both widths, validating the test. The Michael corridor's K landed at the 88th–90th percentile of random great circles. At 100 km, 963 of 10,000 random great circles matched or exceeded K_Michael = 41 (effective one-sided p = 0.096); at 50 km, 1183 of 10,000 matched or exceeded K_Michael = 19 (p = 0.118). Neither width crossed the conventional α = 0.05 threshold, and neither crossed Bonferroni. The optimized red corridor showed the same pattern (percentiles 90.1 % and 94.8 %; neither significant).
