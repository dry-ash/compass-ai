"""
standards.py  (COMPASS-AI v2.0)

Single source of truth for the routing tool. Three things live here:

1. LIFECYCLE: the eight research-lifecycle stages.
2. STANDARDS: all 31 instruments of the corpus (manuscript Table 1), each with
   its function category, lifecycle-stage span, declared study-type scope,
   what the instrument is about (the AI under study, or AI used as a tool in
   the research process), citation and DOI. Stage spans and scopes are the
   coded values in Supplementary Table S1.
3. ROUTES: the ten study-type routes. Each route names its core instruments
   by role, an operational definition shown to users, a lifecycle window, and
   any related instruments. The foundation-model route does not name its
   instruments: they are computed from the registry by a fixed rule
   (router.nearest_fit), so that the open node returns the same set for every
   user; its reporting and appraisal members update automatically when a new
   instrument is added.

Changes from v1.0 are listed in CHANGELOG.md.
"""

def _u(doi: str) -> str:
    return f"https://doi.org/{doi}"


# ---------------------------------------------------------------------------
# 1. Lifecycle
# ---------------------------------------------------------------------------
LIFECYCLE = {
    "S1": "Problem definition and study design",
    "S2": "Data and dataset governance",
    "S3": "Model development and training",
    "S4": "Internal validation",
    "S5": "External and clinical validation",
    "S6": "Clinical trials",
    "S7": "Implementation and deployment",
    "S8": "Monitoring and governance",
}

def _stages(*spec):
    """_stages('S1-S4', 'S8') -> {'S1','S2','S3','S4','S8'}"""
    out = set()
    for s in spec:
        if "-" in s:
            a, b = (int(x[1:]) for x in s.split("-"))
            out.update(f"S{i}" for i in range(a, b + 1))
        else:
            out.add(s)
    return frozenset(out)


# ---------------------------------------------------------------------------
# 2. Standards registry (n = 31)
# ---------------------------------------------------------------------------
# category: reporting | appraisal | min_info | governance | other
# scope:    study-type keys (see ROUTES) or "general"
# task_specific: True for instruments limited to one task type (excluded from the open-node nearest fit)
# object:   "ai_under_study"  - the instrument governs reporting/appraisal of the AI being studied
#           "research_tool"   - the instrument governs AI used as a tool in the research process
STANDARDS = {
    "MINIMAR": dict(
        full_name="MINimum Information for Medical AI Reporting",
        category="min_info", stages=_stages("S1-S5"), scope={"general", "prediction_model"},
        object="ai_under_study",
        citation="Hernandez-Boussard T, Bozkurt S, Ioannidis JPA, Shah NH. J Am Med Inform Assoc 2020;27(12):2011-2015.",
        doi="10.1093/jamia/ocaa088"),
    "TRIPOD+AI": dict(
        full_name="Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis, AI extension",
        category="reporting", stages=_stages("S1-S5", "S7"), scope={"prediction_model"}, object="ai_under_study",
        citation="Collins GS, Moons KGM, Dhiman P, et al. BMJ 2024;385:e078378.", doi="10.1136/bmj-2023-078378"),
    "PROBAST+AI": dict(
        full_name="Prediction model Risk Of Bias ASsessment Tool, AI extension",
        category="appraisal", stages=_stages("S1-S5"), scope={"prediction_model"}, object="ai_under_study",
        citation="Moons KGM, Damen JAA, Kaul T, et al. BMJ 2025;388:e082505.", doi="10.1136/bmj-2024-082505"),
    "MI-CLAIM": dict(
        full_name="Minimum Information about Clinical Artificial Intelligence Modeling",
        category="min_info", stages=_stages("S1-S4"), scope={"prediction_model"}, object="ai_under_study",
        citation="Norgeot B, Quer G, Beaulieu-Jones BK, et al. Nat Med 2020;26:1320-1324.", doi="10.1038/s41591-020-1041-y"),
    "TRIPOD-LLM": dict(
        full_name="TRIPOD reporting guideline for studies using large language models in health care",
        category="reporting", stages=_stages("S1-S5", "S7-S8"), scope={"llm_generative"}, object="ai_under_study",
        citation="Gallifant J, Afshar M, Ameen S, et al. Nat Med 2025;31(1):60-69.", doi="10.1038/s41591-024-03425-5"),
    "CLAIM": dict(
        full_name="Checklist for Artificial Intelligence in Medical Imaging (2024 update)",
        category="reporting", stages=_stages("S1-S5"), scope={"imaging"}, object="ai_under_study",
        citation="Tejani AS, Klontzas ME, Gatti AA, et al. Radiol Artif Intell 2024;6(4):e240300.", doi="10.1148/ryai.240300"),
    "BIAS": dict(
        full_name="Transparent reporting of biomedical image analysis challenges",
        category="reporting", stages=_stages("S1-S4", "S7"), scope={"imaging"}, object="ai_under_study",
        citation="Maier-Hein L, Reinke A, Kozubek M, et al. Med Image Anal 2020;66:101796.", doi="10.1016/j.media.2020.101796"),
    "CAIR": dict(
        full_name="Clinical AI Research checklist",
        category="other", stages=_stages("S1-S4"), scope={"general"}, object="ai_under_study",
        citation="Olczak J, Pavlopoulos J, Prijs J, et al. Acta Orthop 2021;92(5):513-525.", doi="10.1080/17453674.2021.1918389"),
    "CREMLS": dict(
        full_name="Consolidated Reporting Guidelines for Prognostic and Diagnostic Machine Learning Models",
        category="reporting", stages=_stages("S1-S5"), scope={"prediction_model", "diagnostic_accuracy"}, object="ai_under_study",
        citation="El Emam K, Leung TI, Malin B, Klement W, Eysenbach G. J Med Internet Res 2024;26:e52508.", doi="10.2196/52508"),
    "APPRAISE-AI": dict(
        full_name="Tool for quantitative evaluation of AI studies for clinical decision support",
        category="appraisal", stages=_stages("S1-S5", "S7"), scope={"prediction_model", "early_clinical_eval"}, object="ai_under_study",
        citation="Kwong JCC, Khondker A, Lajkosz K, et al. JAMA Netw Open 2023;6(9):e2335377.", doi="10.1001/jamanetworkopen.2023.35377"),
    "STARD-AI": dict(
        full_name="Standards for Reporting of Diagnostic accuracy studies, AI extension",
        category="reporting", stages=_stages("S1-S5"), scope={"diagnostic_accuracy"}, object="ai_under_study",
        citation="Sounderajah V, Guni A, Liu X, et al. Nat Med 2025;31(10):3283-3289.", doi="10.1038/s41591-025-03953-8"),
    "SPIRIT-AI": dict(
        full_name="Standard Protocol Items: Recommendations for Interventional Trials, AI extension",
        category="reporting", stages=_stages("S1-S2", "S6-S7"), scope={"interventional_trial"}, object="ai_under_study",
        citation="Cruz Rivera S, Liu X, Chan AW, et al. Nat Med 2020;26:1351-1363.", doi="10.1038/s41591-020-1037-7"),
    "CONSORT-AI": dict(
        full_name="Consolidated Standards Of Reporting Trials, AI extension",
        category="reporting", stages=_stages("S1-S2", "S6-S7"), scope={"interventional_trial"}, object="ai_under_study",
        citation="Liu X, Cruz Rivera S, Moher D, et al. Nat Med 2020;26:1364-1374.", doi="10.1038/s41591-020-1034-x"),
    "CHEERS-AI": dict(
        full_name="Consolidated Health Economic Evaluation Reporting Standards for Interventions That Use Artificial Intelligence",
        category="reporting", stages=_stages("S1-S5", "S7-S8"), scope={"economic"}, object="ai_under_study",
        citation="Elvidge J, Hawksworth C, Avsar TS, et al. Value Health 2024;27(9):1196-1205.", doi="10.1016/j.jval.2024.05.006"),
    "DECIDE-AI": dict(
        full_name="Reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence",
        category="reporting", stages=_stages("S1-S2", "S6-S7"), scope={"early_clinical_eval", "implementation"}, object="ai_under_study",
        citation="Vasey B, Nagendran M, Campbell B, et al. Nat Med 2022;28:924-933.", doi="10.1038/s41591-022-01772-9"),
    "ELEVATE-GenAI": dict(
        full_name="Reporting guidelines for the use of large language models in health economics and outcomes research",
        category="reporting", stages=_stages("S2-S4", "S7-S8"), scope={"llm_generative", "economic"}, object="research_tool",
        citation="Fleurence RL, Dawoud D, Bian J, et al. Value Health 2025;28(11):1611-1625.", doi="10.1016/j.jval.2025.06.018"),
    "CLIX-M": dict(
        full_name="Clinician-informed XAI evaluation checklist with metrics",
        category="appraisal", stages=_stages("S1", "S3-S5", "S7"), scope={"early_clinical_eval"}, object="ai_under_study",
        citation="Brankovic A, Cook D, Rahman J, et al. npj Digit Med 2025;8(1):364.", doi="10.1038/s41746-025-01764-2"),
    "GAMER": dict(
        full_name="Reporting guideline for the use of Generative AI tools in MEdical Research",
        category="reporting", stages=_stages("S2-S3"), scope={"general", "llm_generative"}, object="research_tool",
        citation="Luo X, Tham YC, Giuffre M, et al. BMJ Evid Based Med 2025;30(6):390-400.", doi="10.1136/bmjebm-2025-113825"),
    "CHART": dict(
        full_name="Chatbot Assessment Reporting Tool",
        category="reporting", stages=_stages("S1-S4"), scope={"chatbot"}, object="ai_under_study",
        citation="Huo B, Collins G, Chartash D, et al. BMC Med 2025;23(1):447.", doi="10.1186/s12916-025-04274-w"),
    "Do No Harm": dict(
        full_name="Do No Harm safety checklist for launching AI-based medical technology",
        category="governance", stages=_stages("S1-S8"), scope={"general", "implementation"}, object="ai_under_study",
        citation="Khan WU, Seto E. J Med Internet Res 2023;25:e43386.", doi="10.2196/43386"),
    "FUTURE-AI": dict(
        full_name="International consensus guideline for trustworthy and deployable artificial intelligence in healthcare",
        category="governance", stages=_stages("S1-S5", "S7-S8"), scope={"general"}, object="ai_under_study",
        citation="Lekadir K, Frangi AF, Porras AR, et al. BMJ 2025;388:e081554.", doi="10.1136/bmj-2024-081554"),
    "SALIENT": dict(
        full_name="SALIENT end-to-end clinical AI implementation framework",
        category="governance", stages=_stages("S1-S8"), scope={"implementation"}, object="ai_under_study",
        citation="van der Vegt AH, Scott IA, Dermawan K, et al. J Am Med Inform Assoc 2023;30(9):1503-1515.", doi="10.1093/jamia/ocad088"),
    "TRUST-AI": dict(
        full_name="High-level guide to trustworthy AI for healthcare professionals",
        category="governance", stages=_stages("S1-S2", "S4-S5", "S7-S8"), scope={"general"}, object="ai_under_study",
        citation="Rothwell R, Julius A, Crichton R. J Perioper Pract 2026;36(1-2):6-11.", doi="10.1177/17504589251396483"),
    "HAIRA": dict(
        full_name="Healthcare AI Governance Readiness Assessment (maturity model)",
        category="governance", stages=_stages("S1-S5", "S7-S8"), scope={"general", "implementation"}, object="ai_under_study",
        citation="Hussein R, Zink A, Ramadan B, et al. npj Digit Med 2026;9(1):236.", doi="10.1038/s41746-026-02418-7"),
    "STANDING Together": dict(
        full_name="Consensus recommendations to tackle algorithmic bias and promote transparency in health datasets",
        category="min_info", stages=_stages("S1-S4", "S8"), scope={"general"}, object="ai_under_study",
        citation="Alderman JE, Palmer J, Laws E, et al. Lancet Digit Health 2025;7(1):e64-e88.", doi="10.1016/S2589-7500(24)00224-3"),
    "MI-CLAIM-GEN": dict(
        full_name="Minimum Information about Clinical Artificial Intelligence Modeling for Generative models",
        category="min_info", stages=_stages("S1-S4", "S8"), scope={"llm_generative", "foundation_model"}, object="ai_under_study",
        citation="Miao BY, Chen IY, Williams CYK, et al. Nat Med 2025;31(5):1394-1398.", doi="10.1038/s41591-024-03470-0"),
    "DEAL": dict(
        full_name="Development, Evaluation, and Assessment of Large language models checklist",
        category="appraisal", stages=_stages("S1-S5"), scope={"llm_generative", "foundation_model"}, object="ai_under_study",
        citation="Tripathi S, Alkhulaifat D, Doo FX, et al. NEJM AI 2025;2(6):AIp2401106.", doi="10.1056/AIp2401106"),
    "Stevens 2020": dict(
        full_name="Recommendations for reporting machine learning analyses in clinical research",
        category="reporting", stages=_stages("S1-S5"), scope={"general", "prediction_model"}, object="ai_under_study",
        citation="Stevens LM, Mortazavi BJ, Deo RC, Curtis L, Kao DP. Circ Cardiovasc Qual Outcomes 2020;13(10):e006556.",
        doi="10.1161/CIRCOUTCOMES.120.006556"),
    "MI-CLEAR-LLM": dict(
        full_name="Minimum reporting items for clear evaluation of accuracy reports of large language models in healthcare (2025 update)",
        category="min_info", stages=_stages("S2-S4"), scope={"llm_generative", "chatbot"}, object="ai_under_study",
        citation="Park SH, Suh CH, Lee JH, et al. Korean J Radiol 2025;26(12):1123-1132.", doi="10.3348/kjr.2025.1522"),
    "MEDAI-LLM-SUMM": dict(
        full_name="Reporting checklist for medical text summarization studies using large language models",
        category="reporting", stages=_stages("S1-S4", "S7-S8"), scope={"llm_generative"}, object="ai_under_study",
        task_specific=True,
        citation="Khoruzhaya AN, Varyukhina MD, Erizhokov RA, et al. Front Digit Health 2026;8:1761601.",
        doi="10.3389/fdgth.2026.1761601"),
    "Luo 2016": dict(
        full_name="Guidelines for developing and reporting machine learning predictive models in biomedical research",
        category="reporting", stages=_stages("S1-S5"), scope={"general", "prediction_model"}, object="ai_under_study",
        citation="Luo W, Phung D, Tran T, et al. J Med Internet Res 2016;18(12):e323.", doi="10.2196/jmir.5870"),
}
for _v in STANDARDS.values():
    _v["url"] = _u(_v["doi"])


# ---------------------------------------------------------------------------
# 3. Routes
# ---------------------------------------------------------------------------
# window: the lifecycle stages at which a study of this type generates its evidence
# (defined by the study type, independent of the stage spans of the instruments).
# Roles in a routed set (core = counted in reporting burden):
#   primary      reporting guideline(s) the report follows
#   framework    governance framework that structures the report (implementation only)
#   appraisal    risk-of-bias / quality-appraisal companion
#   conditional  added only when a stated combination of answers occurs
#   min_info     one minimum-information standard (cross-cutting slot, chosen by rule)
#   cross_cutting FUTURE-AI and STANDING Together (every study)
#   generative   GAMER, when generative AI was used in the research process (Gate 3)
# Not counted in burden:
#   related      instruments whose declared scope covers the route; consult as needed
#
# min_info_class selects the cross-cutting minimum-information standard:
#   "generative"  -> MI-CLAIM-GEN   (the AI under study is generative)
#   "development" -> MI-CLAIM       (the study builds or validates a model)
#   "application" -> MINIMAR        (the study applies an existing model in care or evaluation)
# With two study types, precedence is generative > development > application.

ROUTES = {
    "prediction_model": dict(
        label="Clinical prediction or prognostic model",
        definition="Develops, validates or updates a model that estimates an individual's risk of a current "
                   "(diagnostic) or future (prognostic) outcome from several predictors.",
        window=_stages("S3-S5"), primary=["TRIPOD+AI"], appraisal=["PROBAST+AI"],
        min_info_class="development", related=["CREMLS", "Luo 2016", "Stevens 2020", "APPRAISE-AI"]),
    "diagnostic_accuracy": dict(
        label="Diagnostic accuracy study",
        definition="Estimates how accurately an AI test, or readers with and without AI assistance, classify a "
                   "target condition against a reference standard. Multi-reader and crossover reading studies, "
                   "including simulated or retrospective reading sessions, belong here.",
        window=_stages("S3-S5"), primary=["STARD-AI"], appraisal=["PROBAST+AI"],
        min_info_class="development", related=["CREMLS"]),
    "imaging": dict(
        label="Medical imaging AI study",
        definition="Develops or evaluates an AI model whose input is medical images or video (radiology, "
                   "pathology, endoscopy, ophthalmology, echocardiography). Select it together with the type "
                   "that describes the evaluation, if one applies.",
        window=_stages("S3-S5"), primary=["CLAIM"], appraisal=["PROBAST+AI"],
        min_info_class="development", related=["BIAS"],
        related_note={"BIAS": "if the study is or reports a biomedical image analysis challenge"}),
    "interventional_trial": dict(
        label="Interventional clinical trial of an AI intervention (conducted)",
        definition="Assigns participants (patients or clinicians) to AI-supported versus comparator arms, by "
                   "randomisation or concurrent control, and compares outcomes. Studies in which the same readers "
                   "interpret cases with and without AI are diagnostic accuracy studies.",
        window=_stages("S6"), primary=["CONSORT-AI"], appraisal=[],
        min_info_class="application", related=["SPIRIT-AI"],
        related_note={"SPIRIT-AI": "cite if the trial protocol was registered or published"}),
    "early_clinical_eval": dict(
        label="Early-stage live clinical evaluation of a decision-support system",
        definition="First small-scale use of an AI decision-support system by clinicians in live care, reporting "
                   "clinical utility, safety and human factors before a comparative trial.",
        window=_stages("S6-S7"), primary=["DECIDE-AI"], appraisal=["APPRAISE-AI"],
        min_info_class="application", related=["CLIX-M"],
        related_note={"CLIX-M": "if explanations shown to clinicians are evaluated"}),
    "chatbot": dict(
        label="Health-advice chatbot or conversational agent",
        definition="Evaluates the answers or advice a conversational agent gives to patients, the public or "
                   "clinicians.",
        window=_stages("S3-S5"), primary=["CHART"], appraisal=[],
        min_info_class="generative", related=["MI-CLEAR-LLM"]),
    "economic": dict(
        label="Economic evaluation of an AI intervention",
        definition="Compares the costs and consequences of an AI intervention with an alternative (for example "
                   "cost-effectiveness or budget impact).",
        window=_stages("S6-S8"), primary=["CHEERS-AI"], appraisal=[],
        min_info_class="application", related=[]),
    "implementation": dict(
        label="Implementation or real-world deployment study",
        definition="Reports the deployment of an AI system in routine care at scale, including adoption, "
                   "workflow, outcomes after go-live, and monitoring.",
        window=_stages("S7-S8"), primary=["DECIDE-AI"], framework=["SALIENT"], appraisal=["APPRAISE-AI"],
        min_info_class="application", related=["Do No Harm", "HAIRA"],
        note="No dedicated reporting checklist for implementation studies was identified in the corpus. DECIDE-AI is returned as the "
             "nearest-fit checklist for human-factors and workflow items, and SALIENT as the translation framework "
             "that structures the report; state what neither covers."),
    "llm_generative": dict(
        label="Large language model or generative model study",
        definition="Develops, adapts or evaluates a large language model or other generative model performing a "
                   "defined task.",
        window=_stages("S3-S5"), primary=["TRIPOD-LLM"], appraisal=["DEAL"],
        min_info_class="generative", related=["MI-CLEAR-LLM", "MEDAI-LLM-SUMM"],
        related_note={"MEDAI-LLM-SUMM": "if the task is medical text summarisation"}),
    "foundation_model": dict(
        label="Multimodal foundation model (many tasks, not one bounded task)",
        definition="Develops or evaluates a model trained on broad data that performs many tasks across "
                   "modalities, rather than one bounded task.",
        window=_stages("S3-S5"), computed=True, min_info_class="generative", related=[],
        open_node=True,
        uncovered_domains=[
            "Emergent, open-ended multi-task behaviour (pre-specified task set; per-task performance; tasks attempted but not validated)",
            "Cross-modal grounding and consistency between modalities",
            "Clinical factuality and hallucination assessed per task and modality",
            "Failure-mode and safety analysis across tasks",
            "Post-deployment model and prompt drift",
        ],
        note="OPEN NODE. No dedicated standard for multimodal foundation models was identified in the corpus. The nearest-fit set is "
             "computed by a fixed rule (see Supplement); report the domains listed below "
             "explicitly. Add the imaging or other modality route as a secondary type when it applies."),
}

# Gate 1: a protocol is pre-conduct and routes to SPIRIT-AI regardless of design.
PROTOCOL_PRIMARY = ["SPIRIT-AI"]
PROTOCOL_MIN_INFO_CLASS = "application"

# Gate 3: generative AI used as a tool in the research process (writing, coding, analysis).
GENAI_IN_RESEARCH = ["GAMER"]

# Fixed cross-cutting standards (every study) plus one minimum-information slot.
CROSS_CUTTING = ["FUTURE-AI", "STANDING Together"]
MIN_INFO_BY_CLASS = {"generative": "MI-CLAIM-GEN", "development": "MI-CLAIM", "application": "MINIMAR"}
MIN_INFO_PRECEDENCE = ["generative", "development", "application"]

# Conditional core additions triggered by combinations of answers.
# ELEVATE-GenAI governs LLM use in health economics and outcomes research.
CONDITIONAL = [
    dict(standard="ELEVATE-GenAI",
         when=lambda types, genai: "economic" in types and genai,
         reason="economic evaluation in which generative AI was used in the research process"),
]

VERSION = "2.0.0"
