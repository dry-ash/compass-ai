"""
analysis.py  (COMPASS-AI v2.0)

Reproduces the corpus analyses reported in the manuscript from the registry:
  coverage()      instruments per lifecycle stage, by function category (Table S2)
  burden()        core and related instruments per route (Table S3)
  co_occurrence() which instruments appear in how many routes (Figure S1)
Run:  python analysis.py
"""
from collections import Counter
from standards import STANDARDS, ROUTES, LIFECYCLE
from router import route, core_set

CATS = ["reporting", "appraisal", "governance", "min_info", "other"]


def coverage():
    rows = []
    for s in LIFECYCLE:
        c = Counter(m["category"] for m in STANDARDS.values() if s in m["stages"])
        rows.append({"stage": s, **{k: c.get(k, 0) for k in CATS}, "total": sum(c.values())})
    return rows


def burden(genai=False):
    rows = []
    for k in ROUTES:
        r = route(primary_type=k, genai_in_research=genai)
        rows.append({"route": k, "core": r["n_core"], "related": r["n_related"],
                     "core_set": sorted(core_set(r)), "related_set": r["related"]})
    return rows


def co_occurrence():
    c = Counter()
    for k in ROUTES:
        c.update(core_set(route(primary_type=k)))
    return dict(sorted(c.items(), key=lambda x: (-x[1], x[0])))


if __name__ == "__main__":
    print("Coverage by stage (RG, RoB, GOV, MI, OTH, total)")
    for r in coverage():
        print(r)
    tot = Counter(m["category"] for m in STANDARDS.values())
    print("Corpus totals:", dict(tot), "n =", len(STANDARDS))
    print("\nBurden per route (no generative AI in research process)")
    b = burden()
    for r in b:
        print(f"{r['route']:22s} core={r['core']} related={r['related']}")
    cores = [r["core"] for r in b]
    print(f"range {min(cores)}-{max(cores)}, mean {sum(cores)/len(cores):.1f}")
    print("\nCore co-occurrence across the ten routes:", co_occurrence())
