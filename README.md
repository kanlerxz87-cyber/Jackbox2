# Central Los Angeles NNN QSR (Jack in the Box) — Decision Dashboard

**Live GitHub Pages Dashboard:** `https://kanlerxz87-cyber.github.io/Jackbox2/`

An anonymous, verification-first research and decision-support dashboard built to evaluate strategic paths for a Central Los Angeles single-tenant Jack in the Box NNN lease expiring in the **2030–2035** window (sell taxable, IRC §1031 exchange, negotiated early renewal / blend-and-extend, hold to expiration / re-tenant, or transit-corridor redevelopment).

## Privacy & Anonymization Mandate
- **Zero Personal Information Published:** All parcel identifiers (APN, street address), owner entity names, private lease terms, store sales, debt balances, and tax basis records are strictly excluded from this repository and replaced with anonymized placeholders.
- **100% Client-Side Private Calculator (W-02):** All calculations execute locally in the reader's browser with zero external CDNs, zero analytics, and zero network transmission.
- **No Winner Selected Without Verified Inputs:** Public official research establishes benchmarks and risk structure; binding decisions remain gated until offline legal, CPA, engineering, and brokerage verification completes.

## Dashboard Pages & Workstreams
| Page | Workstream | Purpose |
| --- | --- | --- |
| `index.html` | Executive Summary | Verified KPI benchmarks, synthesis, 6 strategic decision options with BAU + Black Swan risk matrix |
| `tenant-analysis.html` | SEC EDGAR Series | Multi-year Jack in the Box Inc. (`NASDAQ: JACK`, CIK `0000807882`) SSS, unit counts, closures, franchise rental revenue, debt & governance |
| `market-trade-area.html` | **W-01** | Regional baselines vs. offline Census tract trade-area workflow, schools, jobs, AB 1228, Metro D Line, zoning & 2026–2035 projection system |
| `hazards-risk.html` | **W-04** | Parcel-level hazard screening framework (CGS EQ Zapp, FEMA, CAL FIRE 2025 LRA, FAIR Plan) & joint rent-loss/repair/liquidity stress tests |
| `lease-calendar.html` | Gate 1 Legal & Tax | Private lease abstract checklist, local-only Notice Calendar reconciliation tool & verified IRS/FTB/BOE/LA Finance Measure ULA rules |
| `calculator.html` | **W-02** | Private local browser Sell-vs-Hold & After-Tax Calculator, Short-Lease BOV discount pricer & versioned 10-yr cash-flow model (`v1.0.0-2026.11`) |
| `decision-gates.html` | **W-03** | Interactive Decision-Gate Progress Board (Gate 0 &rarr; Gate 5) |
| `questions-gaps.html` | Missing Info Q&A | Decision-blocking questions contrasting verified knowledge vs. missing private data + safe discovery plan |
| `suggestions.html` | Site Roadmap | Dedicated suggestions review section to evaluate and select enhancements before implementation |
| `advisor-summary.html` | **W-10** | Print-optimized one-page summary for real estate counsel, CPA, insurance broker, and NNN brokers |
| `flagged-review.html` | Audit Log | All unverified/blank fields, pending filings (e.g., FY2026 10-K), and cross-agency divergences with official source links |

## Verification & Local Development
Rebuild the offline-compatible data bundle from `data/*.json` and run full automated link, source, data, and privacy checks:
```bash
node scripts/build_data_bundle.mjs
node scripts/verify_site.mjs
```
To preview locally (or simply open `index.html` offline in a browser):
```bash
python3 -m http.server 8000 --bind 0.0.0.0
```
See `COORDINATION.md` for the shared task board, verification log, official source register, and PR/deployment history.
