# 1. Introduction

## 1.1 The alignment-claim problem

A recurring class of hypothesis in the cultural-geographic and archaeological literature concerns whether geographically dispersed sites — temples, prehistoric monuments, churches, sacred landscapes — lie along corridors more tightly than would be expected by chance. Such alignment claims appear in contexts ranging from antiquarian ley-line speculation (Watkins 1925) and contemporary "earth grid" hypotheses to formal landscape-archaeology questions about deliberate spatial planning across prehistoric and early-historic eras. The question is not whether any given line *appears* to align several sites — given a large enough catalog, alignment claims can be generated trivially — but whether the alignment is statistically distinguishable from what dense site distributions and chosen catalog curation will produce regardless of any underlying causal pattern.

The methodological challenge is sharper than it first appears. Three distinct confounds operate simultaneously:

1. **Catalog curation.** The sites selected to test an alignment claim are often selected *because* they lie on the proposed alignment. Internal-null tests on such catalogs measure curation tightness rather than population-level signal.
2. **Background density.** Dense site landscapes guarantee that any line drawn through a populated region will pass near many sites by chance.
3. **Orientation effects.** In landmasses with strong directional structure (Britain's NE-SW long axis, for instance), corridors aligned with that direction will trivially over-populate site catalogs without implying any specific alignment.

Each of these has been recognized in prior critiques of alignment claims, but the standard statistical treatments in the literature have addressed them piecemeal rather than as a unified framework. The present work introduces a six-concentric-tests methodology that addresses all three confounds, plus three further confounds (correlated-catalog conjunction, definition sensitivity, and regional-versus-global scope), in a single sequence applicable to any corridor-alignment hypothesis.

## 1.2 Prior statistical critiques

The earliest alignment claims in the modern literature came from Watkins (1925), whose proposed "ley" lines of prehistoric trackways across Britain rested on the visual observation that named sites — standing stones, churches built on prehistoric foundations, hilltops, fords, ancient yew trees — appeared to lie on straight lines across Ordnance Survey maps. Watkins offered no statistical test; his claim rested on the apparent improbability of the observed alignments.

Statistical scrutiny of such claims began in earnest with Bob Forrest's Monte Carlo simulations, first published in a 1976 article "Linearity and Ley Lines" (The Ley Hunter, No. 74). Forrest's program randomly scattered points across a map and measured how frequently apparent alignments emerged from pure randomness; the result was that leys formed routinely by chance. He extended the critique by mapping mundane modern features — public telephone kiosks (Forrest 1977), electricity pylons, and municipal locations (Forrest 1978) — and showed that these arbitrary catalogs produced the same geometric patterns as prehistoric monuments.  As Forrest's Monte Carlo simulations demonstrated (1976), if a catalog is sufficiently dense, apparent alignments are inevitable — a conclusion reinforced by Broadbent's (1980) peer‑reviewed simulation in the Journal of the Royal Statistical Society. The dense-landscape critique thus received its first computational formulation in this 1976–1978 body of work, preceding the better-known statistical treatment of Williamson and Bellamy (1983).

The most sustained statistical treatment was that of Williamson and Bellamy (1983), who applied rigorous Monte Carlo methods to British monument catalogs and concluded that ley-line claims at the precision conventionally used (sites within a few hundred metres of a corridor) were not statistically supported once the high density of British archaeology was properly accounted for. Their work is the canonical statistical refutation in this literature.

A parallel critique developed in landscape archaeology, summarized by Johnson (*Ideas of Landscape*, Wiley-Blackwell; 2006) and others: the density of recorded archaeological sites in the British landscape is so great that *any* line cut across a map will inevitably intersect numerous historical markers, rendering raw site-counts uninformative as evidence for intentional alignment. This is the dense-landscape critique in its mature form, and it is the central methodological motivation for the present work.

Two further observations from this literature deserve mention. First, Richard Atkinson — the excavator of Stonehenge — gave this critique its most vivid formulation in a 1982 article, "In the Spirit of the Ley Hunter", where he observed that random straight lines drawn across a map of Britain, like spaghetti thrown on the paper, would intersect telephone boxes as readily as they intersect ancient monuments. The analogy captures the dense-landscape critique in its essence: in a sufficiently rich catalog, pattern detection is not evidence of structure. Second, Clive Ruggles (2015), working on archaeoastronomical alignment claims, has emphasized the importance of pre-registering catalog selection and corridor parameters before testing, to avoid the multiple-comparison problem implicit in choosing the best-fitting alignment among many candidates.

Each of these critiques is well-founded. None, however, is operationalized as a portable framework for adjudicating future alignment claims on the same terms.

## 1.3 The methodological gap

The standard rebuttal to a ley-line claim, in the literature surveyed above, takes the following form: "the British landscape is dense; chance alignments are expected; therefore the claim is not supported." This is correct but underspecified. A claimant can in principle respond: "but my specific corridor exceeds chance even at this density." The exchange that follows typically reaches an impasse, because the necessary comparison — the claimant's corridor against a properly-constructed null distribution of comparable corridors — is rarely performed.

What such a comparison requires, when one stops to enumerate it, is:

(a) A test statistic measuring the corridor's site count against an independent reference catalog (not the catalog used to define the corridor in the first place);
(b) A null distribution of random corridors drawn within the same data region;
(c) Orientation control, so that corridors aligned with the landmass long axis are not artifactually privileged;
(d) Multiple-catalog conjunction, so that one significant marginal does not drive the result;
(e) Sensitivity to the precise corridor definition, since alignment claims often rest on conventional rather than data-derived line definitions;
(f) A separate scale-of-claim check distinguishing regional from global significance.

We are not aware of any prior published alignment study that addresses all six. Most address two or three.

## 1.4 Contribution

The present work introduces a six-concentric-tests framework that operationalizes each requirement above as a Monte Carlo procedure on a fixed bounding box and a fixed corridor parameterization. The tests are designed so that a corridor of genuine population significance must survive *all six* tests; survival of any subset is treated as informative but not sufficient. Failure of any test is informative on its own terms — it identifies which class of confound is driving an apparent alignment.

The six tests, summarized:

1. **Internal null** — establishes that the curated catalog of canonical sites is internally tight on the corridor, but conditional only on the curator's choices and not interpretable as population evidence.
2. **Population null (isotropic)** — tests the canonical corridor against random great circles through the same region, using a reference catalog that is exhaustive within the bbox and independent of the curated catalog.
3. **Population null (bearing-restricted)** — repeats (2) under the constraint that random corridors must align with the canonical bearing within ±D°, controlling for landmass orientation.
4. **Joint conjunction** — tests whether the canonical corridor simultaneously exceeds chance on multiple independent reference catalogs from the same set of trials.
5. **Pole sensitivity** — verifies that the result is robust across multiple defensible definitions of the canonical corridor, including data-derived fits to the underlying tradition's vertex data.
6. **Global sanity check** — tests whether the corridor's significance extends to planetary scale or is regionally bounded.

Each test addresses a specific class of confound. Each is computationally light (under a minute on commodity hardware). The framework is portable to any corridor-alignment hypothesis where (i) a candidate corridor can be specified and (ii) reference catalogs of relevant cultural sites can be assembled within a bounded region.

## 1.5 Demonstration case: the canonical Michael Line

To demonstrate the framework, we apply it to the canonical "Michael ley line" in southern Britain — the alignment first proposed in the contemporary form by Miller and Broadhurst (*The Sun and the Serpent*, 1989), running from St Michael's Mount in Cornwall through Glastonbury Tor, Avebury, and a series of churches dedicated to St Michael, terminating in East Anglia. The Miller–Broadhurst tradition associates this alignment with paired "Mary" and "Michael" energetic currents meandering around a central axis. The alignment is one of the better-known contemporary ley-line claims and has accumulated a substantial popular literature without, to our knowledge, a published statistical adjudication that controls for all six classes of confound.

The reference catalogs we use are drawn entirely from OpenStreetMap and are independent of the Miller–Broadhurst tradition: 754 St Michael place-of-worship records, 2422 strict prehistoric and Iron-Age monuments, and 5500 broader archaeological records. The canonical corridor is defined by the great circle through the best site pair from a 130-site KML extraction of the alignment.

The data give a clear answer. The canonical Michael corridor passes all four population-level tests (Tests 2–5) at the 50 km width, with joint conjunction p = 0.0002 (one-sided, 10,000 trials) under the isotropic null, surviving Bonferroni correction across five widths. The result is stable across three bearing-restriction tolerances (±30°, ±15°, ±5°) and across four independent corridor pole definitions (range 0.0001 to 0.0004). The K_null mean is invariant across orientation tolerances, ruling out the landmass-diagonal confound. The global UNESCO sanity check (Test 6) does not reach significance — the corridor is statistically distinguishable from random great circles within Britain but not from random great circles globally.

The empirical claim is therefore narrow: the canonical Michael corridor over-populates independent reference catalogs of culturally significant sites in southern Britain at population scale, beyond what is explained by catalog curation, background site density, landmass orientation, multiple-comparison effects, or pole-definition sensitivity. The claim is silent on mechanism, and the corridor's extended trajectory beyond southern Britain shows no global signal.

This result is, in our view, of secondary importance to the present paper. The framework is the principal contribution; the Michael Line is a worked example. The remainder of the paper proceeds as follows. Section 2 details the methodology (test statistic, reference catalogs, the six tests, software). Section 3 reports per-test results for the Michael Line. Section 4 discusses the data's interpretation and limitations, and proposes the framework's broader applicability to other alignment claims.
