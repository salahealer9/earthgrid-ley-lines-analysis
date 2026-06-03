# Population Corridor Protocol — Belinus Line

**Status**: Pre-registered. All test parameters — bounding box, canonical source, reference catalogs, statistical thresholds, bearing tolerances, and reporting commitments — are specified below before any computation against these parameters is performed. This protocol is structurally parallel to `POPULATION_CORRIDOR_PROTOCOL_V2.md` (the Michael Line protocol) with parameters adapted for the Belinus Line. The git commit of this document, signed and timestamped, establishes the pre-registration anchor.

**Companion document**: `POPULATION_CORRIDOR_PROTOCOL_V2.md` (Michael Line). Where this protocol defers to V2, V2 is taken as authoritative for methodological detail.

---

## 1. Motivation

The Michael Line analysis (POPULATION_CORRIDOR_PROTOCOL_V2.md) demonstrated the six-concentric-tests framework on a single canonical corridor. To establish portability of the framework — and to address the editorial concern that a single worked example is insufficient evidence of methodological generality — we apply the same framework to a second canonical British alignment claim: the Belinus Line.

The Belinus Line claim is independent of the Michael Line tradition. It is canonically defined by Biltcliffe and Hoare's *The Spine of Albion* (Sacred Lands Publishing, 2012, revised ePub edition 2020/2021) and runs approximately north-south from Balnakeil (north coast of Scotland) to the Isle of Wight, passing through Inverness, Perth, Carlisle, Manchester, Birmingham, Stratford-upon-Avon, and Winchester among other named places. The published tradition includes a central straight-line alignment, two meandering "currents" (the **Belinus current** and the **Elen current**, analogous to the Michael and Mary currents of the Miller-Broadhurst tradition), and named "node-points" where the currents and central line converge.

This second case study tests the framework's discriminating power. If the Belinus Line passes the same six tests as the Michael Line, the framework's value is in identifying real population-level alignments. If it fails one or more tests, the framework's value is in actively discriminating between curated and population-level patterns — equally informative methodologically.

**Pre-committed reporting**: results are reported regardless of outcome. The Belinus analysis will appear in the manuscript whether it passes or fails any subset of the six tests. The framework's contribution does not depend on Belinus succeeding.

---

## 2. Canonical Belinus alignment

### 2.1 Authoritative source

The canonical Belinus alignment is defined by the maps and node-point list published in:

> Biltcliffe, G. and Hoare, C. (2012). *The Spine of Albion: An exploration of earth energies and landscape mysteries along the Belinus Line*. Sacred Lands Publishing. Revised three-volume ePub edition (2020/2021) containing all canonical node-points with detailed per-node maps.

The ePub edition is the source consulted for this analysis. It contains detailed per-node maps with the central line and currents traced through each region; the original 2012 paperback edition is referenced for contextual passages including the canonical bearing definition.

### 2.2 Public-source variants (background only)

Two public-source variants of the alignment exist but are not used as primary canonical sources:

- The map at `belinusline.com/sites.php` (© 2020–2021; accessed 2026-05-25; archived at archive.today on 2026-05-25 at `https://archive.ph/oWLKc`) shows approximately 33 named places but with some differences in node selection from the eBook.
- A derivative review map at `benlovegrove.com/the-spine-of-albion-review/` displays the alignment with 30+ named nodes, also with selection differences.

These sources confirm that the Belinus Line claim is publicly disseminated, but they do not match the eBook's specific node-list. For this analysis, the eBook is taken as authoritative because:

1. It is Biltcliffe and Hoare's own primary publication.
2. It contains the explicit per-node maps with detailed geometry.
3. It is the citation reviewers will expect for a methodological evaluation of the Belinus Line claim.

The disagreement between public-source variants confirms that "33 nodes" is the tradition's approximate canonical count rather than a precise enumeration. This protocol therefore does not pre-commit to a specific count (see Section 6.1).

### 2.3 Canonical structure

The Belinus alignment, per the eBook, consists of three geometric layers:

- **Central line**: a straight alignment from Balnakeil to the Isle of Wight, depicted as a single line on overview maps and traced through per-node maps. The central line is defined mathematically in Section 2.4 below; the eBook traces are taken as visual approximations of this mathematical line.
- **Belinus current**: a meandering trace running roughly parallel to the central line, depicted in the eBook in orange/yellow.
- **Elen current**: a second meandering trace, also roughly parallel, depicted in purple.

**Canonical node-points** are named places that the eBook places on the central alignment. Two complementary definitions of the canonical node set apply to this analysis:

**A. The strict canonical 33-node list (added in v0.3.0)**: Biltcliffe and Hoare (2012, revised ePub edition), Volume 3, Location 211 of 230, contains an explicit map enumerating exactly 33 canonical nodes along the Belinus Line. This enumeration is the authoritative source-derived canonical reference. In `nodes.csv`, membership in this list is flagged by the column `in_canonical_33 = TRUE`. The 33 nodes are listed in `docs/PROTOCOL_AMENDMENT_v0.3.0.md` Section 5.

This canonical-33 enumeration was not visible at v0.2.0 commit time. The protocol is amended in v0.3.0 to incorporate it as the primary canonical reference; see `docs/PROTOCOL_AMENDMENT_v0.3.0.md` for the full discussion.

**B. The broader per-map canonical set (retained from v0.2.0)**: every named place encountered in the eBook's regional and node-detail maps is recorded in `nodes.csv` with a boolean `is_canonical` flag indicating whether the eBook's per-map evidence places the named site as a primary node-point on the central alignment. This flag retains its v0.2.0 semantics (per-map judgment) for continuity with the pre-registration record.

The two flags are not mutually exclusive. A node may be in the strict canonical-33 list, in the broader per-map set, in both, or in neither. The strict canonical-33 list is used for primary reporting in Tests 1 and 5; the broader per-map set is reported alongside for transparency. Tests 2-4 and 6 test the canonical great circle (Section 2.4) and do not depend on either flag.

Auxiliary named places (on the currents but not on the central line, or near but not on either) are recorded with `is_canonical = FALSE` and `in_canonical_33 = FALSE` for traceability.

### 2.4 Mathematical definition of the central line (canonical)

The Belinus central line is defined mathematically, not by manual tracing. The definition uses two pieces of information from Biltcliffe and Hoare (2012, revised ePub edition):

**Bearing**: 345.5° from Ordnance Survey grid north (equivalently, 14.5° west of grid north). Stated by Biltcliffe and Hoare at loc. 267–278 in the revised ePub edition.

**Anchor**: St Oswald's Church, Widford, Oxfordshire (**51.8068° N, −1.6048° W**; WGS84). Coordinates obtained by visual identification in Google Earth Pro, cross-referenced against Historic England (Grade I listed building, List Entry 1369267). A small 13th-century church built on the site of a Roman villa.

Biltcliffe and Hoare describe the central alignment as passing through this point in the published text (Volume 1, Location 2118 of 2948 in the revised ePub edition):

> "Just to the east of Burford, the alignment passes through a little church built over a Roman villa at Widford, dedicated to St Oswald of Worcester..."

The point is also marked with a "+" symbol on the eBook map indicating a location where the central straight line passes through a named feature. Widford is therefore an anchor designated by the source text itself, not an analyst inference; the central line is constrained to pass through it.

**Conversion of the bearing to true north**: Biltcliffe specifies the bearing in OS grid-north terms. The OS grid convergence at Widford (longitude −1.6048°, east of the OS central meridian at longitude −2.0°) is approximately +0.31°. The true-north initial bearing of the canonical Belinus great circle at the Widford anchor is therefore:

> bearing_true(at Widford) = 345.5° + 0.31° = 345.81° (≈ 345.8°)

**Equivalence statement**: The values 345.5° (grid-north) and 345.8° (true-north at Widford) describe the same physical great circle in two different coordinate systems. We use 345.8° as the analysis input because our Monte Carlo framework generates random great circles on WGS84 (referenced to true north). Using 345.5° in true-north reference would test a *different* line. The conversion is a coordinate-system transformation, not a modification of the canonical claim.

**The canonical Belinus Line is uniquely defined** by this (anchor + bearing) pair: the great circle on WGS84 passing through St Oswald's Church, Widford (51.8068° N, −1.6048° W) at initial true-north bearing 345.8°. All other canonical nodes (including those on the Isle of Wight, in Scotland, and elsewhere) are evaluated against this great circle but do not contribute to its definition. The line is fully specified by the (anchor + bearing) pair alone, with no degrees of freedom from data extraction.

**On reproducibility of coordinates**: The Widford anchor coordinates are obtained by visual identification in Google Earth Pro, cross-referenced against the Historic England record. The exact coordinates used are permanently archived in this protocol and in the Zenodo deposit.

**Geometric consistency check**: The Isle of Wight central-line nodes extracted from Biltcliffe's own map lie within 1.5 km of this canonical great circle. This consistency is well within the headline test width of 50 km and confirms that Biltcliffe's textual claim and his map are in good agreement. The IOW nodes are *test points* evaluated against the canonical line; they do not define it.

**IOW central nodes** (`data/belinus/iow_central_nodes.csv`):

| name | lat | lon |
|------|-----|-----|
| Battery Gardens | 50.6501 | −1.1607 |
| Christ Church | 50.6510 | −1.1613 |
| St Patrick's Church | 50.6517 | −1.1604 |
| Bloodstone Spring | 50.6856 | −1.1783 |
| East Ashey Earthworks | 50.6910 | −1.1747 |
| Kemphill | 50.7094 | −1.1878 |

Canonical great circle construction:

```bash
python scripts/generate_widford_great_circle.py
```

Output:

```
Constructing great circle through Widford Church (51.8068, -1.6048)
True-north bearing: 345.8° (equivalent to Biltcliffe's 345.5° grid-north)
Constructed pole: (-8.7242°, -80.3571°)
KML saved to results_corridor/belinus_canonical_widford.kml
```

Distances from IOW nodes to the canonical great circle:

```bash
python scripts/widford_iow_distances.py
```

Output:

```
Distances from Widford-anchored canonical great circle:
------------------------------------------------------------
Battery Gardens           → 1.166 km
Christ Church             → 1.183 km
St Patrick's Church       → 1.102 km
Bloodstone Spring         → 1.424 km
East Ashey Earthworks     → 1.034 km
Kemphill                  → 1.439 km
```

All six IOW nodes lie within 1.5 km of the canonical great circle, confirming the internal consistency of Biltcliffe's claim at the scale of the analysis.

### 2.5 Anchor sensitivity (used in Test 5)

The canonical pole defined in Section 2.4 uses Widford church as the anchor. The Belinus Line as described by Biltcliffe and Hoare passes through many designated points along its length, any of which could equally serve as the anchor for a canonical bearing-defined great circle. To verify that the choice of anchor does not materially affect the test outcome, the canonical great circle is re-defined using three alternative anchor points from Biltcliffe's designated central-line locations:

1. **St Michael and All Angels, Great Wolford** (north of Widford on the alignment, in the eBook's central-line description).
2. **Meon Hill, Warwickshire** (a major hillfort designated in the eBook as on the alignment).
3. **St Catherine's Hillfort, Hampshire** (a southern designated central-line point).

For each alternative anchor, a new great circle is constructed (anchor + 345.5° grid-north bearing → corresponding true-north bearing at the anchor's longitude) and the population tests (Tests 2–4) are re-run. The four resulting p_joint values (primary Widford-anchored plus three alternatives) should agree to within Monte Carlo noise if the central line is well-defined.

---

## 3. Bounding box

Latitude ∈ [50.0°, 59.0°] N, longitude ∈ [−5.5°, +1.5°] E.

The box encloses the entire Balnakeil-to-Isle-of-Wight alignment with > 50 km margin on all sides, excludes Ireland, the Outer Hebrides, and the Northern Isles (Orkney/Shetland), and excludes continental Europe. It is larger and differently shaped than the Michael Line bbox (49.5–53.5° N, 6.5° W–2.5° E) because the Belinus alignment is approximately N-S whereas the Michael alignment is approximately NE-SW.

The bounding-box centre is approximately (54.5° N, 2.0° W); the half-diagonal is approximately 530 km. The half-diagonal is used as the rejection-sampling tolerance for random corridors required to pass through the data region (Test 2 and onward).

---

## 4. Reference catalogs

### 4.1 Catalog reuse and rebuilds

Catalogs B1 (strict prehistoric and Iron-Age monuments) and B2 (broad archaeological) are rebuilt for the new bbox using the same OSM Overpass filters as in POPULATION_CORRIDOR_PROTOCOL_V2.md, Sections 2.2.B1 and 2.2.B2. The filter logic is unchanged; only the bbox is changed.

### 4.2 Catalog A — independent reference Christian churches

For the Belinus Line, Catalog A is defined as all Christian churches in the bounding box queried from OpenStreetMap via the Overpass API, without consulting Biltcliffe and Hoare's published maps. The filter is:

> OSM tag combination: `amenity=place_of_worship` AND `religion=christian`
> within the Belinus bbox (50.0–59.0°N, 5.5°W–1.5°E)

This is a broader filter than the Michael Line's Catalog A (which used a name-prefix filter for "St Michael" / "St Mary" dedications). The Michael Line could exploit the specific dedication naming because the tradition is explicitly Christian and named after St Michael; the Belinus tradition is pre-Christian (associated with the Celtic deity Belinos/Belenos) and does not map to a specific Christian dedication naming convention. The broader "all Christian churches" filter is the closest defensible analog.

The expected catalog size is on the order of several thousand churches across the new bbox. This is larger than the Michael Line's 754 St Michael churches; the larger catalog provides more statistical power for the population test, but the threshold for over-population is correspondingly higher.

**Independence**: This catalog is constructed by an objective OSM filter, without reference to Biltcliffe and Hoare's curated selection of churches on the Belinus maps. Biltcliffe's curated churches are recorded in `nodes.csv` with `is_canonical = TRUE`, but they are not used to construct Catalog A. This independence is what makes the population test diagnostic: the canonical Belinus great circle should over-populate Christian churches at greater than chance rates only if real population-level alignment exists, not merely because Biltcliffe selected specific churches.

### 4.3 UNESCO catalog (Test 6)

The UNESCO World Heritage Sites catalog used in Test 6 of the Michael Line analysis (N = 1154) is reused unchanged for the Belinus global sanity check. The catalog is global; only the great circle being tested differs.

---

## 5. Test statistic

Unchanged from POPULATION_CORRIDOR_PROTOCOL_V2.md Section 2.1. Specifically:

- Distance from point to great circle: d(p, n) = arcsin(|p · n|) · R⊕, with R⊕ = 6371 km.
- Test statistic: K(w; n; C) = #{p ∈ C : d(p, n) ≤ w}.
- Widths swept: w ∈ {5, 10, 20, 50, 100} km.
- Trials per null: T = 10,000.
- p-value: p(w) = (#{K_null ≥ K_real} + 1) / (T + 1).
- z-score: (K_real − E[K_null]) / SD[K_null].

---

## 6. Data schema

Five CSV files in `data/belinus/`, all with the schemas locked at the time of this protocol commit. Data populates the files after the schema is committed; the schema is part of the pre-registration.

### 6.1 `nodes.csv` — the primary analysis catalog

Every named place encountered in the eBook's Belinus Line maps, with per-row judgments on (a) whether the eBook's per-map evidence places it on the central alignment, and (b) whether it appears in the canonical 33-node enumeration at Volume 3, Location 211 of 230.

```
map_name, node_name, node_type, lat, lon, on_central_line, on_belinus_current, on_elen_current, is_canonical, in_canonical_33, notes
```

Field definitions:

- `map_name`: name of the eBook map the node appears on (e.g. `IOW`, `Carlisle`, `Scotland_North`).
- `node_name`: canonical name from the eBook (preserve original spelling).
- `node_type`: one of `{prehistoric, christian, hillfort, holy_well, cliff, modern_landmark, estate_house, castle, other}`.
- `lat`, `lon`: decimal degrees, WGS84, identified by visual inspection in Google Earth Pro by cross-referencing the eBook map's named feature against the satellite imagery. For features with named OSM records, the Google Earth-identified coordinates are expected to agree with OSM Nominatim to within a few tens of metres; where substantial discrepancies arise, they are documented in the `notes` column.
- `on_central_line`: TRUE if the node lies on the central line (or within ~250 m of it). Generous tolerance reflects the mathematical precision of the central-line definition (Section 2.4) and the eBook's schematic representation of it. The proximity is recorded in the `notes` column.
- `on_belinus_current` and `on_elen_current`: judged visually against the meandering current as drawn in the eBook map. The analyst marks TRUE if the node symbol appears to lie on the drawn current line, FALSE if it lies adjacent to but not on the line. No fixed distance threshold is applied, because the currents are schematically drawn and meandering; a node that the analyst judges to be "on" the drawn line is accepted as such even if precise coordinates place it a few hundred metres away. The `notes` field records the judgment.
- `is_canonical`: TRUE if the node is considered a primary node-point in the Belinus tradition per per-map judgment from the eBook's regional and node-detail maps (e.g., it is named as a node in the eBook's descriptions or appears as a prominent node symbol on the maps). FALSE for all other named places (those on the currents and those near the alignment). This flag retains its v0.2.0 semantics.
- `in_canonical_33`: TRUE if the named place appears in the canonical 33-node map at Volume 3, Location 211 of 230, of Biltcliffe and Hoare (2012). FALSE otherwise. This column is added in v0.3.0; see `docs/PROTOCOL_AMENDMENT_v0.3.0.md` Section 5 for the full canonical 33-node list.
- `notes`: free text.

The primary canonical set for Tests 1 and 5 is the subset where `in_canonical_33 = TRUE`. The broader per-map canonical set (`is_canonical = TRUE`) is reported alongside for transparency. The two are not mutually exclusive; see Section 2.3 for the interpretation matrix.

Tests 2-4 (population nulls against catalogs A, B1, B2) and Test 6 (UNESCO global) test the mathematical canonical great circle defined in Section 2.4 and do not depend on either canonical-node subset.

Auxiliary nodes (where both `is_canonical` and `in_canonical_33` are FALSE) are recorded for traceability but are not used in the primary analysis or in the anchor sensitivity tests. They may be used for supplementary visualisation or future work.

### 6.2 `central_line_vertices.csv` — optional traced central line geometry

```
map_name, vertex_index, lat, lon, vertex_type, name, notes
```

Vertices traced from the eBook maps along the central straight-line alignment. `vertex_index` is sequential per map (0, 1, 2, ...) from south to north. `vertex_type` is one of `{endpoint, crossing, generic}` where `crossing` marks intersections with the meandering currents. The `name` column records toponyms attached to vertex points; `notes` captures contextual annotations such as "continues off map".

This file is **optional**. The canonical central line is defined mathematically in Section 2.4 and does not require manual tracing. The anchor sensitivity tests in Test 5 use alternative anchor points (Section 2.5), not traced central-line vertices. Vertices traced into this file may be used for visualisation or future supplementary work. If no central-line tracing is performed, this file remains empty (header only).

### 6.3 `elen_current_vertices.csv` — Elen meandering current

```
map_name, vertex_index, lat, lon, vertex_type, name, notes
```

Same schema as `central_line_vertices.csv`, applied to the purple Elen current trace.

### 6.4 `belinus_current_vertices.csv` — Belinus meandering current

```
map_name, vertex_index, lat, lon, vertex_type, name, notes
```

Same schema, applied to the orange/yellow Belinus current trace.

### 6.5 `map_metadata.csv` — per-map metadata

```
map_name, map_type, region, ebook_volume, ebook_page, bearing_at_centre_deg, has_central_line, has_elen_current, has_belinus_current, n_nodes, n_central_vertices, n_elen_vertices, n_belinus_vertices, notes
```

Field definitions:

- `map_name`: name of the map (matches the `map_name` column in the other files)
- `map_type`: one of `{region_overview, node_detail, area_currents}` — disambiguates whether a missing feature flag (e.g. `has_central_line = FALSE`) indicates absence at the location vs. omission from the specific map's depiction
- `region`: broad regional label (e.g. `Scotland`, `Northern England`, `Midlands`, `Southern England`)
- `ebook_volume`, `ebook_page`: source location in the eBook for traceability
- `bearing_at_centre_deg`: documentation field recording the canonical Belinus Line bearing as stated by Biltcliffe and Hoare (2012): 14.5° west of grid north (equivalently, 345.5° clockwise from grid north). Constant across all maps. Not used as analysis input; the great circle for all tests is defined mathematically in Section 2.4.
- `has_central_line`, `has_elen_current`, `has_belinus_current`: boolean presence flags indicating whether the eBook map depicts the corresponding feature
- `n_nodes`, `n_central_vertices`, `n_elen_vertices`, `n_belinus_vertices`: completeness counts (cross-checkable against the corresponding vertex files)
- `notes`: free text

### 6.6 Naming convention across files

When a place name appears in multiple files (e.g. `node_name` in `nodes.csv` and `name` in one of the vertex files), the same spelling is used across all files. This ensures that joins on the name field work without normalisation. `nodes.csv` is the canonical name registry; vertex-file `name` entries should match its `node_name` spelling exactly when referring to the same place.

### 6.7 Tracing the meandering currents (Elen and Belinus)

The Elen and Belinus currents are not mathematically defined. Their shapes must be extracted from the eBook maps by manual tracing.

**Procedure**:

1. Open the eBook (Biltcliffe and Hoare 2012) at the relevant map location (e.g., Isle of Wight overview map; Volume 1, location 839 of 2948).
2. In Google Earth Pro, add the eBook map as an image overlay. The map is used only for visual reference; the overlay is not distributed.
3. Georeference the overlay by aligning known landmarks (coastline, major towns, roads) with the satellite view. The alignment is approximate; priority is given to matching the drawn currents to the underlying terrain.
4. Using the "Add Path" tool, trace the Elen current (purple line) and the Belinus current (gold/orange line) vertex by vertex, clicking at intervals of approximately 200–500m to capture the meander shape.
5. At named places that correspond to rows in `nodes.csv`, snap the traced path to the node coordinates (or add a vertex at that location).
6. Save each traced path as a KML file.
7. Convert the KML files to CSV vertices using `scripts/kml_to_csv.py` (to be added to the repository in a subsequent commit before data extraction begins).
8. Store the CSV files as `elen_current_vertices.csv` and `belinus_current_vertices.csv`.

The eBook maps are used only for visual guidance; the traced coordinates are original data generated by the analyst. No map images are reproduced in this repository.

The traced vertices are used for visualisation and may inform future supplementary analyses. They are **not** used in the primary anchor sensitivity tests (Test 5), which rely only on Biltcliffe's alternative designated anchors (Section 2.5).

Because the eBook maps are schematic, the tracing process is approximate. Copyright considerations for the traced shapes are addressed in Section 13.

---

## 7. The six tests

Structurally identical to POPULATION_CORRIDOR_PROTOCOL_V2.md Section 2.5, with parameters adapted as below. The order of tests is preserved.

### 7.1 Test 1 — Internal null

The internal null fixes the canonical nodes (`nodes.csv` with `in_canonical_33 = TRUE`, the strict canonical-33 subset; secondary report on `is_canonical = TRUE` subset) and randomizes the corridor via three rearrangement schemes (`lon_shuffle`, `uniform_sphere`, `lon_uniform`), as in V2 Section 2.5.1. Computed by `scripts/corridor_null_test.py`.

Expected behaviour: high z-scores indicating internal tightness of the curated canonical nodes against the mathematical canonical pole. Not interpretable as population evidence; reported for completeness and to compare against the Michael Line's internal-null result.

### 7.2 Test 2 — Population null (isotropic)

Canonical Belinus corridor fixed at the mathematical pole defined in Section 2.4. 10,000 random great-circle poles sampled uniformly on S² subject to bbox-passage (Section 3). K computed against A, B1, and B2 independently. Computed by `scripts/population_corridor_test.py`.

### 7.3 Test 3 — Population null (bearing-restricted)

Random corridors additionally constrained to lie within ±D° of the canonical bearing at the bbox centre, where the canonical bearing is the true-north bearing of the mathematical great circle (Section 2.4) at the bbox-centre coordinate (54.5° N, 2.0° W). Tolerances: D ∈ {30°, 15°, 5°}. Computed by `scripts/population_corridor_test.py --bearing-tolerance D`.

The orientation confound concern is stronger for an approximately N-S alignment than for the Michael Line's NE-SW alignment, because the British landmass is more elongated in the N-S direction than along its diagonal. The bearing-restricted test is therefore more informative for Belinus than it was for Michael.

### 7.4 Test 4 — Joint conjunction (three-catalog)

Random poles sampled once and K computed against all three catalogs (A, B1, B2) from the same set of trials. The joint test statistic at width w is:

> n_joint(w) = #{t : K_t^A(w) ≥ K_real^A(w) ∧ K_t^B1(w) ≥ K_real^B1(w) ∧ K_t^B2(w) ≥ K_real^B2(w)}

with p_joint(w) = (n_joint(w) + 1) / (T + 1). The Bonferroni threshold from Section 8 applies to each width independently.

Pearson correlation of K across trials between each catalog pair is recorded to quantify catalog dependence.

This is structurally identical to the Michael Line's three-catalog joint conjunction test (POPULATION_CORRIDOR_PROTOCOL_V2.md Section 2.5.4), with Belinus Catalog A defined by a broader OSM filter (all Christian churches) than Michael Line Catalog A (St Michael dedications specifically).

### 7.5 Test 5 — Pole sensitivity (anchor robustness)

The primary canonical pole is defined in Section 2.4 (Widford Church + 345.5° grid-north bearing → 345.8° true-north). To assess whether the population-level significance is robust to the choice of anchor point among Biltcliffe's designated central-line locations, the canonical great circle is re-defined using three alternative anchor points (Section 2.5):

1. **St Michael and All Angels, Great Wolford**
2. **Meon Hill, Warwickshire**
3. **St Catherine's Hillfort, Hampshire**

For each alternative anchor, a new great circle is constructed (anchor + 345.5° grid-north bearing, converted to true-north at that anchor). Tests 2–4 are then run for each alternative great circle. The resulting p_joint values (at w = 50 km) are compared with the primary Widford-anchored p_joint. If all values are within Monte Carlo noise of each other (expected), the choice of anchor is considered robust. Substantial divergence would indicate sensitivity to anchor selection and would be reported as a limitation.

The traced central line, Elen current, and Belinus current vertices are **not** used in this test; the anchor sensitivity framework relies only on Biltcliffe's designated points, not on derived geometries.

The internal-tightness check that anchors the Widford pole's consistency (Section 2.4 geometric consistency check on IOW nodes) is repeated for the canonical-33 subset as a whole once data extraction completes. The expected outcome is that all 33 canonical-list nodes lie within Monte Carlo noise of the canonical great circle; if substantial deviations appear, they are reported in the manuscript as evidence of internal inconsistency in the source claim.

### 7.6 Test 6 — Global sanity check (UNESCO)

The mathematical canonical Belinus great circle (Section 2.4) is extended globally and tested against 10,000 random great circles uniform on S² (no bbox restriction), with K = number of UNESCO World Heritage Sites within w km of the great circle. Computed by `scripts/unesco_global_sanity_check.py`.

The Michael Line landed at the 90th percentile globally (regional signal only, not planet-wide). The Belinus Line's percentile may differ — pre-committed reporting applies: whatever percentile it lands at is reported.

---

## 8. Significance threshold

Bonferroni correction at α = 0.05 across the five widths, giving a per-width threshold of p < 0.01. Cells crossing this threshold are reported as Bonferroni-significant. Cells with raw p < 0.05 but failing Bonferroni are reported as marginal.

This is identical to the Michael Line protocol's threshold and is used here without modification.

---

## 9. Pre-committed reporting and outcome neutrality

The Belinus Line analysis will be reported in the manuscript regardless of outcome. Specifically:

1. **If Belinus passes all six tests** (parallel to Michael), the manuscript reports both case studies as confirmed regional alignments. The framework's contribution is shown to be in identifying such alignments rigorously.

2. **If Belinus passes some but not all tests**, the failing tests are reported with the same precision as the passing tests. The pattern of which tests fail (e.g. Test 3 bearing-restricted but not Test 2 isotropic, or Test 4 joint but not Test 2 marginal) is discussed in the manuscript Discussion section.

3. **If Belinus fails the primary headline test (Test 4 joint conjunction)**, the manuscript reports this as the framework actively discriminating between curated and population-level patterns. The Discussion section is rewritten to emphasize this discriminating power as the framework's contribution.

In all three cases, the framework's value is established. The Michael Line case study is the worked example of a passing alignment; the Belinus Line is the worked example of either confirmation (case 1, 2) or discrimination (case 3).

No selective reporting. No post-hoc filtering. No file-drawer outcomes.

---

## 10. Differences from the Michael Line analysis

For transparency, the asymmetries between the two case studies are noted here and acknowledged in the manuscript:

| Aspect | Michael Line | Belinus Line |
|---|---|---|
| Canonical source | Google My Maps (Anonymous, 2017) | Biltcliffe and Hoare (2012), revised eBook |
| Canonical pole definition | SVD fit to 130 KML sites (data-derived) | Mathematical: great circle through St Oswald's Church Widford at 345.8° true-north (= 345.5° grid-north per Biltcliffe 2012) |
| Canonical waypoint count | 130 sites (fixed by source KML) | 33 nodes (Vol 3 Loc 211 canonical list; added in v0.3.0 amendment); broader per-map subset retained as secondary reporting |
| Catalog A (dedicated) | 754 St Michael churches | All Christian churches via OSM (`amenity=place_of_worship` AND `religion=christian`) |
| Joint conjunction | three-catalog | three-catalog (parallel to Michael) |
| Pole sensitivity | 4 SVD-fit poles (130-site SVD, Michael current SVD, Mary current SVD, combined SVD) | 3 alternative anchor points (Great Wolford, Meon Hill, St Catherine's Hillfort) at the same canonical bearing |
| Bounding box | 49.5–53.5° N, 6.5° W–2.5° E (southern Britain) | 50.0–59.0° N, 5.5° W–1.5° E (full Britain) |

The Belinus case study uses a mathematically-defined canonical pole (with no degrees of freedom from data extraction), whereas the Michael Line uses a data-fitted canonical pole. This makes the Belinus test methodologically stronger in the sense that the pole cannot be "fit to the data we extracted." The Michael Line analysis can be revisited with a similar mathematical anchor + bearing definition in future work if such a definition is published.

The Belinus Catalog A uses a broader OSM filter (all Christian churches) than Michael Line Catalog A (St Michael dedications), reflecting the different relationship between the two traditions and Christian dedication patterns: the Michael Line's name was a Christian-era overlay onto an existing tradition, whereas the Belinus Line's name is pre-Christian and does not produce a specific Christian dedication signature. The larger catalog size for Belinus offsets the broader filter: K_null distributions will be correspondingly higher, and the threshold for over-population is correspondingly higher. The methodological symmetry between the two case studies (three-catalog joint conjunction, three independent catalogs of cultural-geographic sites) is otherwise preserved.

The Belinus pole sensitivity (Test 5) uses 3 alternative anchor points at the same canonical bearing rather than 4 SVD-fitted poles. The two approaches test different aspects of robustness: SVD-fit sensitivity tests whether different data subsets converge on the same pole, whereas anchor sensitivity tests whether the choice of which Biltcliffe-designated point serves as the anchor affects conclusions. For the Belinus case study, the latter is the methodologically harder question, since the canonical pole is already mathematically defined and the IOW data agrees with it at ~1.4 km (Section 2.4).

---

## 11. Versioning and pre-registration anchor

This protocol document is committed to the repository at git path `docs/POPULATION_CORRIDOR_PROTOCOL_BELINUS.md`. The commit is signed with the author's GPG key. After this commit lands and is pushed to the public GitHub repository, the v0.2.0 release tag is cut, and the corresponding Zenodo deposit becomes the immutable timestamp anchor for the pre-registration.

The five CSV files (`nodes.csv`, `central_line_vertices.csv`, `elen_current_vertices.csv`, `belinus_current_vertices.csv`, `map_metadata.csv`) are committed with their schema headers only (no data rows) in the same commit as this protocol document, establishing the schema commitment alongside the methodological commitment.

The `scripts/kml_to_csv.py` conversion script referenced in Section 6.7 is to be added in a subsequent commit before data extraction begins. The commit landing the script will be tagged in the commit log so the order of operations (protocol → script → data) remains auditable.

Data population — extracting node coordinates and vertex traces from the eBook — proceeds after the script lands, and is committed in subsequent commits clearly distinguishable from the protocol commit. The test runs proceed after data population.

---

## 12. Anticipated reporting structure in the manuscript

The Belinus Line case study will be reported as a new section (provisional Section 3.7 "Second worked example: the Belinus Line") in the Results section of the existing manuscript. The Discussion section will be expanded to include a comparative subsection contrasting the two case studies and discussing what their respective outcomes jointly imply.

Specific anticipated wording is reserved until after the data are collected and the tests are run, because the appropriate framing depends on the test outcomes.

---

## 13. Data availability and third-party copyright

The canonical Belinus great circle is defined mathematically from Biltcliffe and Hoare's (2012) published bearing and anchor point. Coordinates of named places (`nodes.csv`) are geographic facts identified in Google Earth Pro and are published under CC-BY-4.0 in the Zenodo deposit accompanying this protocol.

The public Zenodo deposit for v0.2.x will contain:

- This protocol document
- `nodes.csv` (coordinates of named places, factual geographic data)
- `central_line_vertices.csv`, `elen_current_vertices.csv`, `belinus_current_vertices.csv` — schema headers only, with traced vertex data omitted as described below
- `map_metadata.csv` (per-map metadata)
- All analysis scripts in `scripts/`
- All results in `results_corridor/` (summary statistics, fitted poles, test outputs)
- The mathematical canonical great circle (derived from Biltcliffe's stated bearing and anchor, computed by `scripts/generate_widford_great_circle.py`)

Excluded from the public deposit:

- Traced vertex data for the Elen current, Belinus current, and (if traced) the central line. These traced shapes are derived from manual tracing of maps in Biltcliffe and Hoare (2012) and may be subject to the copyright of the underlying source.
- Any reproductions of maps from Biltcliffe and Hoare (2012).

To respect the copyright of the underlying source, the traced vertex files are **not included** in the public Zenodo deposit by default. If explicit permission to publish is obtained from the source authors before the v1.0.0 release, they will be added in an addendum commit and re-deposited. Otherwise, researchers wishing to reproduce the current tracing may do so by following the procedure described in Section 6.7, using their own copy of the eBook.

This data-availability decision is itself pre-registered: it is locked at the v0.2.0 commit and any change before v1.0.0 (e.g., addition of traced files following explicit permission) will be documented transparently in the commit log and Zenodo release notes.

---

*End of pre-registered protocol.*
