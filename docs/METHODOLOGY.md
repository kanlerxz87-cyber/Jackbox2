# Methodology — how the projection spine is built, and what it will not do

## Purpose

The brief asks for "a reliable projection system for the area" and for "a versioned, cash-flow
model" that distinguishes observations from assumptions. This document defines how that is
built, what may enter it, and what disqualifies it. It is deliberately written before the model
exists, because a model written first and justified afterwards is how bad decisions get made.

## The four evidence classes

Every number entering the analysis carries exactly one class:

| Class | Definition | May it enter a projection? |
|---|---|---|
| **Observed** | Printed by an official source, quoted as-is with a link. | Yes — as a data point. |
| **Derived** | Arithmetic on observed values, with the formula shown. | Yes — as a data point, provided the formula is reproducible. |
| **Assumption** | A judgement with no official source behind it. | Yes, but it must be labelled in the output and stress-tested. |
| **Unverified** | Sought and not obtained. | **No.** It stays blank. It is never substituted with an estimate. |

A figure that cannot be classified does not enter the model.

## Versioning

Every model run records:

1. a version id and timestamp;
2. the source-ledger version (which `data/sources.json` was in force);
3. the full input vector, with each input's evidence class;
4. the code hash of the calculation;
5. the output, and a diff against the previous run.

A result that cannot be reproduced from its recorded input vector is discarded, not explained.

## The projection spine

The regional spine is built only from series that are actually published, at the smallest
geography available:

* **Employment** — BLS LAUS for the county, BLS CES for the metro area. Both obtained.
* **Prices** — BLS CPI-U and CPI-W for the metro area. Both obtained.
* **Population** — Census population estimates obtained at city level; the California
  Department of Finance county projections are the correct instrument for a forward view but
  their workbooks could not be opened in this environment, so **no projection is published**.
  Flagged as I-09.
* **Trade area** — the ACS tract set. Blocked on the parcel location; method specified in
  `data/trade_area.json`.

## What the spine is allowed to claim

The spine may claim **direction** from a series. It may not claim a **rate** from a short
series. Concretely:

* Two years of flat metro employment (+0.19%) supports "no growth cycle here". It does **not**
  support a projection of 0.1% growth per year for a decade.
* A six-year realised CPI growth of 3.79%/yr supports "test the escalation clause against
  roughly 3.8%". It does **not** support asserting 3.8% as the indexation rate in the lease.
* A 10-year Treasury at 4.92% supports "the risk-free anchor is 4.92%". It does **not** support
  a discount rate, because the spread above it is unverified.

## Back-testing, and when it is meaningful

Back-testing requires at least one full cycle of comparable history **for the thing being
modelled**. For a single restaurant parcel, that means unit-level sales across a downturn —
which is not public and not available. Therefore:

* the model may be back-tested on the **regional spine** (does a rent-escalation assumption
  track observed CPI over 2019–2025? — yes, this is testable and is done);
* the model may **not** be back-tested on the property's own cash flows until verified inputs
  and sufficient comparable history exist. Gate G-09 stays open until they do.

Claiming a property-level back-test with no property-level history would be the most
sophisticated form of fabrication available in this project, and it is explicitly refused.

## Stress design

The three hazard legs — loss of rent, repair cost, exit liquidity — are correlated, not
independent, because a regional event triggers all three simultaneously. The model therefore
runs them as a single joint scenario rather than three marginal cases. Treated marginally, the
tail is understated by a wide margin.

For the observed severe shock, the spine uses the Los Angeles County unemployment peak of
**18.9% in May 2020** (BLS LAUS) as the anchor, because it is the last verified severe
disruption rather than an invented one.

## What disqualifies a model

* Any unverified input, however "reasonable".
* A discount rate without a documented comparable spread.
* A property-level back-test without property-level history.
* A point estimate where the input is a range. The lease expiration is a 2030–2035 range, so
  every output is a range until gate G-04 closes.
* An assumption that is not visible in the output the owner reads.
