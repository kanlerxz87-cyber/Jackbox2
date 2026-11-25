# Property Decision Desk

A public, anonymous static decision-support site for an unidentified single-tenant restaurant property. The case description is user-reported and unverified. No property or owner records belong in this public repository, GitHub Pages, browser inputs on untrusted devices, issue trackers, or pull requests.

## Build and test

The generated HTML pages are committed so GitHub Pages can publish them from the root of `main`. Regenerate them with `python3 scripts/build.py`; run `python3 scripts/check.py` to validate internal navigation, table-source links, generated output and privacy-sensitive browser behavior. No dependencies or server are needed. Open `index.html` or serve the directory using any static server. Links to external primary sources may change and should be periodically reviewed.

The optional calculator uses in-memory browser JavaScript only, no backend, storage, cookies, analytics or third-party resources. It accepts adviser-provided aggregate financial assumptions, not personal identifiers. It uses CPA-estimated tax totals, not a tax rules engine. Its constant annual cash flow simplification is not a fully versioned forecast. Do not enter sensitive information on a shared or untrusted device.

The repository is public and does not provide the access-controlled workspace the analysis requires. Formal counsel, engineering, insurance, valuation and tax review must be arranged privately; no adviser engagement or parcel screening is implied.
