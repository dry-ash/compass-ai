"""
router.py

The routing algorithm as a pure function. No user interface, no printing,
no global state. Given the answers to the three gates, it returns the routed
standard set, deduplicated and grouped by the role each standard plays.

The three gates, exactly as in the manuscript:

  Gate 1  Is the work a protocol for an interventional AI trial not yet
          conducted?  If yes, route to SPIRIT-AI.
  Gate 2  What is the primary study type?  Return a primary reporting
          guideline and an appraisal companion where one exists. A study
          may span two design families (for example an LLM study that is
          also a trial), so an optional secondary type is allowed.
  Gate 3  Was generative AI used in the research process itself?  If yes,
          add the reporting guideline for that use (GAMER).

A small set of cross-cutting standards is always added.

Deduplication rule: a standard is listed once, under the most specific role
it plays in the routed set. Role precedence is
  primary  >  appraisal  >  generative  >  cross_cutting
so, for example, if a study's primary route already returns a standard, it is
not repeated in the cross-cutting block.
"""

from standards import (
    STANDARDS,
    ROUTES,
    CROSS_CUTTING,
    PROTOCOL_PRIMARY,
    GENAI_IN_RESEARCH,
)


class RoutingError(ValueError):
    """Raised when the inputs do not describe a routable study."""


def route(
    is_trial_protocol: bool = False,
    primary_type: str | None = None,
    secondary_type: str | None = None,
    genai_in_research: bool = False,
) -> dict:
    """Return the routed standard set for one study.

    Parameters
    ----------
    is_trial_protocol : bool
        Answer to Gate 1. True routes to SPIRIT-AI.
    primary_type : str or None
        A key of standards.ROUTES. Required unless is_trial_protocol is True.
    secondary_type : str or None
        An optional second key of standards.ROUTES for studies that span two
        design families. Must differ from primary_type.
    genai_in_research : bool
        Answer to Gate 3. True adds GAMER.

    Returns
    -------
    dict with keys:
        primary, appraisal, generative, cross_cutting : list[str]
            Standard ids, deduplicated across the whole result by role
            precedence.
        open_node : bool
            True if any selected route is the multimodal foundation-model node.
        notes : list[str]
            Any honest caveats attached to the selected routes.
        n_standards : int
            Count of distinct standards a team must consult.
    """
    if not is_trial_protocol and not primary_type:
        raise RoutingError(
            "Select a primary study type, or indicate that the work is a trial protocol."
        )
    for key in (primary_type, secondary_type):
        if key is not None and key not in ROUTES:
            raise RoutingError(f"Unknown study type: {key!r}")
    if secondary_type is not None and secondary_type == primary_type:
        raise RoutingError("Secondary study type must differ from the primary type.")

    primary: list[str] = []
    appraisal: list[str] = []
    generative: list[str] = []
    notes: list[str] = []
    open_node = False

    # Gate 1: trial protocol.
    if is_trial_protocol:
        primary.extend(PROTOCOL_PRIMARY)

    # Gate 2: primary (and optional secondary) study type.
    for key in (primary_type, secondary_type):
        if key is None:
            continue
        r = ROUTES[key]
        primary.extend(r.get("primary", []))
        appraisal.extend(r.get("appraisal", []))
        if r.get("open_node"):
            open_node = True
        if r.get("note"):
            notes.append(r["note"])

    # Gate 3: generative AI used in the research process.
    if genai_in_research:
        generative.extend(GENAI_IN_RESEARCH)

    # Cross-cutting standards always apply.
    cross_cutting = list(CROSS_CUTTING)

    # Deduplicate across the whole result by role precedence.
    seen: set[str] = set()

    def dedup(items):
        out = []
        for s in items:
            if s not in seen:
                seen.add(s)
                out.append(s)
        return out

    result = {
        "primary": dedup(primary),
        "appraisal": dedup(appraisal),
        "generative": dedup(generative),
        "cross_cutting": dedup(cross_cutting),
        "open_node": open_node,
        "notes": notes,
    }
    result["n_standards"] = sum(
        len(result[k]) for k in ("primary", "appraisal", "generative", "cross_cutting")
    )
    # Validate that every returned id is a known, verified standard.
    for k in ("primary", "appraisal", "generative", "cross_cutting"):
        for s in result[k]:
            if s not in STANDARDS:
                raise RoutingError(f"Routed an unknown standard: {s!r}")
    return result


def as_markdown(result: dict, title: str = "Reporting-standard routing result") -> str:
    """Render a routed result as a plain-Markdown compliance summary.

    Suitable for a download button or for pasting into a methods section.
    """
    roles = [
        ("primary", "Primary reporting guideline"),
        ("appraisal", "Appraisal companion"),
        ("generative", "Generative-AI standard (research process)"),
        ("cross_cutting", "Cross-cutting standard (applies to every study)"),
    ]
    lines = [f"# {title}", ""]
    if result["open_node"]:
        lines += [
            "> OPEN NODE: this study reaches a point where no dedicated standard "
            "exists. Nearest-fit standards are listed; document explicitly what "
            "they do not cover.",
            "",
        ]
    lines.append(f"**Standards to consult: {result['n_standards']}**")
    lines.append("")
    for key, heading in roles:
        ids = result[key]
        if not ids:
            continue
        lines.append(f"## {heading}")
        for s in ids:
            meta = STANDARDS[s]
            lines.append(f"- **{s}**: {meta['full_name']}. {meta['citation']} {meta['url']}")
        lines.append("")
    if result["notes"]:
        lines.append("## Notes")
        for n in result["notes"]:
            lines.append(f"- {n}")
        lines.append("")
    lines.append("---")
    lines.append(
        "Generated by the lifecycle-aware reporting-standard routing tool. "
        "This tool selects standards; it does not assess whether a study meets them."
    )
    return "\n".join(lines)
