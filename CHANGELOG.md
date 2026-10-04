# Changelog

## v2.0.0 (October 2026)

Release accompanying the revised manuscript. Changes since v1.0.0 (the interim v1.1.x tags made during the revision are superseded by this release):

### Corpus and registry
- Registry of 31 instruments (the v1.0.0 registry implemented 19). Each instrument carries its function category, declared scope, lifecycle-stage span from the verified coding, and citation and DOI.
- Every instrument has a defined route, role or trigger, so all 31 can be returned.

### Routing
- **Two output tiers.** Core standards (counted as reporting burden) and related instruments (consult as needed, not counted).
- **One core minimum-information slot**, filled by rule: MI-CLAIM-GEN when the AI under study is generative, MI-CLAIM when the study builds or validates a model, MINIMAR when it applies an existing model (precedence in that order).
- **Gate 3** concerns generative AI used as a tool in the research process and adds GAMER; studying or testing a generative model is answered at Gate 2.
- **Conditional rule.** ELEVATE-GenAI is added for economic evaluations that used generative AI in the research process.
- **Implementation route** returns DECIDE-AI as the nearest-fit reporting checklist, SALIENT as the translation framework and APPRAISE-AI as appraisal companion.
- **Operational definitions** for every study type, shown in the app. Multi-reader and crossover reading studies, including simulated reading, are diagnostic accuracy studies; trials require allocation of participants to AI-supported and comparator arms.
- **Open node computed by rule.** The foundation-model route names no instruments; `router.nearest_fit()` selects reporting, minimum-information and appraisal instruments about the AI under study whose scope covers LLM or foundation models, whose stages overlap S3-S5 and that are not limited to a single task. The route also returns five domains that the nearest-fit standards do not address specifically for multi-task multimodal use.
- **Lifecycle made explicit.** Every study type has a lifecycle window (the stages at which a study of that type generates evidence); an optional stage input adds stage-specific general instruments and reports whether the stage lies in the window of the chosen study type.

### Final source and confidentiality check
- P04 Ng 2023 uses implementation plus imaging (eight core instruments).
- P05 O’Sullivan 2026 uses trial plus LLM, with Gate 3 = yes because Gemini analysed research feedback; GAMER is added (seven core instruments).
- The manuscript demonstration is restricted to routing; unverified reporting-gap scores were withdrawn.
- Participant-level role and experience links are withheld from the public response workbook; all nine evaluators remain included on the basis of subsequent author-confirmed anonymous-use consent.
- DOI labels distinguish the version 2.0 record from the concept DOI.
- Added reproducible lifecycle-verification and item-inventory summaries.

### Software
- `analysis.py` reproduces the coverage, burden and co-occurrence analyses from the registry.
- `evaluation/` contains the de-identified external-evaluation responses and a script that reproduces the reported results.
- `tests/test_routing.py` pins the router to the manuscript (routing table of Table 2, demonstration studies with an imaging secondary type where the AI's input is medical images, reachability of all 31 instruments, deterministic open node, one core minimum-information slot, study-type and fixed-type stage behaviour, no duplicates).
- The complete repository is archived with each Zenodo release.

## v1.0.0 (July 2026)
Initial release accompanying the submitted manuscript.
