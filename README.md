# Jack in the Box — Central Los Angeles decision workspace

An anonymous, source-linked workspace for one decision: **sell this single-tenant Jack in the Box net-lease
parcel before the lease expires, or renew it?** The lease expiry window is 2030–2035 according to the owner's
brief and is not yet verified against the lease.

The site does not answer that question. On verified evidence, neither branch can be priced, so the deliverable
is a decision-gate sequence, the incidence of each risk, and the arithmetic that turns verified inputs into one
comparable number the day those inputs arrive.

## Two rules that shape everything

**Privacy.** No owner name, entity, street address, parcel number, lease document or owner financial record is
published. Placeholders are used (`[PARCEL — WITHHELD]`, `[OWNER — WITHHELD]`). Those records stay with
authorised advisers in an access-controlled internal workspace. Only aggregate, non-identifying findings appear
on the site. See the [privacy page](privacy.html).

**Verification.** Every published figure links to the official page that printed it and carries the date it was
read. Where a value could not be confirmed it is left blank and listed on the
[Flagged for review](flagged.html) page with the official link needed to check it. No value is inferred,
estimated, interpolated or copied from another dashboard.

## The site (static, no build step required to view)

Live site: **https://kanlerxz87-cyber.github.io/Jackbox2/**

| Page | Purpose |
|---|---|
| `index.html` | Landing dashboard, key verified figures, archive of earlier parallel work |
| `executive-summary.html` | Bottom line, three candidate paths with written tests, the eight-week sequence |
| `decision-gates.html` | Seven gates in order, the artefact that clears each, what reopens it |
| `verification.html` | Line-by-line ledger: every figure, source, period and check date |
| `flagged.html` | Twenty blank items with the exact check to run, plus irregularities found |
| `trade-area.html` | County and metro context, explicitly labelled as context; tract selection rule |
| `hazards.html` | Earthquake, flood, fire and insurance screening; the three stresses run together |
| `sell-vs-hold.html` | After-tax module, short-lease discount priced from quotes, what would make it a comparison |
| `calculator.html` | Private browser calculator: no network, no storage, nothing sent anywhere |
| `risks.html` | Risk by decision, black swan register, three thresholds that make "manageable" checkable |
| `questions.html` | 28 questions with owner, document, gate and what changes with the answer |
| `suggestions.html` | 15 proposals, ordered; site changes left unimplemented for review |
| `sources.html` | Official source register and the hierarchy applied |
| `printable-summary.html` | One page for advisers |
| `privacy.html` | What is published, what is withheld, how the layers are separated |

## Build and check

```bash
python3 tools/build_root.py      # regenerate all 15 pages from data/root.json
python3 tests/check_root.py      # provenance, links, privacy patterns, calculator inertness
```

`tools/build_root.py` refuses to render a verified value without a known source id, and renders an empty cell
for any row not marked verified. `tests/check_root.py` fails on a missing source, a broken internal link, a
non-official external host, an identifier pattern, or a single line of network or storage code in the
calculator.

The data layer is `data/root.json`: sources, findings, gates, risks, black swans, questions, suggestions and
flags. Nothing in it identifies the property or the owner.

## Archive — earlier parallel work, kept and dated

Several sessions worked on this repository concurrently. Their dashboards are retained rather than deleted.
They do not agree on every figure because they were built at different cut-off dates; this site's
[verification ledger](verification.html) is the reference.

| Location | What it is | Cut-off it states |
|---|---|---|
| `central-la-2026/index.html` | Eleven-page refresh with notice calendar and local calculator | Verified through 25 November 2026; FY2026 Q1–Q3 |
| `site/index.html` | Analytical dashboard generated from `data/` by `tools/build.py` | FY2025 fourth-quarter and full-year release |
| `docs/index.html` | Session fb776066 pages | FY2025 filings |
| `docs/arena-75e09b85/index.html` | Session 75e09b85 pages | FY2025 filings |
| `privacy-first/index.html` | Conservative no-fabrication framework | Framework only |
| `alternative-research/index.html` | Independent second research pass | FY2025 issuer report |

## What this repository deliberately does not contain

- Personal or parcel-identifying information.
- A property valuation, appraisal, cap rate or sale price.
- A projection or forecast for the trade area, because a defensible projection needs verified inputs and
  back-testing that do not yet exist.
- A recommendation to sell or to renew.

## Coordination and change history

Session claims, evidence logs, handoffs and merge records are in [`COORDINATION.md`](COORDINATION.md).
Contributions are welcome, subject to the two rules above: no identifiers, and no unsourced figure.

Nothing here is legal, tax, appraisal or investment advice.

## Repository status after consolidation

The three navigation groups above are the single entry point. Independently built dashboards are preserved in
`central-la-2026/`, `site/`, `docs/`, `docs/arena-75e09b85/`, `privacy-first/` and `alternative-research/`.
They are separately maintained outputs with their own cut-off dates and their own flagged pages — not a
synchronised copy of this site. Do not assume a figure in one applies to another; the
[verification ledger](verification.html) states the period for every value published here.

## Full check set

```bash
python3 tests/check_dashboard.py   # this site: provenance, links, privacy, calculator
node    tests/calc_root.test.js    # this site's calculator arithmetic and inertness
python3 tests/check_root.py        # repo-wide: conflict markers, every local link, PII, root tables
node    tests/root_calc.test.js    # legacy root calculator
python3 tests/check_site.py        # analytical dashboard links and provenance
node    tests/calc.test.js         # analytical dashboard calculator
python3 tools/build.py && python3 tools/check.py
python3 privacy-first/tests/check.py
cd alternative-research && python3 tests/check.py
cd central-la-2026 && node scripts/verify_site.mjs && node scripts/test_runtime.mjs
```

A passing check establishes structure, provenance wiring and the absence of identifier patterns. It does not
prove that an external page still says what it said on the check date, which is why every row carries its
own date.
