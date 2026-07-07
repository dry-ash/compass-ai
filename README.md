# COMPASS-AI

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21215393.svg)](https://doi.org/10.5281/zenodo.21215393)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lifecycle-aware router for reporting standards in healthcare AI. Answer three
questions about your study and read off the standards that govern it, positioned
across an eight-stage research lifecycle. COMPASS-AI operationalises the routing
algorithm described in the accompanying manuscript, "COMPASS-AI: A Lifecycle-aware
Algorithm for Selecting Reporting Standards in Healthcare AI Research."

The three questions are whether the work is a trial protocol, what the primary
study type is, and whether generative AI was used in the research process. The
tool returns a deduplicated set of the primary reporting guideline, its appraisal
companion where one exists, any generative-AI standard, and the cross-cutting
standards that apply to every study, each with its citation and DOI.

COMPASS-AI selects standards. It does not judge whether a study meets them.

## What is in this repository

| File | Purpose |
|---|---|
| `app.py` | Streamlit web interface (the three-question form) |
| `router.py` | The routing algorithm as a pure, testable function |
| `standards.py` | Verified standards registry and routing table (single source of truth) |
| `tests/test_demonstration.py` | Asserts the router reproduces the twelve published demonstration studies (Table 3) |
| `requirements.txt`, `LICENSE`, `CITATION.cff` | Environment, licence, and citation metadata |

Every standard in `standards.py` carries the exact citation and DOI used in the
manuscript. The routing table is the published algorithm expressed as data, not
a new mapping.

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

## Run the tests

```bash
pip install pytest
python -m pytest -q
# or, without pytest:
python tests/test_demonstration.py
```

The tests pin the tool to the manuscript: if the routing ever drifts from the
twelve demonstration studies, they fail.

## Deploy it (Streamlit Community Cloud, free)

1. Go to https://share.streamlit.io, sign in with GitHub, and choose "New app".
2. Point it at this repository, branch `main`, file `app.py`.
3. Deploy. You will get a public URL of the form `https://<name>.streamlit.app`.

## Archived release and DOI

This repository is archived on Zenodo with a citable DOI:
**https://doi.org/10.5281/zenodo.21215393**

To publish a new archived version, edit the code, then create a new GitHub
release (Releases, then Draft a new release, tag such as `v1.1.0`, publish).
Zenodo archives the release automatically and mints a version DOI, while the DOI
above always resolves to the latest version.

## Citation

If you use COMPASS-AI, please cite both the software archive and the paper. See
`CITATION.cff`; GitHub shows a "Cite this repository" button.

- Software: Jain Y, Wu D, Wang Z, Wang Z. COMPASS-AI: a lifecycle-aware router for
  reporting standards in healthcare AI. Zenodo. https://doi.org/10.5281/zenodo.21215393
- Paper: citation to be added on acceptance.

## Licence

MIT (see `LICENSE`). You are free to reuse and adapt the code with attribution.
