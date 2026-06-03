# Earth Grid Ley Lines Analysis

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20307500.svg)](https://doi.org/10.5281/zenodo.20307500)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A six-concentric-tests statistical framework for evaluating great-circle alignment claims about cultural sites at population scale. Worked examples: the **Michael Line** in southern Britain (analysis complete) and the **Belinus Line** across full Britain (pre-registered protocol; data extraction and analysis in progress).

## What this is

This repository implements a six-concentric-tests methodology for evaluating whether a hypothesized corridor of aligned sites is statistically exceptional, beyond what could be explained by:

1. **Catalog curation** — the sites tested were chosen *because* they appear aligned
2. **Background site density** — the underlying landscape is so site-rich that almost any line catches sites
3. **Orientation effects** — corridors oriented along a landmass diagonal trivially catch more sites than perpendicular ones
4. **Multiple-comparison artifacts** — passing one test out of several does not establish significance
5. **Definition sensitivity** — small changes in how the corridor is defined shouldn't dramatically change the result
6. **Scale of claim** — regional significance shouldn't be confused with planet-wide significance

The framework is portable to any corridor-alignment claim. It is currently applied to two case studies: the Michael Line (worked example of a passing alignment) and the Belinus Line (in-progress second worked example, pre-registered).

## Project status

| Case study | Status | Source |
|---|---|---|
| Michael Line (southern Britain) | Analysis complete (v0.1.0 / v0.1.1). Six-test results in [`docs/MICHAEL_LEY_LINES_RESULT.md`](docs/MICHAEL_LEY_LINES_RESULT.md). | Anonymous (2017) Google My Maps |
| Belinus Line (full Britain) | Protocol pre-registered (v0.2.0). Amended at v0.3.0 to incorporate the canonical 33-node list from Volume 3, Location 211 of 230 — see [`docs/PROTOCOL_AMENDMENT_v0.3.0.md`](docs/PROTOCOL_AMENDMENT_v0.3.0.md). Data extraction in progress. | Biltcliffe and Hoare (2012), *The Spine of Albion* |

## Headline result — Michael Line

The canonical Michael corridor in southern Britain over-populates three independent reference catalogs (754 Christian dedications, 2422 prehistoric monuments, 5500 broad archaeological sites) simultaneously at the 50 km width, with joint conjunction p = 0.0002 (one-sided, 10,000 trials). The result survives Bonferroni correction across five widths, orientation restriction to ±5° of the canonical bearing, and sensitivity to four independent pole definitions (canonical 130-site, Michael current fit, Mary current fit, combined currents fit).

A separate UNESCO global sanity check confirms the signal is **regional, not global**: the Michael corridor extended worldwide hits 41 UNESCO World Heritage Sites within 100 km — at the 90th percentile of random great circles, well outside the threshold for a global claim.

The finding is statistical and geographic. It establishes that the canonical Michael Line corridor exists at population scale and is not explained by curation, density, orientation, or chance alignment with the British landmass. It does not establish any proposed mechanism (geophysical, energetic, or otherwise) and does not validate the broader ley-line tradition's interpretive claims.

## Pre-registered second case study — Belinus Line

A pre-registered protocol for the Belinus Line is committed at v0.2.0 and amended at v0.3.0. The Belinus Line is canonically defined by Biltcliffe and Hoare (2012), runs approximately north-south from Balnakeil (Scotland) to the Isle of Wight, and is structurally analogous to the Michael Line tradition (central straight-line alignment plus two meandering "currents"). The protocol specifies a mathematically-defined canonical pole (great circle through St Oswald's Church, Widford, Oxfordshire at 345.8° true-north), an independent reference Catalog A of OSM Christian churches, and three alternative anchor points for the Test 5 sensitivity analysis.

**v0.3.0 amendment**: during data extraction, the analyst identified that Biltcliffe and Hoare (2012) Volume 3, Location 211 of 230, contains an explicit map enumerating exactly 33 canonical nodes along the Belinus Line. This authoritative source-internal enumeration was not visible at v0.2.0 commit time. The protocol is amended in v0.3.0 to incorporate the canonical 33-node list as the primary canonical reference, alongside the broader per-map judgment set retained from v0.2.0 for continuity. See [`docs/PROTOCOL_AMENDMENT_v0.3.0.md`](docs/PROTOCOL_AMENDMENT_v0.3.0.md) for the full record of what changed and why.

Pre-committed reporting applies: results will appear in the manuscript regardless of outcome. If the Belinus Line passes the same tests as the Michael Line, the framework's value is in identifying real population-level alignments. If it fails one or more tests, the framework's value is in actively discriminating between curated and population-level patterns — equally informative methodologically.

Full Belinus protocol in [`docs/POPULATION_CORRIDOR_PROTOCOL_BELINUS.md`](docs/POPULATION_CORRIDOR_PROTOCOL_BELINUS.md).

## Paper draft

The manuscript is in `paper/`:

- `abstract.md`, `introduction.md`, `methods.md`, `results.md`, `discussion.md`
- `references.bib` (BibTeX)
- `figures/` (Figures 1–3 as PNG/PDF)

The current draft covers the Michael Line case study. A second worked-example section for the Belinus Line will be added once data extraction and analysis are complete.

## Methodology (Michael Line — six-test results)

| Test | Question | Status |
|---|---|---|
| 1. Internal null | Are these 130 curated sites tightly aligned? | z = 16–245 (curation-inflated) |
| 2. Population isotropic | Does the corridor over-populate independent catalogs vs random great circles? | p = 0.0004 (B1, w=50km) |
| 3. Bearing-restricted | Does it survive when only NE-SW corridors are sampled? | p ≤ 0.003 at ±5° tolerance |
| 4. Joint conjunction | Does it beat the canonical K on all three catalogs simultaneously? | **p_joint = 0.0002** |
| 5. Pole sensitivity | Robust to the exact corridor definition? | yes, 4 fits within MC noise |
| 6. UNESCO global | Significant at planetary scale? | no, 90th percentile only |

Full Michael Line methodology in [`docs/POPULATION_CORRIDOR_PROTOCOL_V2.md`](docs/POPULATION_CORRIDOR_PROTOCOL_V2.md). Full Belinus Line pre-registered protocol in [`docs/POPULATION_CORRIDOR_PROTOCOL_BELINUS.md`](docs/POPULATION_CORRIDOR_PROTOCOL_BELINUS.md); v0.3.0 amendment in [`docs/PROTOCOL_AMENDMENT_v0.3.0.md`](docs/PROTOCOL_AMENDMENT_v0.3.0.md).

## Reproducing the Michael Line results

Requirements: Python 3.10+, numpy. No other dependencies — all data fetching uses the standard library.

```bash
git clone https://github.com/salahealer9/earthgrid-ley-lines-analysis
cd earthgrid-ley-lines-analysis
python -m venv venv && source venv/bin/activate
pip install numpy

# Build reference catalogs (one-time fetch from OSM Overpass + Wikidata)
python scripts/build_population_catalogs.py --skip-wikidata

# Run the joint conjunction test (Test 4)
python scripts/triple_corridor_test.py \
  --catalog data/population/catalog_B1_strict.csv:B1 \
  --catalog data/population/catalog_A_michael.csv:A \
  --catalog data/population/catalog_B2_broad.csv:B2 \
  --canonical-pole 33.330 -147.354 \
  --widths-km 5 10 20 50 100 \
  --trials 10000 \
  --out-prefix results_corridor/population/triple_canonical130_iso

# Run the global UNESCO sanity check (Test 6)
python scripts/unesco_global_sanity_check.py \
  --width-km 100 --trials 10000 \
  --out results_corridor/unesco_sanity_check_100km.json
```

The Belinus Line analysis follows the same scripts with different inputs (new bounding box, new catalogs, Widford-anchored canonical pole). Reproduction instructions will be added when the analysis is complete.

## Repository layout

```
data/
  population/         Reference catalogs (A, B1, B2) and UNESCO
  ley_lines/          Canonical 130-site and current LineString extractions (Michael)
  belinus/            Belinus Line data: per-map nodes and (optional) traced current vertices
scripts/
  build_population_catalogs.py    OSM Overpass + Wikidata catalog builder
  corridor_null_test.py           Test 1: internal nulls
  population_corridor_test.py     Tests 2 & 3 with --bearing-tolerance
  triple_corridor_test.py         Test 4: joint conjunction
  best_fit_great_circle.py        Test 5: SVD pole fit
  extract_kml_coordinates.py      Mary/Michael current vertex extraction
  unesco_global_sanity_check.py   Test 6: global null
docs/
  POPULATION_CORRIDOR_PROTOCOL_V2.md         Michael Line pre-registered protocol
  POPULATION_CORRIDOR_PROTOCOL_BELINUS.md    Belinus Line pre-registered protocol
  PROTOCOL_AMENDMENT_v0.3.0.md               Belinus protocol amendment (canonical 33-node list)
  BELINUS_DATA_EXTRACTION_GUIDE.md           Belinus data extraction workflow guide
  MICHAEL_LEY_LINES_RESULT.md                Michael Line full results writeup
results_corridor/                Test outputs (JSON summaries + logs)
paper/                           Manuscript draft (abstract, sections, figures)
```

## Limitations

- **OSM coverage variability.** Reference catalogs are drawn from OpenStreetMap, which has uneven mapping density across the bbox.
- **Bbox specificity.** Michael Line results are conditional on the southern-Britain bbox (lat 49.5–53.5°N, lon -6.5–+2.5°E). The Belinus Line uses a different bbox (50.0–59.0°N, 5.5°W–1.5°E) covering full Britain. The Michael Line continental extension through Mont-Saint-Michel and Skellig Michael is future work.
- **No mechanism.** The methodology establishes statistical significance only. It is silent on causation.

## Citation

If you use this methodology or the catalogs, please cite the latest release via the concept DOI (which always points to the most recent version):

> Gherbi, S.-E. (2026). *Six-concentric-tests framework for ley-line corridor claims: case studies of the Michael and Belinus Lines in Britain*. Zenodo. https://doi.org/10.5281/zenodo.20307500

For citing a specific version:

- v0.3.0 (Belinus protocol amended with canonical 33-node list): [10.5281/zenodo.20524063](https://doi.org/10.5281/zenodo.20524063)
- v0.2.0 (Belinus Line protocol pre-registered): [10.5281/zenodo.20386489](https://doi.org/10.5281/zenodo.20386489)
- v0.1.1 (Michael Line analysis, B2 matrix complete): [10.5281/zenodo.20312153](https://doi.org/10.5281/zenodo.20312153)
- v0.1.0 (Michael Line initial release): [10.5281/zenodo.20307501](https://doi.org/10.5281/zenodo.20307501)

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

## License

Code: Apache-2.0 (see [`LICENSE`](LICENSE)).
Data and documentation: CC-BY-4.0.

Reference catalogs derived from OpenStreetMap are © OpenStreetMap contributors under the [ODbL](https://www.openstreetmap.org/copyright). UNESCO World Heritage Sites data is © UNESCO / World Heritage Centre. The Belinus Line canonical alignment is sourced from Biltcliffe and Hoare (2012), *The Spine of Albion*; see Section 13 of the Belinus protocol for data-availability and third-party copyright handling.

## Acknowledgments

The 130-site Michael alignment KML was extracted from a publicly published Google My Maps document (2017). The Belinus Line is canonically defined by Biltcliffe and Hoare's *The Spine of Albion* (Sacred Lands Publishing, 2012, revised ePub edition 2020/2021); the author thanks Gary Biltcliffe for correspondence regarding the methodology and case-study handling.

The methodology engages with — and is in part motivated by — Matthew Johnson's critique that dense archaeological landscapes render naive site-counting along alignments uninformative; this framework is designed to address that critique directly.
