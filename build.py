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
import glob
import io
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


PRIZE_ZH = {
    "iGEM Spirit Award": "iGEM 精神獎",
    "Best New Basic Part": "最佳新基礎元件",
    "Best New Composite Part": "最佳新複合元件",
    "Best New Improved Part": "最佳改良元件",
    "Best Part Collection": "最佳元件集",
    "Best Alternative Platform": "最佳替代平台",
    "Best Measurement": "最佳量測",
    "Best Model": "最佳模型",
    "Best Software": "最佳軟體",
    "Best Hardware": "最佳硬體",
    "Best Education": "最佳教育",
    "Best Project Promotion Video": "最佳專案宣傳影片",
    "Best Presentation": "最佳簡報",
    "Best Wiki": "最佳 Wiki",
    "Best Integrated Human Practices": "最佳整合式人類實踐",
    "Inclusivity Award": "包容性獎",
    "Safety and Security Award": "安全與保安獎",
    "Best Sustainable Development Impact": "最佳永續發展影響",
    "Best Entrepreneurship": "最佳創業",
    "iGEMers Prize": "iGEMers 票選獎",
    "Best Village Project": "最佳 Village 專案",
}
SECTION_ZH = {"Undergrad": "大學組", "Overgrad": "研究生組", "High School": "高中組",
              "Undergrad & Overgrad": "大學暨研究生組"}
VILLAGE_ZH = {
    "Conservation": "保育", "Bioremediation": "生物復育", "Agriculture": "農業",
    "Food & Nutrition": "食品與營養", "Fashion & Cosmetics": "時尚與美妝",
    "Diagnostics": "診斷", "Infectious Diseases": "傳染病", "Oncology": "腫瘤",
    "Therapeutics": "治療", "Foundational Advance": "基礎推進",
    "Software & AI": "軟體與 AI", "Biomanufacturing": "生物製造", "Space": "太空",
    "Art & Design": "藝術與設計", "Climate Crisis": "氣候危機",
}


def award_zh(label):
    """Translate one generated award string, e.g. 'Best Model - Winner (Overgrad)'."""
    s = label
    m = re.match(r"^Grand Prize Winner \((.+)\)$", s)
    if m:
        return "總冠軍（%s）" % SECTION_ZH.get(m.group(1), m.group(1))
    m = re.match(r"^(1st|2nd) Runner-up \((.+)\)$", s)
    if m:
        return "%s（%s）" % ("亞軍" if m.group(1) == "1st" else "季軍",
                              SECTION_ZH.get(m.group(2), m.group(2)))
    m = re.match(r"^Top 10 \((.+)\)$", s)
    if m:
        return "Top 10（%s）" % SECTION_ZH.get(m.group(1), m.group(1))
    m = re.match(r"^Best Village Project — (Winner|Nominee) \((.+)\)$", s)
    if m:
        village = m.group(2)
        for en, zh in VILLAGE_ZH.items():
            village = village.replace(en, zh)
        return "最佳 Village 專案 — %s（%s）" % ("得主" if m.group(1) == "Winner" else "入圍", village)
    m = re.match(r"^(.+?) — (Winner|Nominee)(?: \((.+)\))?$", s)
    if m:
        prize, kind, sec = m.group(1), m.group(2), m.group(3)
        zh_prize = PRIZE_ZH.get(prize)
        if zh_prize is None:
            mm = re.match(r"^Best (.+) Project$", prize)
            if mm:
                zh_prize = "最佳%s專案" % VILLAGE_ZH.get(mm.group(1), mm.group(1))
            else:
                zh_prize = prize
        out = "%s — %s" % (zh_prize, "得主" if kind == "Winner" else "入圍")
        if sec:
            out += "（%s）" % SECTION_ZH.get(sec, sec)
        return out
    return s


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
        t["awards_zh"] = [award_zh(a) for a in t["awards"]]
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


ZH_TOP = ("projectTitle", "tagline", "summary", "gemsTakeaway")
ZH_DRY = ("frameworks", "dataviz", "datascience", "software")
ZH_GOOD = ("publicEngagement", "ihp", "realWorld")


def zh_audit(teams):
    """Per-file translation state.

    Worth doing properly: translation agents share a scratchpad, and a helper
    script clobbered by a sibling can no-op a file without raising, so an
    agent's own "translated N files" is not evidence. This counts the keys.
    """
    full, partial, none = [], [], []
    for t in teams:
        need = done = 0
        missing = []

        def chk(obj, keys, prefix=""):
            nonlocal need, done
            for k in keys:
                v = (obj or {}).get(k)
                if isinstance(v, str) and v.strip():
                    need += 1
                    if (obj or {}).get(k + "_zh"):
                        done += 1
                    else:
                        missing.append(prefix + k)

        chk(t, ZH_TOP)
        chk(t.get("dry"), ZH_DRY, "dry.")
        chk(t.get("good"), ZH_GOOD, "good.")
        for i, m in enumerate(t.get("images") or []):
            if (m.get("caption") or "").strip():
                need += 1
                if m.get("caption_zh"):
                    done += 1
                else:
                    missing.append("img%d.caption" % i)
        row = (t["id"], t["team"], done, need, missing)
        (full if done == need else partial if done else none).append(row)
    return full, partial, none


# ---------------------------------------------------------------- char audit
# Three failure modes actually seen in this repo's Chinese, all from translation
# agents working at speed. Each check is written to avoid the false positives
# that were investigated and cleared once already (see research/MANAGER.md):
#   - 算法 is fine inside 演算法, which is correct Taiwan usage
#   - a lone Greek letter is scientific notation, not a slip
SIMPLIFIED = {
    "们": "們", "这": "這", "个": "個", "过": "過", "时": "時", "样": "樣",
    "现": "現", "发": "發", "对": "對", "说": "說", "实": "實", "学": "學",
    "动": "動", "试": "試", "验": "驗", "语": "語", "读": "讀", "题": "題",
    "数": "數", "录": "錄", "级": "級", "质": "質", "继": "繼", "续": "續",
    "测": "測", "构": "構", "标": "標", "应": "應", "该": "該",
    "开": "開", "关": "關", "专": "專", "业": "業", "务": "務", "产": "產",
    "资": "資", "台": None,  # 台 is correct in Taiwan usage; never flag it
    "软": "軟", "硬": None, "网": "網", "计": "計", "认": "認", "识": "識",
    "总": "總", "结": "結", "论": "論", "据": "據", "库": "庫", "报": "報",
    "马": "馬", "鸟": "鳥", "车": "車", "东": "東", "问": "問", "间": "間",
}
CJK = r"\u4e00-\u9fff\u3400-\u4dbf"
# Latin inside Chinese is normal in this repo: tool names, model names, gene
# names, units and iGEM wiki page names all stay in English. Flagging every one
# buries the real slips, so instead flag only ORDINARY English words, which have
# no business in Chinese prose. This list is what actually went wrong before
# ("operating" dropped into a Chinese sentence) plus the obvious neighbours.
LATIN_BAD = frozenset("""
the and but with without using used use for from into onto that this these those
which while when where what who whom whose there their they them then than
have has had having been being was were are and also just only more most much many
data result results finding findings analysis analyse analyze method methods
report reports reported reporting state states stated states section sections
page pages claim claims claimed says said note notes noted record records
operating operate running run build built make made show shows shown
because however therefore although though since about against between among
should would could must can may might will shall
""".split())


def parallel_audit(root="research"):
    """Find translatable parallel arrays that have no _zh twin, or a ragged one.

    The per-key translation audit only looks at keys that exist, so a card's
    `chips` list with no `chips_zh` beside it was invisible to it for twenty
    blocks running. Anything rendered as a list of short strings belongs here.
    """
    PAIRS = ("chips", "items", "checklist", "antipatterns", "careerPaths", "openQuestions")
    out = []

    def walk(node, path, where):
        if isinstance(node, dict):
            for k in PAIRS:
                v = node.get(k)
                if isinstance(v, list) and v and all(isinstance(x, str) for x in v):
                    z = node.get(k + "_zh")
                    if not z:
                        out.append((path, "%s: %d untranslated" % (k, len(v)), where(node)))
                    elif len(z) != len(v):
                        out.append((path, "%s_zh: %d vs %d" % (k, len(z), len(v)), where(node)))
            for kk, vv in node.items():
                walk(vv, path, where)
        elif isinstance(node, list):
            for x in node:
                walk(x, path, where)

    def label(n):
        for k in ("title", "id", "kicker"):
            if isinstance(n.get(k), str):
                return n[k][:40]
        return ""

    for path in sorted(glob.glob(os.path.join(root, "**", "*.json"), recursive=True)):
        try:
            doc = json.load(io.open(path, encoding="utf-8"))
        except (ValueError, OSError) as e:
            print("  parallel-array audit could not read %s: %s" % (path, e))
            continue
        walk(doc, path, label)
    return out


def char_audit(root="research"):
    """Flag Simplified characters, Cyrillic, Greek runs and English words
    stranded inside Chinese prose. Returns a list of (path, kind, sample)."""
    hits = []
    simp = {k: v for k, v in SIMPLIFIED.items() if v}
    cyr = re.compile(r"[\u0400-\u04ff]+")
    greek_run = re.compile(r"[\u0370-\u03ff]{2,}")
    latin_in_cjk = re.compile(r"(?<=[%s])\s?([A-Za-z][A-Za-z'\-]{2,})\s?(?=[%s])" % (CJK, CJK))
    for path in sorted(glob.glob(os.path.join(root, "**", "*.json"), recursive=True)):
        try:
            raw = open(path, encoding="utf-8").read()
        except OSError:
            continue
        blob = json.loads(raw)
        texts = []

        def walk(o, key=""):
            if isinstance(o, dict):
                for k, v in o.items():
                    walk(v, k)
            elif isinstance(o, list):
                for v in o:
                    walk(v, key)
            elif isinstance(o, str) and key.endswith("_zh"):
                texts.append(o)

        walk(blob)
        joined = "\n".join(texts)
        if not joined:
            continue
        for bad, good in simp.items():
            if bad in joined:
                i = joined.index(bad)
                hits.append((path, "simplified %s should be %s" % (bad, good),
                             joined[max(0, i - 12):i + 12].replace("\n", " ")))
        m = cyr.search(joined)
        if m:
            hits.append((path, "cyrillic", m.group(0)))
        m = greek_run.search(joined)
        if m:
            hits.append((path, "greek run", m.group(0)))
        for m in latin_in_cjk.finditer(joined):
            w = m.group(1)
            if w == w.lower() and w in LATIN_BAD:
                i = m.start()
                hits.append((path, "english inside chinese: " + w,
                             joined[max(0, i - 14):i + len(w) + 14].replace("\n", " ")))
    return hits

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

        out.append("\n\n# " + H("Results", "成績"))
        for sec, g in (results.get("grandPrize") or {}).items():
            ru = "; ".join("%s %s" % (r["rank"], r["team"]) for r in g.get("runnersUp", []))
            out.append("- **%s** — %s (%s, %s)%s" % (sec, g["winner"], g["village"], g["country"],
                                                     (" · " + ru) if ru else ""))
        for sec, names in (results.get("top10") or {}).items():
            out.append("- **Top 10 %s** — %s" % (sec, ", ".join(names)))

        # The site groups sections under tabs; a linear read should too, rather
        # than interleaving tabs because they happen to share an `order`.
        TABS = [("overview", H("Overview", "總覽")), ("drylab", H("Dry lab", "乾實驗室")),
                ("good", H("Science for good", "科學向善")), ("teams", H("Team analysis", "團隊分析")),
                ("roadmap", H("Roadmap", "路線圖"))]
        ordered = []
        for tab, _ in TABS:
            ordered += [b for b in (report.get("sections") or []) if b.get("tab") == tab]
        ordered += [b for b in (report.get("sections") or [])
                    if b.get("tab") not in dict(TABS)]

        seen_tab = None
        for b in ordered:
            if b.get("tab") != seen_tab:
                seen_tab = b.get("tab")
                label = dict(TABS).get(seen_tab)
                if label:
                    out.append("\n\n# " + label)
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
            out.append("\n\n# " + head)
            for t in tl:
                out.append("\n### " + md_escape(lang(t, "title", l)))
                out.append(md_escape(lang(t, "oneLine", l)))
                out.append("\n" + md_escape(lang(t, "body", l)))
                if t.get("gemsAction"):
                    out.append("\n**%s** %s" % (H("GEMS action.", "GEMS 行動。"),
                                                md_escape(lang(t, "gemsAction", l))))

        out.append("\n\n# " + H("The four phases", "四個階段"))
        for i, p in enumerate(report.get("roadmap") or [], 1):
            out.append("\n### %d. %s (%s)" % (i, md_escape(lang(p, "title", l)), lang(p, "when", l)))
            if p.get("lede"):
                out.append(md_escape(lang(p, "lede", l)))
            items = (p.get("items_zh") if l == "zh" else None) or p.get("items") or []
            out += ["- " + md_escape(x) for x in items]
            if p.get("outcome"):
                out.append("\n_%s %s_" % (H("Done looks like:", "完成的樣子："), md_escape(lang(p, "outcome", l))))

        out.append("\n\n# " + H("Team files", "團隊檔案"))
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
    # The findings index names how many findings it lists. Set that from the
    # cards, so adding an analysis can never leave a stale number on the page.
    for blk in insights:
        if blk.get("id") == "findings-index":
            n = len(blk.get("cards") or [])
            blk["title"] = "%d findings, and where to read each one" % n
            blk["title_zh"] = "%d 個發現，以及各自該讀哪一頁" % n

    # `order` lets an analysis block sit above the written framing on its tab
    # (default 50). Python's sort is stable, so equal orders keep file order.
    report["sections"] = sorted((report.get("sections") or []) + insights,
                                key=lambda b: b.get("order", 50))

    # The full team records are large, and most of that weight is prose nobody
    # reads until they open a tab that needs it. Ship a light index up front and
    # lazy-load the rest on the first tab (or sheet) that actually uses it.
    INDEX_KEYS = ("id", "team", "section", "country", "village", "wiki", "rank", "awards", "awards_zh",
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

    zh_full, zh_part, zh_none = zh_audit(teams)
    # a block counts as translated when the prose it actually has is translated;
    # the findings index has no body, only a lede and cards.
    zh_ins = sum(1 for b in insights
                 if (b.get("body_zh") if b.get("body") else b.get("lede_zh")))
    print("\n%d team files · %d academic trends · %d industry trends · %d insight blocks (%d translated)"
          % (len(teams), len(trends["academic"].get("trends", [])),
             len(trends["industry"].get("trends", [])), len(insights), zh_ins))
    print("Chinese: %d complete · %d PARTIAL · %d untouched"
          % (len(zh_full), len(zh_part), len(zh_none)))
    if zh_part:
        print("\npartially translated — these look done but are not:")
        for tid, name, done, need, missing in sorted(zh_part, key=lambda r: r[2] - r[3]):
            print("  %-6s %-22s %2d/%-2d  missing: %s"
                  % (tid, name, done, need, ", ".join(missing[:6])))
    if zh_none:
        print("\nno Chinese yet: %s" % " ".join(r[0] for r in zh_none))
    missing = coverage(teams, results)
    if missing:
        print("\nstill missing a file (Top 10 or special-prize winner):")
        for m in missing:
            print("  -", m)
    pa = parallel_audit()
    if pa:
        n = sum(int(k.split(":")[1].split()[0]) for _, k, _ in pa if "untranslated" in k)
        print("\nparallel-array audit \u2014 %d lists unpaired (%d strings):" % (len(pa), n))
        for path, kind, sample in pa[:20]:
            print("  %-46s %-26s %s" % (path, kind, sample))
        if len(pa) > 20:
            print("  ... and %d more" % (len(pa) - 20))
    ch = char_audit()
    if ch:
        print("\ncharacter audit — %d to look at:" % len(ch))
        for path, kind, sample in ch[:25]:
            print("  %-46s %-34s %s" % (path, kind, sample))
        if len(ch) > 25:
            print("  ... and %d more" % (len(ch) - 25))

    if problems:
        print("\nwarnings:")
        for p in problems:
            print("  -", p)


if __name__ == "__main__":
    main()
