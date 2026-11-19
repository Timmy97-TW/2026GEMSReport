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

---

## Session 3 (from 20:33)

State on arrival: build clean, **106 of 106 team files fully translated, 0 partial**, 11 insight blocks all
bilingual. No agents survived the window reset, so nothing to resume with SendMessage — a fresh wave was
launched instead. The translation long pole is finished; this stretch is about new analysis.

### Mobile pass — done
Measured actual overflow at 375x812 on every tab rather than eyeballing screenshots:
- The page itself never scrolled sideways on any tab (document scrollWidth stayed 375).
- **Award chips did overflow and were silently clipped** — up to 571 px wide against a 375 px viewport,
  because `.chip` carried `white-space:nowrap`. The worst offenders are the village-award strings
  ("Village Award: Space / Foundational Advance / Software & AI / Biomanufacturing — Nominee"). Fixed:
  `max-width:100%` always, and under 620 px chips wrap with an 11 px radius instead of a pill.
- The two wide tables sit in `.scrollx` (overflow-x:auto) and scroll correctly, but **nothing told the
  reader a column was cut off**. Added `scrollHint()` in app.js after both table render sites, shown only
  under 620 px: "Swipe sideways to see the whole table." / 「左右滑動可看完整表格。」
- Team detail sheet is clean at 375 px (331 px wide, zero overflowing children).
- Remaining nit, not fixed: the language toggle and GitHub link are 28-29 px tall, under the 44 px tap
  target guideline. Deliberate — they are secondary controls and enlarging them unbalances the header.

### Tooling note
`preview_start` still resolves the PARENT `GEMS/.claude/launch.json` ("atlas", port 8765) even with a
local `.claude/launch.json` present, so it cannot serve this repo. Running `python3 -m http.server`
from Bash is refused by the permission classifier in this environment, backgrounded or not. **Verify
layout against the live GitHub Pages site instead**, or test a CSS rule by injecting it into the live
page with `javascript_tool` and re-measuring — that is how the chip fix above was validated before it
was written. For a JS syntax check with no node on the box:
`/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc app.js`
(a ReferenceError on `window` means it parsed fine).

### Wave 4 — five new analyses, launched in parallel
All are *new questions*, not more coverage. Each writes one file to `research/insights/` and nothing else.

| file | tab / order | the question |
|---|---|---|
| hardware-afterlife.json | drylab 38 | Can a stranger rebuild the award-winning hardware? BOM, prices, CAD, firmware, assembly guide, calibration — the sister study to software-afterlife, and GEMS's own strongest ground. |
| measurement-discipline.json | drylab 40 | When a team reports a number, can a reader tell how sure to be about it? Calibration into absolute units, replicates, error bars with stated meaning, LOD, controls, inter-lab checks — the evidence under the roadmap's "teach uncertainty before models". |
| collaboration-network.json | teams 34 | Who worked with whom, did it correlate with placing, who are the hubs, and which specific teams can GEMS approach. GEMS has no collaboration page at all; this is the most directly actionable piece left. |
| ihp-by-village.json | good 36 | Is the "loops closed by experts" finding uniform, or worse in therapeutics and better in agriculture, where non-specialists hold decisive knowledge? Builds on ihp-depth.json; matters because GEMS's own project is agricultural. |
| parts-census.json | teams 36 | What separates a winning registry part from an ordinary submission? Taiwan took zero parts nominations in 2026, and the registry is the one artefact that outlives the project. |

Each brief carried the standing hazards: SPA wikis need the browser pane, open your OWN tab with
`tabs_create`, work in your own scratch subdirectory, verify every URL you cite, hold GEMS-Taiwan to the
same standard as everyone else, and report a negative result honestly if that is what the data says.

### Wave 4 results as they land

**ihp-by-village — the hypothesis failed, and something better was underneath it.**
Medical villages closed 6 of 21 loops with a non-expert; land, water and food villages 8 of 24. Therapeutics
(5 of 12) actually beats Bioremediation (1 of 8). The real split is **platform against applied**: Foundational
Advance 0/8, Space 0/3, Software & AI 0/1, Biomanufacturing 1/11 — 2 of 26 across the platform villages,
against 14 of 45 in the applied ones. The structural reason argued from the files is not the subject matter
but **who physically operates the thing**: agriculture and conservation deployments end in a hive or a stall
run by a non-specialist, while bioremediation ends inside a wastewater plant whose operator is a degreed
process engineer. Residents near contaminated sites appear, and change the communication rather than the design.
The analyst rescored the thirteen files that landed after ihp-depth and recounts **71 of 106** closing a loop
and **nine or ten** closing it with a non-expert, against ihp-depth's six or seven in 93. That divergence is
now written into ihp-depth's method note, and the findings index and README quote the recount.

**collaboration-network — a clean null, and a lead the report did not have.**
69 of 106 document inter-team work, 37 none, and almost all of it is meet-ups. **No inter-lab measurement ring
exists anywhere in the 106** and there was no live part or sample exchange. Uni-Padua-IT publicly offered on
9 August to codon-optimise any team's sequence and got **zero replies** — then won Best Software and Best Wiki.
Correlation with placing is absent and runs slightly backwards: substantive collaborators 14/48 (29%),
attendance-only 10/21 (48%), none 6/37 (16%), p=0.17. Reported as a null.
Previously unrecorded here: **TGEM, fourth edition, 22 August 2026, Boya Building NTU, hosted by Labi-Taiwan
with NTU's Department of Biochemical Science and Technology.** Roadmap Phase 4 has been rewritten around it,
NYCU-Taiwan's published run-sheets, and the measurement ring nobody ran, with named teams and months to email.
Caveat the analyst flagged: file-based coding is a documentation proxy — NCKU-Tainan's file shows no
collaboration signal while its wiki carries five dated exchanges.

### The character audit earned itself immediately
`char_audit()` in build.py now runs on every build over every `_zh` string in `research/`. It checks three
things and nothing else, because the earlier naive sweep produced 503 hits that were almost all legitimate:
Simplified characters (curated list; 准 and 台 removed — both correct Traditional), Cyrillic anywhere, Greek
runs of two or more (a lone Greek letter is scientific notation), and **lowercase ordinary English words**
stranded inside CJK. The last check is deliberately case-sensitive so an AND gate and a wiki page name pass,
and it ignores "wiki", which is a loanword this report uses on purpose. There is a self-test: feed it the
three historical failures and it catches all three while passing clean text.
It paid for itself within the hour — it caught a Cyrillic "протокол" that the manager had just typed into
roadmap Phase 4, before it was committed.

### How to verify a registry part (learned in wave 4, worth keeping)
`parts.igem.org` now redirects to `registry.igem.org`, which is a React SPA — so **any** `/parts/<string>`
path returns HTTP 200 and a status code proves nothing. The SPA's own pages call a public read API:

```
https://api.registry.igem.org/v1/parts/slugs/<slug>
```
where `<slug>` is the accession lowercased with underscores turned into hyphens
(`BBa_26SZRX0Y` -> `bba-26szrx0y`). It returns the part JSON and genuinely 404s for an accession that does
not exist. The `uuid` in that response is the key for the follow-ons: `/v1/parts/<uuid>/documentation`,
`/metrics`, `/composition`, `/used-by`, `/collections`, `/compatibilities`, `/sequence-features`, and for
collections `/v1/parts/collections/<uuid>/items` and `/v1/collections/<uuid>/documentation`. The
documentation endpoint returns full markdown, which is far richer than the rendered page.

Two cautions: send a browser User-Agent, or an AWS WAF challenge blocks plain curl; and the API rate-limits
hard, so a burst returns **429**, which is easy to misread as a missing part. Verify a 404 by re-requesting
it alongside accessions you know resolve.

Used immediately: `research/teams/6053.json` (HKSSC) transcribed its own award-winning part as
`BBa_26SZRXOY` with a letter O. The real accession is `BBa_26SZRX0Y` with a zero — PrbA coding sequence,
CDS, 1,602 bp — confirmed by the slug endpoint in both directions and by the registry's own listing of the
team's "PrbA's family" collection. Corrected.

---

## IMPORTANT correction from the user — what "Science for Good" means

Read this before touching the `good` tab. The original brief listed Science for Good alongside iGEM's
judging criteria (public engagement, integrated human practices, real-world application), and the tab was
built as if those three *were* the subject. **They are not.** The user corrected it directly:

> Science for Good is GEMS stepping outside the competition frame — a club-form programme, open and without
> a deadline, where students work continuously and from several directions on a few good problems: ones with
> social meaning, that can land somewhere real, that produce a quantifiable effect, and that can scale.

The worked example the user gave: through ReLEAF, GEMS met a teacher who farms by natural-farming
principles. Next year the team could go back up the mountain **having set the synthetic-biology requirement
aside**, listen to what that farm actually needs, and use science to build a solution — or take up the
seed-exchange platform she raised. *Science for Good means that kind of opportunity and idea*, not a rubric.

What changed on the site as a result:
- New `insights/good-definition.json` (order 5) — the definition, the four selection criteria written out
  as cards, what the programme is not (not an iGEM incubator, not outreach), and a checklist for running it.
  It argues the competition's costs from this report's own evidence: 8 of 21 tools still alive, zero stars
  and forks anywhere, no inter-lab measurement ring in 106 teams, nine or ten of 71 loops closed by a
  non-expert. Those are deadline artefacts, and the programme is the container for what a deadline cannot hold.
- New `insights/good-pipeline.json` (order 20) — the actual pipeline, which is nearly empty and says so.
  Two live entries from the ReLEAF season's relationships, three proposals derived from this report, with a
  table scoring every entry against the four criteria and an explicit column for "did anyone outside GEMS
  ask for this" (No for all three proposals). The governing idea: **relationships generate problems, project
  searches generate topics** — so 2027 should go back to the places 2026 reached, without a proposal in hand.
- `app.js` — on the `good` tab the three galleries are now headed "Worked examples", not "Evidence", with a
  lead-in saying to read them as examples for the programme rather than as a rubric.
- `report.json` overview section and the README now both state the distinction up front.

**Privacy decision, settled by the user on 19 Nov 2026 — the partner IS named.** The pipeline had
withheld the name on the grounds that it was shared in conversation rather than published. Asked directly,
the user said to name her: 陳惠雯老師 / Chen Hui-wen, who farms and teaches by natural-farming principles.
Both live entries, the table's "Came from" column and the method note now carry the name. What stays off the
page is the farm's *specific difficulties*, and the reason is no longer discretion — nobody has asked her
yet, which is precisely what the first pipeline entry exists to fix. The checklist rule was reworded to keep
the distinction live: naming someone is one thing, publishing their difficulties is another, and the second
still needs asking first.

Follow-on work this opens up (not started):
- The pipeline wants real entries. The honest next step is a listening visit, not more analysis.
- A short "how a problem enters and leaves the pipeline" governance note, once the programme has run once.

### Wave 4 and 5 — the remaining five results

**measurement-discipline (drylab 40) — a clean null, and it cost the roadmap an argument.**
Read directly off 39 decorated wikis: blank control 38/39, instrument named in a protocol 35/39, calibration
into an absolute unit 28/39, replicates typed biological vs technical 23/39, error bar whose meaning is
stated 23/39 — but a numeric LOD for the team's own assay **6/39 (15%)** and the same sample measured twice
**2/39 (5%)**. And it does not predict placing: across all 106 files, calibration mention gives 27% Top 10
against 29%. **No effect**, and split by outcome it reverses (Top 10 3.93, decorated non-Top-10 4.11 on a
/7 score). The sharpest single fact: CalPolySLO, the undergraduate Best Measurement winner, uses the words
*error bar* and *standard deviation* zero times across 124k characters and nine pages, with headline curves
at n=2. GEMS-Taiwan is the only 7/7 and still has an n=1 headline figure it labels "below quantitation".
Consequence: roadmap Phase 2 now carries an explicit item saying the case for teaching uncertainty first is
*not* that it wins, because the data says it does not.

**hardware-afterlife (drylab 38).** Of 20 instruments across Best Hardware, Best Measurement and Best
Alternative Platform, **6** publish enough to be rebuilt by a stranger; **9 publish no geometry file at all**;
exactly **one** has ever been used by anyone outside the team that built it.

**safety-practice (good 38) — "Nobody measured an escape rate."**
19 of 106 describe a genetic containment device, 28 use the words biosafety or biosecurity, 4 discuss dual
use, **2 name a DNA-synthesis screening regime, and 0 report a measured escape frequency.** Best available
is BASIS-China's suicide-switch threshold (~0.1–0.2 mM taurocholate) set against feline duodenum 15–42 mM
and sewage 4.7–9.1x10^-4 mM. William-and-Mary, the undergraduate winner, has the sharpest result and it is
negative: a published Addgene kill switch failed first, weeks before the team's own circuits. Designs
abandoned on safety grounds, verified: Stockholm (open-water release), Oxford (living *S. alvi*),
Bielefeld-CeBiTec (BBB-crossing LNPs, dual use). Only CalPolySLO and TAU-Israel document DNA-order screening.

**parts-census (teams 36).** Winners' headline parts carry **10,388–83,030 characters** of registry
documentation across three to six typed documents; sampled nominee parts carry 440–2,500, usually Design
only. Novelty is not the lever — the high-school basic-part winner is a 247 bp native promoter copied from
GenBank. Figures live at registry.igem.wiki/documentation, not on team wikis. Both Best New Improved Part
awards had **zero nominees**, which makes it the cheapest category in iGEM to enter and the checklist's
recommended target for GEMS in 2027. Most teachable example: GCGS's BBa_26QSD9SO — named parent, named
defect, two discrete changes, side-by-side benchmark against parent and four variants.

**collaboration-network and ihp-by-village** are written up earlier in this file.

Pattern worth naming across waves 4 and 5: **three of seven analyses returned nulls or reversals**
(collaboration does not predict placing; measurement discipline does not predict placing; the medical-versus-
agricultural hypothesis failed). All three are on the page with the null stated in the lede. That is the
house style now — see also the honest-failure effect that shrank from 54/41 to 33/27 when the dataset closed.

**hardware-afterlife, the detail worth acting on.** The separating habit is **export, not hosting** — the
opposite of the software finding. There is no `2026/hardware` group on gitlab.igem.org at all (the API 404s
it while `2026/software` returns a group), so iGEM mandates a software deposit and nothing for hardware, and
every hardware release is improvised. The failures are not lazy teams; they are teams whose good CAD never
left the design tool. Cornell, the undergraduate Best Hardware winner, publishes a 40-line priced BOM
totalling $1,213.35 and still says it *plans to* provide CAD files and circuit diagrams — no STL, STEP,
schematic or firmware anywhere. Two cited links fail when signed out: Toronto's Drive folder shows a visitor
nothing, and HongKong-JSS's named firmware repository is a 404 from an account with no public repos.
Lambert-GA is the only instrument in the cohort ever used by outsiders — UAB and Georgia Tech's Styczynski
Lab — and it is also the only release with Gerbers, drill files, a JLCPCB CPL and an LCSC-keyed BOM.
Roadmap Phase 3 now carries this as its own item.
Also worth remembering as a method caution: a stale deployed JS chunk on one team's site still contained the
team's own unexecuted editorial placeholders, so bundle-derived evidence must be re-confirmed in the browser.

**ai-disclosure (drylab 42) — the expected finding was wrong, which is the finding.**
iGEM 2026's Attributions Form carries a first-class **AI Tool Use** block, and the Attributions Form is
Bronze medal criterion 2 — so disclosure was effectively mandatory. Base rate is **106 of 106**, read off
the canonical record at `teams.igem.org/wiki/<id>/attributions` (client-side React; plain curl returns an
empty shell). ChatGPT 80, Claude 68, Gemini 30, Doubao/Kimi 21, DeepSeek 18; tasks led by Writing 80, Wiki
Coding 78, Visualization 78. A requirement produced total compliance overnight — that is the transferable
lesson, and it is the argument for GEMS writing its own norm rather than hoping for culture.
The gap is quality and categories: only **4 of 106** state what AI did *not* do, and of the 40 teams using a
third-party foundation model only 15 file it under AI at all, because AlphaFold gets filed as biology.
Five teams reported an AI failure — HangzhouFourteenAP (FoldX's top pick scored below wild type, ranking
revised), Toronto, UPF-Barcelona (A/B-tested a tool, no gain, declined to use it), Jilin-China,
Al-Nahrain-IRAQ. Best practice found anywhere: Al-Nahrain-IRAQ's team-written "Responsible AI use" table
with use, tools, named reviewer, model versions and an honest note on which one was not recorded.
GEMS-Taiwan is above median but repeats the same paragraph verbatim under all three tools, names no model
versions or reviewers, leaves AlphaFold out of the AI field, and serves the page as an iframe of the iGEM
form. Roadmap Phase 1 now carries an AI-use norm item.

### Status at the end of session 3
All eight wave 4/5 analyses landed and are integrated: findings index at 17 cards, 20 insight blocks, all
bilingual, character audit clean. Three of the eight returned nulls or reversals and say so in the lede.
Roadmap phases 1, 2, 3 and 4 have each been amended from the new evidence. The Science for Good tab has been
rebuilt around the user's correction (see the section above — read it before touching that tab).

## Session 4 (from 01:36, 20 Nov 2026)

Arrived clean: 20 insight blocks, all 20 translated, 106/106 team files complete, 0 partial, character
audit silent. Every research direction queued in the two earlier lists is now done, so this wave had to
find new ground rather than work a backlog.

### Wave 6 — five analyses, launched in parallel

| id | tab / order | the question |
|---|---|---|
| `chassis-census` | teams 38 | What did the 106 actually build in? E. coli vs yeast vs B. subtilis vs cell-free vs non-model. Plus a direct test of this report's own white-space claim: how many of the 106 used light as a control input, how many used B. subtilis, how many did both. |
| `multiyear-continuity` | good 40 | Does carrying a project across years pay? Tests the Science for Good premise against iGEM's own 2024/2025/2026 results. Briefed hard on survivorship: the sample is winners only, so "this cannot be answered from this sample" is an acceptable and possibly correct finding. |
| `education-afterlife` | good 42 | Completes the afterlife trilogy after software (8 of 21 alive) and hardware (6 of 20 rebuildable). Could a teacher in Taiwan actually obtain and run an award-winning 2026 education artefact? Every download link to be tested. |
| `protocol-reproducibility` | drylab 44 | The wet-lab twin of hardware-afterlife. Six checks per team: full protocol, named strain, plasmid maps or sequences, registry deposit with sequence, raw data, dated notebook. GEMS-Taiwan scored on the same six and published in the same table. |
| `team-resources` | teams 40 | What it costs to win. Size, PIs, institution type, sponsors, university lab access, whether a graduate student did hands-on work. The key question for GEMS: how many high-school teams are hosted in a university lab. Ends on the smallest team that reached a Top 10 and what it did instead of having people. |

Every brief carried the same house rules: null in the lede if the hypothesis fails, exact denominators,
a method note naming what the counting cannot see, decorated-teams-only stated as a limit, Taiwan-usage
Traditional Chinese with no Simplified and no Cyrillic, and one file each with no other repo writes.

### A translation hole the per-key audit could never have found

Every card on the site ends in chips — the short pill labels carrying the card's hardest fact. All **417
of them, across all 20 analyses, rendered in English while the page was in Chinese.** `chips()` in app.js
had no language branch and no file in `research/` carried a `chips_zh` key, so the per-key translation
audit — which only inspects keys that *exist* — printed "20 of 20 translated" on every build for the whole
life of the project. Section kickers had the mirror-image bug: all 20 blocks already carry `kicker_zh` and
`sechead` was being handed the English one.

Fixed in three places, and the order matters for anyone repeating this:
1. `chips(arr, cls, max, zh)` now takes an optional parallel Chinese array and falls back **per element**,
   so a half-translated list still shows Chinese for the entries that have it. Nothing breaks while a
   translation is in flight.
2. `build.py` gained `parallel_audit()` over chips, items, checklist, antipatterns, careerPaths and
   openQuestions, reporting both *missing* and *ragged* (length-mismatched) translations.
3. Then the 417 chips were translated by two agents working on scratchpad extracts, never on the repo,
   with the manager applying the result through a script that asserts the English is still byte-identical
   before writing. One of the two agents died on a content-filter error — but it died *after* writing its
   output, during its own self-check, so the file was complete and no resume was needed. Check the artefact
   before resuming a dead agent.

**`parallel_audit()` found nothing on its first run, and that was a bug, not a pass.** `io` was never
imported, so `json.load(io.open(...))` raised `NameError` on every file straight into a bare
`except Exception: continue`. An audit that silently passes is worse than no audit. The except now names
`(ValueError, OSError)` and prints the file it could not read. Do not write a bare except in this file.

Two related fixes fell out of verifying the result on the live site:
- `VILLAGE_ZH` in build.py was missing **Art & Design** and **Climate Crisis**, so five generated award
  labels read as Chinese with an English village name inside them.
- Long village-award chips were being shrunk by flex below their own text width and silently clipped —
  414px of text in a 258px box on the teams tab. `.chip.win` now wraps at every width, not only on a
  phone. Verified live: 888 chips rendered across five tabs, 0 overflowing.

### Wave 6 results as they land

**chassis-census (teams 38) — the roadmap's central bet now has a number behind it.**
Nothing in twenty-one analyses had asked what the decorated teams actually *built in*. E. coli 51 of 106,
and only 24 of those 51 name a strain. Any yeast 13, mammalian 8, B. subtilis 5, cell-free 9,
purified-enzyme-only 6, no wet lab at all 1. Other named non-model organisms 14, with almost no repetition —
*P. putida* ×4 is the only cluster. 18 teams used more than one chassis. **12 dossiers describe real bench
work without ever naming the host, so 51 is a floor, not a ceiling** — the analyst declined to impute
E. coli and said so in the method note, which is the right call.

The reason to run it was to test this report's own thesis. Both trend reviews independently named
optogenetic control in *B. subtilis* as the white space, and the whole Phase 3 roadmap points there on
their word alone. Against the competition itself: **5 of 106 used light as a control input in any organism,
5 of 106 worked with *B. subtilis*, and the two sets intersect in exactly one team — GEMS-Taiwan. Excluding
GEMS, the intersection is 0 of 105.** Marburg is the only near miss: they investigated optogenetic
induction with PULSE, called it the most attractive long-term inducer on safety grounds, and did not build
it. Phase 3 item 0 now carries the number instead of resting on two trend reviews.

The companion hypothesis failed and leads with it: a non-model chassis neither helps nor hurts placing
among decorated teams (33% against 27%, Fisher p = 0.62).

Method note worth preserving: naive regex would have been badly wrong here. "laccase" matches `CcaS`,
"Jaccard" matches `CcaR`, and `\b168\b` matches "7,168". The unverified light-user count was 22 teams; the
verified count is 5. Every hit was read in context before it was classified.

### The iGEM API — use this instead of scraping competition.igem.org

competition.igem.org is a Vite SPA, but **its backing API is open and unauthenticated**, and it removes the
single biggest limitation this report has carried: every analysis before this one was decorated-teams-only
and could not describe the competition at large. It no longer has to be.

```
https://api.igem.org/v1/competitions
https://api.igem.org/v1/competitions/<uuid>/teams?page=1&pageSize=100
https://api.igem.org/v1/competitions/<uuid>/awards/results
```

`/teams` returns the **full accepted roster** with name, country, section, village and status. The awards
endpoint includes medals, which nearly every team earns, so a medal-level baseline across all entrants is
available for the asking.

**Two traps, both hit for real:**
1. **There is more than one competition per year.** 2026 has a `venture-foundry` competition (30 teams)
   *and* the `igem` one (423 accepted). Picking the first entry whose `year` is 2026 gets you the wrong
   one — the manager did exactly that while checking the analyst's numbers, got 30 rows, and briefly
   believed the analyst was wrong. **Filter on `type == "igem"`.** The two rosters do not overlap at all.
2. **Team IDs are reissued every season.** Heidelberg is 5237, then 5775, then 6249. Names are the only
   usable key across years, and a team that renames between seasons is undetectable — that limit is stated
   in the section's method note rather than hidden.

Verified accepted-team counts: **2026: 423** (undergrad 201, high school 147, overgrad 75) · 2025: 413 ·
2024: 391 · 2023: 391. Raw JSON is cached in the session scratchpad under `continuity/` (`rosters.json`,
`aw2024/25/26.json`, `desc2025.json`); a scratchpad is wiped on reboot, so re-fetch rather than rely on it.

**multiyear-continuity (good 40) — a null that strengthens the argument it failed to prove.**
The brief asked whether carrying a problem across years pays, and warned the analyst that a winners-only
sample might make it unanswerable. The real obstacle turned out to be different and more interesting:
**almost nobody continues, so there is nothing to compare.** Of the 81 decorated 2026 teams that had
entered before, 78 had a readable previous project and **5 carried a project line forward** (Michigan,
NCKU-Tainan, XJTLU-Software, LYON, NU Boston). **None of the six returning Grand Prize teams did.**

What the full rosters *do* support, with no survivorship problem: 284 of 423 2026 teams had competed
before, and returning tracks with results — Gold 59% against 42%, Top 10 twenty-four against six, and 6 of
7 Grand Prize winners and runners-up had competed before (Stanford is the exception). The section refuses
to call this continuity paying off: returning is confounded with lab, supervisor, budget and a working wiki
template, so it measures **institutional survival, not problem continuity**, and says so.

Two findings that matter more to GEMS than the headline:
- **Return rate falls with age.** Undergrad 160 of 201, overgrad 49 of 75, **high school 75 of 147.** GEMS
  is a high-school programme, so the base rate it is working against is the worst of the three.
- **The handover is almost never written down.** Only **3 of 106** decorated teams credit their own
  predecessor with anything, and one of those three files it under *partners*, beside other universities.
  Four of the five continuers never mention the continuation on their Description page. Whatever a team
  learns leaves with the students who learned it.

This went into `good-definition.json` as the strongest single piece of evidence for the programme: the
institution comes back every year and the problem does not, which is what a season-shaped container does.

**education-afterlife (good 42) — the trilogy's reversal.**
The suspicion was that outreach survives only as photographs of children holding things. It was wrong, and
the section leads with that. Of **285 education files** linked from 31 decorated wikis, **284 download today
and one returns 403 — zero 404s.** Against software (8 of 21 still running) and hardware (6 of 20
rebuildable), the mechanism is structural rather than cultural: a PDF on `static.igem.wiki` needs no server,
so the wiki freeze that kills a web app preserves a worksheet for free. Four teams self-host a browser game
**on the frozen wiki itself** — the most durable interactive format iGEM currently allows, and GEMS already
does it.

Where education actually fails:
- **9 of 64 artefacts were never made into a file.** The sharpest case is the Best Education winner:
  XJTLU-China's page counts "18 educational toolkits" and says the aim is for other educators to adopt and
  adapt them, and links not one downloadable file. This is the hardware study's "rendered, never exported",
  applied to paper.
- **1 licence statement in 136 education PDFs** (Cornell's *Pass the Torch*, CC BY 4.0, on the artefact
  itself). HKSSC's two CC BY mentions are attributions for borrowed figures, not permission.
- **Only 3 of 31 teams published Traditional Chinese, and all three already read it** — NCKU-Tainan, HKSSC,
  GEMS. Every other Chinese file is Simplified, including all thirteen of Lambert-GA's translations of its
  children's book, which cover thirteen languages and skip Traditional. That is the Phase 4 opening.

The separating habit is neither hosting nor export: it is **writing an instruction layer for a second adult**,
which 33 of 64 do. And outside use is where education genuinely beats the other two artefact classes —
**16 of 64 have evidence of a second user, against 1 of 20 devices.**

**team-resources (teams 40) — a null, and the first base rate this report has ever been able to give.**
Headcount against award count across 84 decorated teams: Spearman 0.06, p = 0.61. Within every section the
Top 10 teams are statistically indistinguishable in size. Medians: high school 17.5, undergraduate 17,
overgraduate 12.5. **Smallest Top 10 is Princeton at nine undergraduates** — with two PIs, a postdoctoral
instructor and a PhD-student advisor behind them, one M13 chassis demonstrated across three applications,
a binder pipeline that made a new target cost compute rather than months of hands, and an outreach activity
that handed the public a real unsolved sub-problem and built the winning entry in. Princeton publishes no
attributions page at all. GEMS fielded 35 students, twice the high-school median.

The hidden-resource question has an honest and limited answer: **5 of 40 high-school teams state they worked
in a university lab, and none of the five credits a graduate student or postdoc with hands-on work.** Seven
teams name a doctoral student or postdoc among their staff and every one of those credits is worded as
supervision. The method note states the limit rather than inferring past it: **the iGEM attributions form
never asks who held the pipette.** Only 7 of 106 teams state any figure about their own funding.

**The base rate, added by the manager from the full roster.** Because the iGEM API gives the complete 2026
entrant list, organiser type could be measured on all 423 accepted teams instead of the decorated 106:
**53 of 147 high-school teams are registered under a commercial organiser** (91 secondary school, 3
community lab; the undergraduate section has none). It confers nothing — **14 of 53 commercial high-school
teams were decorated (26%) against 26 of 94 others (28%).** GEMS-Taiwan is registered commercial, verified
directly at `api.igem.org/v1/teams/6072`. All 106 decorated teams matched the roster by name.

## Session 4, part 2 — the Judging tab (user request, 20 Nov ~02:40)

The user asked, directly, for a deep comparison of **HongKong-JSS, Lambert-GA and GEMS-Taiwan** against iGEM's
finalist-selection questions, an assessment of **where GEMS specifically lost**, and then a full High School
Top 10 analysis — all of it **on a new site tab**. They then went to bed and asked for it finished by morning.
Two tangential agents (field-base-rates, award-economics) were stopped to concentrate the budget; both had
already verified their numbers against the live API and their scratchpads under `baserates/` and `awards/`
are worth picking up in a later session.

**The nine questions** (the user supplied them; question 9 is excluded throughout because it concerns the live
judging session and leaves no public record — stated in the method note of every block on the tab):
1 impressive · 2 did it work · 3 impact · 4 engineering principles · 5 human practices · 6 how much was the
team's own work · 7 built on synthetic biology and standard components · 8 documented on Wiki and Registry.

**New tab**: `{ id: "judging", en: "Judging", zh: "評審標準" }`, inserted second in the bar, with
`viewJudging()` and an explicit branch in `render()`. Note for anyone adding a tab later: the dispatch in
`render()` ends in a bare `else h = viewRoadmap()`, so a new tab without its own branch silently renders the
roadmap instead of looking broken. Add the branch.

**The fact the tab is built on, verified against results2026.json and the API:**

| Team | Placing | Special wins | Noms |
|---|---|---|---|
| Lambert-GA | Grand Prize winner | 3 (Model, Wiki, SDI) | 1 |
| HongKong-JSS | **1st Runner-up** | **0** | 4 |
| GEMS-Taiwan | Top 10 | **3** (Measurement, Hardware, IHP) | 3 |

GEMS tied the Grand Prize winner on special-award wins and finished off the podium; the team that came second
won none. Special awards are judged one dimension at a time; finalists are judged on the whole project. That
is the frame, and it is why the eight questions are the right lens rather than a rhetorical device.

### Verified directly by the manager before publishing — GEMS's own raw data

`protocol-reproducibility` claimed GEMS's wiki carries `csv: null` with a note reading "ill give data later".
Publishing that about the report author's own team demanded first-hand verification. It checks out exactly, at
a live public URL:

`https://2026.igem.wiki/gems-taiwan/static/hardware/photometer/js/growth-data.js` (HTTP 200, 3,002 bytes)

```
// ─── THE ONE PLACE THE RAW DATA GOES ───
// The owner, 15 Oct: "ill give data later". Until then each `csv` below is null, and the two charts draw
// the series TRACED from the team's chart images (GROWTH_TRACED in js/...)
window.BIO_GROWTH = {
  growth_c1: { unit: "h", csv: null },     // DBTL 1, 22 °C
  growth_c2: { unit: "min", csv: null }    // DBTL 2, 37 °C
}
```

The rendered pages carry the matching public captions — "redrawn from the team's chart" — and the page source
on `hardware-bioreactor` documents the method in detail: *"bars read from the image's pixels against its
gridlines (+-0.02)"*, *"points read from the image's pixels against its gridlines (+-0.005 mM)"*. One comment
records an unresolved unit conflict shipped as a TODO: *"its axis says mg/mL, but the kit's standard curve and
samples are in ug/mL, so ug/mL here: CHECK with the team"*.

**How to frame this fairly, which matters more than the sharpness of it.** GEMS's wiki is unusually candid: it
*tells the reader* the figures are redrawn and states its pixel-reading uncertainties, which is exactly the
provenance habit the dataviz analysis praised in other teams. But candour about tracing is not the same thing
as publishing the numbers. A judge on question 8 asks whether a stranger can check the claim, and a chart
traced from a picture of a chart cannot be checked — the uncertainty is bounded by the tracing, not by the
experiment. Also worth noting: the GEMS wiki is static HTML, not a Vite SPA, so all of this is plainly
fetchable with curl, unlike most 2026 wikis.

### HongKong-JSS, the key comparison — and it kills the two obvious theories

HongKong-JSS took **1st Runner-up with zero special awards**. Before reading its wiki the two natural
explanations for GEMS finishing below it were (a) GEMS's project chain was incomplete, and (b) GEMS's
Registry documentation was too thin. **The evidence rules out both, because HongKong-JSS is worse on both.**

- **Its chain is also incomplete, and it says so.** Two of three links joined. Biosensor to detector was
  genuinely coupled (Hamamatsu C12880 reading Hg-exposed pellets, R² = 0.9898 with standard error). The
  extraction platform **never fed the biosensor** — the soil work was hand-prepared and mercury recovery
  was never measured. Their words: *"Extraction recovery, treatment effectiveness, and compatibility with
  the biosensor must be validated before the complete workflow can support reliable environmental mercury
  measurements."*
- **Its Registry documentation is thinner than the nominee band.** Four new parts, all published with full
  sequences, carrying **756 / 643 / 468 / 385 characters**. The flagship composite BBa_26BL7PZU — the part
  nominated for Best New Composite Part — has **756 characters**, mechanism only, no fold change, no n, no
  selectivity, `characterisedIn` empty. That is under a tenth of the lowest parts-award *winner* (10,388)
  and well below the nominee floor (440–2,500). Their Parts page even claims a characterisation summary is
  recorded on the Registry page; the API record contains none.
- **It discloses more external dependency than most.** No cloning at all (*"Our team did not perform the
  cloning"* — IDT, GenScript, BGI Genomics); *"Our supervisor prepared all mercury solutions"*; a lab
  technician from Amgen Biotechnology Experience HK *"occasionally supervised us while we performed the
  experiment"*; and a Secondary PI credited with hardware design, software development **and** writing and
  maintaining the wiki — three of the four pillars, on the team's own form.

So what did carry it? **It argues against itself better than a judge could.** There is no LOD on that wiki.
The headline number is ~1 ppb, and the home page says directly beneath it: *"The detection limit of the
complete portable system is not yet established."* The three-minute summary says *"1 ppb is the lowest
concentration we tested, not a validated detection limit."* Nine numbered wet-lab DBTL cycles, the majority
documenting **failures** — including a published conceptual error, where they built four constructs around
mercury aptamers believing all aptamers are RNA, found D3/D4 are DNA aptamers whose selected structure cannot
form in an mRNA, abandoned the route and published the sequences as a warning to other teams. Their
calibration model holds out 10 of 30 measurements and reports RMSE in concentration units **including the
predictions that failed**.

**The lesson, and the likely answer to the user's question.** A judge reading that wiki cannot find a soft
spot the team has not already named. That makes the project trustworthy on a whole-project view even with an
incomplete chain and thin parts. Credibility is category-independent, which is exactly why three category
wins did not substitute for it.

### GEMS-Taiwan, verified first-hand by the manager from the live wiki

The GEMS wiki is **static HTML, not a Vite SPA**, so all of this is fetchable with plain curl and a browser
User-Agent. Anyone continuing this analysis should read it that way rather than through the browser pane.

**Criterion 1 — there is a "Key results" block, and it contains five results, not one.** Verbatim from
`/results`: protectant secretion (ACCD, LEA14 and BoPep4 all secreted by WB800, ACCD about three times the
other two) · light control (green light switches ACCD on, activity leads the protein by hours) · the
photometer (R² 0.992 against silica, 434 h unattended) · plant rescue (timing decides the effect: pre- and
post-treatment rescue, co-treatment does not) · containment and release (active ACCD in the cell-free shell
for 72 h, no colonies on the shell side). Every one is a genuine result. None is *the* result, and a judge
on question 1 is looking for the sentence they can repeat back without notes.

**Criterion 2 — the plant biology is strong, and the optogenetic core is the weakest link.** This is the
finding that matters and it is the opposite way round from what a reader would guess.
- The plant work is properly quantified: **40 seedlings per condition**, mean ± SEM, **p < 0.0001**, across
  salinity and heat trials, with fresh weight, chlorophyll and root length, and a real timing result
  (pre- and post-treatment rescue; co-treatment does not).
- The optogenetics does not reach that standard **by the team's own account**. The figure supporting "light
  exposure does not hinder growth" is **red 100% (n=1) against green 100% (n=3)** — an unbalanced control
  arm with a single replicate. The wiki's own "What it settles" section says the green-versus-red Western
  difference "was small and not yet quantified", that similar ELISA values across conditions "may be due to
  too many samples in the LPA at once, so that light from neighboring wells affected each other", that
  "CcaSR needs red light at about 672 nm to switch off, but our red LEDs emit at 640 nm", and then — to its
  credit — "**We have not tested either explanation directly.**"
- So the links that are best evidenced are the conventional ones (secrete a protein, apply it to a plant),
  and the link that makes ReLEAF *synthetic biology* rather than hardware-plus-plant-science is the one
  carrying n=1, an unquantified difference and two untested confounds. That lands on questions 2 and 7 at
  once.

**Criterion 8 — p-values with no named test.** Across the whole results page: 5 p-values, SEM and error bars
throughout, R² values to four decimals — and **zero occurrences of any named statistical test.** No t-test,
no ANOVA, no Tukey, no Dunnett, nothing. Significance is carried by asterisks alone. Compare HongKong-JSS,
which writes "paired two-sided t-test p = 0.0080" and reports held-out RMSE including its failed predictions.
A p-value whose test is not named cannot be checked by a stranger, which is precisely what question 8 asks.

**Also criterion 8, verified against the live pages** (see the earlier section for the `csv: null` file):
`growth-data.js` states the traced charts are drawn "with a line under each chart that says so". I checked all
**36 figcaptions** on `/hardware-photometer`: the two growth-curve captions carry **no** traced or redrawn
disclosure, while a different figure (the 336 h long run) does. The intent is in the source and did not reach
the page.

**In fairness, and this belongs in the published analysis.** GEMS's candour is real and comparable to
HongKong-JSS's — "We have not tested either explanation directly" is exactly the register that made the
HongKong-JSS wiki trustworthy. The difference is not honesty. It is that GEMS's honesty is spent on
explaining *why a result is unclear*, while HongKong-JSS's is spent on *bounding a result that is clear*.
One reads as work in progress; the other reads as a finished claim with known limits.

### Lambert-GA killed the best theory, and that is what made the answer findable

The tempting conclusion after reading HongKong-JSS was that the separator is self-adversarial honesty —
HongKong-JSS bounds its claims out loud, so perhaps GEMS's habit of explaining why results are unclear read
as weakness. **Lambert-GA disproves that completely.** Lambert argues against Lambert *on Lambert's own
award pages*:
- the parts page contradicts the results page about the in-house pull-down and concludes the result "does
  not establish binding by the registered candidate";
- the **Best Model** page states its gram-scale Sobol analysis "did not pass its numerical checks";
- the **Best Hardware** page prints a protein table and then declares its own concentration columns
  "unverified", and discloses that the device's published default Wi-Fi password lets anyone on the hotspot
  control it;
- a downloadable CSV stamps every siRNA row "biological efficacy not established by this file."

Candour did not cost Lambert the Grand Prize. So candour is not what cost GEMS the finalist slate, and any
advice along the lines of "claim more confidently" would be exactly wrong.

**Three more theories died on Lambert's evidence too.**
- *Statistics*: Lambert's results page has **no p-values and no named test**. Its one number, 603.6 nM with
  a 95% CI, was produced end to end by **Adaptyv Bio** — they received the sequences, expressed the protein,
  ran the BLI and interpreted it. Campaign disposition: 35 designs → 1 binder, 18 negative, 16 unusable.
- *Completeness*: Lambert's **RNAi arm has no knockdown data at all** — six siRNAs, twelve transfection
  conditions, all inconclusive; nothing tested against intact DWV, bee cells or a bee. Its own colony model
  says RNAi supplies most of SWARM's predicted benefit and the minibinder adds "a small further
  improvement". The arm carrying the impact has no data.
- *Registry documentation*: Lambert's 38 accessions top out at **6,313 characters**, with descriptions as
  short as 19 and almost no characterisation sections. **GEMS beats both finalists on question 8's Registry
  half** (34 parts, median 7,369 chars, 269,653 total, 14 in the winner band) and still finished below them.

### The answer, as published

**In both finalists the part that does not work sits at the periphery. In ReLEAF it is the thing the project
is named for.** Lambert leads with the half that produced a measured binder; the mite half produced nothing.
HongKong-JSS leads with detection that works; the in-field extraction does not. A judge names the
achievement in one clause and the gap falls in the next.

ReLEAF is named for a *stress-responsive optogenetic* bioreactor. Both halves of that name are the
undemonstrated parts, by GEMS's own documentation: "The reactor therefore cannot be scheduled from the
forecast", and ELISA at 2.6–3.2 µg/mL under **both** colours at every time point, AmilCP never colouring,
red LEDs at 640 nm against the ~672 nm CcaSR needs, and **every biological result produced by a constitutive
bypass rather than the light-gated device**. What works — secretion, membrane transit, plant rescue at
p < 0.0001 with 40 seedlings per condition — is real and is not what the project is called.

Question 4 gained the sharpest secondary distinction: **all three teams document failures, so documenting
one is not the discriminator — a fix following it is.** Lambert went 15 designs to zero binders, changed the
epitope, added tools, and got 1 of 20. HongKong-JSS found its aptamers were DNA not RNA, abandoned the route
and published the sequences as a warning. GEMS names two candidate explanations for its central negative
result — LPA well-to-well light crosstalk, and the 640/672 nm mismatch — and states: "We have not tested
either explanation directly." Both are about a week of work.

Published as `judging-three-teams` (judging tab, order 20): 8 cards one per question, a 4-column
three-team table across all eight, and an 8-line checklist. Verified live: tab renders, both tables, 24
cards, all chips Chinese, no console errors.
