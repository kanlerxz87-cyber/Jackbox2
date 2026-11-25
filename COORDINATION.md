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
| W-01 | Replace city/county proxies with trade-area figures | in progress | fb776066 | docs/trade-area.html, docs/data/*.json |
| W-02 | Extend private worksheet to sell-vs-hold comparison | in progress | fb776066 | docs/sell-vs-hold.html, docs/calculator.html, docs/assets/calc.js |
| W-03 | Decision-gate progress board | in progress | fb776066 | docs/decision-gate.html |
| W-04 | Parcel-level hazard screening | in progress | fb776066 | docs/hazard-screening.html |
| W-10 | One-page printable summary for advisors | in progress | fb776066 | docs/printable-summary.html |
| X-01 | Private in-browser calculator | in progress | fb776066 | docs/calculator.html, docs/assets/calc.js |
| X-02 | Neighbourhood-level data around parcel | in progress | fb776066 | docs/neighbourhood.html |
| X-03 | After-tax module | in progress | fb776066 | docs/after-tax.html |
| X-04 | Price short-lease discount from real quotes | in progress | fb776066 | docs/short-lease-discount.html |
| X-05 | Tract-level trend evidence | in progress | fb776066 | docs/tract-trends.html |
| X-06 | Executive summary | in progress | fb776066 | docs/executive-summary.html, docs/index.html |
| X-07 | Risks incl. black-swan stress | in progress | fb776066 | docs/risks.html |
| X-08 | Questions / informations / answers + discovery plan | in progress | fb776066 | docs/questions.html |
| X-09 | Suggestions & site-improvement backlog | in progress | fb776066 | docs/suggestions.html |
| X-10 | Flagged for Review page | in progress | fb776066 | docs/flagged-review.html |
| X-11 | Sources & verification log | in progress | fb776066 | docs/sources.html |
| X-12 | Site shell, nav, styles, GitHub Pages | in progress | fb776066 | docs/index.html, docs/assets/style.css, docs/assets/nav.js |

Status key: unclaimed / in progress / done / needs review (published on Flagged for Review, non-blocking).

## Verification log (official sources only)
- Census QuickFacts LA city + LA County (V2025, ACS 2020–2024): population, income, poverty, housing, education, labour force — fetched 2026-11-25. URL: https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,losangelescountycalifornia/PST045224
- Jack in the Box Inc. FY2025 10-K (SEC EDGAR, filed 2025-11): franchise rental revenues $368.6M (2025) vs $375.4M (2024); Jack franchise rental $332.7M vs $347.2M; unit counts 2,136 total Jack (150 company / 1,986 franchise). URL: https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm
- Jack in the Box Q4/FY2025 earnings release (Investor Relations, 2025-11-19): same-store sales -4.2% FY2025 (-7.4% Q4); opened 31 / closed 86 in FY2025. URL: https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Reports-Fourth-Quarter-and-Full-Year-2025-Earnings/default.aspx
- IRS Topic 409 (2025): capital gains 0%/15%/20%, unrecaptured §1250 max 25%. URL: https://www.irs.gov/taxtopics/tc409
- FTB Capital gains and losses: California taxes capital gains as ordinary income, no lower rate. URL: https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html
- USGS UCERF3 FAQ: LA region 30-yr probabilities M6.7 60%, M7 46%, M7.5 31%. URL: https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area
- BEA County GDP & Personal Income 2024 (2026-02-05): LA County personal income $818.5B (largest county). URL: https://www.bea.gov/news/2026/gross-domestic-product-county-and-personal-income-county-2024
- BLS QCEW / LAUS: LA County employment +0.1% YoY (Jun 2024), LA metro unemployment ~5–6% range. URL: https://www.bls.gov/qcew/ and https://www.bls.gov/regions/west/ca_losangeles_msa.htm
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
