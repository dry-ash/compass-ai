"""
test_demonstration.py

Pins the routing tool to the manuscript. Each case below is one of the twelve
published demonstration studies (Table 3), with the routed standard set exactly
as reported. If the routing logic ever drifts from the paper, these tests fail.

Run from the repository root:  python -m pytest -q
Or without pytest:            python tests/test_demonstration.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router import route  # noqa: E402

CC = {"FUTURE-AI", "STANDING Together", "MI-CLAIM", "MINIMAR"}

# study id -> (kwargs to route(), expected set of ALL returned standard ids)
CASES = {
    "P01 prediction model (Rao 2025)": (
        dict(primary_type="prediction_model"),
        {"TRIPOD+AI", "PROBAST+AI"} | CC,
    ),
    "P02 diagnostic accuracy (Gulshan 2016)": (
        dict(primary_type="diagnostic_accuracy"),
        {"STARD-AI", "PROBAST+AI"} | CC,
    ),
    "P03 pragmatic RCT (Lin 2024)": (
        dict(primary_type="interventional_trial"),
        {"CONSORT-AI"} | CC,
    ),
    "P04 early live CDS (Ng 2023)": (
        dict(primary_type="early_clinical_eval"),
        {"DECIDE-AI", "APPRAISE-AI"} | CC,
    ),
    "P05 LLM + RCT dual (O'Sullivan 2026)": (
        dict(primary_type="interventional_trial", secondary_type="llm_generative"),
        {"CONSORT-AI", "TRIPOD-LLM", "DEAL"} | CC,
    ),
    "P06 chatbot (Ayers 2023)": (
        dict(primary_type="chatbot"),
        {"CHART"} | CC,
    ),
    "P07 imaging (McKinney 2020)": (
        dict(primary_type="imaging"),
        {"CLAIM", "PROBAST+AI"} | CC,
    ),
    "P08 economic (Wang 2024)": (
        dict(primary_type="economic"),
        {"CHEERS-AI"} | CC,
    ),
    "P09 economic (Hsieh 2025)": (
        dict(primary_type="economic"),
        {"CHEERS-AI"} | CC,
    ),
    "P10 implementation (Wong 2021)": (
        dict(primary_type="implementation"),
        {"SALIENT", "APPRAISE-AI"} | CC,
    ),
    "P11 LLM (Aali 2025)": (
        dict(primary_type="llm_generative"),
        {"TRIPOD-LLM", "DEAL"} | CC,
    ),
    "P12 foundation model, open node (Vukadinovic 2025)": (
        dict(primary_type="foundation_model"),
        {"TRIPOD-LLM", "MI-CLAIM-GEN", "DEAL"} | CC,
    ),
}


def _returned_set(result):
    ids = set()
    for k in ("primary", "appraisal", "generative", "cross_cutting"):
        ids.update(result[k])
    return ids


def test_all_twelve_demonstration_studies():
    failures = []
    for name, (kwargs, expected) in CASES.items():
        got = _returned_set(route(**kwargs))
        if got != expected:
            failures.append(
                f"{name}\n    expected: {sorted(expected)}\n    got:      {sorted(got)}"
            )
    assert not failures, "Routing drifted from the manuscript:\n" + "\n".join(failures)


def test_open_node_only_for_foundation_model():
    assert route(primary_type="foundation_model")["open_node"] is True
    assert route(primary_type="prediction_model")["open_node"] is False


def test_protocol_routes_to_spirit():
    r = route(is_trial_protocol=True)
    assert "SPIRIT-AI" in r["primary"]


def test_no_duplicate_standards():
    r = route(primary_type="llm_generative", secondary_type="interventional_trial",
              genai_in_research=True)
    everything = r["primary"] + r["appraisal"] + r["generative"] + r["cross_cutting"]
    assert len(everything) == len(set(everything)), "a standard was listed twice"


if __name__ == "__main__":
    # Allow running without pytest installed.
    for fn in [
        test_all_twelve_demonstration_studies,
        test_open_node_only_for_foundation_model,
        test_protocol_routes_to_spirit,
        test_no_duplicate_standards,
    ]:
        fn()
        print(f"PASS  {fn.__name__}")
    print("\nAll checks passed. The tool reproduces the twelve demonstration studies.")
