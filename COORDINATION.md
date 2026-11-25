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
- PR #3 https://github.com/kanlerxz87-cyber/Jackbox2/pull/3 merged as bb5e90bf619e8149edffba0fb08904644be0df33. Legacy Pages build/deploy run https://github.com/kanlerxz87-cyber/Jackbox2/actions/runs/45626308715 succeeded; Pages API reported built at that commit. A separate pre-existing `Deploy static content to Pages` run https://github.com/kanlerxz87-cyber/Jackbox2/actions/runs/45626308516 failed; its logs could not be retrieved. This does not alter the successful legacy deployment but needs owner review. Node 20 action deprecation warning was emitted by legacy build.
- The required pull --rebase attempted to flatten the parallel integration merge and produced conflicts; aborted it without discarding either session, confirmed the remote branch was an ancestor, and pushed the resolved merge. Subsequent pull performed after synchronization.
