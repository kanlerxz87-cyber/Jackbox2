# Anonymous property decision workspace

A privacy-first GitHub Pages dashboard for comparing a possible sale with a negotiated renewal of an anonymous Central Los Angeles quick-service property. The brief describes an NNN lease with a 2030–2035 expiry window; neither the lease nor the exact expiry has been verified. **No sale or renewal winner is selected.**

The immediate recommendation is procedural: have counsel commission a private lease abstract and reconcile the notice calendar, while authorized advisers obtain written comparable quotes, a CPA-specific after-tax analysis, parcel-level hazard and insurance evidence, and the owner's objectives. None of that private work has been commissioned or verified by this website.

## Privacy and evidence

- This is a **public** site, not an access-controlled internal workspace. Never publish names, entity details, address, parcel number, lease documents, owner finances, quotes, or identifying local research in the repository, issues, pull requests, screenshots, or deployment. Private records belong with authorized advisers in a separately controlled workspace; no such workspace has been created by this project.
- Public observations use official agency, SEC, Federal Reserve or issuer-primary sources, with periods and links. Unknown property-specific values stay blank and are [flagged](flagged.html). Sources on discovery and process rows are context, not proof of private facts.
- Every canonical root table row carries a source/reference link. The structural tests check links and patterns; they cannot guarantee the truth or freshness of external pages, anonymity against re-identification, or privacy on an untrusted device.
- The public website, ordinary hosting logs, browser, extensions and external lookups have their own privacy risks. The worksheet's JavaScript intentionally makes no network or persistent-storage calls; its best-effort clear on page exit is not a device privacy guarantee. Use a trusted device and an offline copy where practical.

## Main pages

| Page | Purpose |
|---|---|
| `index.html` | Dashboard, decision posture and links to preserved earlier dashboards |
| `executive-summary.html` / `decision-gates.html` | No-winner recommendation, evidence gates and private notice-calendar process |
| `trade-area.html` / `tenant.html` | Regional context and multi-period issuer disclosures, with local gaps kept blank |
| `hazards.html` / `risks.html` | Parcel-screening routes, ordinary risks and combined catastrophe/rent/exit stresses |
| `sell-vs-hold.html` / `calculator.html` | Same optional, blank-by-default worksheet for adviser-supplied after-tax equity cash flows and comparable quotes |
| `projection.html` | Versioned development and walk-forward back-test protocol, not a forecast |
| `questions.html` / `suggestions.html` | Private discovery routes and proposals for review before implementation |
| `printable-summary.html` | Anonymous, print-oriented adviser brief |
| `verification.html` / `sources.html` / `flagged.html` / `requirements.html` | Source ledger, reference library, open discrepancies and honest delivery status |
| `privacy.html` | Public/private boundary and residual risks |
| `audit/index.html` | Independent publication-integrity audit and limits on archival provenance |

The worksheet does **not** calculate tax, infer a lease discount, forecast a sale price, or recommend a winner. It requires a CPA-supplied incremental sale tax, all sale costs and debt, after-tax annual hold equity cash flows, terminal after-tax equity, and a consistent annual discount rate. All fields are blank; an explicit zero is accepted only when supplied. Quote arithmetic is not a market observation until actual matched quotes are obtained. It cannot replace professional review of basis, §1250, NIIT, California tax, transfer taxes, §1031 timing, entity structure or future cash needs.

## Build and verify

A static copy works without a server. To regenerate the canonical root pages and run the local checks:

```bash
python3 tools/build_root.py                 # current canonical build; preserves the prior source ledger
python3 tests/root_check.py                 # every root table row, links, privacy patterns, reproducibility
python3 tests/check_dashboard.py            # ledger structure, source allowlist and site checks
python3 tests/check_root.py                 # repository links, conflict markers, PII patterns
node tests/calc_root.test.js                # generated worksheet and like-for-like arithmetic
node tests/root_calc.test.js                # explicit-zero and invalid-input regression cases
node tests/root_calculator.test.js          # arithmetic, quotes, clearing and browser harness
python3 tests/check_site.py && node tests/calc.test.js
python3 tools/build.py && python3 tools/check.py
python3 tools/public_site_audit.py && python3 tests/test_public_site_audit.py
python3 privacy-first/tests/check.py
(cd alternative-research && python3 tests/check.py)
(cd central-la-2026 && node scripts/verify_site.mjs && node scripts/test_runtime.mjs)
```

`tests/root_build.py` is the canonical renderer, invoked by `tools/build_root.py`. It retains the completed parallel integration's `data/root.json` ledger, flags, questions and proposals. The previous generator templates are retained in `tools/build_root.py` as historical work, but its old embedded calculator and markup were unsafe and are never used by the supported build. `assets/app.js` is the reviewed worksheet source; the build copies it to `assets/calc.js` for the published page. CI checks that the files match and that generated pages are reproducible.

## Earlier parallel work, preserved

These independently maintained dashboards remain in the repository with their own cutoffs, caveats and source registers. They are not synchronized with the canonical root site. In particular, some historical calculators compare pre-tax or partially taxed hold values with after-tax sale proceeds or use illustrative defaults; **do not rely on those outputs without an independent audit**. See the [review register](flagged.html).

| Location | Historical dashboard |
|---|---|
| `central-la-2026/index.html` | FY2026 Q1–Q3 research refresh and notice calendar |
| `site/index.html` | Analytical dashboard generated from the separate `data/` layer |
| `docs/index.html` | Earlier research and decision framework |
| `docs/arena-75e09b85/index.html` | Independent research pages |
| `privacy-first/index.html` | Conservative no-fabrication framework |
| `alternative-research/index.html` | Independent second research pass |

Session claims, evidence logs, handoffs, conflicts and deployment records are in [`COORDINATION.md`](COORDINATION.md). Nothing here is legal, tax, appraisal or investment advice.
