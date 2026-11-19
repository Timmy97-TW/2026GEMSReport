# 2026 GEMS Report

GEMS Research's review of **iGEM 2026**, built for the people doing research at GEMS — not just for the next competition season.

**Live: https://timmy97-tw.github.io/2026GEMSReport/**

It covers every Top 10 team in all three sections (Undergraduate, Overgraduate, High School), every special-prize
winner and the nominees behind them, and reads each of them against the two questions GEMS Research cares about:

- **Computation, modelling and data analysis** — what machine learning, AI and simulation actually decided in the
  project, how teams made complex data intuitive, and what software and hardware they released.
- **Science for Good** — public engagement formats that worked, integrated human practices that visibly changed a
  design, and the plans teams have for taking the work into the real world.

Two more tabs track where the field is going: **academic trends** from the Nature portfolio synthetic-biology feed,
and **industry trends** from SynBioBeta and the funding and policy news around it. The last tab is the
**Drylab roadmap** — what GEMS Research should build over the next eighteen months, written so any researcher here
can pick up a phase and start.

English and Traditional Chinese throughout; the switch is in the top right and is remembered per browser.

## Layout

```
index.html          the whole site — tabs, routing, both languages
app.js              rendering
build.py            assembles data/*.js from research/*.json
data/               generated — do not edit by hand
research/
  results2026.json  official 2026 results, captured from competition.igem.org
  teams/<id>.json   one file per team, keyed by iGEM team id
  trends/*.json     academic and industry trend analysis
  report.json       the written synthesis and the roadmap
```

Edit anything under `research/`, then:

```bash
python3 build.py
```

No build step runs in the browser and there are no runtime dependencies. To preview locally:

```bash
python3 -m http.server 8787
```

## Sources and credit

Team photographs and figures are reproduced from the teams' own iGEM 2026 wikis (`static.igem.wiki`) for
non-commercial educational review; each image is credited to its team and links back to the source wiki. Project
descriptions are our summaries, not the teams' words. Results are from
[competition.igem.org/results/2026](https://competition.igem.org/results/2026). This is not an official iGEM
publication.
