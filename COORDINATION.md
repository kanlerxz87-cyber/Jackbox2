# Coordination Board (`COORDINATION.md`)

> **Branch Policy Note:** This session operates exclusively on its assigned working branch `arena/ae0d8ac3-jackbox2` (branched from `main` at `d1f3bf8b6c453a009ac95b51862a5f9d37d66a5c`) in compliance with workspace session tracking rules. No confidential owner, parcel, or lease PII is stored anywhere in this repository.

## Active Session
- **Session ID:** `arena/ae0d8ac3-jackbox2`
- **Started (UTC):** 2026-11-25
- **Completed Verification Pass (UTC):** 2026-11-25

## Task Board

| Task ID | Workstream / Description | Status | Owning Session | File Scope | Notes |
| --- | --- | --- | --- | --- | --- |
| T-00 | Repo review, privacy framework, `.nojekyll`, `README.md`, and `COORDINATION.md` | `done` | `arena/ae0d8ac3-jackbox2` | `COORDINATION.md`, `.nojekyll`, `README.md` | Verified clean starting repo (`main` @ `d1f3bf8`); GitHub Pages legacy `main` `/` active |
| T-01 | Tenant & Brand Multi-Year SEC Filing Verification (Jack in the Box Inc., CIK `0000807882`) | `done` | `arena/ae0d8ac3-jackbox2` | `data/tenant.json`, `tenant-analysis.html` | Verified FY22–Q3 FY26 SEC 10-K/10-Q/8-K series; FY26 full-year 10-K flagged pending (`FLG-01`) |
| T-02 | **W-01** · Central LA Economic, Demographic, Labor, School, Transit, Zoning & Projection Research | `done` | `arena/ae0d8ac3-jackbox2` | `data/market-w01.json`, `market-trade-area.html` | Census, CA DOF Jan 2026 E-1, BLS Sep/Oct 2026, CA EDD, CDE/LAUSD, CA DIR AB 1228, Wages LA, LA Metro, SCAG, AB 2011; parcel trade area left blank & flagged (`FLG-03`) |
| T-03 | **W-04** · Parcel-Level Hazard Screening & Black Swan Stress Framework | `done` | `arena/ae0d8ac3-jackbox2` | `data/hazards-w04.json`, `hazards-risk.html` | USGS UCERF3, CGS EQ Zapp, FEMA MSC, CAL FIRE 2025 LRA & Jan 2025 Palisades/Eaton official stats, CDI FAIR Plan Orders `2025-1`/`2026-1`/`2026-2`; parcel zone cells left blank & flagged (`FLG-04`) |
| T-04 | Tax, Transfer Tax (Measure ULA), Prop 13/19, Lease Abstract & Notice Calendar | `done` | `arena/ae0d8ac3-jackbox2` | `data/tax-lease.json`, `lease-calendar.html` | IRS Topic 409 / Pub 550 / NIIT / Form 8824, CA FTB, CA BOE, LA Assessor, LA RRCC, LA Finance Measure ULA (eff. Jul 1, 2026 `$5.4M/$10.9M`), U.S. Treasury 10Y (`4.91%`); lease abstract cells blank & flagged (`FLG-02`, `FLG-06`) |
| T-05 | **W-02** · Private Browser Sell-vs-Hold & After-Tax Calculator + Short-Lease Discount + Versioned Cash-Flow Model (`v1.0.0-2026.11`) | `done` | `arena/ae0d8ac3-jackbox2` | `assets/js/calculator.js`, `calculator.html` | 100% client-side, zero network calls, Measure ULA cliff detector verified, no winner selected without attested verified inputs |
| T-06 | **W-03** · Decision-Gate Progress Board, Decision Options Matrix, Missing Info Q&A & Site Suggestions | `done` | `arena/ae0d8ac3-jackbox2` | `data/gates-w03.json`, `data/questions-suggestions.json`, `decision-gates.html`, `questions-gaps.html`, `suggestions.html`, `assets/js/gates.js` | Interactive local-only gate tracker & suggestions selector; all 6 courses of action analyzed for BAU & Black Swan risks |
| T-07 | Executive Summary Landing Page, **W-10** One-Page Printable Advisor Summary, Flagged for Review Page | `done` | `arena/ae0d8ac3-jackbox2` | `index.html`, `advisor-summary.html`, `flagged-review.html`, `data/flagged.json`, `assets/css/styles.css`, `assets/js/app.js` | Shared dashboard shell, `@media print` 1-page US Letter layout, 10 flagged audit entries |
| T-08 | Automated Link, Source, Privacy/PII, Math & Runtime Verification, PR Creation, Merge & GitHub Pages Confirmation | `in progress` | `arena/ae0d8ac3-jackbox2` | `scripts/build_data_bundle.mjs`, `scripts/verify_site.mjs`, `scripts/test_runtime.mjs`, `COORDINATION.md` | All automated checks passed (0 errors across 11 pages, 7 JSON datasets, 129 verified table rows); ready for PR, merge & live deploy check |

## Official Sources Verified (2026-11-25)
- **SEC EDGAR (Jack in the Box Inc., CIK `0000807882`):**
  - FY2023 Form 10-K: `https://www.sec.gov/Archives/edgar/data/807882/000080788223000020/jack-20231001.htm`
  - FY2025 Form 10-K: `https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm`
  - Q1–Q4 FY2025 Earnings Releases (`ex991-q125earningsrelease.htm` through `ex991-q425earningsrelease.htm`)
  - Q1–Q3 FY2026 Form 10-Q & Releases: `jack-20260118.htm`, `jack-20260412.htm`, `jack-20260705.htm`, `ex991-q326earningsrelease.htm`
  - Series 2026-1 `$500M` `7.624%` Securitized Notes Form 8-K (Jun 23, 2026): `https://www.sec.gov/Archives/edgar/data/807882/000080788226000079/jack-20260623.htm`
  - Executive Departures Form 8-K (Nov 17, 2026): `https://www.sec.gov/Archives/edgar/data/807882/000080788226000100/jack-20261113.htm`
- **Demographics, Labor, Economy, Education & Transit:**
  - U.S. Census Bureau QuickFacts & Profile (`census.gov`, `data.census.gov`)
  - California Dept. of Finance E-1 Report (May 2026) & K-12 Enrollment Projections (`dof.ca.gov`)
  - U.S. Bureau of Labor Statistics Metro Employment, Unemployment & LA CPI-U (Oct/Nov 2026, `bls.gov`)
  - California Employment Development Department 2025 Jobs Report (`edd.ca.gov`)
  - California Dept. of Education LAUSD Profile & 2024–25 CAASPP/Graduation Dashboard (`cde.ca.gov`)
  - California Dept. of Industrial Relations AB 1228 FAQ (`dir.ca.gov`) & LA City Office of Wage Standards (`wagesla.lacity.gov`)
  - LA Metro D Line Subway Extension (`metro.net`), LA City Planning (`planning.lacity.gov`), CA Legislature AB 2011 (`leginfo.legislature.ca.gov`), SCAG Connect SoCal 2024 (`scag.ca.gov`), Caltrans (`dot.ca.gov`)
- **Tax, Transfer Tax, Property Assessment & Capital Markets:**
  - IRS Topic No. 409, Publication 550 (2025), NIIT Q&A, 2026 Instructions for Form 8824 (`irs.gov`)
  - California Franchise Tax Board Capital Gains & Pub 1067 (`ftb.ca.gov`)
  - California Board of Equalization Prop 13 / Prop 19 (`boe.ca.gov`) & LA County Assessor (`assessor.lacounty.gov`)
  - LA County Registrar-Recorder/County Clerk Documentary Transfer Tax (`lavote.gov`)
  - City of Los Angeles Office of Finance Measure ULA FAQ (`finance.lacity.gov`)
  - U.S. Dept. of the Treasury Daily Par Yield Curve (Nov 24, 2026) & FRED `DGS10` (`home.treasury.gov`, `fred.stlouisfed.org`)
- **Physical Hazards & Insurance:**
  - USGS UCERF3 Los Angeles Earthquake Probabilities (`usgs.gov`)
  - California Geological Survey EQ Zapp & Nov 2025 Fault Zones (`conservation.ca.gov`)
  - FEMA Flood Map Service Center & Zone Definitions (`fema.gov`)
  - CAL FIRE Official Palisades & Eaton Fire Incident Pages & OSFM 2025 LRA FHSZ Maps (`fire.ca.gov`, `osfm.fire.ca.gov`)
  - California Dept. of Insurance FAIR Plan Orders `2025-1`, `2026-1`, `2026-2` (`insurance.ca.gov`)

## Verification Performed & Flagged Irregularities (Published on `flagged-review.html`)
- **Automated Verification (`scripts/verify_site.mjs` & `scripts/test_runtime.mjs`):**
  - 11 HTML pages verified `200 OK` over HTTP, zero JS syntax errors, zero DOM runtime exceptions.
  - Zero broken internal links; zero external CDN/tracking/analytics requests; zero PII patterns detected.
  - All 129 table rows (121 dynamic + 8 static) verified to include trusted `https://` official links.
  - Measure ULA post-June 30, 2026 cliff math (`$5.4M` / `$10.9M`) and Notice Calendar tool unit-tested.
- **Flagged Irregularities (`needs review` on `flagged-review.html` — non-blocking):**
  - `FLG-01`: Jack in the Box FY2026 Form 10-K / Q4 FY2026 actuals not yet filed on SEC EDGAR as of 2026-11-25 (cells blank).
  - `FLG-02` to `FLG-06`: Confidential private lease abstract, parcel trade area/jurisdiction, parcel hazard zones, broker BOV cap-rate quotes, and owner tax basis intentionally left BLANK for privacy & offline advisor verification.
  - `FLG-07`: LA County population estimate divergence between U.S. Census V2025 (`9,694,934`; LA City V2025 `NA`) and CA DOF Jan 2026 E-1 (`9,837,286`; LA City `3,806,201`).
  - `FLG-08`: BLS Nov 2026 West CPI table leaves Oct 2025–Oct 2026 12-month LA CPI-U `%` blank (`-`); verified Sep 2026 (`+3.7%`) reported without interpolation.
  - `FLG-09`: Partial quarterly sub-splits in Q1/Q2 FY2026 summary excerpts left blank rather than inferred.
  - `FLG-10`: Del Taco Discontinued Operations accounting recast (sold Dec 22, 2025); standalone Jack in the Box brand segment isolated throughout.

## PR & Deployment Record
- **PR URL:** Pending creation
- **Merge Status:** Pending merge
- **GitHub Pages Live URL:** `https://kanlerxz87-cyber.github.io/Jackbox2/` (Pending final deployment confirmation)
