"""Console menu shared by client.py (network) and main.py (stand-alone)."""
from analyser import format_report, to_csv


def ask(prompt, valid=None):
    while True:
        v = input(prompt).strip()
        if valid is None or v in valid:
            return v
        print("  Invalid input, try again.")


def rate_skills(skills_needed):
    ratings = {}
    print("\nRate yourself 0 (none) to 5 (expert) for each skill:")
    for s, (need, _) in skills_needed.items():
        ratings[s] = int(ask(f"  {s} (needed level {need}): ", {str(i) for i in range(6)}))
    return ratings


def run(api, title):
    print("=" * 66 + f"\n  STUDENT SKILL GAP ANALYSER  -  {title}\n" + "=" * 66)
    user = None
    while not user:
        c = ask("\n1.Register  2.Login  3.Exit > ", {"1", "2", "3"})
        if c == "3":
            return
        name, pw = input("Username: ").strip(), input("Password: ").strip()
        r = api.call("register" if c == "1" else "login", username=name, password=pw)
        print(" ", r.get("message") or "Error: " + r["error"])
        if c == "2" and r["ok"]:
            user = name
    ratings, last = {}, None
    while True:
        c = ask("\n1.Analyse skill gap  2.Best-fit roles  3.History  "
                "4.Export last report (CSV)  5.Logout > ", {"1", "2", "3", "4", "5"})
        if c == "1":
            roles = api.call("roles")["roles"]
            names = list(roles)
            for i, n in enumerate(names, 1):
                print(f"  {i}. {n}")
            role = names[int(ask("Choose target role: ", {str(i) for i in range(1, len(names) + 1)})) - 1]
            ratings.update(rate_skills(roles[role]))
            r = api.call("analyse", role=role, ratings=ratings)
            if r["ok"]:
                last = r["result"]
                print("\n" + format_report(last, user))
            else:
                print("Error:", r["error"])
        elif c == "2":
            if not ratings:
                print("  Run option 1 first so your skills are known."); continue
            print("\nBest-fit roles (based on the skills you have rated):")
            for x in api.call("rank", ratings=ratings)["ranking"]:
                print(f"  {x['role']:<24}{x['readiness']:>6} %   (skills covered: {x['coverage']}%)")
        elif c == "3":
            h = api.call("history")["history"]
            print("\n  No history yet." if not h else "\n  Date              Role                      Ready   Level")
            for x in h:
                print(f"  {x['time']}  {x['role']:<24}{x['readiness']:>6}%  {x['level']}")
        elif c == "4":
            print("  Run option 1 first." if not last else "  Saved: " + to_csv(last, user))
        else:
            print("Goodbye!"); return
