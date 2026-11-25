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

## This repository contains five dashboards

Multiple parallel sessions built dashboards before seeing the others' branches. Rather than
delete work, all are retained. They do not contradict each other on any verified figure; they
differ in structure and depth.

| Dashboard | Entry point | Character |
|---|---|---|
| Root dashboard | `index.html` | Entry point. Six decision gates, executive summary, key findings. |
| **Analytical dashboard** | `site/index.html` | Depth. Twelve gates, full evidence ledger, after-tax templates, browser calculator, 12 flagged items. Generated from `data/` by `tools/build.py`. |
| Alternative research | `alternative-research/index.html` | Independently researched second pass. |
| Docs dashboard | `docs/index.html` | Session `fb776066`'s board and pages. |
| Privacy-first workflow | `privacy-first/index.html` | Conservative no-fabrication framework: redaction controls, empty/flagged inputs, seven decision gates, risk/Q&A/suggestions registers. |

The analytical dashboard presents a **later** reporting period than the root dashboard: the
tenant filed Q4 and full-year FY2025 results on 19 November 2025, disclosing same-store sales
of −7.4% in Q4 and −4.2% for the year. Both are flagged as I-11 on the analytical dashboard's
Flagged for Review page.

No figure in any dashboard is estimated. Where an official value could not be obtained it is
blank and flagged.

