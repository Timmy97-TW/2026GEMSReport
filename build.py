#!/usr/bin/env python3
"""Assemble data/*.js for the GEMS iGEM 2026 report from research/*.json.

    python3 build.py

Reads:
    research/results2026.json      official 2026 results, captured from competition.igem.org
    research/teams/<id>.json       one file per team, written by the research agents
    research/trends/academic.json  Nature-portfolio trend analysis
    research/trends/industry.json  SynBioBeta trend analysis
    research/report.json           the hand-written bilingual synthesis + roadmap

Writes data/results.js, data/teams.js, data/trends.js, data/report.js.
Nothing here runs in the browser; the site loads the generated files directly.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "research")
OUT = os.path.join(ROOT, "data")


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as e:
        print("  ! bad JSON in %s: %s" % (os.path.relpath(path, ROOT), e), file=sys.stderr)
        return default


def write_js(name, var, obj):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("window.%s = " % var)
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print("  %-14s %6.1f KB" % (name, os.path.getsize(path) / 1024))


# ---------------------------------------------------------------- awards index
def award_index(results):
    """team name -> list of human-readable 2026 award strings."""
    idx = {}

    def add(team, label):
        idx.setdefault(team, [])
        if label not in idx[team]:
            idx[team].append(label)

    gp = results.get("grandPrize", {})
    for sec, d in gp.items():
        add(d["winner"], "Grand Prize Winner (%s)" % sec)
        for r in d.get("runnersUp", []):
            add(r["team"], "%s (%s)" % (r["rank"], sec))
    for sec, names in results.get("top10", {}).items():
        for n in names:
            add(n, "Top 10 (%s)" % sec)
    for prize, secs in results.get("specialAwards", {}).items():
        for sec, d in secs.items():
            for n in d.get("winner", []):
                add(n, "%s — Winner (%s)" % (prize, sec))
            for n in d.get("nominees", []):
                add(n, "%s — Nominee (%s)" % (prize, sec))
    va = results.get("villageAwards", {})
    for prize, secs in va.get("collegiate", {}).items():
        for sec, d in secs.items():
            for n in d.get("winner", []):
                add(n, "%s — Winner" % prize)
            for n in d.get("nominees", []):
                add(n, "%s — Nominee" % prize)
    for village, d in va.get("highSchool", {}).items():
        for n in d.get("winner", []):
            add(n, "Best Village Project — Winner (%s)" % village)
        for n in d.get("nominees", []):
            add(n, "Best Village Project — Nominee (%s)" % village)
    return idx


def rank_of(awards):
    """Sort weight: the more decorated, the higher up the page."""
    s = 0
    for a in awards:
        al = a.lower()
        if "grand prize winner" in al:
            s += 120
        elif "runner-up" in al:
            s += 95
        elif "top 10" in al:
            s += 70
        elif "winner" in al:
            s += 26
        elif "nominee" in al:
            s += 7
    return s


SECTION_OF = {}


def section_for(name, results):
    if not SECTION_OF:
        for sec, names in results.get("top10", {}).items():
            for n in names:
                SECTION_OF[n] = sec
    return SECTION_OF.get(name)


# ---------------------------------------------------------------- teams
def build_teams(results):
    idx = award_index(results)
    teams, seen, problems = [], set(), []
    d = os.path.join(RES, "teams")
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if not fn.endswith(".json"):
            continue
        t = load(os.path.join(d, fn))
        if not t or not t.get("team"):
            problems.append("%s: unreadable or missing team name" % fn)
            continue
        tid = str(t.get("id") or os.path.splitext(fn)[0])
        if tid in seen:
            problems.append("%s: duplicate team id %s" % (fn, tid))
            continue
        seen.add(tid)
        t["id"] = tid

        # official awards always win over whatever the agent wrote
        official = idx.get(t["team"], [])
        if official:
            t["awards"] = official
        t["awards"] = t.get("awards") or []
        t["rank"] = rank_of(t["awards"])
        t["section"] = section_for(t["team"], results) or t.get("section") or ""

        # drop images that are obviously not content
        imgs = []
        for m in t.get("images") or []:
            u = (m or {}).get("url", "")
            if not u.startswith("https://static.igem.wiki/"):
                continue
            if re.search(r"(logo|favicon|icon|sponsor|banner-?top|header-?bg)", u, re.I):
                continue
            imgs.append(m)
        t["images"] = imgs
        if not imgs:
            problems.append("%s (%s): no usable images" % (t["team"], tid))

        for fkey, sub in (("dry", ("frameworks", "dataviz", "datascience", "software")),
                          ("good", ("publicEngagement", "ihp", "realWorld"))):
            t.setdefault(fkey, {})
            for k in sub:
                t[fkey].setdefault(k, "")
        teams.append(t)
    return teams, problems


def coverage(teams, results):
    """Which decorated teams do we still have no file for?"""
    have = {t["team"] for t in teams}
    want = set()
    for names in results.get("top10", {}).values():
        want |= set(names)
    for secs in results.get("specialAwards", {}).values():
        for d in secs.values():
            want |= set(d.get("winner", []))
    return sorted(want - have)


def main():
    results = load(os.path.join(RES, "results2026.json"))
    if not results:
        sys.exit("research/results2026.json is missing — nothing to build.")

    teams, problems = build_teams(results)
    trends = {
        "academic": load(os.path.join(RES, "trends", "academic.json"), {}) or {},
        "industry": load(os.path.join(RES, "trends", "industry.json"), {}) or {},
    }
    report = load(os.path.join(RES, "report.json"), {}) or {}

    # research/insights/*.json are standalone analysis blocks; they append to the
    # report's sections and render with the same machinery.
    idir = os.path.join(RES, "insights")
    insights = []
    for fn in sorted(os.listdir(idir)) if os.path.isdir(idir) else []:
        if not fn.endswith(".json"):
            continue
        blk = load(os.path.join(idir, fn))
        if not blk or not blk.get("title"):
            print("  ! skipping insights/%s" % fn, file=sys.stderr)
            continue
        blk.setdefault("tab", "overview")
        insights.append(blk)
    report["sections"] = (report.get("sections") or []) + insights

    print("building:")
    write_js("results.js", "RESULTS", results)
    write_js("teams.js", "TEAMS", teams)
    write_js("trends.js", "TRENDS", trends)
    write_js("report.js", "REPORT", report)

    zh = sum(1 for t in teams if t.get("summary_zh"))
    print("\n%d team files · %d translated to Chinese · %d academic trends · %d industry trends · %d insight blocks"
          % (len(teams), zh, len(trends["academic"].get("trends", [])),
             len(trends["industry"].get("trends", [])), len(insights)))
    missing = coverage(teams, results)
    if missing:
        print("\nstill missing a file (Top 10 or special-prize winner):")
        for m in missing:
            print("  -", m)
    if problems:
        print("\nwarnings:")
        for p in problems:
            print("  -", p)


if __name__ == "__main__":
    main()
