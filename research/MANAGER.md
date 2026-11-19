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

**Privacy decision, deliberate and worth preserving:** the partner's name and her farm's specific
difficulties are *withheld* on the public site. They were shared in conversation, not published by her, and
consent to put a named person's difficulties on a public page was never sought. The pipeline says so in the
body and in the method note. If the user wants her named, that is their call to make, not the report's.

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
