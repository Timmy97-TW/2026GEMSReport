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
import time

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


def stamp_index(stamp):
    """Version the script URLs so readers do not get a stale app or stale data.

    GitHub Pages caches assets for several minutes, so without this a returning
    reader can run yesterday's app.js against today's data. The stamp also goes
    into window.BUILD, which app.js appends when it lazy-loads teams-full.js.
    """
    path = os.path.join(ROOT, "index.html")
    with open(path, encoding="utf-8") as f:
        html = f.read()
    new = re.sub(r'(<script src="(?:data/)?[A-Za-z0-9_.-]+\.js)(?:\?v=[^"]*)?(">)',
                 r"\1?v=" + stamp + r"\2", html)
    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
    return len(re.findall(r"\?v=" + re.escape(stamp), new))


def write_js(name, var, obj, append=False):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "a" if append else "w", encoding="utf-8") as f:
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


def md_escape(s):
    return re.sub(r"\n{3,}", "\n\n", str(s or "").strip())


def write_text_mirror(results, teams, trends, report):
    """A plain-Markdown mirror of the whole report, plus llms.txt.

    This exists because of one of the report's own findings: three of the four
    2026 Best Wiki winners ship text that is in the HTML before any JavaScript
    runs, and the fourth (TU Delft) compensates with exactly this — an llms.txt
    index and a Markdown mirror of every page. This site is a client-rendered
    app, so without a mirror its words are invisible to anything that does not
    execute JavaScript. Practising what the analysis preaches.
    """
    def lang(o, k, l):
        return (o.get(k + "_zh") if l == "zh" else None) or o.get(k) or ""

    for l, name in (("en", "report-en.md"), ("zh", "report-zh.md")):
        out = []
        H = (lambda e, z: z if l == "zh" else e)
        out.append("# " + H("GEMS Research · iGEM 2026 Report", "GEMS Research · iGEM 2026 報告"))
        out.append("\n" + H(
            "A review of the iGEM 2026 Top 10 teams across all three sections, every special prize winner "
            "and nominee, and the academic and industry currents around them. Live site: "
            "https://timmy97-tw.github.io/2026GEMSReport/",
            "本報告檢視 iGEM 2026 三個組別的 Top 10 團隊、所有特別獎得主與入圍隊伍，以及其背後的學術與產業趨勢。"
            "網站：https://timmy97-tw.github.io/2026GEMSReport/"))

        out.append("\n## " + H("Results", "成績"))
        for sec, g in (results.get("grandPrize") or {}).items():
            ru = "; ".join("%s %s" % (r["rank"], r["team"]) for r in g.get("runnersUp", []))
            out.append("- **%s** — %s (%s, %s)%s" % (sec, g["winner"], g["village"], g["country"],
                                                     (" · " + ru) if ru else ""))
        for sec, names in (results.get("top10") or {}).items():
            out.append("- **Top 10 %s** — %s" % (sec, ", ".join(names)))

        for b in report.get("sections") or []:
            out.append("\n## " + md_escape(lang(b, "title", l)))
            if b.get("lede"):
                out.append("\n_" + md_escape(lang(b, "lede", l)) + "_")
            if b.get("body"):
                out.append("\n" + md_escape(lang(b, "body", l)))
            for c in b.get("cards") or []:
                out.append("\n### " + md_escape(lang(c, "title", l)))
                out.append(md_escape(lang(c, "body", l)))
            for key, head in (("checklist", H("Checklist", "檢查清單")),
                              ("antipatterns", H("Effort that did not pay off", "投入了卻沒有回報的事"))):
                items = (b.get(key + "_zh") if l == "zh" else None) or b.get(key) or []
                if items:
                    out.append("\n**%s**\n" % head)
                    out += ["- " + md_escape(x) for x in items]
            if b.get("method"):
                out.append("\n_" + H("Method and limits.", "方法與限制。") + " " +
                           md_escape(lang(b, "method", l)) + "_")

        for key, head in (("academic", H("Academic trends", "學術趨勢")),
                          ("industry", H("Industry trends", "產業趨勢"))):
            tl = (trends.get(key) or {}).get("trends") or []
            if not tl:
                continue
            out.append("\n## " + head)
            for t in tl:
                out.append("\n### " + md_escape(lang(t, "title", l)))
                out.append(md_escape(lang(t, "oneLine", l)))
                out.append("\n" + md_escape(lang(t, "body", l)))
                if t.get("gemsAction"):
                    out.append("\n**%s** %s" % (H("GEMS action.", "GEMS 行動。"),
                                                md_escape(lang(t, "gemsAction", l))))

        out.append("\n## " + H("Roadmap", "路線圖"))
        for i, p in enumerate(report.get("roadmap") or [], 1):
            out.append("\n### %d. %s (%s)" % (i, md_escape(lang(p, "title", l)), lang(p, "when", l)))
            if p.get("lede"):
                out.append(md_escape(lang(p, "lede", l)))
            items = (p.get("items_zh") if l == "zh" else None) or p.get("items") or []
            out += ["- " + md_escape(x) for x in items]
            if p.get("outcome"):
                out.append("\n_%s %s_" % (H("Done looks like:", "完成的樣子："), md_escape(lang(p, "outcome", l))))

        out.append("\n## " + H("Team files", "團隊檔案"))
        for t in sorted(teams, key=lambda x: (-(x.get("rank") or 0), x["team"])):
            out.append("\n### %s — %s" % (t["team"], md_escape(lang(t, "projectTitle", l))))
            out.append("%s · %s · %s" % (t.get("section", ""), t.get("country", ""), t.get("wiki", "")))
            out.append(md_escape(lang(t, "summary", l)))
            for grp, keys in (("dry", ("frameworks", "datascience", "dataviz", "software")),
                              ("good", ("ihp", "publicEngagement", "realWorld"))):
                for k in keys:
                    v = lang(t.get(grp) or {}, k, l)
                    if v:
                        out.append("\n**%s.** %s" % (k, md_escape(v)))
            if t.get("gemsTakeaway"):
                out.append("\n**%s** %s" % (H("For GEMS:", "給 GEMS："), md_escape(lang(t, "gemsTakeaway", l))))

        path = os.path.join(ROOT, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")
        print("  %-14s %6.1f KB" % (name, os.path.getsize(path) / 1024))

    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("""# GEMS Research · iGEM 2026 Report

> A review of the iGEM 2026 Top 10 teams across all three sections (Undergraduate, Overgraduate, High
> School), every special prize winner and nominee, and the academic and industry trends around them. Two
> questions run through it: how teams turn biology into computation, and how they turn science into
> something a community can use. Built for GEMS Research, a synthetic biology research institution in Taiwan.

The site itself is a client-rendered application. These Markdown mirrors carry the full text.

- [Full report, English](report-en.md): every written section, all %d team files, %d trends and the roadmap
- [Full report, Traditional Chinese](report-zh.md): the same, in 繁體中文
- [Official 2026 results](https://competition.igem.org/results/2026): the source for every award in this report

## Data

- [results.js](data/results.js): the complete official 2026 results as JSON
- [teams.js](data/teams.js): a light index of every team file
- [teams-full.js](data/teams-full.js): the full team records
- [trends.js](data/trends.js): academic and industry trend analysis
- [report.js](data/report.js): the written synthesis, the original analyses and the roadmap
""" % (len(teams), sum(len((trends.get(k) or {}).get("trends") or []) for k in ("academic", "industry"))))
    print("  %-14s %6.1f KB" % ("llms.txt", os.path.getsize(os.path.join(ROOT, "llms.txt")) / 1024))


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
    # `order` lets an analysis block sit above the written framing on its tab
    # (default 50). Python's sort is stable, so equal orders keep file order.
    report["sections"] = sorted((report.get("sections") or []) + insights,
                                key=lambda b: b.get("order", 50))

    # The full team records are large, and most of that weight is prose nobody
    # reads until they open a tab that needs it. Ship a light index up front and
    # lazy-load the rest on the first tab (or sheet) that actually uses it.
    INDEX_KEYS = ("id", "team", "section", "country", "village", "wiki", "rank", "awards",
                  "projectTitle", "projectTitle_zh", "tagline", "tagline_zh",
                  "summary", "summary_zh")
    index = []
    for t in teams:
        row = {k: t[k] for k in INDEX_KEYS if t.get(k)}
        if t.get("images"):
            row["images"] = t["images"][:1]
        index.append(row)
    full = {t["id"]: t for t in teams}

    stamp = time.strftime("%Y%m%d%H%M")
    print("building (v%s):" % stamp)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "results.js"), "w", encoding="utf-8") as f:
        f.write('window.BUILD = "%s";\n' % stamp)
    write_js("results.js", "RESULTS", results, append=True)
    write_js("teams.js", "TEAMS", index)
    write_js("teams-full.js", "TEAMS_FULL", full)
    write_js("trends.js", "TRENDS", trends)
    write_js("report.js", "REPORT", report)
    write_text_mirror(results, teams, trends, report)
    print("  index.html     %d script tags versioned" % stamp_index(stamp))

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
