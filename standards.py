"""
standards.py

Single source of truth for the reporting-standard routing tool.

This module encodes two things, and nothing else:

1. STANDARDS: a registry of the AI reporting guidelines, appraisal tools,
   minimum-information standards, and governance frameworks that the routing
   algorithm can return. Every entry carries the exact citation and DOI used
   in the manuscript's reference list, so the tool never presents a standard
   the paper did not verify.

2. ROUTES and CROSS_CUTTING: the routing table. This reproduces the routed
   sets reported in the manuscript (Table 2 and Table 3). It is not a new or
   "improved" routing; it is the published algorithm expressed as data. The
   accompanying test suite asserts that this table reproduces all twelve
   demonstration studies exactly.

If a standard is added, retired, or re-cited, change it here once and both the
app and the manuscript display items stay consistent.
"""

# ---------------------------------------------------------------------------
# 1. Standards registry
# ---------------------------------------------------------------------------
# category is one of:
#   "reporting"    reporting guideline
#   "appraisal"    risk-of-bias / quality-appraisal tool
#   "min_info"     minimum-information standard
#   "governance"   governance / trustworthiness framework
#
# doi is the bare DOI; url is built from it. Do not hand-edit url.

def _u(doi: str) -> str:
    return f"https://doi.org/{doi}"


STANDARDS = {
    "TRIPOD+AI": {
        "full_name": "Transparent Reporting of a multivariable prediction model for "
                     "Individual Prognosis Or Diagnosis, AI extension",
        "category": "reporting",
        "citation": "Collins GS, Moons KGM, Dhiman P, et al. BMJ 2024;385:e078378.",
        "doi": "10.1136/bmj-2023-078378",
    },
    "PROBAST+AI": {
        "full_name": "Prediction model Risk Of Bias ASsessment Tool, AI extension",
        "category": "appraisal",
        "citation": "Moons KGM, Damen JAA, Kaul T, et al. BMJ 2025;388:e082505.",
        "doi": "10.1136/bmj-2024-082505",
    },
    "STARD-AI": {
        "full_name": "Standards for Reporting of Diagnostic accuracy studies, AI extension",
        "category": "reporting",
        "citation": "Sounderajah V, Ashrafian H, Aggarwal R, et al. Nat Med 2025.",
        "doi": "10.1038/s41591-025-03953-8",
    },
    "CONSORT-AI": {
        "full_name": "Consolidated Standards Of Reporting Trials, AI extension",
        "category": "reporting",
        "citation": "Liu X, Cruz Rivera S, Moher D, et al. Nat Med 2020;26:1364-1374.",
        "doi": "10.1038/s41591-020-1034-x",
    },
    "SPIRIT-AI": {
        "full_name": "Standard Protocol Items: Recommendations for Interventional Trials, "
                     "AI extension",
        "category": "reporting",
        "citation": "Cruz Rivera S, Liu X, Chan AW, et al. Nat Med 2020;26:1351-1363.",
        "doi": "10.1038/s41591-020-1037-7",
    },
    "DECIDE-AI": {
        "full_name": "Reporting guideline for the early-stage clinical evaluation of "
                     "decision support systems driven by artificial intelligence",
        "category": "reporting",
        "citation": "Vasey B, Nagendran M, Campbell B, et al. Nat Med 2022;28:924-933.",
        "doi": "10.1038/s41591-022-01772-9",
    },
    "MI-CLAIM": {
        "full_name": "Minimum Information about Clinical Artificial Intelligence Modeling",
        "category": "min_info",
        "citation": "Norgeot B, Quer G, Beaulieu-Jones BK, et al. Nat Med 2020;26:1320-1324.",
        "doi": "10.1038/s41591-020-1041-y",
    },
    "MINIMAR": {
        "full_name": "MINimum Information for Medical AI Reporting",
        "category": "min_info",
        "citation": "Hernandez-Boussard T, Bozkurt S, Ioannidis JPA, Shah NH. "
                    "J Am Med Inform Assoc 2020;27(12):2011-2015.",
        "doi": "10.1093/jamia/ocaa088",
    },
    "MI-CLAIM-GEN": {
        "full_name": "Minimum Information about Clinical Artificial Intelligence Modeling "
                     "for Generative models",
        "category": "min_info",
        "citation": "Miao BY, Chen IY, Williams CYK, et al. Nat Med 2025.",
        "doi": "10.1038/s41591-024-03470-0",
    },
    "TRIPOD-LLM": {
        "full_name": "TRIPOD reporting guideline for studies using large language models "
                     "in health care",
        "category": "reporting",
        "citation": "Gallifant J, Afshar M, Ameen S, et al. Nat Med 2025;31(1):60-69.",
        "doi": "10.1038/s41591-024-03425-5",
    },
    "CLAIM": {
        "full_name": "Checklist for Artificial Intelligence in Medical Imaging (2024 update)",
        "category": "reporting",
        "citation": "Tejani AS, Klontzas ME, Gatti AA, et al. Radiol Artif Intell 2024.",
        "doi": "10.1148/ryai.240300",
    },
    "CHART": {
        "full_name": "Chatbot Assessment Reporting Tool",
        "category": "reporting",
        "citation": "CHART Collaborative. BMC Med 2025.",
        "doi": "10.1186/s12916-025-04274-w",
    },
    "CHEERS-AI": {
        "full_name": "Consolidated Health Economic Evaluation Reporting Standards for "
                     "Interventions That Use Artificial Intelligence",
        "category": "reporting",
        "citation": "Elvidge J, Hawksworth C, Avsar TS, et al. Value Health 2024.",
        "doi": "10.1016/j.jval.2024.05.006",
    },
    "FUTURE-AI": {
        "full_name": "International consensus guideline for trustworthy and deployable "
                     "artificial intelligence in healthcare",
        "category": "governance",
        "citation": "Lekadir K, Frangi AF, Porras AR, et al. BMJ 2025;388:e081554.",
        "doi": "10.1136/bmj-2024-081554",
    },
    "STANDING Together": {
        "full_name": "Consensus recommendations to tackle algorithmic bias and promote "
                     "transparency in health datasets",
        "category": "governance",
        "citation": "Alderman JE, Palmer J, Laws E, et al. Lancet Digit Health "
                    "2025;7(1):e64-e88.",
        "doi": "10.1016/S2589-7500(24)00224-3",
    },
    "APPRAISE-AI": {
        "full_name": "Tool for quantitative evaluation of AI studies for clinical "
                     "decision support",
        "category": "appraisal",
        "citation": "Kwong JCC, Khondker A, Lajkosz K, et al. JAMA Netw Open "
                    "2023;6(9):e2335377.",
        "doi": "10.1001/jamanetworkopen.2023.35377",
    },
    "DEAL": {
        "full_name": "Development, Evaluation, and Assessment of Large language models "
                     "checklist",
        "category": "appraisal",
        "citation": "Tripathi S, Sukumaran R, Cook TS, et al. NEJM AI 2025;2(6):AIp2401106.",
        "doi": "10.1056/AIp2401106",
    },
    "SALIENT": {
        "full_name": "Five-stage framework for the real-world translation of AI-based "
                     "clinical decision support systems",
        "category": "governance",
        "citation": "van der Vegt AH, Scott IA, Dermawan K, et al. J Am Med Inform Assoc "
                    "2023;30(7):1349-1361.",
        "doi": "10.1093/jamia/ocad075",
    },
    "GAMER": {
        "full_name": "Reporting guideline for the use of Generative AI tools in "
                     "MEdical Research",
        "category": "reporting",
        "citation": "Luo X, Tham YC, Giuffre M, et al. BMJ Evid Based Med 2025.",
        "doi": "10.1136/bmjebm-2025-113825",
    },
}

# Attach the resolved URL to each entry.
for _k, _v in STANDARDS.items():
    _v["url"] = _u(_v["doi"])


# ---------------------------------------------------------------------------
# 2. Routing table
# ---------------------------------------------------------------------------
# Cross-cutting standards apply to every route (three slots: a trustworthiness
# framework, a dataset-diversity standard, and a minimum-information floor that
# cites both MI-CLAIM and MINIMAR).
CROSS_CUTTING = ["FUTURE-AI", "STANDING Together", "MI-CLAIM", "MINIMAR"]

# Each study-type route returns a primary reporting guideline and, where one
# exists, an appraisal companion. "label" is what the user sees in the app.
ROUTES = {
    "prediction_model": {
        "label": "Clinical prediction or prognostic model",
        "primary": ["TRIPOD+AI"],
        "appraisal": ["PROBAST+AI"],
    },
    "diagnostic_accuracy": {
        "label": "Diagnostic accuracy study",
        "primary": ["STARD-AI"],
        "appraisal": ["PROBAST+AI"],
    },
    "imaging": {
        "label": "Medical imaging AI study",
        "primary": ["CLAIM"],
        "appraisal": ["PROBAST+AI"],
    },
    "interventional_trial": {
        "label": "Interventional clinical trial of an AI intervention (conducted)",
        "primary": ["CONSORT-AI"],
        "appraisal": [],
    },
    "early_clinical_eval": {
        "label": "Early-stage live clinical evaluation of a decision-support system",
        "primary": ["DECIDE-AI"],
        "appraisal": ["APPRAISE-AI"],
    },
    "chatbot": {
        "label": "Health-advice chatbot or conversational agent",
        "primary": ["CHART"],
        "appraisal": [],
    },
    "economic": {
        "label": "Economic evaluation of an AI intervention",
        "primary": ["CHEERS-AI"],
        "appraisal": [],
    },
    "implementation": {
        "label": "Implementation or real-world deployment study",
        "primary": ["SALIENT"],
        "appraisal": ["APPRAISE-AI"],
        # Honest note surfaced in the app: no dedicated reporting checklist exists
        # for implementation; SALIENT is a translation framework, not a checklist.
        "note": "No dedicated reporting checklist exists for implementation studies. "
                "SALIENT is a real-world translation framework and is returned as the "
                "nearest-fit instrument; report against it and state what it does not cover.",
    },
    "llm_generative": {
        "label": "Large language model or generative model study",
        "primary": ["TRIPOD-LLM"],
        "appraisal": ["DEAL"],
    },
    "foundation_model": {
        "label": "Multimodal foundation model (many tasks, not one bounded task)",
        "primary": ["TRIPOD-LLM", "MI-CLAIM-GEN"],
        "appraisal": ["DEAL"],
        "open_node": True,
        "note": "OPEN NODE. No dedicated standard exists for multimodal foundation "
                "models. The nearest-fit standards are returned; you must document "
                "explicitly what they do not cover, in particular emergent multi-task "
                "behaviour, clinical factuality and hallucination, and failure analysis. "
                "See Supplementary Table S4 for a provisional scaffold.",
    },
}

# The trial-protocol gate (question 1) is handled separately from the study-type
# routes because a protocol is pre-conduct and routes to SPIRIT-AI regardless of
# the eventual design.
PROTOCOL_PRIMARY = ["SPIRIT-AI"]

# The generative-in-research gate (question 3) adds the reporting guideline for
# generative AI used in the research process itself.
GENAI_IN_RESEARCH = ["GAMER"]
