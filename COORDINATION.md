# COORDINATION — Jackbox2 Decision Workspace

Session ID: `fb776066` (branch `arena/fb776066-jackbox2`)
Owner: single integration session — all tasks claimed by this session. No other sessions active at start (repo was empty except README).

## Privacy rule (highest priority)
- No personal information, exact address, APN, owner name, or lease file content on the public site.
- Public site uses placeholders only: `[Parcel — Central Los Angeles trade area — REDACTED]`, `[Owner — REDACTED]`, `[Lease expiry — 2030–2035 window as provided — VERIFY]`.
- All identifiers / lease files / owner finances stay offline with authorized advisers. Site publishes aggregate, non-identifying findings only.

## Task board

| ID | Task | Status | Owner | Files touched |
|----|------|--------|-------|---------------|
| W-01 | Replace city/county proxies with trade-area figures | needs review | fb776066 | docs/trade-area.html, docs/data/*.json |
| W-02 | Extend private worksheet to sell-vs-hold comparison | needs review | fb776066 | docs/sell-vs-hold.html, docs/calculator.html, docs/assets/calc.js |
| W-03 | Decision-gate progress board | needs review | fb776066 | docs/decision-gate.html |
| W-04 | Parcel-level hazard screening | needs review | fb776066 | docs/hazard-screening.html |
| W-10 | One-page printable summary for advisors | done | fb776066 | docs/printable-summary.html |
| X-01 | Private in-browser calculator | needs review | fb776066 | docs/calculator.html, docs/assets/calc.js |
| X-02 | Neighbourhood-level data around parcel | needs review | fb776066 | docs/neighbourhood.html |
| X-03 | After-tax module | needs review | fb776066 | docs/after-tax.html |
| X-04 | Price short-lease discount from real quotes | needs review | fb776066 | docs/short-lease-discount.html |
| X-05 | Tract-level trend evidence | needs review | fb776066 | docs/tract-trends.html |
| X-06 | Executive summary | done | fb776066 | docs/executive-summary.html, docs/index.html |
| X-07 | Risks incl. black-swan stress | needs review | fb776066 | docs/risks.html |
| X-08 | Questions / informations / answers + discovery plan | needs review | fb776066 | docs/questions.html |
| X-09 | Suggestions & site-improvement backlog | done | fb776066 | docs/suggestions.html |
| X-10 | Flagged for Review page | done | fb776066 | docs/flagged-review.html |
| X-11 | Sources & verification log | done | fb776066 | docs/sources.html |
| X-12 | Site shell, nav, styles, GitHub Pages | done | fb776066 | docs/index.html, docs/assets/style.css, docs/requirements.html, docs/privacy.html, .github/workflows/validate.yml, tests/ |

Status key: unclaimed / in progress / done / needs review (published on Flagged for Review, non-blocking).

## Verification log (official sources only)
- Census QuickFacts LA city + LA County (V2025, ACS 2020–2024): population, income, poverty, housing, education, labour force — fetched 2026-11-25. URL: https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,losangelescountycalifornia/PST045224
- Company FY2025 earnings release, consolidated statements: franchise rental revenue $368.643M in FY2025 and $375.428M in FY2024 includes Jack and Del Taco. Segment-specific annual figures were excluded because the exact filing lines were not independently checked. URL: https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Reports-Fourth-Quarter-and-Full-Year-2025-Earnings/default.aspx
- Jack in the Box Q4/FY2025 earnings release (Investor Relations, 2025-11-19): same-store sales -4.2% FY2025 (-7.4% Q4); opened 31 / closed 86 in FY2025. URL: https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Reports-Fourth-Quarter-and-Full-Year-2025-Earnings/default.aspx
- IRS Topic 409 (2025): capital gains 0%/15%/20%, unrecaptured §1250 max 25%. URL: https://www.irs.gov/taxtopics/tc409
- FTB Capital gains and losses: California taxes capital gains as ordinary income, no lower rate. URL: https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html
- USGS UCERF3 FAQ: LA region 30-yr probabilities M6.7 60%, M7 46%, M7.5 31%. URL: https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area
- BEA County GDP & Personal Income 2024 (2026-02-05): LA County personal income $818.5B (largest county). URL: https://www.bea.gov/news/2026/gross-domestic-product-county-and-personal-income-county-2024
- Census QuickFacts employer employment 2023: LA County 3,987,736; change 2022–2023 2.3%; regional proxy, not a local forecast. URL: https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,losangelescountycalifornia/PST045224
- FEMA MSC / Risk MAP: flood maps are official NFIP source; parcel zone requires secure lookup. URL: https://msc.fema.gov/portal/home
- CAL FIRE FHSZ Maps 2022: LA SRA map (2023-09-29). URL: https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones/fire-hazard-severity-zones-maps-2022
- LA City Planning General Plan / Housing Element 2021–2029: RHNA 456,643 units. URL: https://planning.lacity.gov/plans-policies/general-plan-updates

## Irregularities flagged
- F-01: Exact parcel location not provided (by design, privacy). Tract-level figures cannot be pulled until secure tract selection is done offline. County/city figures are labelled INTERIM PROXY, not trade-area. See Flagged for Review.
- F-02: Lease expiry given as range "2030–2035" — not a single date. Must be reconciled against private abstract + notice calendar before any commitment. Flagged.
- F-03: No verified cap-rate / broker quotes for short-lease discount on file. Page shows method + blank quote table (unverified), no invented numbers.
- F-04: Parcel hazard zones (FEMA SFHA, CAL FIRE FHSZ, USGS fault/liquefaction) cannot be confirmed without address/APN. Regional context only; parcel status = UNVERIFIED pending secure lookup.
- F-05: Jack in the Box FY2025 same-store sales negative (-4.2%) and net closures (31 open / 86 close) — direction is negative, not one quarter. Reflected in tract-trends / risks, not smoothed.

## Handoff log
- 2026-11-25 fb776066: Created COORDINATION.md, claimed all tasks above (single-session integration). Starting site build.

- 2026-11-25 fb776066: Integrated 19 public static pages and tests. Verified Census QuickFacts figures against the live city/county table, company system results against FY2025 issuer earnings release, BEA county income against its release, and USGS/IRS/FTB guidance against linked official sources. Current-site data contains no address, owner identity, private records or owner financials. Public website is not an access-controlled internal workspace. Private evidence remains missing; needs-review items are documented in docs/flagged-review.html (F-01–F-09) and do not block publication.
- Reconciliation: removed unverified FY2024 openings, Jack-only annual rental numbers and unsupported generic BLS ranges; retained verified consolidated rental numbers and Census employment figures. Replaced tax-rate shortcut with CPA-supplied incremental tax and after-tax hold cash flows; calculator is unvalidated scenario arithmetic, not a forecast or tax engine. No broker quotes, local tract data, parcel zone, or private lease abstract were obtained or commissioned.
- Local integration checks: `python3 tests/check_site.py` and `node tests/calc.test.js` pass. Checks cover local links, table external references, JSON and basic calculator behavior; they do not establish all external link availability or validate the financial model. External source links point to official/issuer sites; links on hypothetical decision rows are context, not evidence for a parcel result.

- Integration PR: https://github.com/kanlerxz87-cyber/Jackbox2/pull/4 — opened; pending checks and merge. GitHub Pages currently configured for main root; intended source after merge is main /docs.
