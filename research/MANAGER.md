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
2. Tell them 2026 wikis are at `https://2026.igem.wiki/<slug>/`. Slug = lowercase team name, hyphenated.
   **CORRECTION, learned the hard way:** most 2026 wikis are client-rendered Vite/React SPAs, so plain `curl`
   returns an empty shell. Only a minority (ETH-Zurich, GEMS-Taiwan) are server-rendered. The reliable recipe is:
   try `curl` first, and **the moment the extracted text is short or empty, switch to the browser pane**
   (`mcp__Claude_Browser__navigate` then `get_page_text`, with a 2-3 s wait for lazy route chunks).
   Route lists can be pulled by grepping `path:"..."` out of the JS bundle. Image URLs must then be collected
   from the live DOM, because most are not string literals in the bundle.
   (`teams.igem.org/<id>` is JS-only and useless to a fetcher.)
3. Give them the text-extraction one-liner:
   `curl -sL --max-time 40 "<url>" | python3 -I -c "import sys,re,html; t=sys.stdin.read(); t=re.sub(r'(?is)<(script|style|nav|footer)[^>]*>.*?</\1>',' ',t); t=re.sub(r'(?s)<[^>]+>',' ',t); print(html.unescape(re.sub(r'[ \t]*\n\s*','\n',re.sub(r'[ \t]+',' ',t)))[:20000])"`
4. Images: `curl -sL "<url>" | grep -oiE 'https://static\.igem\.wiki/teams/<ID>/[^"'"'"' )]+\.(jpg|jpeg|png|webp|svg|avif)' | sort -u`
   — works only on the server-rendered minority. For SPA wikis, read image URLs out of the rendered DOM instead.
   Watch file size: one team shipped a 10 MB animated MD-simulation webp; prefer a lighter figure.
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

---

## Session 2 (from 15:41, after the window reset)

All agents died at the 5-hour limit and were **resumed with SendMessage rather than restarted** — their work
was saved and they continued from their own transcripts. Restarting would have thrown away tens of thousands
of tokens of fetching. Keep doing this.

### Insight blocks complete (7)
`research/insights/*.json` merge into the report's sections via build.py.

| id | tab | the finding |
|---|---|---|
| technique-census | drylab | Teams that fit AND validate reach Top 10 at 53% vs 23% (recomputed on all 106 files; an early 54-file snapshot said 71/40). AlphaFold still dominates iGEM (19 of 54) though the field moved to open models. COPASI is dead (1 mention); Python won. High-school teams do MORE techno-economic analysis than undergraduates. |
| highschool-ceiling | drylab | The HS differentiator is evaluation discipline, not tools. Lambert-GA won Best Model by benchmarking the confidence metrics themselves (38-metric ensemble, ROC-AUC 0.541, its own hit not top-scoring). GCGS is the control: Top 10 with no model page at all. |
| software-afterlife | drylab | 8 of 21 award-winning tools are live. The separating habit is a hosting decision made months early — every live tool was up on freeze day, every source-only tool lists localhost. Zero stars/forks anywhere. |
| ihp-depth | good | 64 of 93 closed a real stakeholder-to-design loop — but almost every loop was closed by a credentialled technical expert. The publics and patients the criterion is about changed the vocabulary, not the vector (6-7 exceptions in 93). |
| good-patterns | good | Four separating habits: design education from survey data and measure it; train the team first (GU Frankfurt / NaWik); put disagreeing stakeholders in contact (Oxford's Buzz In); argue against yourself in public. |
| wiki-craft | teams | Winners ship text in the HTML before JS runs, and build an explicit /judging executive layer that deep-links evidence. Antipatterns that do NOT correlate with winning: dark mode, late alt-text sweeps, huge galleries, mascot systems. What winners DO share is prefers-reduced-motion. |
| taiwan-cohort | teams | Taiwan fielded 13 competing teams and won 6 awards — more than any East Asian territory except China — but every technical award came from the high-school tier, and the island is invisible in parts, software and collegiate modelling. |

### Corrections to earlier assumptions
- **Most 2026 wikis are client-rendered SPAs.** curl returns an empty shell. Only a minority (Heidelberg,
  GEMS-Taiwan, ETH-Zurich) are server-rendered. Use the browser pane, and open your OWN tab with
  `tabs_create` — the pane is shared and agents collide on the default tab, which cost the wiki-craft
  analyst several nominees.
- Nearly all wiki images are `.avif`. The original jpg/png grep found nothing on most teams.
- **Do not trust a hand-written team list.** My Taiwan brief named 6 teams; the analyst found 13 competing,
  via `api.igem.org/v1/teams?year=2026` and `/teams/<id>/awards`. That API is the right source, and it was
  available all along.

### Two devices worth lifting into GEMS practice
- TU Delft labels **every cell** of its entrepreneurship decision matrix with evidence provenance
  (Factual / Inferred / Estimated / Speculative), with a legend saying the tag records the evidence, not the
  judgement. The most copyable single device found anywhere in 2026.
- Lambert-GA closes Human Practices with a dated **Project Pivots** timeline: each pivot names the expert
  whose feedback caused it and shows before to after ("Nanobody to Minibinder").

### Next directions
1. **Apply wiki-craft's checklist to this site.** We are currently its antipattern #4 — a client-rendered app
   serving an empty shell. Mirror TU Delft: emit a static text version plus an `llms.txt` from build.py.
2. Finish the Chinese translation sweep (team files and both trend files).
3. Re-verify every image URL after the final build; drop the dead ones.
4. Mobile pass.
5. Possible further analysis: cross-reference the IHP expert-vs-public finding against village — is the
   "experts only" pattern worse in therapeutics than in agriculture?
6. GEMS has **no collaboration page at all**, and appears on no other Taiwanese team's. NYCU-Taiwan's
   27 July Meet-Up drew 53 people from five teams. That is a standing opportunity, not an observation.

### Operational hazard found the hard way: the shared scratchpad
Translation agents all write helper scripts into the same scratchpad root, and two of them clobbered each
other's helpers mid-run. The failure is **silent** — a clobbered helper no-ops and the agent still reports
"translated N files". One file (6060, DTU-Denmark) also lost four top-level `_zh` keys between a write and
its own verification pass, because a concurrent writer touched it.

Two consequences, both now handled:
1. **Never trust an agent's own completion count.** `build.py` now runs a per-key translation audit and
   prints `Chinese: N complete · N PARTIAL · N untouched`, naming every partially translated file and the
   exact fields it is missing. A file that "looks done but is not" shows up immediately.
2. **Tell each translation agent to work in its own scratch subdirectory**, and to verify its per-file
   `_zh` counts by re-reading the files rather than trusting an earlier "added N" line.

Two agents caught their own errors and said so unprompted — one removed a Cyrillic fragment it had typed
into a Chinese field, one re-added the keys it lost. That is the behaviour to keep asking for.

### Character checks: two false positives, already investigated
A naive scan for Simplified characters and non-Latin scripts flags two things across the repo. Both are fine,
so do not "fix" them:
- **算法** — all 19 occurrences sit inside **演算法**, which is correct Taiwan usage. The substring match is
  the bug, not the text.
- **β** — one occurrence, in scientific notation (beta-2 microglobulin). Greek letters belong in this text.

The checks worth keeping are the Cyrillic/Greek-run scan (which caught a genuine Cyrillic fragment a
translator had typed into a Chinese field) and the latin-inside-CJK scan (which caught an English word that
slipped into a Chinese roadmap item). Both of those now come back clean.

### Translation state at the end of this stretch
106 team files, 98 fully translated, 0 partial, 8 outstanding and all assigned to running agents
(6345 6422 6426 6450 6463 6475 6479 6511). All 11 analyses and both trend files are fully translated,
tables and all. `python3 build.py` prints the live count and names anything incomplete.
