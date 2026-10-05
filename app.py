"""
app.py  (COMPASS-AI v2.0)

Web front end for the lifecycle-aware reporting-standard router. Answer three
questions (and, optionally, the lifecycle stage of the work) and receive the
core standards that govern the study, the related instruments to consult, and
a downloadable summary.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

Routing logic: router.py. Registry and routing table: standards.py.
This file is presentation only.
"""

import streamlit as st

from standards import STANDARDS, ROUTES, LIFECYCLE, VERSION
from router import route, as_markdown, ROLE_ORDER, ROLE_HEADINGS

st.set_page_config(page_title="COMPASS-AI", page_icon="🧭")

CATEGORY_LABEL = {
    "reporting": "Reporting guideline",
    "appraisal": "Appraisal / risk-of-bias tool",
    "min_info": "Minimum-information standard",
    "governance": "Governance / trustworthiness framework",
    "other": "Other",
}


def standard_line(sid, note=None):
    m = STANDARDS[sid]
    stages = ", ".join(sorted(m["stages"]))
    extra = f" ({note})" if note else ""
    return (f"**[{sid}]({m['url']})**{extra}  \n{m['full_name']}  \n"
            f"_{CATEGORY_LABEL[m['category']]}_ · stages {stages} · {m['citation']} · doi:[{m['doi']}]({m['url']})")


st.title("COMPASS-AI")
st.caption(f"A lifecycle-aware router for reporting standards in healthcare AI · version {VERSION}")
st.caption("Answer three questions about your study and read off the standards that govern it. "
           "This tool selects standards; it does not judge whether a study meets them.")
st.divider()

# --- Gate 1 ---------------------------------------------------------------
st.subheader("1. Is this a protocol for an interventional AI trial that has not yet been conducted?")
is_protocol = st.radio("Trial protocol", ["No", "Yes"], horizontal=True, label_visibility="collapsed") == "Yes"

# --- Gate 2 ---------------------------------------------------------------
primary_type = secondary_type = None
labels = {k: v["label"] for k, v in ROUTES.items()}
if not is_protocol:
    st.subheader("2. What is the primary study type?")
    primary_type = st.selectbox("Primary study type", options=list(labels), format_func=lambda k: labels[k],
                                index=None, placeholder="Select the primary design of your study",
                                label_visibility="collapsed")
    with st.expander("Definitions of the study types"):
        for k, r in ROUTES.items():
            st.markdown(f"**{r['label']}**: {r['definition']}")
    if primary_type is not None:
        st.caption(ROUTES[primary_type]["definition"])
        if st.checkbox("This study also falls into a second design family "
                       "(for example, an LLM study that is also a randomised trial, or a trial of an imaging AI)."):
            secondary_type = st.selectbox("Secondary study type", options=[k for k in labels if k != primary_type],
                                          format_func=lambda k: labels[k], index=None,
                                          placeholder="Select the secondary design")
else:
    st.info("A protocol routes to SPIRIT-AI. You can still answer question 3 below.")

# --- Gate 3 ---------------------------------------------------------------
st.subheader("3. Did the research process itself use generative AI tools?")
st.caption("For example, a large language model used to draft text, write code or analyse data. "
           "Studying or testing an LLM is covered by question 2, not here.")
genai = st.radio("Generative AI in the research process", ["No", "Yes"], horizontal=True,
                 label_visibility="collapsed") == "Yes"

# --- Optional lifecycle stage ---------------------------------------------
with st.expander("Optional: which lifecycle stage does this report cover?"):
    stage = st.selectbox("Lifecycle stage", options=[None] + list(LIFECYCLE),
                         format_func=lambda s: "Not specified" if s is None else f"{s} {LIFECYCLE[s]}")

st.divider()

ready = is_protocol or primary_type is not None
if not ready:
    st.warning("Select a primary study type, or indicate that the work is a trial protocol.")
    st.stop()

result = route(is_trial_protocol=is_protocol, primary_type=primary_type, secondary_type=secondary_type,
               genai_in_research=genai, stage=stage)

if result["open_node"]:
    st.error("Open node. No dedicated standard for multimodal foundation models was identified in the corpus. The nearest-fit set "
             "below is computed by a fixed rule; report the domains listed at the end explicitly.")

st.metric("Core standards to consult", result["n_core"])
st.caption("Where two standards ask for the same item, report it once and cross-reference it.")

for key in ROLE_ORDER:
    ids = result[key]
    if not ids:
        continue
    st.markdown(f"### {ROLE_HEADINGS[key]}")
    for sid in ids:
        st.markdown(standard_line(sid, result["related_notes"].get(sid)))

if result["uncovered_domains"]:
    st.markdown("### Domains the nearest-fit standards do not address specifically (report explicitly)")
    for d in result["uncovered_domains"]:
        st.markdown(f"- {d}")

if result["stage_check"]:
    sc = result["stage_check"]
    st.markdown("### Lifecycle check")
    if sc["in_window"]:
        st.markdown(f"Stage {sc['stage']} ({LIFECYCLE[sc['stage']]}) lies within the lifecycle window of the "
                    "selected study type.")
    else:
        st.warning(f"Stage {sc['stage']} lies outside the window of the selected study type. Study types that "
                   f"cover this stage: {', '.join(labels[k] for k in sc['routes_covering_stage'])}.")

if result["notes"]:
    st.markdown("### Notes")
    for n in result["notes"]:
        st.markdown(f"- {n}")

st.divider()
st.download_button("Download this result (Markdown)", data=as_markdown(result),
                   file_name="reporting_standards.md", mime="text/markdown")

with st.expander("About this tool and how to cite it"):
    st.markdown(
        "COMPASS-AI operationalises the routing algorithm described in the accompanying manuscript. It maps 31 "
        "AI-specific reporting guidelines, appraisal tools, minimum-information standards and governance "
        "frameworks across an eight-stage research lifecycle and returns the set that governs a given study.\n\n"
        "Source code: https://github.com/dry-ash/compass-ai\n\n"
        "Archived release (DOI): https://doi.org/10.5281/zenodo.23136990")
