# COORDINATION.md — Shared task board

Repo: `kanlerxz87-cyber/Jackbox2`
Purpose: Decision-support workspace for a single-tenant NNN quick-service restaurant
property in Central Los Angeles (Jack in the Box ground lease, expiry window 2030–2035).

> **Privacy rule (highest priority).** No owner name, entity name, address, APN, lease
> document, email, phone, bank, tax or financing detail may be committed to this repo or
> published on the site. Every such item is replaced with a placeholder token
> (`[OWNER-ENTITY]`, `[APN]`, `[STREET-ADDRESS]`, `[LEASE-FILE]`, …). The public site
> publishes aggregate, non-identifying findings only. See `docs/PRIVACY.md`.

---

## Session registry

| Session ID | Branch | Scope | Started (UTC) |
|---|---|---|---|
| `arena-21b26fee` | `arena/21b26fee-jackbox2` | Full task board (single session on this branch; see note below) | 2026-11-25 |

**Note on branches.** Arena tracks this work on one session branch
(`arena/21b26fee-jackbox2`). The task instructions describe `session-<id>/<task>`
worktrees for parallel sessions; no other session has claimed work here, so this session
holds all scopes on the single branch and keeps file scopes disjoint by directory to avoid
future conflicts (see **File scope map**).

---

## Task board

Status values: `unclaimed` · `in progress` · `done` · `needs review`.

| ID | Task | Status | Owner | File scope | Sources / verification notes |
|---|---|---|---|---|---|
| T-00 | Repository audit + coordination board | in progress | `arena-21b26fee` | `README.md`, `COORDINATION.md` | Audit: repo was a single 10-byte `README.md` stub at `d1f3bf8`; no site, no data, no pages. |
| T-01 | Privacy model + anonymization policy | in progress | `arena-21b26fee` | `docs/PRIVACY.md` | — |
| T-02 | Requirement register (line-by-line, R-xx) | in progress | `arena-21b26fee` | `data/requirements.json` | — |
| T-03 | Official-source evidence ledger | in progress | `arena-21b26fee` | `data/sources.json` | Every row links an official URL opened during this session. |
| T-04 | Regional macro & labour economics (W-01) | in progress | `arena-21b26fee` | `data/economy.json` | BLS LAUS Los Angeles County; BLS CES; Census/CA DOF population. |
| T-05 | Trade-area / tract evidence | in progress | `arena-21b26fee` | `data/trade_area.json` | Census ACS tract selection method; blocked items flagged. |
| T-06 | Property, lease & NNN structure placeholders | in progress | `arena-21b26fee` | `data/property.json` | Lease abstract cannot be produced without `[LEASE-FILE]`; flagged. |
| T-07 | Hazard screening (W-04) | in progress | `arena-21b26fee` | `data/hazards.json` | FEMA NFHL, CalFire FHSZ, USGS/CGS seismic, CalEnviroScreen. |
| T-08 | Sell-vs-hold + after-tax module (W-02) | in progress | `arena-21b26fee` | `data/valuation.json` | IRS Pub 946/544/1031 rules; Treasury curve for discounting. |
| T-09 | Short-lease discount from real quotes | in progress | `arena-21b26fee` | `data/valuation.json` | Comparable quotes are non-public → flagged unverified. |
| T-10 | Decision-gate board (W-03) | in progress | `arena-21b26fee` | `data/gates.json` | — |
| T-11 | Question / unknown register | in progress | `arena-21b26fee` | `data/questions.json` | — |
| T-12 | Risk register (base case + black swan) | in progress | `arena-21b26fee` | `data/risks.json` | — |
| T-13 | Site build (landing, category subpages, tables) | in progress | `arena-21b26fee` | `site/**` | — |
| T-14 | One-page printable advisor summary (W-10) | in progress | `arena-21b26fee` | `site/print.html` | — |
| T-15 | Suggestions review page | in progress | `arena-21b26fee` | `site/suggestions.html` | — |
| T-16 | Link + data integrity check | unclaimed | — | `tools/check.py` | — |
| T-17 | Integration: PR → merge → GitHub Pages deploy | unclaimed | — | `.github/workflows/**`, `COORDINATION.md` | — |

---

## File scope map (conflict avoidance)

| Directory / file | Sole writer |
|---|---|
| `data/*.json` (data layer, single source of truth) | `arena-21b26fee` |
| `site/*.html`, `site/assets/*` | `arena-21b26fee` |
| `docs/*.md` | `arena-21b26fee` |
| `tools/*` | `arena-21b26fee` |
| `COORDINATION.md`, `README.md` | integration session (this session, last commit) |
| `.github/workflows/*` | integration session (this session, last commit) |

Any future session must claim a row above by editing this table, commit and push the claim
**before** touching files, and must not edit a directory owned by another live session —
log a request here instead.

---

## Verification log

| Date (UTC) | Task | What was checked | Outcome |
|---|---|---|---|
| 2026-11-25 | T-00 | `git log`, full file tree, `gh auth status` | Repo contains only a stub `README.md`; GitHub auth valid for `kanlerxz87-cyber`. |
| 2026-11-25 | T-04 | `api.census.gov` (no key) via HTTP | Returns “Missing Key”; no ACS API access in this environment. |
| 2026-11-25 | T-04 | `data.bls.gov/timeseries/LAUCN060370000000003` | Official LAUS series for Los Angeles County renders with full monthly history — usable, verified. |
| 2026-11-25 | — | Direct `curl` to census.gov / bls.gov / www2.census.gov | Blocked (exit 35). Research channel is the page-fetch tool only; noted as a research limitation. |

---

## Irregularities flagged for review

| # | Item | Detail | Status |
|---|---|---|---|
| I-01 | No subject address / APN supplied | The request describes “a Jack in the Box in Central Los Angeles” with no address, APN, or lease file. Parcel-level screening (W-04) and any numeric valuation are **blocked**; only methodology and aggregate trade-area evidence can be published. | open |
| I-02 | Lease expiry given as a range (2030–2035) | A 5-year window cannot support a single exit date; every projection must be run as a range. Rent, escalations, options and remaining term are unverified. | open |
| I-03 | Census ACS API unavailable without a key | Tract-level income/population cannot be pulled directly; figures must be read from official published tables or left blank. | open |
| I-04 | Commercial comparable sales/rents are not public | CoStar/Reonomy/Crexi are paywalled and non-official; no verified comp set exists for the short-lease discount. Flagged, never inferred. | open |

---

## PR / deploy record

*(Filled by the integration step at the end of this session.)*
