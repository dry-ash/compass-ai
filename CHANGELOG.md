# Changelog

## v1.1.0 (October 2026)

Changes made after the external expert evaluation of v1.0 and in response to peer review.

### Routing
- **All 28 corpus instruments are now routable.** Nine instruments that v1.0 never returned (BIAS, CAIR, CREMLS, ELEVATE-GenAI, CLIX-M, Do No Harm, TRUST-AI, HAIRA, Luo 2016) now have a defined route, role or trigger (manuscript Table 1, Supplementary Table S1).
- **Two output tiers.** *Core* standards (counted as reporting burden) and *related* instruments (consult as needed, not counted).
- **One minimum-information standard per study.** v1.0 returned both MI-CLAIM and MINIMAR for every study. v1.1 fills a single cross-cutting slot by rule: MI-CLAIM-GEN when the AI under study is generative, MI-CLAIM when the study builds or validates a model, MINIMAR when it applies an existing model; precedence generative > development > application.
- **Gate 3 clarified.** The question concerns generative AI used as a tool in the research process (writing, coding, analysis) and adds GAMER. Studying or testing an LLM is handled by Gate 2.
- **Conditional rule.** ELEVATE-GenAI is added for economic evaluations that used generative AI in the research process.
- **Implementation route.** Returns DECIDE-AI as the nearest-fit reporting checklist, SALIENT as the translation framework, and APPRAISE-AI as appraisal companion.
- **Operational definitions** for every study type (shown in the app). Multi-reader and crossover reading studies, including simulated reading, are diagnostic accuracy studies; trials require allocation of participants to AI-supported versus comparator arms.
- **Open node computed by rule.** The foundation-model route names no instruments; `router.nearest_fit()` selects reporting, minimum-information and appraisal instruments about the AI under study whose scope covers LLM or foundation models and whose stages overlap S3-S5. The route also returns the minimum uncovered domains to report.
- **Lifecycle made explicit.** Every route has a lifecycle window; an optional stage input adds stage-specific general instruments and reports whether the stage lies in the window of the chosen study type.

### Software
- Added `analysis.py` (coverage, burden and co-occurrence analyses reproduced from the registry).
- Added `evaluation/` with the de-identified external-evaluation responses and a reproducible analysis script.
- Tests moved to `tests/test_routing.py` and extended (reachability of all 28 instruments, deterministic open node, one minimum-information standard, lifecycle behaviour).
- The complete repository (not only `app.py`) is archived with each Zenodo release.

## v1.0.0 (July 2026)
Initial release accompanying the submitted manuscript.
