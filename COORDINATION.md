# Coordination board

Sessions must check this board and remote branches before claiming work. The Arena-assigned branch is fixed for this session and takes precedence over the requested session branch naming convention.

| Task | Status | Owner / claimed UTC | File scope |
| --- | --- | --- | --- |
| Research, privacy-first dashboard, verification and integration | in progress | arena-2dd721f3 / 2026-11-25 | `index.html`, `assets/`, `scripts/`, `.github/`, `README.md`, `COORDINATION.md` |

## Log

- 2026-11-25: Initial repository contains only `README.md`; no existing board or other remote work branches were present. Claiming integrated work on the fixed Arena branch. Other sessions should not edit the scoped files; log coordination requests here.

## Verification and concurrency note — 2026-11-25

- Source cross-checks: [Census city QuickFacts](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,ca) and [county QuickFacts](https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia,ca) for geography, income and population; [BLS](https://www.bls.gov/opub/ted/2026/unemployment-rates-lower-in-226-metro-areas-from-september-2025-to-september-2026.htm) for metropolitan unemployment; [company FY2025 release](https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Reports-Fourth-Quarter-and-Full-Year-2025-Earnings/default.aspx) for brand results. Company disclosures are primary sources, not independent confirmation of a specific location. The Census three-geography URL initially selected could not be fetched, so it was replaced by separately checked city and county URLs. [Caltrans](https://dot.ca.gov/programs/traffic-operations/census) states its counts cover state highways, not city streets. [CAL FIRE](https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones) distinguishes mapped hazard from risk. Other guidance links include [IRS Pub 544](https://www.irs.gov/publications/p544), [IRS Pub 551](https://www.irs.gov/publications/p551), [FEMA](https://www.fema.gov/flood-maps) and [California Geological Survey](https://www.conservation.ca.gov/cgs/Pages/_Maps-and-Data-Home.aspx).
- `python3 scripts/check.py` passes internal links, table source links and static privacy checks; `node scripts/test-calculator.js` checks arithmetic, zero discount rate and reset. This is not an exhaustive automated test of all external sites or a line-by-line verification of all claims on other branches.
- Missing parcel, lease, financials, bids and owner preferences prevent tract selection, parcel screening, tax computation, a real short-lease discount and a reliable back-tested projection. No private adviser workspace or engagement has been created. These are marked for review on this branch, not treated as verified.
- **Concurrency / integration request:** When this session claimed its scope there were no remote work branches and no board; subsequently, parallel sessions appeared and `main` advanced independently through PRs #1 and #2, with PR #3 open from another session. Their scopes overlap this branch's dashboard and board. Our initial boards were independently created from the same empty base; they were not shared at claim time. Do not overwrite or merge over another session's work. An integration owner should reconcile board histories, review differing site implementations, re-verify external links and data, and avoid replacing their live site wholesale. This branch's implementation remains in progress pending that reconciliation.
