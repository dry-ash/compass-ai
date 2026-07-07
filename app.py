"""
app.py

A dead-simple web front end for the lifecycle-aware reporting-standard router.
The user answers three questions and receives a deduplicated set of the
reporting standards that govern their healthcare-AI study, with citations,
DOIs, and a downloadable summary.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

The routing logic lives in router.py and the verified standards in standards.py.
This file is presentation only.
"""

import streamlit as st

from standards import STANDARDS, ROUTES
from router import route, as_markdown

st.set_page_config(page_title="COMPASS-AI", page_icon="🧭")

CATEGORY_LABEL = {
    "reporting": "Reporting guideline",
    "appraisal": "Appraisal / risk-of-bias tool",
    "min_info": "Minimum-information standard",
    "governance": "Governance / trustworthiness framework",
}

ROLE_ORDER = [
    ("primary", "Primary reporting guideline"),
    ("appraisal", "Appraisal companion"),
    ("generative", "Generative-AI standard (research process)"),
    ("cross_cutting", "Cross-cutting standard (every study)"),
]


def standard_line(sid: str) -> str:
    m = STANDARDS[sid]
    return (
        f"**[{sid}]({m['url']})**  \n"
        f"{m['full_name']}  \n"
        f"_{CATEGORY_LABEL[m['category']]}_ · {m['citation']} "
        f"· doi:[{m['doi']}]({m['url']})"
    )


st.title("COMPASS-AI")
st.caption("A lifecycle-aware router for reporting standards in healthcare AI.")
st.caption(
    "Answer three questions about your study and read off the standards that govern it, "
    "positioned across the research lifecycle. This tool selects standards; it does not "
    "judge whether a study meets them."
)

st.divider()

# --- Gate 1 ---------------------------------------------------------------
st.subheader("1. Is this a protocol for an interventional AI trial that has not yet been conducted?")
is_protocol = st.radio(
    "Trial protocol",
    ["No", "Yes"],
    horizontal=True,
    label_visibility="collapsed",
) == "Yes"

# --- Gate 2 ---------------------------------------------------------------
primary_type = None
secondary_type = None
if not is_protocol:
    st.subheader("2. What is the primary study type?")
    labels = {k: v["label"] for k, v in ROUTES.items()}
    primary_key = st.selectbox(
        "Primary study type",
        options=list(labels.keys()),
        format_func=lambda k: labels[k],
        index=None,
        placeholder="Select the primary design of your study",
        label_visibility="collapsed",
    )
    primary_type = primary_key

    if primary_key is not None:
        spans_two = st.checkbox(
            "This study also falls into a second design family "
            "(for example, an LLM study that is also a randomised trial)."
        )
        if spans_two:
            secondary_options = [k for k in labels if k != primary_key]
            secondary_type = st.selectbox(
                "Secondary study type",
                options=secondary_options,
                format_func=lambda k: labels[k],
                index=None,
                placeholder="Select the secondary design",
            )
else:
    st.info("A protocol routes to SPIRIT-AI. You can still answer question 3 below.")

# --- Gate 3 ---------------------------------------------------------------
st.subheader("3. Did the research process itself use generative AI tools?")
st.caption("For example, using a large language model to draft text, generate code, or analyse data.")
genai = st.radio(
    "Generative AI in the research process",
    ["No", "Yes"],
    horizontal=True,
    label_visibility="collapsed",
) == "Yes"

st.divider()

# --- Result ---------------------------------------------------------------
ready = is_protocol or (primary_type is not None)
if not ready:
    st.warning("Select a primary study type, or indicate that the work is a trial protocol.")
    st.stop()

result = route(
    is_trial_protocol=is_protocol,
    primary_type=primary_type,
    secondary_type=secondary_type,
    genai_in_research=genai,
)

if result["open_node"]:
    st.error(
        "Open node. No dedicated standard exists for this study type. "
        "The nearest-fit standards are listed below; you must document explicitly "
        "what they do not cover. See Supplementary Table S4 for a provisional scaffold."
    )

st.metric("Standards to consult", result["n_standards"])
st.caption(
    "Overlapping items are satisfied once and cross-referenced; the effective burden "
    "is smaller than the raw sum of checklist items across these standards."
)

for key, heading in ROLE_ORDER:
    ids = result[key]
    if not ids:
        continue
    st.markdown(f"### {heading}")
    for sid in ids:
        st.markdown(standard_line(sid))

if result["notes"]:
    st.markdown("### Notes")
    for n in result["notes"]:
        st.markdown(f"- {n}")

st.divider()
summary_md = as_markdown(result)
st.download_button(
    "Download this result (Markdown)",
    data=summary_md,
    file_name="reporting_standards.md",
    mime="text/markdown",
)

with st.expander("About this tool and how to cite it"):
    st.markdown(
        "COMPASS-AI operationalises the routing algorithm described in the accompanying "
        "manuscript. It maps a corpus of AI-specific reporting guidelines, appraisal "
        "tools, minimum-information standards, and governance frameworks across an "
        "eight-stage research lifecycle, and returns the set that governs a given study. "
        "The routing reproduces the manuscript's demonstration exactly; see the test "
        "suite in the repository.\n\n"
        "Source code: https://github.com/dry-ash/compass-ai\n\n"
        "Archived release (DOI): https://doi.org/10.5281/zenodo.21215393"
    )
