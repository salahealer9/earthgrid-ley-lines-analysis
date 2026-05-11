# CORRIDOR — Scientific Protocol

**Purpose.** Test whether the 160 sacred sites cluster along any great-circle corridor more than equivalent catalogs that preserve the same latitude distribution but rearrange longitudes (or under stronger nulls). This addresses one of the limitations explicitly listed in §12 of the research guide ("hidden spatial structure in the catalog") and provides a clean, properly-controlled p-value for the simplest geometric alignment claim that can be made about the catalog — independent of E8.

The test is deliberately orthogonal to the tournament: it asks nothing about projections, edges, vertices, or seeds. It asks only whether the catalog, viewed as a point set on S², admits an unusually rich great-circle alignment.

---

## Question

> Does the actual configuration of 160 sacred sites permit a single great-circle corridor that contains more sites than would be expected if their longitudes were randomly arranged at the same latitudes?

(Plus, as a stronger comparison: does it contain more sites than uniformly-distributed random points would?)

---

## Geometry

A great circle on the unit sphere is the intersection of the sphere with a plane through the origin. The plane has unit normal **n**. For unit vector **p** representing a site on the sphere, the angular distance from **p** to the great circle is

> d(p, n) = arcsin(|n · p|)

A site is "in the corridor" of half-width *w* iff d(p, n) ≤ *w*, equivalently |n · p| ≤ sin(*w*).

For the great circle through two sites **p_i** and **p_j**, the unit normal is

> n_ij = (p_i × p_j) / ‖p_i × p_j‖

(undefined for coincident or antipodal pairs; these are filtered).

---

## Why Haar SO(3) is the wrong null here

The natural analog of Stage 3C — Haar-rotate the catalog, re-enumerate candidate corridors, take the max count — turns out to be **degenerate** for this statistic. The proof is short:

If every site is rotated by R ∈ O(3), then each cross-product normal transforms as n_ij → R n_ij, and hence

> (R n_ij) · (R p_k) = n_ij · p_k

for every (i, j, k). The set of |n_ij · p_k| values is preserved exactly under any rotation (or reflection). Therefore the maximum corridor count is invariant under all of O(3) and the Haar SO(3) "null" returns exactly the real statistic on every trial.

This is the core difference from Stage 3C: in Stage 3C the lattice (E8 projection) is fixed in space and only the sites rotate, so rotation changes which fixed edges each site lies near. In the corridor test the "lattice" is itself derived from the rotated sites, so everything moves together and the statistic is invariant.

A non-isometric perturbation of the catalog is required.

---

## Null perturbations offered

| Mode | Operation | What it controls for | Conservatism |
|---|---|---|---|
| `lon_shuffle` (primary) | Permute longitudes among sites; latitudes unchanged | Latitude marginal exactly preserved; only longitude correlations broken | Most conservative — strips out any signal that is purely a consequence of the latitude distribution |
| `lon_uniform` | Replace each longitude with U(−180°, 180°); latitudes unchanged | Latitude marginal preserved; longitude marginal is uniform (not empirical) | Slightly looser than `lon_shuffle` — won't preserve any longitude clustering that exists in the catalog |
| `uniform_sphere` | Replace catalog with N i.i.d. points uniform on S² | Pure spatial uniformity | Most aggressive — will detect signal that is partly explained by latitude concentration alone |

**Recommended reporting strategy:** run both `lon_shuffle` and `uniform_sphere`. If the signal survives `lon_shuffle`, that is the strong claim. If it survives only `uniform_sphere`, the signal exists but is reducible to latitude concentration ("sites are in inhabited zones"), which is not novel.

The `lon_shuffle` null is the right primary because it answers the genuinely interesting question: *given that the catalog has this latitude distribution (an obvious consequence of human geography), do the longitudes line up along great circles in a non-random way?*

---

## Procedure

### Real statistic

For half-width *w* (in km, converted via R_⊕ = 6371 km):

1. Enumerate the C(N, 2) = 12,720 candidate normals n_ij from all unordered site pairs.
2. For each n_ij, count how many of the N sites satisfy |n_ij · p_k| ≤ sin(*w*).
3. The real statistic is `count_real(w) = max_{ij} count_ij(w)`.

By construction, every count_ij ≥ 2 (the defining pair is at zero angular distance). The optimisation pulls additional sites in.

### Null distribution (per `--null-mode`)

Each null trial:

1. Apply the chosen perturbation to produce a perturbed catalog (lats′, lons′).
2. Convert to unit vectors P′.
3. Re-enumerate candidate normals from P′ pairs.
4. Compute `count_null(w) = max_{ij} count′_ij(w)`.

### Significance

For each width *w*:

- k(w) = number of null trials with count_null(w) ≥ count_real(w)
- p(w) = (k(w) + 1) / (T + 1)
- z(w) = (count_real(w) − μ_null) / σ_null

One-sided test: more sites in a corridor is "better."

### Width sweep and multiple-testing correction

Sweep w ∈ {2, 5, 10, 20} km. Each width is a separate hypothesis, so report:

- Raw p(w) per width.
- Bonferroni-adjusted threshold: α = 0.05 / 4 = 0.0125 for family-wise significance.
- Optional: report the smallest w at which significance holds — a tighter alignment is a stronger claim.

---

## Validation against synthetic catalogs

The script's correctness was checked against two synthetic 20-point catalogs (verifications run at script-finalisation time):

| Catalog | Null mode | Outcome | Why it's the expected outcome |
|---|---|---|---|
| 20 uniform random points | `lon_shuffle` | p ≈ 1 across all widths, z ≈ 0 | A uniform catalog has no exceptional structure; null and real agree. |
| 8 planted near-equator + 12 random | `uniform_sphere` | p = 0.002, z ≈ 15 at w = 10 km | Planted equatorial corridor is detected when the null is "uniform on the sphere" (the latitude concentration of the planted points is itself the signal). |
| Same planted catalog | `lon_shuffle` | p ≈ 1 across all widths | Correct: in this synthetic, the corridor is purely a latitude effect. Shuffling longitudes among the 8 low-latitude sites still produces a tight equatorial cluster. The null is faithfully saying "given these latitudes, the longitudes add nothing" — which is true by construction. |

The third row is the most important: it shows `lon_shuffle` is genuinely the conservative null. If the only "structure" in a catalog is its latitude marginal, `lon_shuffle` will return p ≈ 1 — correctly attributing that structure to latitude rather than to longitude alignment.

---

## Computational details

The test is dominated by a single matrix multiplication per trial: |N · Pᵀ| where N is (12,720, 3) and P is (160, 3). Memory: ~16 MB. Wall clock: a few milliseconds per trial in vectorised numpy. The C/OpenMP backend is not needed — the math is simpler than arc-segment distance and the per-trial work is too small to benefit from parallelism overhead. The full 1,000-trial run takes a few seconds.

Per-trial log is written incrementally to allow `--resume` on interruption.

---

## Sanity checks

- **Chance baseline.** A great-circle band of half-width *w* on the unit sphere covers fraction sin(*w*) of the sphere's area. Expected sites in a *random* great circle = N × sin(w_rad). For w = 10 km, w_rad ≈ 0.00157, so the chance per random circle is about 0.25 sites for N = 160. The maximum over 12,720 candidates will be substantially higher than this *for any catalog* due to selection — that is exactly what the `--null-mode` calibrates.
- **w → 0 limit.** count_real(w) should equal 2 for every pair as w → 0 (only the defining pair lies exactly on the circle). Verify by running with a tiny w.
- **Antipodal filter.** Confirm cross-product norms < 1e-12 are filtered. With well-separated sites this should remove zero pairs in practice.
- **Null saturation.** If `count_real(w) = N` (all sites lie within w of some corridor — extremely unlikely for w ≤ 20 km on global data), the null can only equal it. Not a bug; just unreachable significance.

---

## How to interpret

| Outcome | Interpretation |
|---|---|
| `lon_shuffle` p < 0.0125 (Bonferroni) at small w | The catalog has genuine longitude-arrangement structure: sites lie on great circles more than longitude-shuffled counterparts. This is a non-trivial finding. |
| `lon_shuffle` p ≥ 0.05 at all widths, but `uniform_sphere` p < 0.0125 | The corridor signal is fully explained by latitude concentration. Not a novel result (sacred sites are in inhabited latitudes), but cleanly characterises the situation. |
| Both nulls p ≥ 0.05 at all widths | The catalog has no exceptional great-circle corridor structure. This *sharpens* the E8 result: the alignment cannot be reduced to "the sites lie on great circles." |
| Significant at large w only | Soft alignment tendency; fine-grained alignment claims would be unsupported. |

A null result is genuinely informative. It does not "fail to find anything" — it positively excludes a class of alternative hypotheses about how the E8 alignment could be artifactual.

---

## Pre-registration

Lock these before running on the real catalog:

1. **Catalog.** `data/sacred_sites/sites_energy_centers_160.csv`, identical to the tournament input.
2. **Half-widths.** {2, 5, 10, 20} km.
3. **Null modes.** Both `lon_shuffle` (primary) and `uniform_sphere` (comparison).
4. **Trials.** T = 1,000 per null mode.
5. **Statistic.** max corridor count over C(N, 2) candidates per width.
6. **Significance threshold.** Per-width raw p < 0.05; family-wise Bonferroni p < 0.0125 across 4 widths.
7. **Commitment.** Publish the full curve (both nulls, all widths) regardless of outcome.

---

## Follow-on: held-out E8 cross-test

This protocol does not address the corridor → E8 bridge. The clean follow-on:

1. Split the 160 sites into halves A and B (random partition, fixed seed; or jackknife).
2. Run this corridor test on A (using `lon_shuffle`). Identify corridors significant at p < 0.05.
3. Run the standard tournament (Stages 1–3C) on B alone, locking in the best E8 orientation for B.
4. Ask: what fraction of B's E8 edges (at the locked orientation) lie within the corridors discovered from A?
5. Null: re-randomise the partition (or perturb B), repeat. The independence of A and B in the partition removes the circularity.

This requires no new infrastructure beyond this script and the existing tournament — just careful bookkeeping on the partition. Defer until the standalone corridor test results are in hand.

---

## Files

- `corridor_null_test.py` — implementation, with `--smoke-test` for quick validation, `--resume` for batch runs, and `--null-mode` to select between perturbations.
- `corridor_null_<timestamp>.json` — summary output (per-width p, z, real count, null statistics).
- `corridor_null_<timestamp>.trials.csv` — per-trial log for reproducibility and resume.
