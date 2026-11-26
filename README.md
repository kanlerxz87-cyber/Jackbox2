# Jack in the Box — Central LA Decision Dashboard

Anonymous sell-vs-hold decision workspace for one Central Los Angeles Jack in the Box NNN parcel (expiry 2030–2035, per brief).

**Privacy:** No personal identifiers, APN, lease files, or owner finances are published. Placeholders only (`[PARCEL — WITHHELD]`). Publish only aggregate, non-identifying findings.

**Verification:** Every table row links to an official source (SEC, Census, BLS, FRED, IRS, USGS, FEMA, CAL FIRE). Unverified values are blank and listed on `flagged.html`. Never inferred.

## Site map (GitHub Pages, static — no build step)

| Page | Purpose |
|------|---------|
| `index.html` | Landing dashboard + key verified findings |
| `executive-summary.html` | Bottom line, knowns/unknowns, recommended path |
| `decision-gates.html` | W-03 progress board (no commitment until gates clear) |
| `trade-area.html` | W-01 county context + blank tract table (pending APN) |
| `hazards.html` | W-04 parcel hazard screening framework |
| `sell-vs-hold.html` | W-02 after-tax comparison + private browser calculator |
| `risks.html` | Risks per decision + black-swan stress tests |
| `questions.html` | Open questions + missing-info discovery plan |
| `suggestions.html` | Suggestions backlog (review before implementing) |
| `flagged.html` | Flagged for Review (blank/unverified + irregularities) |
| `printable-summary.html` | W-10 one-page printable advisor summary |
| `sources.html` | Official source list |

See `COORDINATION.md` for the shared task board and session log.

---

## This repository contains seven dashboards

Multiple parallel sessions built dashboards before seeing the others' branches. Rather than
delete work, all are retained. They do not contradict each other on any verified figure; they
differ in structure, depth, and filing cutoff date.

| Dashboard | Entry point | Character |
|---|---|---|
| Root dashboard | `index.html` | Entry point. Seven decision gates, executive summary, key findings, browser calculator. |
| **Central LA 2026 Refresh (Nov 2026 verified)** | `central-la-2026/index.html` | Latest filing cutoff (verified 2026-11-25, spot-checked 2026-11-26): 11-page W-01–W-10 dashboard incorporating Jack in the Box FY2022–Q3 FY2026 SEC series (Del Taco sale Dec 2025, `$500M` Series 2026-1 `7.624%` refinancing, Nov 17, 2026 C-suite 8-K), post-June 30, 2026 Measure ULA `$5.4M/$10.9M` cliff detector, May 2026 CA DOF E-1 & Metro D Line Sec. 1 opening, Jan 2025 LA wildfire / CDI FAIR Plan orders, Notice Calendar tool, and 100% client-side W-02 calculator (`v1.0.0-2026.11`). |
| **Analytical dashboard** | `site/index.html` | Depth. Twelve gates, full evidence ledger, after-tax templates, browser calculator, 12 flagged items. Generated from `data/` by `tools/build.py`. |
| Alternative research | `alternative-research/index.html` | Independently researched second pass. |
| Docs dashboard | `docs/index.html` | Session `fb776066`'s board and pages. |
| Privacy-first workflow | `privacy-first/index.html` | Conservative no-fabrication framework: redaction controls, empty/flagged inputs, seven decision gates, risk/Q&A/suggestions registers. |
| Session `75e09b85` workspace | `docs/arena-75e09b85/index.html` | Anonymized static decision workspace (market research, risk analysis, client-side calculator, flagged review, source registry). |

The analytical dashboard and the Central LA 2026 Refresh present **later** reporting periods than the root dashboard's Q3 FY2025 headline (Q4/FY2025 filed 19 November 2025; Q3 FY2026 filed 12 August 2026; Form 8-K filed 17 November 2026). Both are cross-referenced on the Flagged for Review pages.

No figure in any dashboard is estimated. Where an official value could not be obtained it is
blank and flagged.
