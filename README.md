# Earth Grid Ley Lines Analysis

A population-level statistical framework for testing great-circle alignment claims about cultural sites, demonstrated on the canonical St Michael ley line in southern Britain.

## What this is

This repository implements a four-concentric-tests methodology for evaluating whether a hypothesized corridor of aligned sites is statistically exceptional, beyond what could be explained by:

1. **Catalog curation** — the sites tested were chosen *because* they appear aligned
2. **Background site density** — the underlying landscape is so site-rich that almost any line catches sites
3. **Orientation effects** — corridors oriented along a landmass diagonal trivially catch more sites than perpendicular ones
4. **Multiple-comparison artifacts** — passing one test out of several does not establish significance

The framework is portable to any corridor-alignment claim. It is applied here to the Michael ley line as a worked example.

## Headline result

The canonical Michael corridor in southern Britain over-populates three independent reference catalogs (754 Christian dedications, 2422 prehistoric monuments, 5500 broad archaeological sites) simultaneously at the 50 km width, with joint conjunction p = 0.0002 (one-sided, 10,000 trials). The result survives Bonferroni correction across five widths, orientation restriction to ±5° of the canonical bearing, and sensitivity to four independent pole definitions (canonical 130-site, Michael current fit, Mary current fit, combined currents fit).

A separate UNESCO global sanity check confirms the signal is **regional, not global**: the Michael corridor extended worldwide hits 41 UNESCO World Heritage Sites within 100 km — at the 90th percentile of random great circles, well outside the threshold for a global claim.

The finding is statistical and geographic. It establishes that the canonical Michael Line corridor exists at population scale and is not explained by curation, density, orientation, or chance alignment with the British landmass. It does not establish any proposed mechanism (geophysical, energetic, or otherwise) and does not validate the broader ley-line tradition's interpretive claims.

## Methodology

| Test | Question | Status |
|---|---|---|
| 1. Internal null | Are these 130 curated sites tightly aligned? | z = 16–245 (curation-inflated) |
| 2. Population isotropic | Does the corridor over-populate independent catalogs vs random great circles? | p = 0.0004 (B1, w=50km) |
| 3. Bearing-restricted | Does it survive when only NE-SW corridors are sampled? | p ≤ 0.003 at ±5° tolerance |
| 4. Joint conjunction | Does it beat the canonical K on all three catalogs simultaneously? | **p_joint = 0.0002** |
| 5. Pole sensitivity | Robust to the exact corridor definition? | yes, 4 fits within MC noise |
| 6. UNESCO global | Significant at planetary scale? | no, 90th percentile only |

Full methodology in [`docs/POPULATION_CORRIDOR_PROTOCOL_V2.md`](docs/POPULATION_CORRIDOR_PROTOCOL_V2.md). Results in [`docs/MICHAEL_LEY_LINES_RESULT.md`](docs/MICHAEL_LEY_LINES_RESULT.md).

## Reproducing the results

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

## Repository layout

```
data/
  population/         Reference catalogs (A, B1, B2) and UNESCO
  ley_lines/          Canonical 130-site and current LineString extractions
scripts/
  build_population_catalogs.py    OSM Overpass + Wikidata catalog builder
  corridor_null_test.py           Test 1: internal nulls
  population_corridor_test.py     Tests 2 & 3 with --bearing-tolerance
  triple_corridor_test.py         Test 4: joint conjunction
  best_fit_great_circle.py        Test 5: SVD pole fit
  extract_kml_coordinates.py      Mary/Michael current vertex extraction
  unesco_global_sanity_check.py   Test 6: global null
docs/
  POPULATION_CORRIDOR_PROTOCOL_V2.md   Pre-registered protocol
  MICHAEL_LEY_LINES_RESULT.md          Full results writeup
results_corridor/                Test outputs (JSON summaries + logs)
```

## Limitations

- **OSM coverage variability.** Reference catalogs are drawn from OpenStreetMap, which has uneven mapping density across the bbox.
- **Bbox specificity.** Results are conditional on the southern-Britain bbox (lat 49.5–53.5°N, lon -6.5–+2.5°E). The continental extension through Mont-Saint-Michel and Skellig Michael is future work.
- **No mechanism.** The methodology establishes statistical significance only. It is silent on causation.

## Citation

If you use this methodology or the catalogs, please cite the Zenodo deposit (DOI added on release).

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

## License

Code: Apache-2.0 (see [`LICENSE`](LICENSE)).
Data and documentation: CC-BY-4.0.

Reference catalogs derived from OpenStreetMap are © OpenStreetMap contributors under the [ODbL](https://www.openstreetmap.org/copyright). UNESCO World Heritage Sites data is © UNESCO / World Heritage Centre.

## Acknowledgments

The 130-site Michael alignment KML was extracted from a publicly published Google My Maps document (2017). The methodology engages with — and is in part motivated by — Matthew Johnson's critique that dense archaeological landscapes render naive site-counting along alignments uninformative; this framework is designed to address that critique directly.
