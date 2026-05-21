# Declarations

## Author Contributions

Salah-Eddin Gherbi conceived the methodology, implemented the computational framework, assembled the reference catalogs, performed the analyses, generated the figures, and wrote the manuscript.

## Data Availability

All reference catalogs (Catalogs A, B1, B2, UNESCO) and the canonical 130-site KML extraction underlying this work are openly available under CC-BY-4.0 in the Zenodo deposit:

> Gherbi, S.-E. (2026). *Population-level corridor test for the Michael ley line in southern Britain* (v0.1.1). Zenodo. https://doi.org/10.5281/zenodo.20312153

The Zenodo deposit additionally includes timestamped raw responses from the OpenStreetMap Overpass API and the UNESCO World Heritage Centre syndication feed, ensuring the reported tests are reproducible against the catalog state at the time of testing even if upstream data sources change.

## Code Availability

All code implementing the six-test framework, the figure-generation scripts, and the supporting utilities is openly available under Apache-2.0 in the same Zenodo deposit above and at the corresponding GitHub repository: https://github.com/salahealer9/earthgrid-ley-lines-analysis. The code is additionally preserved in the Software Heritage long-term archive at `swh:1:dir:eacb8ff55520d38a30109b759eb302e2e43a9eaa`. All scripts use Python 3.10+ with NumPy as the only external dependency for the core analyses; figure generation additionally requires matplotlib and (optionally) cartopy.

## Competing Interests

The author declares no competing interests, financial or otherwise.

## Funding

This research received no external funding and was conducted independently.

## Ethics Approval

Not applicable. This research used only publicly available cultural-geographic catalogs from OpenStreetMap and the UNESCO World Heritage Centre, with no human subjects or non-public data.

## Acknowledgments

The 130-site canonical Michael alignment KML used to define the corridor under test was extracted from the public St Michael Line in UK Google My Maps document (Anonymous 2017), which traces the Miller–Broadhurst tradition (Miller and Broadhurst 1989). The author thanks the OpenStreetMap contributor community for the underlying archaeological-site data that made the population-level tests possible.
