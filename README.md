# 2026 GEMS Report

GEMS Research's review of **iGEM 2026**, built for the people doing research at GEMS — not just for the next
competition season.

**Live: https://timmy97-tw.github.io/2026GEMSReport/**

Every Top 10 team in all three sections, every special-prize winner and the nominees behind them — 106 team
files in all, researched from the teams' own wikis — read against the two questions GEMS Research cares about:
how a project turns biology into computation, and how it turns science into something a community can use.
Plus the academic and industry currents around them, and a Drylab roadmap for the next eighteen months.

**On "Science for Good".** In this report that is not iGEM's judging category. It is the name of a GEMS
programme: club-form, no competition deadline, carrying a few well-chosen problems across years rather than
seasons — problems that matter to someone outside GEMS, that can actually be deployed, whose effect can be
counted, and that get cheaper as they spread. The iGEM human-practices material is kept as worked examples
for that programme, not as a rubric. The Science for Good tab states the definition, the selection criteria
and what is currently in the pipeline.

English and Traditional Chinese throughout; the switch is top right and is remembered per browser.

## What the analysis found

Original cross-team analyses sit on the site, one per tab section. The **Judging** tab is the newest and the
most specific. iGEM records a *Finalist* designation, and in the 2026 High School section 147 teams entered,
10 reached the Top 10 and only 2 were named Finalists — and across 2024, 2025 and 2026 alike that designation
falls on exactly the podium, seven teams a year, so it names the podium rather than a wider round. The tab
reads Lambert-GA (Grand Prize), HongKong-JSS (1st Runner-up) and GEMS-Taiwan against eight of the nine
questions iGEM uses to choose finalists, applies the same lens to the whole High School Top 10, and then asks
where a high-school team can compete at all: per-village base rates across all 423 accepted teams, and the
nominee economics of all 17 special categories over three seasons.

It opens on a fact that changes the question. **GEMS-Taiwan won the 2024 High School Grand Prize**, and was a
Finalist that year; it and Lambert-GA are the only two High School teams in the Top 10 in all three seasons,
each with one Grand Prize in that span. So this is not an account of a bar the team has never reached, but of
one it cleared in 2024 and has not cleared since. The short version of everything else:

- **The podium years are the years the central claim was measured on the real thing — and this is the one
  finding supported from two directions.** Across the 2026 High School Top 10, seven of seven non-podium teams
  stop at a surrogate and exactly one team in ten ran its assay on a real sample; that team took 1st Runner-up.
  Inside GEMS's own three seasons the Grand Prize year is the real-target year: 2024 fed three toxins to live
  *Aedes albopictus* larvae, reported LC50 for all three, examined 98 dead larvae, and ran a qPCR immune-gene
  panel against an empty-vector arm expressly to rule out *E. coli* as the cause of death. In 2026 the plant
  rescue is strong at p < 0.0001 with 40 seedlings a condition, but the preparation sprayed on the plants was
  never assayed.
- **The tempting story about 2024 is wrong, and the wikis say so.** 2024 won Best Wiki and the Grand Prize, so
  the obvious reading is that presentation slipped. Read against all three seasons it breaks: the 2024 site is a
  577-byte script shell with no results page at all, one p-value, and the longest module inventory of the three.
  The 2026 site beats it on every presentation measure. What changed is the evidence, not the writing — and no
  season names a single statistical test, while p-values went 1, then 0, then 5.
- **Choosing a village is not a lever, and at high-school level there are four doors, not thirteen.** Of 147
  accepted High School teams, 47 were decorated (32.0%). The per-village spread, 2 of 17 in Agriculture up to
  12 of 23 in Biomanufacturing, is not distinguishable from 147 teams decorated independently at 32%
  (chi-square 19.64 on 12 df, Monte-Carlo p = 0.088). Year to year only crowding carries (r = +0.91); what a
  village pays does not (Top 10 rate r = +0.17). High-school village awards come from four pooled groups —
  20 citations, 1 in 5.6 to 1 in 9.6 — which is 0.63× an undergraduate team's odds.
- **Four award categories behave like a whole-project verdict; most certify one dimension.** Pooled over
  2024–26, the share of a category's nominees who also took a Top 10 runs from Best Wiki at 60% and Best
  Presentation at 53% down to 0% for Safety, Alternative Platform and New Improved Part. GEMS's three 2026
  wins sit at 45%, 22% and 21%. The figure is near-circular and the analysis says so — Wiki and Presentation
  are judged on how the whole project is communicated, which is the material a Top 10 judgement works on — so
  it maps the categories rather than predicting anything.
- **Closing the model–data loop is the single best predictor of a Top 10.** Teams that both fit a model to
  their own measured data *and* validate it against something held back reached a Top 10 at 53%, against 23%
  for those that did not. All nine who closed the loop without a Top 10 won or were nominated for a major special prize anyway.
- **At high-school level the differentiator is evaluation discipline, not tools.** Eton-College-UK used
  logistic regression and a scoring matrix but ran cluster-aware cross-validation, a label-shuffle control and
  an ablation. Lambert-GA won Best Model for benchmarking the confidence metrics themselves — a 38-metric
  ensemble at ROC-AUC 0.541 — and publishing that its own hit was not the top-scoring design. GCGS reached the
  Top 10 with no model page at all.
- **8 of 21 award-winning software tools are still usable.** Every live one was hosted on wiki-freeze day;
  every source-only tool's wiki lists localhost as its only address. Stars and forks across every repository
  checked: zero.
- **The loops that closed were closed by experts.** Of all 106 decorated teams, 71 can point at a stakeholder
  who visibly changed the design — but almost every one of those stakeholders was a credentialled technical
  expert, with nine or ten exceptions in 106. The split is not medical against agricultural: it is platform
  against applied. Across Foundational Advance, Space, Software & AI and Biomanufacturing, 2 of 26 teams
  closed a design loop at all, against 14 of 45 in the applied villages.
- **The credible commercial sections published a model showing their own product losing** —
  Worldshaper-Shanghai's negative NPV, DTU-Denmark's LCA, Stockholm dismantling its venture when the safety
  board killed open-water release.
- **Best Wiki winners ship an executive layer, not better graphics.** Three of four serve text readable before
  any script runs; all four answer each medal criterion in two or three sentences and deep-link the evidence.
  Dark mode, late alt-text sweeps and mascot systems correlate with nothing.
- **The best figures build the reader's doubt into the picture** — a provenance rail that changes colour where
  measurement stops, a fourth verdict so "not assessed" cannot read as "passed", captions carrying the
  instrument and a link to the raw CSV.
- **Taiwan won six awards across thirteen competing teams**, more than any East Asian territory except China —
  but every technical award came from the high-school tier, with zero nominations in any parts award and zero
  in Best Software.
- **One team in 106 shone light on *B. subtilis*, and it is GEMS.** Both trend reviews independently named
  optogenetic control in *B. subtilis* as the white space this report's roadmap aims at. Tested against the
  competition: 5 of 106 decorated teams used light as a control input in any organism, 5 worked with
  *B. subtilis*, and the two sets intersect in one team. Excluding GEMS, the intersection is 0 of 105.
- **The institution comes back every year; the problem almost never does.** Of the 81 decorated teams that
  had entered iGEM before, 5 carried a project line forward, and none of the six returning Grand Prize
  teams did. Only 3 of 106 credit their own predecessor with anything.
- **Education artefacts outlive software and hardware by a wide margin** — 284 of 285 education files still
  download, against 8 of 21 software tools still running and 6 of 20 devices rebuildable. A PDF needs no
  server. The failure is licensing: 1 licence statement in 136 PDFs.
- **Team size buys nothing.** Headcount against award count across 84 decorated teams correlates at 0.06
  (p = 0.61). The smallest Top 10 team was Princeton, with nine undergraduates and four named scientists
  behind them.
- **Nobody ran an inter-lab measurement ring, nobody measured an escape rate, and measurement discipline
  wins nothing** — 27% against 29% across all 106 files. Three of the last eight analyses returned nulls or
  reversals, and each says so in its opening line.

Both trend reviews — academic (Nature portfolio, bioRxiv, PubMed) and industry (SynBioBeta, funding and policy
news) — were run independently and landed on the same white space: optogenetic control in *Bacillus subtilis*,
a twelve-paper literature in all of PubMed, at the moment light is becoming the control layer of
bioprocessing. That is where the roadmap points.

## Layout

```
index.html          the whole site — tabs, routing, both languages
app.js              rendering
build.py            assembles data/*.js and the Markdown mirror from research/*.json
data/               generated — do not edit by hand
report-en.md        plain-Markdown mirror of the entire report
report-zh.md        the same, in Traditional Chinese
llms.txt            index for anything that reads the text rather than the page
research/
  results2026.json  official 2026 results, captured from competition.igem.org
  teams/<id>.json   one file per team, keyed by iGEM team id
  trends/*.json     academic and industry trend analysis
  insights/*.json   the cross-team analyses; each merges in as a report section
  report.json       the written synthesis and the four-phase roadmap
  MANAGER.md        running log: what is done, what broke, what is queued next
```

Edit anything under `research/`, then:

```bash
python3 build.py
```

The build prints a coverage report (decorated teams with no file yet) and a per-key Chinese translation audit
that names any file which looks translated but is not. It also versions the script URLs, so a returning reader
never runs a stale app against fresh data.

No build step runs in the browser and there are no runtime dependencies. To preview locally:

```bash
python3 -m http.server 8787
```

## Method, and its limits

Team files were researched from each team's own 2026 wiki. Most 2026 wikis are client-rendered single-page
apps that return an empty shell to a plain fetch, so much of this was recovered by rendering the pages or by
extracting string literals from their JavaScript bundles. Where a team's own wiki is thin, the file says so.

Counts in the analyses come from pattern-matching the team files, not from reading the wikis a second time, so
a technique a team used but did not write up is invisible. The sample is decorated teams only — every file is
a Top 10 or special-prize winner or nominee — so in general no baseline here describes the competition at
large. Each analysis states its own method and what it cannot see.

The exceptions are marked where they occur. iGEM's own API (`api.igem.org/v1`) serves the full accepted
roster and the award results for every season, so a few figures — the return rates in the continuity
analysis, and the organiser-type base rate in the team-resources analysis — are measured across all 423
accepted 2026 teams rather than the decorated 106. Where a section does that, it says so in its method note.

GEMS-Taiwan is the report author's own team and is assessed on the same terms as everyone else, weaknesses
included.

## Sources and credit

Team photographs and figures are reproduced from the teams' own iGEM 2026 wikis (`static.igem.wiki`) for
non-commercial educational review; each image is credited to its team and links back to the source wiki.
Project descriptions are our summaries, not the teams' words. Results are from
[competition.igem.org/results/2026](https://competition.igem.org/results/2026). This is not an official iGEM
publication.
