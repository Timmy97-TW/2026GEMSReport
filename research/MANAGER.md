# Manager log — 2026GEMSReport

Running record for whoever (or whatever) picks this up next. Newest notes at the bottom of each section.

## What this is

A bilingual (EN / 繁中) review of iGEM 2026 for GEMS Research, built as a static site on GitHub Pages.
Live: https://timmy97-tw.github.io/2026GEMSReport/ · Repo: Timmy97-TW/2026GEMSReport

Two analytical domains run through every team file:
- **Computation, modelling & data analysis** — frameworks, data visualisation, data science, software/hardware
- **Science for Good** — public engagement, integrated human practices, real-world application

Plus: academic trends (Nature portfolio synbio), industry trends (SynBioBeta), and a Drylab roadmap for GEMS.

## Architecture

```
index.html   shell, nav, tabs, both languages (data-en / data-zh on static text)
app.js       all rendering; dynamic text uses T(obj,'field') which prefers obj.field_zh when lang=zh
build.py     research/*.json  ->  data/*.js     (run after ANY research change)
data/        GENERATED. never hand-edit.
research/
  results2026.json   official results, captured from the JS-rendered competition.igem.org page
  teams/<id>.json    one per team, filename is the iGEM team id
  trends/academic.json, trends/industry.json
  report.json        hand-written synthesis + the 4-phase roadmap (bilingual)
  MANAGER.md         this file
```

`build.py` overwrites each team's `awards` from the official results, computes a `rank` for sort order,
drops non-content images (logos/sponsors), and prints a coverage report of decorated teams with no file yet.
**Always read that coverage report.**

## How to brief a research agent

Agents are `general-purpose` and write files directly; they must NOT paste JSON back (it burns the manager's
context). The brief that worked:

1. Give the team list as `name → iGEM team id`.
2. Tell them 2026 wikis are at `https://2026.igem.wiki/<slug>/`, are **server-rendered**, and that plain `curl`
   works. Slug = lowercase team name, hyphenated. Fall back to WebSearch when a slug 404s.
   (`teams.igem.org/<id>` is JS-only and useless to a fetcher.)
3. Give them the text-extraction one-liner:
   `curl -sL --max-time 40 "<url>" | python3 -I -c "import sys,re,html; t=sys.stdin.read(); t=re.sub(r'(?is)<(script|style|nav|footer)[^>]*>.*?</\1>',' ',t); t=re.sub(r'(?s)<[^>]+>',' ',t); print(html.unescape(re.sub(r'[ \t]*\n\s*','\n',re.sub(r'[ \t]+',' ',t)))[:20000])"`
4. Images: `curl -sL "<url>" | grep -oiE 'https://static\.igem\.wiki/teams/<ID>/[^"'"'"' )]+\.(jpg|jpeg|png|webp|svg|avif)' | sort -u`
   then verify with `curl -sIL -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n"`. 2–4 per team,
   content only (figures, hardware, activities) — never logos. **Note: most 2026 wikis serve `.avif`.**
5. Name the exact output path `research/teams/<id>.json` and the exact schema.
6. Tell them which team ids are another analyst's job, so two agents never write the same file.
7. Demand specifics — named tools, numbers, partners — and permission to say a section is weak.

Sub-pages worth reading: `/description /project /model /software /measurement /hardware /engineering /results
/proof-of-concept /human-practices /education /entrepreneurship /implementation /sustainable /inclusivity /safety
/contribution`

## Status

### Done
- Official 2026 results captured in full (Grand Prize + runners-up, all three Top 10s, 21 special award
  categories with winners and nominees, all collegiate and high-school village awards, team-id map for ~140 teams).
  Source page is React-rendered — had to drive the built-in browser and click through the tabs to get it.
- Site shell, bilingual switching, 7 tabs, team filter/search, detail sheets, build pipeline.
- Repo created, Pages enabled, live.
- Roadmap v1 (4 phases) written bilingually in `research/report.json`.

### Wave 1 — Top 10 (6 agents, 30 teams) and trends (2 agents)
Undergrad ×2, Overgrad ×2, High School ×2 batches; academic trends; industry trends.

### Wave 2 — special prizes (6 agents)
Best Model cohort · Best Software cohort · Measurement + Hardware cohort · Education + Inclusivity cohort ·
IHP + Sustainable Development cohort · Entrepreneurship + Parts + Safety cohort.

### Still to do
- [ ] **Chinese translation pass** over every `research/teams/*.json` and both trend files — add `_zh` siblings
      for `projectTitle, tagline, summary, gemsTakeaway`, `dry.{frameworks,dataviz,datascience,software}`,
      `good.{publicEngagement,ihp,realWorld}`, image `caption`. Traditional Chinese, Taiwan usage.
      Keep tool names, model names and proper nouns in English.
- [ ] Rewrite `report.json` synthesis sections once the research is in — the cross-team conclusions are the
      point of the report and cannot be written before the evidence exists.
- [ ] Verify every image URL still 200s after the full build; drop the dead ones.
- [ ] Mobile pass on the site.

### Research directions queued (the "new insight" work, not just coverage)
1. **Cross-team technique census.** Count which computational tools appear across all ~60 team files
   (AlphaFold3 vs Boltz vs ESMFold; COPASI vs Python ODE; FBA; agent-based). A frequency table of what
   2026's best teams actually reached for is something no other report has, and it directly sets the
   Phase 2 curriculum.
2. **The high-school ceiling.** Compare the dry lab of the HS Top 10 against the UG Top 10 — what did high
   schoolers genuinely achieve, and where is the real gap? This is the honest benchmark for GEMS.
3. **IHP depth scoring.** Grade each team's human practices on whether a stakeholder visibly changed the
   design. Separates the teams worth copying from the teams that just logged meetings.
4. **What the Best Wiki winners did differently** — the report itself is a wiki-shaped artefact, so this is
   directly actionable for 2027.
5. **Taiwan cohort read.** GEMS-Taiwan, Labi-Taiwan, NYCU-Taiwan, NCKU-Tainan, NTHU, Mingdao — how did the
   island do, and where are the collaboration opportunities.
6. **Software afterlife.** Of the award-winning iGEM software tools, how many are actually deployed and
   reachable today? A blunt answer shapes Phase 3.

## Findings log

### 2026-11-19 — the convergence (this is the report's thesis)
The academic trend agent (Nature portfolio + bioRxiv + PubMed) and the industry trend agent (SynBioBeta +
funding/policy news) were run in parallel, from different sources, with no knowledge of each other.
**They landed on the same white space.**

- Academic: light has matured into a real-time actuator for closed-loop fermentation control (~60% titre gain
  reported in a 1 L photobioreactor) — and optogenetics in *Bacillus subtilis* is **twelve papers in all of
  PubMed**, verified directly by the agent.
- Industry: optogenetics is becoming the control and cleaning layer of bioprocessing precisely because light
  lets you retrofit an existing steel fermenter instead of buying a new one — the cheapest route past the
  CapEx wall that is the binding constraint on biomanufacturing right now.
- GEMS already stands in that gap: ReLEAF was a CcaS/CcaR optogenetic circuit in *B. subtilis* driving a
  bioreactor, and it won Best Measurement and Best Hardware for exactly the instrumentation this needs.

Second strategic finding, industry side: Taiwan's state-linked biotech push (TBMC, Hsinchu GMP, ops from
Q2 2026) is a **CDMO/manufacturing** play with no visible synthetic-biology **design** layer, while Singapore
(DayOne biological data centre) and Israel (NIS 70M for biological-AI infrastructure) are funding exactly that
layer. GEMS cannot out-build a CDMO; it can occupy the design position nobody in Taiwan holds.

Both are now written into `report.json` — a "convergence" section on the roadmap tab, and Phase 3 opens with
the Bacillus optogenetics line.

### Other things worth carrying forward
- Structure prediction is commodity now: open Boltz-2 / Chai-1 / OpenFold3 / ColabFold match or beat the gated
  flagship. The scarce skill is reading pLDDT and PAE critically, not getting a fold.
- ML-guided DBTL is the hardest evidence for the dry-lab thesis: 5× isoprenol titre in six cycles, 800,000
  designs cut to ~400.
- US NSTM-6 (Nov 2026) ties federal funding to certified DNA suppliers screening 50+ nucleotide orders, with
  8-year record retention. Reaches anyone selling to US-funded labs. GEMS needs a one-page policy; it is in
  Phase 1 now.
- 2026 pay reality: protein-design roles ~$150K–$215K vs ~$80K–$105K entry-level computational biology.
  Python/PyTorch/foundation models are the named skills. The hybrid "owns the DBTL loop" profile is the target.
- Ginkgo revenue roughly halved to $20.2M in Q2 2026 while Twist grew 22% to $459.4M with positive adjusted
  EBITDA. The platform-company model is dead; picks-and-shovels compounds. Relevant to how GEMS defines its niche.

### Agent waves — status
- Wave 1 (Top 10 ×6, trends ×2): trends **complete**, team batches landing.
- Wave 2 (special prizes ×6): landing.
- Wave 3: remaining collegiate nominees, remaining HS nominees, trend-file Chinese translation — launched.
- Team files on disk at last check: 35.
