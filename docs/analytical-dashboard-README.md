# Jackbox2 — decision support for a single NNN Jack in the Box ground lease

A source-linked, privacy-first workspace for one question:

> The property is a single-tenant Jack in the Box under a NNN lease in Central Los Angeles,
> expiring somewhere between **2030 and 2035**. Should the owner **sell before expiry** or
> **renew**, and what should happen before either commitment is made?

**Live site:** https://kanlerxz87-cyber.github.io/Jackbox2/

---

## What this repository is

It is **not** an appraisal and it contains **no price**. It is the organised evidence base,
the register of what is missing, and the completed comparison structure — so that the moment
real inputs arrive, the decision can be made from arithmetic rather than opinion.

Three principles are enforced mechanically rather than promised:

1. **Nothing is published without an official source link.** Every figure traces to a Tier 1
   document (SEC, BLS, Census, IRS, California agencies, FEMA, USGS, CAL FIRE, CGS). Where a
   value could not be confirmed, it is left **blank** and flagged — never estimated.
2. **No identifier is ever committed.** The data layer has no field for a name, address, parcel
   number or financial record. Privacy is structural, not a redaction step. See
   [`docs/PRIVACY.md`](docs/PRIVACY.md).
3. **Observation, derivation and assumption are labelled separately,** and verified tax rules
   are kept distinct from the formula templates that await inputs.

## Layout

```
data/          verified evidence layer — the single source of truth for the site
  sources.json      23 sources with tier, status and limitation notes
  requirements.json the brief decomposed line by line, with honest statuses
  economy.json      BLS / Census / SEC-derived regional and tenant evidence
  trade_area.json   W-01 method; trade-area figures pending (flagged)
  hazards.json      W-04 seismic / flood / fire screening + stress design
  property.json     lease-abstract schema — empty by design
  valuation.json    verified tax rules + sell and hold formula templates
  gates.json        W-03 twelve decision gates and their sequencing
  questions.json    30 questions, each with a route to its answer
  risks.json        risk by decision path + black-swan block + recommended course
  suggestions.json  ten site improvements + three paths to choose from
docs/          privacy model and methodology
site/          built static site (generated — do not hand-edit)
tools/         build.py (generator) and check.py (integrity + privacy checks)
COORDINATION.md shared task board, verification log and irregularities
```

## Build

```bash
python3 tools/build.py   # regenerate site/*.html from data/*.json
python3 tools/check.py   # link integrity, source allowlist, privacy patterns
```

The build fails if any row cites a source id that is not in `data/sources.json`. The check
fails if any internal link is broken, any external link is not an approved official host, any
identifier pattern appears in the output, or the calculator gains any network capability.

Deployment is automatic on push to `main` via GitHub Actions + GitHub Pages.

## Key findings at a glance

| Finding | Value | Source |
|---|---|---|
| Metro employment vs October 2019 | +1.29% | BLS CES (derived) |
| Metro employment vs October 2024 | +0.19% | BLS CES (derived) |
| City population, 2020 → 2025 | −0.8% | Census QuickFacts |
| LA CPI-U, 12-month | +3.7% | BLS |
| LA CPI-U compound growth 2019–2025 | 3.79%/yr | BLS (derived) |
| Tenant same-store sales, FY2025 | −4.2% | SEC 8-K exhibit 99.1 |
| Tenant same-store sales, Q4 FY2025 | −7.4% | SEC 8-K exhibit 99.1 |
| Tenant closures, FY2025 | 86 units | SEC 8-K exhibit 99.1 |
| Tenant guidance, FY2026 closures | 50–100 units | SEC 8-K exhibit 99.1 |
| Tenant total debt / guided EBITDA | ≈7.3× | SEC (derived) |
| 10-year Treasury | 4.92% | Federal Reserve H.15 via FRED |

**Decision readiness: 0 of 12 gates closed.** The direction of the evidence is legible — the
weight favours acting, and specifically favours selling once a real price exists. The magnitude
is not, because rent, term, obligor, basis, price and parcel hazard status are all unknown.
See the [course of action](https://kanlerxz87-cyber.github.io/Jackbox2/decision.html) page.

## Flagged items

Ten irregularities are published openly on the
[Flagged for review](https://kanlerxz87-cyber.github.io/Jackbox2/flagged.html) page, each with
its severity and the exact route to resolution. The three critical ones are: no address or APN
supplied, lease expiry given as a five-year range, and the obligor's identity unverified
(brand versus franchisee).

## Limitations disclosed

This session could read web pages but could not download binary files or call data APIs.
That blocked the California Department of Finance projection workbooks and the Census ACS API;
both gaps are recorded rather than filled with estimates. Commercial comparable data is
paywalled and non-official, so the short-lease discount is flagged as unverifiable — with a
free route to fixing it via recorded county grant deeds and documentary transfer tax stamps.

## Not advice

Nothing here is an appraisal, a valuation, or legal, tax or investment advice. Engage licensed
advisers before acting.
