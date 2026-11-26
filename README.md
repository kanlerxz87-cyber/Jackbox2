# Jack in the Box — Central LA Decision Dashboard

Anonymous sell-vs-hold decision workspace for one Central Los Angeles Jack in the Box NNN parcel (expiry 2030–2035, per brief).

**Privacy:** No personal identifiers, APN, lease files, or owner finances are published. Placeholders only (`[PARCEL — WITHHELD]`). Publish only aggregate, non-identifying findings.

**Verification:** Every table row links to an official source (SEC, Census, BLS, FRED, IRS, USGS, FEMA, CAL FIRE). Unverified values are blank and listed on `flagged.html`. Never inferred.

## Site map (GitHub Pages, static — no build step)

Live site: **https://kanlerxz87-cyber.github.io/Jackbox2/**

| Page | Purpose |
|------|---------|
| `index.html` | Landing dashboard + key verified findings (re-verified 26 Nov 2026) |
| `executive-summary.html` | Bottom line, knowns/unknowns, recommended path |
| `decision-gates.html` | W-03 progress board (no commitment until gates clear) |
| `trade-area.html` | W-01 tenant trend, footprint, metro and county context, plus a blank tract table (pending APN) |
| `hazards.html` | W-04 verified regional hazard record + parcel lookup checklist |
| `sell-vs-hold.html` | W-02 after-tax comparison + private browser calculator (federal tiering, §1250, NIIT, CA, Measure ULA, stress test) |
| `risks.html` | Risks per decision + black-swan stress tests + red/green flags |
| `questions.html` | 10 answered questions, 22 open ones, and how to close each |
| `suggestions.html` | Site suggestions and decision strategies, review before implementing |
| `flagged.html` | Flagged for Review: F-01–F-22 blanks, source conflicts, repository audit |
| `printable-summary.html` | W-10 one-page printable advisor summary |
| `sources.html` | Official source list |

See `COORDINATION.md` for the shared task board and session log.

## Verification

Every figure on the root pages was re-checked against the issuing agency on 26 November 2026
by opening the source page and reading the specific table or sentence, rather than relying on a
summary. The rules the site enforces on itself are executable:

| Command | What it enforces |
|---|---|
| `python3 tests/check_root.py` | Every table row has an official source link or is explicitly blank; local links and anchors resolve; every external host is on the official allowlist; no personal identifiers; the calculator is offline and stateless |
| `node tests/calc_root.test.js` | Federal LTCG tiering, §1250 cap, Measure ULA thresholds, LA city transfer-tax rounding, and that the calculator never calls the network or storage |
| `python3 tests/check_site.py`, `python3 tools/check.py`, `python3 privacy-first/tests/check.py`, `cd alternative-research && python3 tests/check.py`, `cd central-la-2026 && node scripts/verify_site.mjs` | The other dashboards' own integrity suites |

All of the above run in `.github/workflows/validate.yml` on every pull request and on every push
to `main`. See `flagged.html` for the items that are deliberately blank and the irregularities
found during the audit (R-01 to R-05).

---

## This repository contains six dashboards

Multiple parallel sessions built dashboards before seeing the others' branches. Rather than
delete work, all are retained. They do not contradict each other on any verified figure; they
differ in structure, depth, and filing cutoff date.

| Dashboard | Entry point | Character |
|---|---|---|
| Root dashboard | `index.html` | Entry point. Six decision gates, executive summary, key findings. |
| **Analytical dashboard** | `site/index.html` | Depth. Twelve gates, full evidence ledger, after-tax templates, browser calculator, 12 flagged items. Generated from `data/` by `tools/build.py`. |
| Alternative research | `alternative-research/index.html` | Independently researched second pass. |
| Docs dashboard | `docs/index.html` | Session `fb776066`'s board and pages. |
| Privacy-first workflow | `privacy-first/index.html` | Conservative no-fabrication framework: redaction controls, empty/flagged inputs, seven decision gates, risk/Q&A/suggestions registers. |
| **Central LA 2026 Refresh (Nov 2026 verified)** | `central-la-2026/index.html` | Latest filing cutoff (verified 2026-11-25): 11-page W-01–W-10 dashboard incorporating Jack in the Box FY2022–Q3 FY2026 SEC series (Del Taco sale Dec 2025, `$500M` Series 2026-1 `7.624%` refinancing, Nov 17, 2026 C-suite 8-K), post-June 30, 2026 Measure ULA `$5.4M/$10.9M` cliff detector, May 2026 CA DOF E-1 & Metro D Line Sec. 1 opening, Jan 2025 LA wildfire / CDI FAIR Plan orders, Notice Calendar tool, and 100% client-side W-02 calculator (`v1.0.0-2026.11`). |

The analytical dashboard presents a **later** reporting period than the root dashboard: the
tenant filed Q4 and full-year FY2025 results on 19 November 2025, disclosing same-store sales
of −7.4% in Q4 and −4.2% for the year. Both are flagged as I-11 on the analytical dashboard's
Flagged for Review page.

No figure in any dashboard is estimated. Where an official value could not be obtained it is
blank and flagged.

---

## Session 75e09b85 Addendum

This session added an anonymized, static decision workspace at [`docs/arena-75e09b85/`](docs/arena-75e09b85/index.html). It includes executive summary, market research, risk analysis, decision framework with a client-side calculator, questions/missing-info, suggestions/decision-gate board, flagged review, privacy, and source registry pages. All claimed values are linked to official sources; unverified/missing inputs are left blank and flagged. No personal or parcel-identifying information is published.
