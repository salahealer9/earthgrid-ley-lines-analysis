# Protocol Amendment v0.3.0

**Status**: Amendment to `docs/POPULATION_CORRIDOR_PROTOCOL_BELINUS.md`.
**Effective**: v0.3.0 release tag.
**Pre-registration baseline**: v0.2.0 (Zenodo DOI [10.5281/zenodo.20386489](https://doi.org/10.5281/zenodo.20386489)).
**Date**: 2026-05-26.

This document records a methodological amendment to the Belinus Line pre-registered protocol, prompted by the discovery of new source evidence during data extraction. The amendment is documented separately from the protocol body so that the audit trail of "what changed and why" is preserved in the git log.

---

## 1. Discovery

During Belinus data extraction (subsequent to the v0.2.0 commit), the analyst identified that Biltcliffe and Hoare (2012, revised ePub edition) **Volume 3, Location 211 of 230**, contains an explicit map enumerating exactly **33 canonical nodes** along the Belinus Line. This map is part of the chakra discussion in the closing volume of the eBook. The 33 nodes are listed in full in Section 5 below.

This canonical enumeration was not visible to the analyst at v0.2.0 commit time. The pre-registered protocol explicitly disclaimed knowledge of a canonical count in Section 2.3:

> "The eBook does not enforce a single canonical count of these node-points across its maps; the public derivative sources (belinusline.com/sites.php, benlovegrove.com/the-spine-of-albion-review/) disagree on the specific membership of '33 nodes.' Rather than committing to a fixed count, this protocol records every named place encountered in the eBook's maps in nodes.csv and marks each with a boolean is_canonical flag indicating whether the eBook places the named site on the central line."

The Vol 3 Location 211 finding supersedes this disclaimer with authoritative source evidence.

---

## 2. Why this is new source evidence, not a post-hoc analytical change

Pre-registration is designed to prevent post-hoc analytical choices made after seeing the data. This amendment is not such a choice.

What changed: an authoritative source-internal canonical reference was discovered. The reference exists in the eBook itself and was visible to anyone reading Volume 3, but it was not part of the analyst's working knowledge at v0.2.0 commit time. The v0.2.0 protocol explicitly stated that no such reference was known and that the canonical set would be inferred from per-map judgment.

What did NOT change:
- The canonical great circle (Widford anchor + 345.5° grid-north bearing) — unchanged.
- The reference catalogs (A, B1, B2, UNESCO) — unchanged.
- The six concentric tests and their statistical machinery — unchanged.
- The pre-committed reporting commitment (outcome-neutral) — unchanged.
- The data availability handling for traced vertex files (Section 13) — unchanged.

The amendment adds a new, more specific definition of the canonical node set, derived directly from the source. The pre-registration's analytical core is preserved.

---

## 3. Methodological response

Three options were considered:

- **Option A**: Redefine `is_canonical=TRUE` to mean "appears in the Vol 3 Loc 211 canonical 33-node map." Retro-update existing IOW entries.
- **Option B**: Keep `is_canonical` with its v0.2.0 semantics (per-map judgment of primary node) and add a new boolean column `in_canonical_33` indicating membership in the Vol 3 list.
- **Option C**: As B, but pre-commit to reporting tests on both subsets in the manuscript.

**Adopted approach: Option B.**

Rationale:
1. **Preserves the audit trail**. The v0.2.0 commit captured per-map judgment in good faith. Retro-changing those flags would erase that history. Adding a new column documents both: what the analyst judged from per-map evidence, AND what the canonical Vol 3 source asserts.
2. **Parallels the Michael Line structure**. Michael has 130 KML sites (strict canonical, source-derived) plus a broader Catalog A (754 St Michael churches). Belinus now has 33 canonical-list nodes (strict canonical, source-derived) plus a broader per-map-judgment subset. Symmetric methodology between the two case studies.
3. **Recoverable**. If subsequent analysis reveals the per-map judgment is methodologically suspect, the canonical-33 subset alone can be used as primary, with no further amendment required.

The strict-vs-broader comparison itself becomes a methodologically interesting finding when the tests are run.

---

## 4. Schema change to `data/belinus/nodes.csv`

The schema gains one new boolean column, `in_canonical_33`, and the `node_type` controlled vocabulary gains one new value, `castle`.

**Old schema (v0.2.0):**

```
map_name, node_name, node_type, lat, lon, on_central_line, on_belinus_current, on_elen_current, is_canonical, notes
```

**New schema (v0.3.0):**

```
map_name, node_name, node_type, lat, lon, on_central_line, on_belinus_current, on_elen_current, is_canonical, in_canonical_33, notes
```

The new column is inserted between `is_canonical` and `notes` to keep the boolean flags grouped together for readability.

**Updated definitions** (full text in Section 6.1 of the amended protocol):

- `is_canonical` (unchanged in semantics): TRUE if the node is considered a primary node-point in the Belinus tradition per per-map judgment from the eBook's regional and node-detail maps. FALSE for all other named places (those on the currents and those near the alignment).
- `in_canonical_33` (new): TRUE if the named place appears in the canonical 33-node map at Volume 3, Location 211 of 230, of Biltcliffe and Hoare (2012). FALSE otherwise.
- `node_type` (extended vocabulary): one of `{prehistoric, christian, hillfort, holy_well, cliff, modern_landmark, estate_house, castle, other}`. The `castle` value is added in this amendment to accommodate canonical-33 entries such as Radcliffe Tower, Malcolm Canmore's Tower, and similar.

The two boolean flags are not mutually exclusive. A node may be:

| `is_canonical` | `in_canonical_33` | Interpretation |
|---|---|---|
| TRUE | TRUE | Both per-map judgment AND Vol 3 canonical list identify this as a primary node. Strongest signal. |
| TRUE | FALSE | Per-map judgment identifies as primary; not in the strict Vol 3 canonical list. Includes most existing IOW canonical entries. |
| FALSE | TRUE | In the Vol 3 canonical list but not in the analyst's per-map primary judgment. Per-map evidence should be re-examined. |
| FALSE | FALSE | Auxiliary named place; neither per-map primary nor in canonical 33. |

---

## 5. The canonical 33-node list (Vol 3, Loc 211 of 230)

The full canonical enumeration, ordered south to north:

| # | Node name | Source map reference | Cluster |
|---|---|---|---|
| 1 | Brading Down | (Vol 3 Loc 211 of 230) | Isle of Wight |
| 2 | Titchfield, St Peter's Church | (Vol 1 Loc 1147 of 2948) | Titchfield (1/2) |
| 3 | Titchfield Abbey | (Vol 1 Loc 1147 of 2948) | Titchfield (2/2) |
| 4 | St Catherine's Hillfort | (Vol 1 Loc 1147 of 2948) | Winchester (1/2) |
| 5 | Winchester Cathedral | (Vol 1 Loc 1147 of 2948) | Winchester (2/2) |
| 6 | Beacon Hill | (Vol 3 Loc 211 of 230) | — |
| 7 | Uffington Castle | (Vol 1 Loc 1993 of 2948) | Uffington (1/2) |
| 8 | Dragon Hill | (Vol 1 Loc 1993 of 2948) | Uffington (2/2) |
| 9 | Rollright Stones | (Vol 3 Loc 211 of 230) | — |
| 10 | Stratford-upon-Avon | (Vol 3 Loc 211 of 230) | — |
| 11 | Wootton Wawen | (Vol 3 Loc 211 of 230) | — |
| 12 | Birmingham | (Vol 3 Loc 211 of 230) | — |
| 13 | Barr Beacon | (Vol 3 Loc 211 of 230) | — |
| 14 | Castle Ring | (Vol 3 Loc 211 of 230) | — |
| 15 | Etchinghill | (Vol 3 Loc 211 of 230) | — |
| 16 | The Cloud Hill | (Vol 3 Loc 211 of 230) | — |
| 17 | Alderley Edge | (Vol 3 Loc 211 of 230) | — |
| 18 | Radcliffe Tower | (Vol 3 Loc 211 of 230) | Manchester area |
| 19 | Clitheroe | (Vol 3 Loc 211 of 230) | — |
| 20 | Kirkby Lonsdale | (Vol 3 Loc 211 of 230) | — |
| 21 | Shap | (Vol 3 Loc 211 of 230) | — |
| 22 | Carlisle | (Vol 3 Loc 211 of 230) | — |
| 23 | Peebles | (Vol 3 Loc 211 of 230) | Cademuir Hill area |
| 24 | Dunfermline Abbey | (Vol 3 Loc 90 of 230) | Dunfermline (1/2) |
| 25 | Malcolm Canmore's Tower | (Vol 3 Loc 90 of 230) | Dunfermline (2/2) |
| 26 | Scone | (Vol 3 Loc 211 of 230) | — |
| 27 | Dunkeld Cathedral | (Vol 3 Loc 139 of 230) | Dunkeld (1/2) |
| 28 | King's Seat | (Vol 3 Loc 90 of 230) | Dunkeld (2/2) |
| 29 | Clava Cairns | (Vol 3 Loc 173 of 230) | — |
| 30 | Inverness | (Vol 3 Loc 173 of 230) | Inches |
| 31 | Petty Mound | (Vol 3 Loc 211 of 230) | — |
| 32 | Brock | (Vol 3 Loc 211 of 230) | spelled "Broch" on the map image |
| 33 | Balnakeil | (Vol 3 Loc 211 of 230) | Northern terminus |

The five "dual-node clusters" (Titchfield, Winchester, Uffington, Dunfermline, Dunkeld) are recorded as 10 separate nodes (not 5), reflecting how they appear on the Vol 3 map. Biltcliffe and Hoare describe these as paired-node locations on the alignment.

Each node's WGS84 coordinates are identified by visual inspection in Google Earth Pro and recorded in `nodes.csv` with `in_canonical_33 = TRUE`.

---

## 6. Implications for existing IOW data

The existing IOW entries (committed after v0.2.0) need the new `in_canonical_33` column populated, and one new entry added.

**Current IOW entries in `nodes.csv`** (per-map judgment under v0.2.0 framing):

| Node | `is_canonical` | New `in_canonical_33` | Action |
|---|---|---|---|
| Battery Gardens | TRUE | FALSE | Set new column to FALSE |
| Christ Church | TRUE | FALSE | Set new column to FALSE |
| St Patrick's Church | TRUE | FALSE | Set new column to FALSE |
| Bloodstone Spring | TRUE | FALSE | Set new column to FALSE |
| East Ashey Earthworks | TRUE | FALSE | Set new column to FALSE |
| Kemphill | TRUE | FALSE | Set new column to FALSE |
| (other IOW entries — Upton, Eleanor's Grove, Quarr Abbey, etc.) | FALSE | FALSE | Set new column to FALSE |

**New IOW entry to add**:

| Node | `is_canonical` | `in_canonical_33` | Notes |
|---|---|---|---|
| Brading Down | TBD (per-map evidence dependent) | TRUE | "The southern terminal node on the Isle of Wight" per Vol 3 Loc 211 chakra discussion. Chalk down between Brading and Ashey. Coordinates to be identified in Google Earth Pro. |

The `is_canonical` flag for Brading Down depends on what the per-map IOW maps show: if the IOW overview or detail maps depict Brading Down on the central line, set `is_canonical = TRUE`; if only the Vol 3 chakra map mentions it, set `is_canonical = FALSE`. Either way, `in_canonical_33 = TRUE`.

---

## 7. Implications for the six tests

The Test sections of the protocol (Section 7) need a small clarification: when the canonical-node set is invoked (in Tests 1, 5, and as the input for the canonical pole's consistency check), the new framework distinguishes:

- **Primary canonical set** (used for Tests 1, 5 primary reporting): rows where `in_canonical_33 = TRUE`.
- **Broader canonical set** (used for secondary/supplementary reporting): rows where `is_canonical = TRUE`.

Tests 2–4 (population nulls against B1, A, B2) and Test 6 (UNESCO global) test the canonical great circle (Widford-anchored, Section 2.4 of the protocol). They do not depend on the canonical node set; the node set is used only to verify internal consistency (Test 1) and the anchor's robustness (Test 5).

**Pre-committed reporting**: tests will be run and reported on both subsets where applicable. Primary results use the `in_canonical_33` subset (strict canonical, source-derived). Secondary results on the broader `is_canonical` subset are reported alongside for transparency.

---

## 8. Versioning and release

This amendment is committed as part of the v0.3.0 release. Specifically:

- `docs/PROTOCOL_AMENDMENT_v0.3.0.md` (this document) is added.
- `docs/POPULATION_CORRIDOR_PROTOCOL_BELINUS.md` is updated to reflect the amendment in Sections 2.3, 6.1, and 7 (test-set definitions).
- `data/belinus/nodes.csv` schema is updated to include `in_canonical_33`. Existing IOW entries are updated. Brading Down is added.
- A signed v0.3.0 git tag is cut after these changes land, with a clear commit message describing the source discovery.
- Zenodo deposits the v0.3.0 release; both v0.2.0 and v0.3.0 are preserved in the version history.

The original v0.2.0 protocol document remains the authoritative pre-registration baseline. The v0.3.0 protocol document supersedes it for ongoing analysis. Anyone reproducing the analysis can verify which framework applies at which release by inspecting the git history and the Zenodo deposits.

---

*End of amendment.*
