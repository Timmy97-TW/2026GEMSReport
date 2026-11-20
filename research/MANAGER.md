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

### The 2026 High School Top 10, verified from iGEM's API

| Team | Country | Medal | Finalist | Section wins | Noms |
|---|---|---|---|---|---|
| Lambert-GA | USA | Gold | **YES** | 5 (incl. Grand Prize, Village) | 1 |
| HongKong-JSS | HKG | Gold | **YES** | 2 (1st Runner-up, Village) | 4 |
| GEMS-Taiwan | TWN | Gold | — | **3** (Measurement, Hardware, IHP) | 3 |
| GHCIS | CHN | Gold | — | 2 (Part Collection, Software) | 2 |
| HFI | CHN | Gold | — | 2 (Education, Village) | 3 |
| GCGS | CHN | Gold | — | 1 (New Improved Part) | 3 |
| HangzhouFourteenAP | CHN | Gold | — | 1 (Village) | 4 |
| HKSSC | HKG | **Silver** | — | 1 (New Basic Part) | 2 |
| Eton-College-UK | GBR | Gold | — | 0 | 3 |
| HongKong-HS | HKG | Gold | — | 0 | 2 |

Facts worth carrying forward:
- **GEMS-Taiwan is the most-decorated non-finalist in the section** — three section wins, more than either
  of the two teams that did make the finalist slate on special awards alone (HongKong-JSS won none).
- **HKSSC reached the Top 10 on a Silver medal**, the only team in the ten without Gold. A medal is a
  checklist and the Top 10 is a judgement; they are genuinely independent.
- **Three of the ten won a parts award**: GCGS (New Improved Part), GHCIS (Part Collection), HKSSC (New
  Basic Part). None of the three is a finalist, and the two finalists won no parts award — so parts awards
  do not lead to the podium either, in this section.
- Country spread: China 4, Hong Kong 3, USA 1, UK 1, Taiwan 1. Hong Kong put three teams in ten from a
  single small territory, and one of them took 1st Runner-up.

Section base rates for context (from the API, all 423 accepted teams): 147 high-school teams entered, 135
have a medal recorded (63 Gold, 68 Silver, 4 Bronze), **17 won any section-level or village award**, 47
received at least one nomination, 10 made the Top 10 and **2 were named Finalists**.

### judging-top10 (judging 30) — the rigour inversion, measured across all ten

The three-team comparison could be accused of fitting a story to one outcome, so the same measurements were
taken across the whole cohort. Results pages for GCGS, GHCIS, HFI, HKSSC, HongKong-HS and Lambert-GA are
server-rendered and were fetched with curl; Eton's and HangzhouFourteenAP's are client-rendered and were read
in the browser pane. **This also corrects an assumption worth recording: not all 2026 wikis are SPAs. GEMS's
is static HTML, Lambert's is server-rendered Astro, and six of the ten High School Top 10 pages fetch fine
with a browser User-Agent.** Earlier sessions treated the browser pane as mandatory; it is not.

| Team | Placing | Named test | p-values | n= | Dispersion |
|---|---|---|---|---|---|
| Lambert-GA | Grand Prize | **none** | **none** | **none** | one 95% CI |
| HongKong-JSS | 1st Runner-up | paired two-sided t-test | 0.0080, 0.0346 | n=5 | SD, error bars |
| GEMS-Taiwan | Top 10 | none | five | n=1 and n=3 | SEM, error bars |
| HKSSC | Top 10 | ANOVA | five, incl. exact | none | none |
| HongKong-HS | Top 10 | ANOVA, Dunnett, t-test | three | n=3 | SD |
| HFI | Top 10 | none | four | none | SD |
| GCGS | Top 10 | none | none | none | none |
| GHCIS | Top 10 | none | none | none | none |
| HangzhouFourteenAP | Top 10 | none | none | none | SD |
| Eton-College-UK | Top 10 | — | — | — | **no results page** |

**The inversion: the two best-reported teams placed lowest.** HongKong-HS has the most complete statistical
reporting in the section and **won nothing at all**. HKSSC reports ANOVA with p-values to five decimals and
won one parts award on a Silver medal. The Grand Prize winner names no test, reports no p-value and gives no
replicate count. Five of ten publish no p-value. This reproduces the `measurement-discipline` null (27%
against 29% across 106) inside a cohort of ten, and it means **advice to out-rigour the field is advice to
pull a disconnected lever.** Naming the test is still right — for the reader who wants to check a claim —
and the checklist says so in those terms rather than as a route to placing.

Two more sorting theories die here: **Eton-College-UK made the Top 10 with no results page at all** (it has
description, engineering, protocols, notebook, model, hardware and a game), and **HKSSC placed on Silver**
while the other nine hold Gold. And parts awards: GCGS, GHCIS and HKSSC each won one, all three finished off
the podium, and the two finalists won none between them.

What survives all ten is the shape of the write-up: the two finalists nominate one result as the answer and
bound it in the same breath; the eight non-finalists publish module inventories. **Editorial, not
experimental** — which is also the cheapest thing on this list to change.

### State at the end of the judging work

New tab `judging` (second in the bar), three blocks: `judging-criteria` (order 5), `judging-three-teams`
(order 20), `judging-top10` (order 30). 28 insight blocks total, all bilingual, both audits silent.
Verified live in both languages and at 375 px: 3 sections, 36 cards, 3 tables, 33 chips all translated,
zero chip overflow, no document overflow, scroll hints on all three wide tables, no console errors.

The `others7` analyst was still running when this was written; its brief overlaps `judging-top10`, so if it
lands, treat it as a **cross-check** of per-team detail rather than new material, and reconcile rather than
append. Two stopped analysts (`field-base-rates`, `award-economics`) left verified API data in the
scratchpad under `baserates/` and `awards/` — both were about to write their deliverable and are worth
restarting from their cached data in a later session.

### The cross-check corrected the published answer twice. Both corrections are live.

The `others7` analyst landed after `judging-top10` was first published, and it overturned two things the tab
had already said. Both were fixed rather than defended.

**Correction 1 — the Registry comparison mixed two different quantities.** The first draft compared GEMS's
*documentation payload* against HongKong-JSS's *description field*. Those differ by more than an order of
magnitude on the same part: HKSSC's best part has a **265-character description and 50,189 characters of
documentation**. Re-measured consistently (documentation payload over design/experiment/characterisation/
discussion, six headline parts per team, 58 parts total), the medians are:

HKSSC 23,116 · HFI 17,493 · GCGS 14,763 · **GEMS-Taiwan 8,644** · HangzhouFourteenAP 7,786 ·
HongKong-HS 4,944 · HongKong-JSS 2,606 · GHCIS 1,969 · Eton 1,903 · **Lambert-GA 670**

The conclusion survives and gets stronger: **the Grand Prize winner has the shortest Registry documentation
of all ten and the runner-up is eighth, while the three longest all belong to parts-prize winners who reached
no podium.** Long documentation buys a parts prize, not a placing. Never compare `description` with
documentation payload again.

**Correction 2 — the "one legible claim" thesis does not survive the full cohort.** `judging-three-teams`
argues the finalists each resolve into one sentence while GEMS publishes five key results, and that is true
of those three. But **HangzhouFourteenAP has the clearest single headline among the non-finalists** — a
four-enzyme cocktail cutting biofilm biomass 57.1% against PBS, ANOVA F(5,12) = 29.8, p < 0.001, n = 3, with
every single-enzyme omission significantly worse — and it took a village award and nothing else. GCGS states
an LOD of 53.1 nM with R² = 0.894. HKSSC reports a 2.09× advantage over a commercial esterase defended
through two-way ANOVA, Brown-Forsythe and Welch with Holm correction. One clear claim is not sufficient.

**What those three clear claims have in common is the finding that did survive.** Each is a claim about a
*surrogate*: an artificial calculus model, a synthetic signalling molecule, a model ester. **Seven of seven
non-podium teams substitute something convenient for the thing the project is actually about and stop
there** — synthetic trigger RNA for river water, a synthetic oligo for urine, a tolerance shift for paraben
removal, *B. subtilis* for *S. mutans*, a reporter for a therapy, a sensor never joined to its effector, one
protease at two concentrations. **Exactly one team in the ten ran its assay on a real sample** — HongKong-JSS
on a soil extract — and that team is the 1st Runner-up. Ten teams and two podium places cannot carry a
causal claim, and the tab says so; it is reported as the one line the podium sits on the right side of.

**The published answer is now two routes, and GEMS took neither.** Lambert-GA reached the slate on
**novelty** (a de novo binder reported as a first, measured by a commercial service, on a project whose other
arm has no data and whose results page carries no statistics). HongKong-JSS reached it on **depth** (five
independent matched runs over 51 treatments, leave-one-run-out re-analyses, a three-metal selectivity panel,
a real extract). GEMS's novel element showed no light dependence in its own ELISA with every biological
result coming from the constitutive bypass, and its real depth — the plant work at p < 0.0001 with 40
seedlings per condition — sits on a protectant the reactor did not make, since the preparation sprayed on
the plants was never assayed.

Two further things from the cross-check are now on the tab: **Best Model recognition maps exactly onto the
finalist slate** (Lambert winner, HongKong-JSS nominee, nobody else; flagged as an award predicting an award
and therefore close to circular, with GCGS and HongKong-HS having no model page at all), and **six of seven
non-podium teams publish nothing usable on attributions** (HangzhouFourteenAP's is the unedited template;
GCGS, GHCIS and HongKong-HS have none; HKSSC's points off-wiki; HFI's is an empty iframe) while both
finalists disclosed heavily and neither was punished.

## Session 5 (from 05:47, 20 Nov 2026) — picking up the two stopped analyses

Opened on a clean tree: 28 insight blocks, all bilingual, both audits silent, everything through
`262ff52` pushed. The scratchpad survived, so both stopped analysts' cached API data was still on disk.

### Step 3 of the handover: the `others7` reconciliation was already done

`others7.json` (132 KB, keys `teams` / `pattern` / `_method_note`) is present and was already reconciled at
the end of session 4 — see "The cross-check corrected the published answer twice" above. Both corrections
(the Registry `description`-versus-documentation mix-up, and the collapse of the "one legible claim" thesis)
are live on the tab. Nothing further to reconcile; no third disagreement was found.

### A structural discovery that changes how village choice should be analysed

Looking for GEMS's own village (it is **Biomanufacturing**, not Agriculture — 49 teams, 23 of them
high-school, the most crowded high-school field of any village) turned up something the earlier scripts had
stepped around rather than noticed:

**In the high-school section, village awards are not given per village.** The thirteen villages collapse into
**four award groups**, and iGEM's API records them as **four separate award objects that all carry the title
"Best Village Project"**, with `type: "special"` — *not* `type: "village"`. The thirteen `type == "village"`
objects contain **zero** high-school teams; they are undergrad and overgrad only. Each of the four groups
gives exactly 5 citations (1 winner + 4 nominees), so there are 20 high-school village citations in total.

Two traps in that one sentence, both now recorded:
- Four distinct award objects share the exact string "Best Village Project". A `title ==` dict lookup
  silently collapses them to one. Iterate; do not key.
- `a6.py`/`a8.py` excluded "Best Village Project" from the special-award set, which is right for those
  analyses but meant the high-school village economics had never been measured at all.

The four groups, high-school entrants verified to partition the 147 exactly:

| Group | HS entrants | Citations | Odds | Winner |
|---|---|---|---|---|
| Climate Crisis / Conservation / Bioremediation | 28 (0 + 7 + 21) | 5 | 1 in 5.6 | Lambert-GA |
| Agriculture / Food & Nutrition / Fashion & Cosmetics / Art & Design | **48** (17 + 17 + 14 + 0) | 5 | **1 in 9.6** | HongKong-JSS |
| Infectious Diseases / Therapeutics / Diagnostics / Oncology | 40 (1 + 20 + 13 + 6) | 5 | 1 in 8.0 | HFI |
| Space / Foundational Advance / Software & AI / Biomanufacturing | 31 (4 + 2 + 2 + 23) | 5 | 1 in 6.2 | HangzhouFourteenAP (GEMS-Taiwan nominated) |

So a high-school team picking a village is really picking one of four groups, and **a village's apparent
thinness can be irrelevant once it is pooled**: Software & AI has 2 high-school entrants but sits inside a
31-team group. GEMS's group was the second most generous of the four and GEMS was a nominee in it. Climate
Crisis and Art & Design had **no accepted high-school teams at all**, so a per-village rate for those two is
undefined rather than zero.

This correction was sent to the base-rates analyst mid-run rather than discovered after publishing.

### Verified section-level figures, for reuse without refetching

423 accepted (147 high-school, 201 undergrad, 75 overgrad) · 145 decorated (34.3%) · 59 outright winners
(13.9%) · 393 hold a medal (92.9%) · 249 hold a medal and no award · **29 have neither** · exactly 1 is
decorated without a medal · 104 Gold medals won no award · **7 Finalists across all sections, 2 of them
high-school** · high-school medals Gold 63, Silver 68, Bronze 4 (135 of 147).

### Correction 3, found and fixed in session 5: "Finalist" is the podium, not a round before it

The tab opened on the Finalist designation as though it were a distinct stage — "a designation most reports
never mention" — which lets a reader believe there was a wider slate GEMS nearly reached. Checked against
the cached 2024, 2025 and 2026 award results: in **all three seasons the finalist set and the podium set are
identical**, seven teams a year, and the seven are exactly the Grand Prize winners and the runners-up
(2026: 3 winners + 3 first runners-up + 1 second runner-up). Across all sections, `type == "finalist"` and
`type == "grand-prize"` minus Top 10 return the same seven names every year, with an empty symmetric
difference.

So the designation names the podium. The substance of the tab is untouched — 2 of the 10 High School Top 10
reached it, GEMS did not — but the framing now says so in the lede, the first body paragraph and the method
note of `judging-criteria`, in both languages. Nothing in the analysis depended on a wider round existing.

### Second independent verification of the three load-bearing GEMS claims

These are the most consequential criticisms in the report because they are aimed at the report author's own
team, so they were re-measured from scratch in session 5 against the live wiki rather than trusted from the
session-4 notes. All three hold.

**One trap worth recording, because it nearly produced a false retraction.** A first pass extracting text
from `/results` reported **zero** p-values and six hits for "t test", which would have reversed the
published claim. Both were artefacts:
- The page writes `p &lt; 0.0001` in HTML, so a regex for `p < 0` finds nothing until the entities are
  unescaped. **Always `html.unescape` before pattern-matching a fetched wiki.**
- Every "t test" hit was the ordinary word *test* inside prose — "Endpoint **Tested on**", "we first
  **tested** whether", "We have not **tested** either explanation directly", "gradient **testing**",
  "a simple containment **test**". Searching for a bare `t test` across prose is useless; the earlier
  session's claim was right and my first check was wrong.

Re-measured correctly, from `https://2026.igem.wiki/gems-taiwan/results` (HTTP 200, 160 KB, static HTML,
plain curl with a browser User-Agent):
- **Exactly 5 p-values**: `p <0.0001`, `p < 0.01`, `p < 0.0001`, `p <0.001`, `p < 0.0001`.
- **Zero named statistical tests.** No t-test, ANOVA, Tukey, Dunnett, Welch, Mann-Whitney, Wilcoxon or
  Kruskal anywhere on the page. The four "paired" hits are *540 paired readings* and *45 paired* standards —
  measurement pairing, not a paired test.
- `n=1` and `n=3` are the only replicate counts stated on the page.
- The ELISA claim is verbatim and is **stronger than what was published**: *"The ELISA showed no change over
  time. ACCD was already present at the baseline (about 3.0 µg/mL before illumination) and measured 2.6 to
  3.2 µg/mL at every time point under both colors, well above the plasmid-free control (about 1.3 µg/mL)"*.
  The team states the null itself.

From `https://2026.igem.wiki/gems-taiwan/model` (HTTP 200, 129 KB), both quotes verbatim:
- *"The reactor therefore cannot be scheduled from the forecast."*
- *"Payback 68 years on our loss figure; Geospatial Analysis says 4.9"*

### The finding of session 5: GEMS won the 2024 High School Grand Prize

This surfaced sideways. The award-economics analyst, reading three seasons of cached award results to build its
category table, reported in passing that 2024 is the season GEMS-Taiwan won the high-school Grand Prize. I
verified it directly rather than taking it on trust, and it is correct:

| Season | Placing | Wins | Nominations |
|---|---|---|---|
| **2024** | **Grand Prize Winner · Finalist · Top 10 · Gold** | Best Wiki, Best New Basic Part, Best Project Promotion Video | Best Model, Best Education, Best Presentation |
| 2025 | Top 10 · Gold | **none** | Measurement, Model, Education, Wiki, Best Village Project |
| 2026 | Top 10 · Gold · **not a Finalist** | Measurement, Hardware, Integrated Human Practices | Presentation, Wiki, Best Village Project |

And: **GEMS-Taiwan and Lambert-GA are the only two teams in the High School Top 10 in all three seasons
2024-2026**, each winning exactly one Grand Prize in that span — GEMS in 2024, Lambert in 2026.

**This was a framing error in the published judging tab, not a missing detail.** The tab was built to answer
"what do finalists have that GEMS lacks", when GEMS had already been one. The honest question is narrower and
far more answerable: *GEMS cleared this bar in 2024 and has not since — what changed?* The fact now opens
`judging-criteria` in the lede, in a new second body paragraph and in the method note, and it has an overview
index card. Before this session the 2024 Grand Prize appeared **nowhere** in the report — not in the judging
blocks, not in `multiyear-continuity`, not on the overview.

The shape of the three records is the lead the next session should pull on, and it is already recorded on the
tab as a hypothesis rather than a finding: **2024's wins were Best Wiki, Best New Basic Part and the promotion
video; 2026's were Measurement, Hardware and Integrated Human Practices.** Pooled over three seasons, Best Wiki
nominees also take a Top 10 **60%** of the time and Best Presentation **53%**, against **22%** for Measurement
and **21%** for Hardware. In 2024 GEMS won the whole-project communication award; in 2026 it won three
single-dimension awards and was only nominated for the communication ones. An agent is reading all three GEMS
wikis against that hypothesis for a `gems-three-seasons` block (judging, order 7). It may break — one team,
one data point a season, and the cohort and project change every year.

### Wave 7 results: the two relaunched analyses

Both were restarted from the cached scratchpad data, both reproduced every figure I had verified
independently, and both are published on the judging tab.

**`village-baserates` (judging 40) — a null, and it kills the premise I gave the agent.** I briefed it that
the per-village base rate "is the number GEMS needs to choose a village for 2027". It is not, and the agent
showed why. Of 147 accepted high-school teams, 47 were decorated (32.0%) and 10 took a Top 10 place. The
per-village spread, 2 of 17 in Agriculture up to 12 of 23 in Biomanufacturing, is **not distinguishable from
147 teams decorated independently at 32%** (chi-square 19.64 on 12 df, Monte-Carlo p = 0.088 over 100,000
draws holding real village sizes). Joined to 2025 by village name, the only property that carries is
crowding: entrant count r = +0.906 (p < 0.0001), while Top 10 rate r = +0.171 (p = 0.575) and Gold rate
r = +0.346 (p = 0.244). Broad decoration rate does persist at r = +0.673 (p = 0.005) and survives a size
control, but it leaves a 13.0 pp out-of-sample error and falls to r = +0.600, p = 0.153 among the seven
villages with 10 or more high-school teams both years — reported as a weak instrument, not a lever. Also
measured: high-school teams get **0.63×** an undergraduate team's odds on a village award (20 of 147 against
60 of 276), and GEMS's own Biomanufacturing was both the most crowded high-school field (23 of 147, the
largest) and the most decorated (12 of 23, z = +2.08), taking **all five** of its group's Best Village
Project citations and leaving none for the group's other eight teams.

One thing I corrected after delivery: the four group labels in its table — Environment, Food & Consumer,
Health, Advanced & Manufacturing — are **this report's own shorthand**, because the API gives those four
award objects no distinguishing title. The method note now says so, and the first card lists each group's
villages in full.

**`award-economics` (judging 50) — the reframing of the circularity is the finding.** Pooled over 2024-26 the
17 special categories nominate between 3 and 26 teams, and the share of each category's nominees who also
took a Top 10 runs from 60% to 0%: Best Wiki 60% (49/81), Best Presentation 53% (42/79), Best Model 50%
(20/40), Integrated Human Practices 45% (17/38), down through Measurement 22% and Hardware 21% to Best New
Basic Part 9%, SDI 10%, and 0% for Alternative Platform, Safety and New Improved Part. The agent refused the
easy reading and the block says why: Wiki and Presentation are judged on how the whole project is
*communicated*, which is the same material a Top 10 judgement works on, so the number predicts nothing and
instead **maps which categories proxy a whole-project verdict and which certify one isolated dimension**.
That is the same structure the tab already argued from the other direction — GEMS won three categories and
missed the podium because categories are judged one dimension at a time.

It also corrected my brief on a point of fact. I had written that GEMS "was nominated in the two
highest-co-occurrence categories and converted neither". The 60%/53% figures are about co-occurrence with a
**Top 10**, and GEMS placed Top 10 in all three seasons, so the co-occurrence held; what did not convert was
the category win. Other verified figures from it: high-school citation slots were 74 in 2024, 80 in 2025 and
82 in 2026, GEMS held 5, 4 and 5 of them and was the **most-cited high-school team of 2026**; five categories
have offered a constant high-school slate for three seasons (Model, Education, Presentation, Wiki, IHP); and
GEMS has never been cited in **9 of the 17** categories, though several of those are thin for high-school
teams generally rather than a GEMS-specific gap (Alternative Platform 0/0/1 high-school nominees, Software
0/1/1, Safety 0/1/0).

### The character audit held 41 Simplified forms and was letting slips through

Writing the reframing I introduced a Simplified 张 into a method note through a mistyped escape, and the build
said nothing. `char_audit` does screen Simplified characters, but against a `SIMPLIFIED` map that held only 41
entries and did not include it. The map now holds **144** active forms. On its first run it immediately caught
two more of my own slips — a Simplified 门 in 门檻 in both `findings-index` and `judging-criteria`, from the
same class of mistyped escape — plus a pre-existing 条目 in `good-pipeline`. All three are fixed.

Two characters were tried and **removed** rather than kept: 后 is correct Traditional in 蟻后 and in mainland
place names such as 台州后安村, and 并 is correct in fused-ring chemical nomenclature such as 二苯并噻吩.
Both produced false positives on existing team files on the first run. Forms that are themselves valid
Traditional characters — 台, 制, 里, 干, 只 — are deliberately absent for the same reason. An audit with false
positives gets ignored, which is worse than a narrower one.

**Lesson for anyone writing Chinese into these files: do not hand-write `\uXXXX` escapes.** Three of the four
character errors this session came from them (门 for 門, 张 for 張, 制 for 製). Write the characters literally
in a UTF-8 heredoc with `PYTHONUTF8=1` and let the audit check the result.

### Wave 7, third result: the three-season comparison broke my hypothesis

I briefed the analyst with a hypothesis and told it to break the hypothesis if the wikis did not support it.
They did not, and this is now the strongest finding on the tab.

**What I predicted:** that the whole-project communication layer slipped between the 2024 Grand Prize and 2026
— because 2024's wins were Best Wiki and parts awards while 2026's were three single-dimension awards, and
because Best Wiki nominees take a Top 10 60% of the time against 22% for Measurement.

**What the three wikis show:** the 2024 Grand Prize and Best Wiki year is **the weakest presented of the
three.** `https://2024.igem.wiki/gems-taiwan/` is a **577-byte JavaScript shell** whose whole site — routes,
prose, captions — sits in one **1,690,501-byte** bundle; `/results` **404s because there is no results page at
all**; the entire site carries **one p-value** (0.0003) and no named test; and its summary is a **nine-item
achievement list**, the longest module inventory of the three seasons (nine, then thirteen, then five). The
2026 site is server-rendered, carries five p-values and 67 uniquely numbered figures, and publishes a
`/development` page that grades five stages against criteria written down before the runs. So the "one
nominated result versus a module inventory" distinction fails outright on GEMS's own history: the Grand Prize
year has the longest inventory.

All figures above verified by me first-hand from the bundle, not taken on the analyst's word: the 577-byte
shell, the 1,690,501-byte bundle, the 404 on `/results`, and **488** unique `static.igem.wiki` asset URLs
(379 png, 54 pdf, 29 jpg, 12 gif, 6 jpeg, 6 webp, 1 csv).

**What actually separated 2024, verified verbatim from the bundle:**
- *"We conducted a WHO larvicidal assay (World Health Organization, 2005) by exposing 10 stage 2 larvae in
  each cup to different concentrations of toxins. All assays were conducted in triplicates."* LC50 reported
  for all three toxins — Cyt2ba **5.29E+06 CFU/mL**, Xpp81Aa1 1.98×10⁷, BmK IT1 **179 mg/mL** — with the
  incomplete arm disclosed: *"Each concentration was tested in triplicates except for BmK IT1 due to a lack
  of available larvae."*
- *"In total, we examined 98 dead larvae that were mounted onto the slides for microscopic examination."*
- The rival explanation was **experimentally excluded**: a *Gambicin / Rel1 / Rel2 / Defensin* qPCR panel
  against a BL21(DE3) arm, because *"We want to rule out the effect of E. coli in the death of mosquito
  larvae."*
- Two confounds eliminated by the team in the attractant assay — position bias, then colour: *"we covered
  each solution with black paper … so that the selection of oviposition sites is based on odorant factors
  only"* — after which the preference held at p = 0.0003.
- A randomised 10-household field trial reported **against itself**: *"only 6.7% of the users rated 5 out of
  5"*, *"trial 4 caught 33 mosquitoes, but most of them were Culex spp."*, *"only trial 12 caught 5 Aedes"*,
  and the limit stated plainly: *"There was no synthetic biology component involved throughout our field
  trial (we did not have them test our biolarvacides)."*

**This converges with what the tab already published from the other direction, and that convergence is the
result.** Cross-sectionally, across the 2026 High School Top 10, seven of seven non-podium teams stop at a
surrogate and exactly one team in ten ran its assay on a real sample — HongKong-JSS on a soil extract — and
that team took 1st Runner-up. Longitudinally, inside GEMS's own three seasons, the podium year is the
real-target year. Two independent directions, one line. Nothing else in the report is supported both ways.

**And one thing is genuinely worse in 2026: the headline outruns the body.** Verified first-hand on three
live pages. The home page sells, as a feature of the machine, *"On-demand — Green light switches production
on when the environmental sensors and forecasts decide to."* The results page says *"The ELISA showed no
change over time"* and that the amount *"did not rise with light"*, and that *"Despite repeated experiments,
the medium remained colorless"*. The model page says *"The reactor therefore cannot be scheduled from the
forecast."* One sentence on the front page is contradicted by two other pages of the team's own. 2024 left
its chain unjoined too but hedged in the same breath — *"**partially** proved the chromosome-free system"*,
*"Integration … **will be** a powerful vector control tool"*. Hedging inside the same sentence as the claim
is the habit to copy, and it is free.

**A constant, not a change:** zero named statistical tests in any of the three seasons — no t-test, ANOVA,
Tukey, Dunnett, Welch, Mann-Whitney, Wilcoxon or Kruskal, in any year. p-values went 1, then 0, then 5. So
statistical reporting improved while the podium was lost, which reproduces the `measurement-discipline` null
a third time.

Published as `gems-three-seasons` (judging, order 7): 8 cards, a 7-column three-row table, an 8-line
checklist whose second item is **"Do not spend 2027 rebuilding the wiki"**. The overview gained a card for it
and the refuted reading was corrected in the 2024 index card rather than left standing. Roadmap: phase 3's
real-sample gate now carries the longitudinal evidence, and phase 1 gained "make the landing page say only
what the results page still supports".

**One correction to my own checking, recorded because it nearly caused a false retraction in the other
direction.** I searched the bundle for `98 larvae`, got nothing, and told the user I could not verify the
figure. The string is `98 dead larvae`, and my regex pass printed only the first three of 29 matches, all of
which happened to be library noise. The analyst was right and my spot-check was badly built. Print all
matches, or filter by context, before doubting a sourced number.

### A semantic character error no audit can catch

Two of my Chinese edits contained 宣傀影片 where the award name is 宣傳影片 — 傀 instead of 傳, from the same
mistyped-escape habit. The character audit cannot see this: 傀 is a perfectly valid Traditional character, it
is just the wrong word. Script-level audits catch Simplified and Cyrillic; they cannot catch a real character
in the wrong place. The only defence is writing Chinese literally rather than as escapes, and re-reading the
rendered text.

### A third audit: the renderer was shipping raw markup, on two tabs, for an unknown time

Verifying the new block on the live site I counted **two literal asterisks rendered on the page**. Chasing it
turned up a renderer limitation and four live strings, two of them nothing to do with this session's work.

`rich()` in app.js is exactly two replacements:

```js
.replace(/\*\*([^*]+?)\*\*/g, "<strong>$1</strong>")
.replace(/(^|[^*\w])\*([^*\n]+?)\*(?![*\w])/g, "$1<em>$2</em>")
```

The bold pattern's content class is `[^*]+?` — **it may not contain an asterisk.** So an italic nested inside
bold, which is ordinary Markdown, never matches the bold rule at all, and the `**` reaches the reader. Four
strings were live:

- `research/report.json`, roadmap phase 3 item 0, both languages: `**5 worked with *B. subtilis***`, which
  rendered as *5 worked with* with a stray `**` before it and `0 of 105**` after. **This predates this
  session** and was on the roadmap tab the whole time.
- `research/insights/ai-disclosure.json`, body and body_zh, two passages each: `**… a first-class *AI Tool
  Use* block**` and the verdict sentence with `*at*` inside the bold span. Drylab was showing **four** raw
  asterisk runs. I had swept judging, overview and roadmap in earlier sessions and never swept drylab.
- `research/insights/gems-three-seasons.json` card 3, both languages: the significance markers written out as
  literal asterisk runs inside code spans, `` `**p < 0.01` ``, `` `***p<0.001` ``. Described in words now.

All six strings fixed. `**` in a code span is still unsafe, because `rich()` runs before any code handling
and there is no code handling.

**New `md_audit()` in build.py, wired in beside the other two.** It simulates both of the renderer's rules on
every string under `research/` and reports any **`**`** that survives. Two deliberate design choices, both
recorded in the docstring:

- It ignores a **lone** surviving asterisk. Those are almost always intended and render correctly — allele
  names such as `HLA-A*01` on team 6108, globs, footnote markers. Flagging them produced 30 false positives
  on the first run, so the condition is a surviving `**`, which is always wrong.
- It spells out `[A-Za-z0-9_]` instead of using Python's `\w`. JavaScript's `\w` is ASCII-only while Python's
  is Unicode-aware and matches CJK, so a direct translation of the italic regex misreports every Chinese
  string.

Self-tested against the three strings that were actually broken and five that are not — the two fixed
versions, a legitimate `***bold italic***`, `HLA-A*01`, and ordinary mixed emphasis. It flags exactly the
three. Worth knowing: **`***text***` renders correctly** — the bold rule matches the inner pair and the italic
rule wraps the result — so a triple run is not by itself a fault, which is why the audit simulates the
renderer rather than pattern-matching asterisk runs.

Three audits now run on every build: parallel-array, character, and markdown. All three are silent.

## Session 6 (from 10:38, 20 Nov 2026) — three new directions

Build on entry: 31 blocks, 31 translated, all three audits silent, 106 team files complete.

### The audits are genuine, not merely quiet

A silent audit and a broken audit look identical, so all three were tested against a
planted fault file rather than trusted. Each one fired: parallel_audit caught a chips_zh
of length 2 against chips of length 3; char_audit caught the Simplified 这 and 制造 and
条目; md_audit caught `**5 strains of *E. coli* here**` surviving as a raw asterisk pair.
SIMPLIFIED now holds 146 entries. The silence on the real corpus is real.

### Correction 4 — the continuity denominator was 78, not 81

findings-index card 18 and the README both said that of the 81 decorated teams that had
entered iGEM before, 5 carried a project line forward. multiyear-continuity.json, which
is the measurement, is narrower and says so plainly: 81 returned, 78 had a readable
previous project, and 5 of those 78 continued. Three could not be classified at all --
Stockholm's 2025 wiki is the unedited iGEM template, ASIJ-Tokyo has no 2025 wiki, and
Madrid-UCM's 2024 wiki is an empty shell. The chips on that same card already carried
"5 of 78", so the card disagreed with itself. Both languages and the README are fixed.

A cross-check was then run over all 27 overview cards and all 11 README figures: every
"N of M" claim was matched against the source blocks and report.json. The 78/81 slip was
the only one. That check is worth re-running whenever the overview tab is edited, because
the overview restates 30 other blocks and is the natural place for drift.

### Negative result — do NOT build a Taiwan terminology audit

Tested the idea that the character audit should be joined by a terminology audit for
mainland-versus-Taiwan word choices. Scanned the whole corpus (insights, trends, report,
all 106 team files) against 39 candidate pairs. Roughly 95% of the hits were false
positives, and the failure modes are instructive:

- Substring collisions. 算法 matched 23 times, every one of them inside 演算法, which is
  correct. 靶標 matched once, inside 脫靶標籤. 標準差 was a no-op pair.
- Correct Taiwan usage that merely looks mainland. 水平轉移 is the standard term for
  horizontal gene transfer. 質量 in 質量標準化指標 and 等質量下 is physical mass. 正規表達式
  is the Taiwan term for a regular expression. 文件 (217 hits) means document. 項目 means
  item. 設置 means to install. 網絡 is right for an abstract or social network, while
  網路 is the internet. 默認作答傾向 is acquiescence bias.
- Proper nouns. 微信視頻號 is WeChat Channels. 新基因組技術 is the EU's New Genomic
  Techniques regulation. 給付代碼 is a reimbursement code.

The only pair with any substance was 基因組 against 基因體, where Taiwan's standard term
is 基因體 and the corpus runs 69 to 12 the other way -- but 25 of the 69 are 基因組尺度
for genome-scale models, where both forms are current in Taiwanese writing. This is a soft
preference, not an error, so nothing was renamed. Mass-renaming 69 strings across 23 files
for a soft preference is churn that risks real damage for no reader benefit.

The standing lesson from 后 and 并 holds and now has a second case: false positives make an
audit get ignored, which is worse than having no audit. Script-level checks catch script
errors. Word choice needs a reader.

### Wave 8 — three agents, all on ground the report has never covered

Checked first that none of the 31 existing blocks already does this work. real-world.json
is about commercial honesty, measurement-discipline.json about calibration habits, and
protocol-reproducibility.json about whether a stranger could repeat the method. None of
them touches the three questions below.

1. falsification-controls.json (drylab, order 46). The report's two-direction finding has
   two halves -- measured on the real target, AND the rival explanation experimentally
   excluded -- and only the first half has ever been measured across the field. Cohort: the
   30 teams of the 2026 Top 10 across all three sections, read from their own wikis,
   because a control is exactly what a summary omits. Type specimen is GEMS 2024's qPCR
   immune-gene panel against a BL21(DE3) empty-vector arm, whose written rationale is "We
   want to rule out the effect of E. coli in the death of mosquito larvae". Agent is told a
   null is a valuable result here, because it would narrow the two-direction finding to the
   real-target half alone.
2. real-target-routes.json (good, order 35). The report says the podium goes to the team
   that measured on the real thing. It has never said how a team gets to one. An atlas of
   access routes: the sample, who held the key, what permit or biosafety level applied,
   whether a high-school team could reproduce it, and where the chain breaks for teams that
   did part of it on a surrogate. Also gives the field-wide base rate instead of the
   High-School-Top-10-only figure.
3. good-governance.json (good, order 22). The entry and exit rules for the Science for Good
   pipeline, plus the listening-visit instrument for the farm visit that good-pipeline.json
   records as the next action. Argued from three verified figures: 71 of 106 closed a
   stakeholder loop but nearly all those stakeholders were credentialled experts; 5 of 78
   carried a problem across years; 3 of 106 credit their predecessor. The exit rule is the
   point -- a programme with no way to end a problem does not carry problems across years,
   it accumulates them until a cohort graduates and the list is silently dropped.

All three agents were sent the method reminders: curl before the browser pane, html.unescape
before pattern-matching, never a bare "t test", print all regex matches, literal Chinese
characters in a UTF-8 heredoc rather than hand-written escapes, and the markdown rule that
bold content may not contain an asterisk.
