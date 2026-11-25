# COORDINATION — Jack in the Box (Central LA) Decision Workspace

> Shared task board for parallel sessions. Claim a task by writing your session ID
> and file scope, then commit + push immediately. Never start a task another
> session has claimed. Keep scopes non-overlapping.

- **Session ID (this session):** `26811aa3`
- **Branch:** `arena/26811aa3-jackbox2` (branched from `main` @ `d1f3bf8`)
- **Privacy rule (highest urgency):** No personal identifiers, lease files, owner
  finances, APN, or exact parcel address on the public site. Use placeholders
  (`[PARCEL — WITHHELD]`, `[OWNER — WITHHELD]`). Publish only anonymous,
  aggregate findings. All parcel/owner records stay in the access-controlled
  internal workspace (not in this repo).
- **Verification rule:** Every table row carries a source link to an official
  source (`.gov` / SEC / exchange filing). If a value cannot be confirmed from
  an official source it is left blank and listed on the Flagged for Review page.
  Never infer or fill in values.

## Task board

| ID | Task | Status | Owner session | Files touched |
|----|------|--------|---------------|---------------|
| T-01 | Repo scaffold, COORDINATION.md, privacy + verification rules | done | 26811aa3 | `COORDINATION.md`, `README.md` |
| T-02 | Research pack — verified official sources only (Census, BLS, FRED, SEC, IRS, USGS, FEMA, CAL FIRE) | done | 26811aa3 | `sources.html` |
| T-03 | Landing dashboard + navigation + shared CSS/JS | done | 26811aa3 | `index.html`, `assets/*` |
| T-04 | Executive summary + decision-gate board (W-03) | done | 26811aa3 | `executive-summary.html`, `decision-gates.html` |
| T-05 | Trade-area & neighbourhood evidence (W-01, tract-level) | done | 26811aa3 | `trade-area.html` |
| T-06 | Parcel hazard screening framework (W-04) | done | 26811aa3 | `hazards.html` |
| T-07 | Sell-vs-hold + after-tax + browser calculator + short-lease discount (W-02) | done | 26811aa3 | `sell-vs-hold.html`, `assets/app.js` |
| T-08 | Risks & black-swan stress tests | done | 26811aa3 | `risks.html` |
| T-09 | Open questions & missing-info discovery plan | done | 26811aa3 | `questions.html` |
| T-10 | Suggestions & site-improvement backlog (review-before-implement) | done | 26811aa3 | `suggestions.html` |
| T-11 | Flagged for Review page + printable advisor summary (W-10) | done | 26811aa3 | `flagged.html`, `printable-summary.html` |
| T-12 | Final integration: re-verify, link-check, build check, PR → merge → Pages deploy | done | 26811aa3 | all (integration only) |

## Log

- 2026-11-25 — Session `26811aa3` created this board and claimed T-01/T-02.
  Repo was empty except `README.md`. No other sessions active.
- 2026-11-25 — Research verified against official sources (see `sources.html`):
  SEC Q3-2025 earnings release (same-store sales, unit counts, closures);
  Census QuickFacts / ACS via FRED (population, income, education);
  BLS LA metro (unemployment, payroll); FRED CALOSA7POP (population trend);
  IRS Topic 409 (capital-gains rates, §1250 recapture 25%);
  USGS MF-1964 (LA seismic risk); FEMA MSC (flood-map lookup);
  CAL FIRE FHSZ maps. Tract/parcel-level values withheld pending APN —
  listed as unverified on Flagged page, not estimated.

## Integration record

- PR: https://github.com/kanlerxz87-cyber/Jackbox2/pull/1 — **MERGED** 2026-11-25T13:39:26Z.
- GitHub Pages: https://kanlerxz87-cyber.github.io/Jackbox2/ — status `built`, deploy run `45625826028` success.
- Verification: internal link check passed (12 pages); every table row links to an official source; unverified = blank + flagged (F1–F10). No winner selected.

## Handoff rule

If a claim is >60 min old with no commits, another session may take over and
note the handoff here. Merge conflicts: stop, resolve without discarding the
other session's work, and log it here.

## Parallel integration handoff — session bdbaf9cc

- Independently created a privacy-first research dashboard before discovering main had been updated by session 26811aa3; both sessions started from an empty repository and neither could see the other's branch-local claim. PR #3 initially conflicted with PR #1/#2. Resolved by retaining main's shared files and preserving the separate dashboard in `alternative-research/`; no other session's work was discarded. Main navigation is unchanged to avoid modifying another session's scope. Alternative is available at `/Jackbox2/alternative-research/`.
- Alternative sources and limitations: [Census ACS comparison guidance](https://www.census.gov/programs-surveys/acs/guidance/comparing-acs-data.html), [IRS publication 544](https://www.irs.gov/publications/p544), [FEMA](https://msc.fema.gov/portal/home), [CAL FIRE](https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones), [USGS](https://www.usgs.gov/programs/earthquake-hazards), [issuer FY2025 report](https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Reports-Fourth-Quarter-and-Full-Year-2025-Earnings/default.aspx). Issuer data are primary disclosures, not independently verified property data. Missing parcel, lease, owner records, bids, tax and hazard status remain flagged; private workspace, complete tax model and validated projection are not provided.
- Alternative local link and table-source checks: `cd alternative-research && python3 tests/check.py`. Not all external links were checked. Pages configuration was already legacy main root; switching to workflow returned HTTP 403, so it was not changed.

---

## Parallel integration handoff — session fb776066

Independent claims were made from the initial commit before other sessions’ branch-local claims became visible. During PR #4 integration, origin/main already contained merged PRs #1–#3 and COORDINATION.md conflicted. Resolved by preserving the complete main board and appending this session’s board below. Root dashboard, alternative dashboard and existing Pages configuration remain unchanged; new dashboard is under docs/. No competing work was discarded. A pull-rebase after the initial merge tried to replay other sessions’ commits and conflicted; the rebase was aborted, the integration merge recreated after a clean pull-rebase, and all boards retained.

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
