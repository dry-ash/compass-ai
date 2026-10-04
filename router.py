"""
router.py  (COMPASS-AI v2.0)

The routing algorithm as a pure function. No user interface, no global state.

Formal statement
----------------
Let R be the set of ten study-type routes, I the 31 instruments, and for each
instrument i: stages(i), scope(i), category(i), object(i). Inputs are

    p   Gate 1, protocol of an interventional AI trial not yet conducted (bool)
    T   Gate 2, one or two study types, T subset of R (empty only if p)
    g   Gate 3, generative AI used as a tool in the research process (bool)
    s   optional lifecycle stage of the work being reported, s in S1..S8

The routed set is

    Core(T,p,g) = Protocol(p) U Primary(T) U Framework(T) U Appraisal(T)
                  U Conditional(T,g) U {FUTURE-AI, STANDING Together}
                  U {MinInfo(T,p)} U Generative(g)
    Related(T,s) = Related(T) U { i : "general" in scope(i), s in stages(i),
                                       object(i) = AI under study }  minus Core

Lifecycle enters in two ways. (1) Each route r has a window W(r): the stages at
which a study of that type generates its evidence, so the study type the user selects already fixes
where in the lifecycle the work sits: moving a project from development (S3-S5)
to a trial (S6) or deployment (S7-S8) changes the route and therefore Core.
(2) When s is given, general-scope instruments covering s are added to
Related, and the router reports whether s lies in W(r) for the chosen types.

The foundation-model route names no instruments. Its nearest-fit set is
computed by nearest_fit(): the reporting, minimum-information and appraisal
instruments that are about the AI under study, whose declared scope includes
large language / generative or foundation models, whose stage span
overlaps the route window, and that are not limited to a single task.
With a fixed study type, the stage input s changes Related and the window
check but not Core. In protocol mode T is empty.

Deduplication: an instrument is listed once, under its highest-precedence
role: primary > framework > appraisal > conditional > min_info >
cross_cutting > generative > related.
"""

from standards import (
    STANDARDS, ROUTES, LIFECYCLE, CROSS_CUTTING, PROTOCOL_PRIMARY, PROTOCOL_MIN_INFO_CLASS,
    GENAI_IN_RESEARCH, MIN_INFO_BY_CLASS, MIN_INFO_PRECEDENCE, CONDITIONAL, VERSION,
)

ROLE_ORDER = ["primary", "framework", "appraisal", "conditional", "min_info",
              "cross_cutting", "generative", "related"]
CORE_ROLES = ROLE_ORDER[:-1]


class RoutingError(ValueError):
    """Raised when the inputs do not describe a routable study."""


def nearest_fit(route_key="foundation_model"):
    """Deterministic nearest-fit rule for the open node.

    Returns {"primary": [...], "appraisal": [...]} computed from the registry:
    instruments with object == ai_under_study, category in {reporting, min_info,
    appraisal}, scope intersecting {llm_generative, foundation_model}, and stage
    span overlapping the route window, excluding instruments limited to a single
    task (a single-task checklist cannot be the nearest fit for a multi-task
    model). Minimum-information instruments are
    handled by the cross-cutting slot, so they are not repeated here.
    """
    window = ROUTES[route_key]["window"]
    hit = sorted(
        k for k, m in STANDARDS.items()
        if m["object"] == "ai_under_study"
        and m["category"] in {"reporting", "min_info", "appraisal"}
        and m["scope"] & {"llm_generative", "foundation_model"}
        and m["stages"] & window
        and not m.get("task_specific", False)
    )
    return {
        "primary": [k for k in hit if STANDARDS[k]["category"] == "reporting"],
        "appraisal": [k for k in hit if STANDARDS[k]["category"] == "appraisal"],
        "min_info_candidates": [k for k in hit if STANDARDS[k]["category"] == "min_info"],
    }


def _route_parts(key):
    r = ROUTES[key]
    if r.get("computed"):
        nf = nearest_fit(key)
        return nf["primary"], [], nf["appraisal"]
    return list(r.get("primary", [])), list(r.get("framework", [])), list(r.get("appraisal", []))


def route(is_trial_protocol=False, primary_type=None, secondary_type=None,
          genai_in_research=False, stage=None):
    """Return the routed standard set for one study (see module docstring)."""
    if not is_trial_protocol and not primary_type:
        raise RoutingError("Select a primary study type, or indicate that the work is a trial protocol.")
    for key in (primary_type, secondary_type):
        if key is not None and key not in ROUTES:
            raise RoutingError(f"Unknown study type: {key!r}")
    if secondary_type is not None and secondary_type == primary_type:
        raise RoutingError("Secondary study type must differ from the primary type.")
    if stage is not None and stage not in LIFECYCLE:
        raise RoutingError(f"Unknown lifecycle stage: {stage!r}")

    types = [] if is_trial_protocol else [t for t in (primary_type, secondary_type) if t]
    roles = {k: [] for k in ROLE_ORDER}
    notes, related_notes, uncovered = [], {}, []
    open_node = False

    if is_trial_protocol:
        roles["primary"].extend(PROTOCOL_PRIMARY)
    for key in types:
        p, f, a = _route_parts(key)
        roles["primary"] += p
        roles["framework"] += f
        roles["appraisal"] += a
        r = ROUTES[key]
        roles["related"] += r.get("related", [])
        related_notes.update(r.get("related_note", {}))
        if r.get("open_node"):
            open_node = True
            uncovered += r.get("uncovered_domains", [])
        if r.get("note"):
            notes.append(r["note"])

    for c in CONDITIONAL:
        if c["when"](set(types), genai_in_research):
            roles["conditional"].append(c["standard"])
            notes.append(f"{c['standard']} added: {c['reason']}.")

    classes = {ROUTES[t]["min_info_class"] for t in types} or {PROTOCOL_MIN_INFO_CLASS}
    chosen_class = next(c for c in MIN_INFO_PRECEDENCE if c in classes)
    roles["min_info"].append(MIN_INFO_BY_CLASS[chosen_class])
    roles["cross_cutting"] += CROSS_CUTTING
    if genai_in_research:
        roles["generative"] += GENAI_IN_RESEARCH

    stage_check = None
    if stage is not None:
        roles["related"] += sorted(k for k, m in STANDARDS.items()
                                   if "general" in m["scope"] and stage in m["stages"]
                                   and m["object"] == "ai_under_study")
        windows = {t: sorted(ROUTES[t]["window"]) for t in types}
        in_window = any(stage in ROUTES[t]["window"] for t in types) if types else stage in {"S1", "S6"}
        suggest = sorted(k for k, r in ROUTES.items() if stage in r["window"])
        stage_check = dict(stage=stage, in_window=in_window, windows=windows,
                           routes_covering_stage=suggest)

    seen, result = set(), {}
    for k in ROLE_ORDER:
        out = []
        for s in roles[k]:
            if s not in seen:
                seen.add(s)
                out.append(s)
        result[k] = out
    for k in ROLE_ORDER:
        for s in result[k]:
            if s not in STANDARDS:
                raise RoutingError(f"Routed an unknown standard: {s!r}")

    result.update(
        open_node=open_node,
        uncovered_domains=uncovered,
        notes=notes,
        related_notes={k: v for k, v in related_notes.items() if k in result["related"]},
        stage_check=stage_check,
        n_core=sum(len(result[k]) for k in CORE_ROLES),
        n_related=len(result["related"]),
        version=VERSION,
    )
    result["n_standards"] = result["n_core"]  # v1.0 name kept for compatibility
    return result


def core_set(result):
    return {s for k in CORE_ROLES for s in result[k]}


ROLE_HEADINGS = {
    "primary": "Primary reporting guideline",
    "framework": "Translation framework",
    "appraisal": "Appraisal companion",
    "conditional": "Conditional addition",
    "min_info": "Minimum-information standard (cross-cutting)",
    "cross_cutting": "Cross-cutting standard (every study)",
    "generative": "Generative AI used in the research process",
    "related": "Related instruments (consult as needed; not counted)",
}


def as_markdown(result, title="Reporting-standard routing result"):
    lines = [f"# {title}", "", f"COMPASS-AI v{result['version']}", ""]
    if result["open_node"]:
        lines += ["> OPEN NODE: no dedicated standard was identified in the corpus. The nearest-fit set below is computed by a fixed "
                  "rule; report the domains listed below explicitly.", ""]
    lines += [f"**Core standards to consult: {result['n_core']}**", ""]
    for k in ROLE_ORDER:
        if not result[k]:
            continue
        lines.append(f"## {ROLE_HEADINGS[k]}")
        for s in result[k]:
            m = STANDARDS[s]
            extra = f" ({result['related_notes'][s]})" if s in result.get("related_notes", {}) else ""
            stages = ", ".join(sorted(m["stages"]))
            lines.append(f"- **{s}**{extra}: {m['full_name']}. Stages {stages}. {m['citation']} {m['url']}")
        lines.append("")
    if result["uncovered_domains"]:
        lines.append("## Domains the nearest-fit standards do not address specifically (report explicitly)")
        lines += [f"- {d}" for d in result["uncovered_domains"]] + [""]
    if result["stage_check"]:
        sc = result["stage_check"]
        lines.append("## Lifecycle check")
        lines.append(f"- Stage reported: {sc['stage']} ({LIFECYCLE[sc['stage']]}); inside the window of the "
                     f"selected study type: {'yes' if sc['in_window'] else 'no'}.")
        if not sc["in_window"]:
            lines.append(f"- Study types whose window covers {sc['stage']}: {', '.join(sc['routes_covering_stage'])}.")
        lines.append("")
    if result["notes"]:
        lines.append("## Notes")
        lines += [f"- {n}" for n in result["notes"]] + [""]
    lines += ["---", "This tool selects standards; it does not assess whether a study meets them."]
    return "\n".join(lines)
