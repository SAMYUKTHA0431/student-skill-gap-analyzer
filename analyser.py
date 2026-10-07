"""Core skill-gap logic (no I/O, easy to test)."""
import csv
import os
from skills_db import ROLES, RESOURCES

WEEKS_PER_LEVEL = 2          # estimated study weeks to raise a skill by 1 level


def level_name(pct):
    if pct >= 85: return "Job Ready"
    if pct >= 65: return "Almost There"
    if pct >= 40: return "Developing"
    return "Beginner"


def analyse(role, ratings):
    """ratings: {skill: 0..5}. Returns a result dict for the chosen role."""
    if role not in ROLES:
        raise KeyError(f"Unknown role: {role}")
    rows, got, total = [], 0, 0
    for skill, (need, weight) in ROLES[role].items():
        have = max(0, min(5, int(ratings.get(skill, 0))))
        gap = max(0, need - have)
        got += min(have, need) * weight
        total += need * weight
        rows.append({"skill": skill, "required": need, "current": have,
                     "gap": gap, "weight": weight, "priority": gap * weight})
    readiness = round(100 * got / total, 1)
    rows.sort(key=lambda r: (-r["priority"], r["skill"]))
    plan = [{"skill": r["skill"], "gap": r["gap"], "weeks": r["gap"] * WEEKS_PER_LEVEL,
             "tip": RESOURCES.get(r["skill"], "Practise regularly.")}
            for r in rows if r["gap"] > 0]
    return {"role": role, "rows": rows, "readiness": readiness,
            "level": level_name(readiness), "plan": plan,
            "total_weeks": sum(p["weeks"] for p in plan)}


def rank_roles(ratings, min_coverage=0.5):
    """Rank roles using only the skills the student has rated."""
    out = []
    for role, req in ROLES.items():
        known = [s for s in req if s in ratings]
        coverage = len(known) / len(req)
        if coverage < min_coverage:
            continue
        got = sum(min(int(ratings[s]), req[s][0]) * req[s][1] for s in known)
        tot = sum(req[s][0] * req[s][1] for s in known)
        out.append({"role": role, "readiness": round(100 * got / tot, 1),
                    "coverage": round(coverage * 100)})
    return sorted(out, key=lambda r: -r["readiness"])


def bar(cur, need, width=16):
    filled = round(min(cur / need, 1) * width) if need else width
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def format_report(res, student=""):
    line = "=" * 66
    out = [line, f" SKILL GAP REPORT | Role: {res['role']} | Student: {student}", line,
           f" {'Skill':<20}{'Req':>4}{'Now':>5}{'Gap':>5}   Progress", "-" * 66]
    for r in res["rows"]:
        out.append(f" {r['skill']:<20}{r['required']:>4}{r['current']:>5}{r['gap']:>5}   "
                   f"{bar(r['current'], r['required'])}")
    out += ["-" * 66,
            f" Overall readiness : {res['readiness']} %  ({res['level']})"]
    if res["plan"]:
        out += [f" Estimated time to close gaps: {res['total_weeks']} weeks", "",
                " LEARNING PLAN (highest priority first)"]
        for i, p in enumerate(res["plan"], 1):
            out += [f"  {i}. {p['skill']} (gap {p['gap']}, ~{p['weeks']} wks)",
                    f"     -> {p['tip']}"]
    else:
        out.append(" No gaps found - you meet every requirement!")
    out.append(line)
    return "\n".join(out)


def to_csv(res, student, folder="reports"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{student}_{res['role'].replace('/', '-').replace(' ', '_')}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Skill", "Required", "Current", "Gap", "Priority"])
        for r in res["rows"]:
            w.writerow([r["skill"], r["required"], r["current"], r["gap"], r["priority"]])
        w.writerow([]); w.writerow(["Readiness %", res["readiness"], res["level"]])
    return path
