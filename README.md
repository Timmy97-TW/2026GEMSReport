# 2026 GEMS Report

GEMS Research's review of **iGEM 2026**, built for the people doing research at GEMS — not just for the next
competition season.

**Live: https://timmy97-tw.github.io/2026GEMSReport/**

Every Top 10 team in all three sections, every special-prize winner and the nominees behind them — 106 team
files in all, researched from the teams' own wikis — read against the two questions GEMS Research cares about:
how a project turns biology into computation, and how it turns science into something a community can use.
Plus the academic and industry currents around them, and a Drylab roadmap for the next eighteen months.

English and Traditional Chinese throughout; the switch is top right and is remembered per browser.

## What the analysis found

Ten original cross-team analyses sit on the site. The short version:

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
- **The loops that closed were closed by experts.** Of 93 decorated teams, 64 can point at a stakeholder who
  visibly changed the design — but almost every one of those stakeholders was a credentialled technical
  expert, with six or seven exceptions in 93.
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
  insights/*.json   the ten cross-team analyses; each merges in as a report section
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
a Top 10 or special-prize winner or nominee — so no baseline here describes the competition at large. Each
analysis states its own method and what it cannot see.

GEMS-Taiwan is the report author's own team and is assessed on the same terms as everyone else, weaknesses
included.

## Sources and credit

Team photographs and figures are reproduced from the teams' own iGEM 2026 wikis (`static.igem.wiki`) for
non-commercial educational review; each image is credited to its team and links back to the source wiki.
Project descriptions are our summaries, not the teams' words. Results are from
[competition.igem.org/results/2026](https://competition.igem.org/results/2026). This is not an official iGEM
publication.
