# Jack in the Box — Central Los Angeles property decision workspace

A public, static evidence and decision-support site for an **anonymous** Jack in the Box NNN property described in the project brief as being in the Central Los Angeles area, with a lease-expiry window of 2030–2035. Those property and lease particulars are user-supplied, not independently verified.

## Start here

- **[Dashboard](index.html)** — landing page and current-workspace navigation.
- **[Central LA 2026 evidence workspace](central-la-2026/index.html)** — latest dated workstream dashboard (evidence cutoff stated on its pages); includes trade-area evidence framework, tenant disclosures, hazard framework, gate board, browser-only calculator, questions, suggestions, advisor summary, and Flagged for Review.
- **[Flagged for Review](central-la-2026/flagged-review.html)** — missing private inputs, unresolved geography, pending data, and limitations.
- **[Printable advisor summary](central-la-2026/advisor-summary.html)**.
- **[Privacy-first workflow](privacy-first/index.html)** — additional privacy and process materials.

Other analytical and historical dashboards are retained in `site/`, `docs/`, `alternative-research/`, and `docs/arena-75e09b85/`. Their reporting cutoffs and scope differ. They are supporting/archival material, not interchangeable snapshots; use the dated source and limitations on each page. Do not treat older dashboard values as current.

## Decision posture

**No sell, renew, or hold winner is selected.** The public workspace does not contain the executed lease, verified notice deadlines, parcel identity, verified rent/NOI, basis/depreciation, broker bids, exact tract set, or parcel-level hazard/insurance determinations. The brief's expiry window is not a substitute for a lease abstract. A decision should follow the documented gates and private verification with authorized legal, tax, brokerage, and insurance advisers.

## Privacy boundary

This repository and the GitHub Pages site are public. They are **not** an access-controlled internal workspace. Do not add an owner name, address, APN, lease file, owner financial information, contact details, or other identifying information here. Keep those materials offline in a suitably access-controlled adviser workflow. The calculator runs in the reader's browser and does not provide a secure vault; do not enter sensitive facts on a shared or untrusted device. Public reporting should remain aggregate and non-identifying.

## Verification policy

- Use primary official sources for public facts where available (SEC EDGAR, Census, BLS, IRS, state/local agencies, USGS, FEMA, CAL FIRE).
- A linked source supports only the specific public fact stated; it does not verify this private property's attributes.
- Leave unknown property-specific values blank and list the route to verify them on **Flagged for Review**. Do not infer results from a county or city proxy.
- Regional hazard rates are context, not parcel hazard status. Brokerage opinions and comparable transactions are not available unless specifically sourced and documented.
- Model outputs are scenarios, not a forecast, valuation, legal opinion, or tax advice. No recommendation is calculated until verified inputs exist.

## Repository layout and checks

| Path | Purpose |
|---|---|
| `central-la-2026/` | Dated W-01–W-10 dashboard, its JSON evidence, browser scripts, and verification scripts |
| `index.html`, root `*-*.html` | Public landing and supporting pages |
| `data/`, `tools/` | Analytical evidence layer, generator, and checks |
| `privacy-first/`, `site/`, `docs/`, `alternative-research/` | Additional/archival dashboards and supporting documents |
| `COORDINATION.md` | Historical task log and current audit notes |

Run from repository root:

```sh
python3 tests/check_site.py
node tests/calc.test.js
python3 tools/build.py
python3 tools/check.py
python3 privacy-first/tests/check.py
python3 alternative-research/tests/check.py
(cd central-la-2026 && node scripts/verify_site.mjs && node scripts/test_runtime.mjs)
```

The checks validate local links, provenance markup, data shape, privacy patterns, and calculator/runtime behavior. They do **not** independently verify every external source's current availability or prove every fact correct; source review and flagged limitations remain necessary.

## GitHub Pages

The repository's configured Pages endpoint is [kanlerxz87-cyber.github.io/Jackbox2](https://kanlerxz87-cyber.github.io/Jackbox2/). The primary dated dashboard is available at [`/central-la-2026/`](https://kanlerxz87-cyber.github.io/Jackbox2/central-la-2026/).
