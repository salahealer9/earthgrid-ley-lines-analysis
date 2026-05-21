# 4. Discussion

## 4.1 What the data establish

The canonical Michael ley line corridor in southern Britain over-populates three independent reference catalogs of culturally significant sites at population scale. The joint conjunction p-value of 0.0002 at the 50 km width (one-sided, 10,000 trials) survives Bonferroni correction across five widths and is stable across three bearing-restriction tolerances (isotropic p_joint = 0.0002; ±5° p_joint = 0.0006) and four independent corridor pole definitions (range 0.0001 to 0.0004). The K_null mean was effectively invariant across orientation tolerances in all three catalogs, indicating no detectable orientation confound from the NE-SW British landmass diagonal. The 12-site and 130-site canonical poles, ~50 km apart, gave nearly identical results, as did SVD fits performed directly against the meandering "current" LineStrings from the source KML (residual RMS 2.95–3.76 km against thousands of vertices). The corridor therefore behaves as a *region* rather than a brittle line: small perturbations of the canonical pole within ~50 km do not shift the significance appreciably.

This is the strongest empirical claim the data support: the alignment is a real population-level feature of southern Britain, not an artifact of the curated catalog or its orientation.

## 4.2 Addressing the dense-landscape critique

Following Williamson and Bellamy (1983) and Johnson (2006), the density of archaeological sites in the British landscape is sufficient that a great circle drawn through almost anywhere will pass near many sites. Williamson and Bellamy were the first to apply a rigorous statistical treatment to British alignment claims, demonstrating that the high monument density of England renders raw site-counting along any line statistically uninformative. We endorse this critique entirely — it is precisely why naive site-counting along an alignment is uninformative, and why this work adopts a population-level statistical test rather than reporting raw counts.

Under our test, both the canonical Michael corridor's K_real and the null distribution's K_t are computed against the *same* dense reference catalog within the *same* bounding box. Catalog density therefore enters symmetrically on both sides of the comparison. If the British landscape were uniformly site-rich, the null mean would simply rise to match — as it does (K_null mean = 31 sites within 5 km for B1, against K_real = 199). The test asks whether the canonical corridor's count is unusual *relative to its own null*, not whether it crosses an absolute threshold.

The bearing-restricted null (Section 3.3) further controls for any tendency of NE-SW great circles to over-populate the British landmass diagonal. The flatness of K_null mean across tolerance levels in all three catalogs (variation under 1 site across the four conditions, in catalogs containing 754 to 5500 sites) confirms that the orientation confound — the natural reviewer follow-up to the density critique — is not present. The corridor's significance is location-specific, not orientation-driven.

The dense-landscape critique is therefore not an objection to overcome but the methodological foundation our test was built on. The test survives it.

## 4.3 What the data do not establish

Three claims, each plausibly inferable from a less careful reading of the results, are not supported by the data.

**The corridor is not unique.** The K_null maximum at w = 5 km is 436 sites for B1 — more than twice the canonical corridor's K_real = 199. The canonical Michael corridor sits at approximately the 98th percentile of the null distribution under each per-catalog test and at the ~99.98th percentile under the joint test, but it is not the maximal alignment. Other great circles through the UK would individually capture more prehistoric monuments. We make no claim about whether these alternative alignments are themselves culturally specified or merely statistical artifacts of the upper null tail; characterizing the structure of the upper tail is left as a question for future work.

**The signal is regional, not planet-wide.** The global UNESCO sanity check (Section 3.6) placed the canonical Michael great circle at the 88th–90th percentile of random global great circles' UNESCO hit counts, with effective one-sided p ≈ 0.10 at both widths tested. Neither value approaches statistical significance. The corridor's intersection with internationally recognizable sites (Nazca, Alice Springs, Moncong Lompobattang and the like) is consistent with the standard "ley-line fallacy": any 40,000 km great circle through populated regions will pass near comparable numbers of named sites. Quantification removes this observation as evidence for a global pattern.

**The test is silent on mechanism.** Our methodology establishes only statistical and geographic significance at the level of population geography. It does not address — and we make no claim about — what process produced the corridor: a previously unrecognized landscape or topographic feature; a cultural transmission of alignment knowledge across pre-Christian, Christian, and later eras; a continuous-reuse pattern in which Christian sites were deliberately placed on prehistoric ones along a known axis; or some combination of these. The result does *not* validate the broader ley-line tradition (Watkins 1925; Miller and Broadhurst 1989) and its interpretive claims about energetic currents along the corridor. Mechanism is a separate scientific question requiring different data and methods.

## 4.4 Reading B1 versus B2

The strict prehistoric catalog B1 and the broad archaeological catalog B2 produced qualitatively equivalent significance patterns, with Pearson correlation of K across trials rising monotonically with width: 0.93 at w = 5 km, 0.94 at w = 10 km, 0.95 at w = 20 km, 0.97 at w = 50 km, and 0.99 at w = 100 km. The corridor's over-population is not specific to prehistoric monuments — it also accommodates Roman villas, ridge-and-furrow agriculture, medieval settlements, and other post-prehistoric material in B2. Two non-mutually-exclusive readings are consistent with this pattern.

The parsimonious reading is **trans-temporal reuse**: a geographic corridor that mattered in prehistory continued to be built upon in subsequent eras, accumulating sites of multiple periods. This is consistent with the well-attested archaeological observation, surveyed by Hutton (1991), that significant prehistoric places (henges, hilltops, springs) are frequently reused into Iron Age, Roman, and Christian contexts.

A more cautious reading is **catalog non-independence**: OpenStreetMap contributors mapping archaeological sites may have referenced the same cultural-geographic intuitions that produce ley-line catalogs in the first place, partially weakening the "independent" status of B2. This cannot be fully excluded without a non-OSM control catalog (for instance, from a state heritage register applied through an automated geocoding pipeline without contributor curation). We do not have such a catalog available within the current study, and we therefore present (1) as the parsimonious reading while acknowledging (2) as a residual possibility.

Either reading is compatible with the population-level finding; the choice between them affects interpretation, not the validity of the statistical claim.

## 4.5 Effect size and width selection

The per-catalog effect sizes (z ≈ 2.2 to 3.4 in Bonferroni-significant cells) are an order of magnitude smaller than the internal-null z-scores on the curated catalogs (z = 16.5 to 245). This ratio is the empirical signature of curation: the curator-selected catalog is internally tight, but stripped of the curator's choices the underlying population corridor is a moderate-size effect. Treating z ≈ 3 as the headline magnitude — modest, real, and statistically anomalous without being dramatic — is the calibration the methodology produces. Reporting z ≈ 100 would be more attention-grabbing but would misrepresent what the population test actually measures.

The 50 km width emerges as the headline cell across all four population tests. Two factors converge to make this width optimal. At narrower widths (5–20 km), the population catalog is sparse along any single corridor: even a real alignment captures only a fraction of nearby sites because most of the catalog lies in the broader landscape. At wider widths (100 km), the corridor's footprint approaches the bounding-box scale itself, the null distribution broadens, and corridor specificity is lost. The 50 km half-width is approximately the scale at which the corridor's "shadow" on the broader landscape is most distinguishable from random alignments through the same dense region. The 50 km cell is the only width that crossed Bonferroni unambiguously across all null variants, though the 5–20 km widths showed consistent joint significance below 0.005. The fact that the same width emerges as the strongest cell in all six tests is, in our view, methodologically informative rather than a free parameter to be discounted.

## 4.6 Limitations

**OpenStreetMap coverage variability.** The three primary reference catalogs are drawn from OSM, which has uneven coverage across the bounding box. Under-mapping is correlated with land use and accessibility, neither of which is independent of the corridor. The result is robust only to the extent that coverage gaps are not spatially aligned with the corridor itself; a sensitivity check against a non-OSM catalog (such as a state heritage register applied automatically) would strengthen the result.

**UNESCO catalog coverage.** The catalog used for the global sanity check (Section 3.6) has well-known regional and conceptual biases: European sites are over-represented, oral and intangible heritage is under-represented, and inscription is itself a curated cultural process. The negative result (Michael corridor at the 88–90th percentile globally) is robust to these biases — they would inflate, not suppress, the elevated reading we observed, and the corridor still failed to reach significance. A more exhaustive global heritage catalog, were one available, would be preferable.

**Bounding-box specificity.** Results are conditional on the southern-Britain bbox (49.5–53.5° N, 6.5° W–2.5° E). The extension of the canonical alignment beyond this region — through Mont-Saint-Michel and onward to Skellig Michael in the west, or eastward across continental Europe — would require a different bbox and different reference catalogs, and is reserved for future work. Our finding speaks only to the southern-British corridor.

**Single canonical pole class.** While the four-pole sensitivity test (Section 3.5) confirms robustness within the cross-pole stability envelope of ~50 km, a continuous scan over the corridor parameterization to map the full significance landscape was not performed. This would be a useful extension to characterize the size of the "equivalent-result region" around the canonical pole.

**No mechanism.** As noted in Section 4.3, the test is silent on causation. This is not a limitation specific to this work but to the population-test paradigm generally.

## 4.7 Methodological implications

The principal contribution of this work is the six-concentric-tests framework rather than the specific finding for the Michael Line. The framework is portable: any claim of a corridor of aligned cultural sites, anywhere on Earth, can be evaluated by the same sequence of progressively stricter null tests. Other regional ley-line claims — the St. Michael continental axis through Mont-Saint-Michel, the Belinus Line, and others — can be adjudicated by the same methodology on equal terms, and the design is, we believe, equally applicable to corridor-alignment hypotheses outside the specifically ley-line literature.

In each case, the test design forces a specific question: not "does this look like an alignment?" but "would a random great circle through the same region, with no privileged orientation or selection, do as well?" That reframing is the methodological centerpiece.

The code and reference catalogs are open-source and citable (Section 2.7). We invite researchers working on other alignment claims to adopt and adapt the framework; results that fail any of the six tests are as scientifically informative as results that survive them.

The Michael Line, in this work, served as a demonstration case rather than the principal subject. Its survival of all six tests is the substantive empirical finding, but the framework's portability is the more transferable contribution.
