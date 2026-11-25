# Coordination board

| Task | Status | Owner | Scope |
|---|---|---|---|
| Integrated privacy-first decision dashboard, sources, tests and deployment | in progress | bdbaf9cc | site files, tests, workflow, README, COORDINATION.md |

No other claims existed when this board was created. The Arena session is restricted to its assigned branch; it serves as the integration session.

## Integration notes — 2026-11-25
- Static dashboard and browser-only arithmetic comparison implemented; local navigation and a source link in each data row checked with `python3 tests/check.py`.
- Primary sources: [Census ACS comparison guidance](https://www.census.gov/programs-surveys/acs/guidance/comparing-acs-data.html), [IRS publication 544](https://www.irs.gov/publications/p544), [FEMA map service](https://msc.fema.gov/portal/home), [CAL FIRE](https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones), [USGS](https://www.usgs.gov/programs/earthquake-hazards), and [issuer FY2025 report](https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Reports-Fourth-Quarter-and-Full-Year-2025-Earnings/default.aspx). Issuer data are primary disclosures, not independently verified property data.
- Irregularities: address, lease, owner records, bids, tax and hazard status unavailable; all property-specific values flagged, not invented. No private workspace provisioned; no full tax model or back-tested projection is possible with available inputs. Some source links are research starting points, not proof of a private fact. No claim of exhaustive external link or line-by-line verification is made.
