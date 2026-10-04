# COMPASS-AI

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23116822.svg)](https://doi.org/10.5281/zenodo.23116822)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lifecycle-aware router for reporting standards in healthcare AI (version 2.0). Answer three
questions about your study, optionally state the lifecycle stage of the work, and read off the
standards that govern it. COMPASS-AI operationalises the routing algorithm described in the
manuscript "COMPASS-AI: A Lifecycle-aware Algorithm for Selecting Reporting Standards in Healthcare
AI Research."

1. Is the work a protocol for an interventional AI trial not yet conducted?
2. What is the primary study type (and, optionally, a second design family)?
3. Did the research process itself use generative AI tools?

The tool returns **core** standards (the primary reporting guideline, its appraisal companion,
any conditional addition, one minimum-information standard chosen by rule (MI-CLAIM-GEN, MI-CLAIM or
MINIMAR), FUTURE-AI and STANDING Together, and
GAMER when generative AI was used in the research process) and **related** instruments to consult.
All 31 instruments in the corpus are reachable. COMPASS-AI selects standards; it does not judge
whether a study meets them.

## Repository

| File | Purpose |
|---|---|
| `app.py` | Streamlit web interface |
| `router.py` | The routing algorithm as a pure, testable function (formal statement in the docstring) |
| `standards.py` | Registry of the 31 instruments (category, lifecycle stages, scope, citation, DOI) and the routing table |
| `reproduce_supporting_analyses.py` | Reconciles lifecycle verification and item-level overlap from the supplied workbooks in `data/` |
| `analysis.py` | Reproduces the coverage, burden and co-occurrence analyses |
| `tests/test_routing.py` | Pins the router to the manuscript |
| `evaluation/` | De-identified external-evaluation responses and the script that reproduces the reported results (uses the archived v1.0 router the participants used) |
| `CHANGELOG.md` | Changes between versions |

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Tests and analyses

```bash
pip install pytest
python -m pytest -q          # or: python tests/test_routing.py
python analysis.py
python reproduce_supporting_analyses.py
python evaluation/analyse_external_evaluation.py
```

## Deployed app

https://app-compass-ai.streamlit.app/

## Archive and citation

Version 2.0 record: https://doi.org/10.5281/zenodo.23116822.
All-versions (concept) record: https://doi.org/10.5281/zenodo.21215392.
The previous v1 record is https://doi.org/10.5281/zenodo.21215393.
See `CITATION.cff`.

## Licence

MIT (see `LICENSE`).
