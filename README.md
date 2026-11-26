# Jack in the Box — Central Los Angeles Decision Workspace

A public, anonymous decision-support site for the scenario described in the brief: a Jack in the Box NNN property in Central Los Angeles with an unverified lease-expiry window of 2030–2035. The repository does **not** contain an address, APN, lease, owner identity, tax records, bids, or other private inputs.

## Start here

- [`index.html`](index.html) — simple landing dashboard and main site navigation.
- [`central-la-2026/index.html`](central-la-2026/index.html) — expanded November 2026 research dashboard, including tenant filings through Q3 FY2026, lease/notice workflow, market context, hazards framework, questions, and a browser calculator.
- [`site/index.html`](site/index.html) — evidence-led analytical dashboard generated from `data/` by `tools/build.py`.
- [`flagged.html`](flagged.html) — root dashboard's review items; each expanded dashboard has its own corresponding flagged page.

The repository also preserves independently built dashboards in `privacy-first/`, `alternative-research/`, `docs/`, and `docs/arena-75e09b85/`. These are separately maintained outputs, not a single synchronized application. Check each dashboard's own sources, cutoff and flagged items; do not assume a figure in one dashboard applies to another.

## Decision rule

**No sell/renew winner is selected.** The lease abstract, exact notice dates, current sale bids, renewal economics, tax basis, parcel-level hazards and trade-area evidence, and the owner's objectives are not present in this public repository. Aggregate regional indicators and tenant-wide disclosures are context only, not parcel-level proof. A qualified adviser team must verify the missing inputs and compare sale and hold outcomes on a consistent after-tax basis before a commitment.

## Privacy

Personal information and property identifiers must stay offline with authorized advisers in an access-controlled workspace. This public repository is not that workspace. Do not submit confidential or identifying information to the site or commit it here. Public pages use placeholders and aggregate information only. See [`docs/PRIVACY.md`](docs/PRIVACY.md).

## Verification

The site distinguishes observations, derived values, legal rules, templates and unverified inputs. Missing values are left blank and listed on a “Flagged for Review” page. A passing local checker establishes structural checks only; it does not independently establish the correctness or continued availability of every external source.

Run the core checks from the repository root:

```sh
python3 tests/check_site.py
node tests/calc.test.js
python3 tools/build.py
python3 tools/check.py
python3 privacy-first/tests/check.py
```

For the November 2026 dashboard's own checks, run from its directory:

```sh
cd central-la-2026
node scripts/verify_site.mjs
node scripts/test_runtime.mjs
```

## GitHub Pages

This repository is configured to publish its static root via GitHub Pages. The site is plain HTML/CSS/JavaScript; no visitor account or server-side calculator is used. The private worksheet runs in the reader's browser, but it is not an access-controlled private workspace—do not enter sensitive information on a shared or untrusted device.


## Independent dashboard map

The repository preserves several separately maintained static dashboards. They are not a synchronized application and may use different cutoffs or gate structures. Review each dashboard's source ledger and Flagged for Review page; do not assume the contents agree.

| Dashboard | Entry point | Notes |
|---|---|---|
| Root | `index.html` | Main landing page, with supporting root-level sections and the root source audit. |
| Central LA 2026 | `central-la-2026/index.html` | Separate W-01–W-10 dashboard; see its own source and flagged pages. |
| Analytical | `site/index.html` | Generated from `data/` by `tools/build.py`; the focused decision-neutrality audit is recorded here. |
| Alternative research | `alternative-research/index.html` | Independent research pass. |
| Docs | `docs/index.html` | Separate documentation dashboard. |
| Privacy-first | `privacy-first/index.html` | Privacy and decision-gate workflow. |
| Archived session workspace | `docs/arena-75e09b85/index.html` | Additional independent research artifact. |

The core validation commands also include `python3 tests/check_root.py` and `node tests/root_calc.test.js`; these validate root table provenance, privacy, links and calculator arithmetic. The checks are structural and do not replace adviser review or a fresh source verification.
