# Privacy policy and anonymisation model

This document is the governing rule for the repository. If any other file appears to conflict
with it, this file wins.

## The single rule

> **No identifier is ever committed, and no identifier is ever published.**
> The public site is assembled from `data/*.json`, and those files contain **no identifier
> fields at all** — not empty ones, not masked ones. There is nowhere in the data model for a
> name, an address, a parcel number or a bank balance to be stored. Privacy here is
> structural, not a redaction step applied afterwards.

## Placeholder tokens

| Token | Replaces | Held where |
|---|---|---|
| `[OWNER-ENTITY]` | legal owner / borrowing entity | offline |
| `[STREET-ADDRESS]` | street address | offline |
| `[APN]` | assessor's parcel number | offline |
| `[LEASE-FILE]` | executed lease and amendments | offline |
| `[SITE-PLAN]` / `[SURVEY]` | site plan, ALTA survey | offline |
| `[TITLE-REPORT]` | title commitment | offline |
| `[INSURANCE-POLICY]` | certificate of insurance, loss runs | offline |
| `[TAX-RETURNS]` | owner returns, basis, depreciation history | offline — never in this repo |
| `[TENANT-FINANCIALS]` | franchisee/guarantor financials | offline, under confidentiality |
| `[BROKER-QUOTE-1..3]` | written market quotes | offline; entered only into the browser calculator |

## What may be published

Only **aggregate, non-identifying findings**:

* government statistics about a county, city or metro area, cited to the agency that released them;
* statements of law or regulation from a primary source;
* the tenant's own public SEC disclosures, which are public by law;
* methodology, gate definitions, question registers, risk registers and formula templates;
* the *fact* that a value is unknown, with the route to obtaining it.

## What may never be published

* any person's name, email, phone number, or postal address;
* the property's street address or parcel number;
* the owner's entity name, tax position, basis, income, or net worth;
* rent, sales, or guaranty figures from the private lease file;
* broker bids or quotes;
* anything that would let a reader identify the parcel by combining published facts.

## The combination rule

Individual aggregate facts can become identifying when combined. The specific risk here is
that "a Jack in the Box in Central Los Angeles with a lease expiring between 2030 and 2035"
plus a narrow geographic descriptor could narrow to a small set of parcels. For that reason:

* submarket is described only as broadly as the brief describes it ("Central Los Angeles");
* no map, no coordinates, no tract id, no drive-time ring is published — the method is
  published, the result is not;
* no trade-area figure is published until the ring is defined *and* the ring is wide enough
  that it cannot be inverted to a parcel.

## Enforcement

`tools/check.py` fails the build on any of the following appearing in `site/` or `data/`:

1. a US ZIP code pattern (`\b\d{5}(-\d{4})?\b`) — note that published statistics are quoted
   without ZIP codes for this reason;
2. a street-address pattern (number followed by a street suffix such as St, Ave, Blvd, Rd);
3. an assessor parcel number pattern (`\b\d{3,4}-\d{3}-\d{3}\b`);
4. an email address;
5. a US phone number;
6. a Social Security number pattern;
7. any of the placeholder tokens appearing **outside** the documentation that defines them —
   a placeholder in a rendered page is acceptable, an unresolved identifier is not;
8. any occurrence of `fetch(`, `XMLHttpRequest`, `localStorage`, `sessionStorage`, or a
   `<form action=` with a non-empty target inside `site/calculator.html`, because the
   calculator must not be able to transmit or retain anything.

## Handling of research findings

During this project, research touched only public corporate filings and public government
statistics. One individual's contact details appear inside a public SEC exhibit (an
investor-relations contact). That information was read but is **deliberately not reproduced**
on the site: the source is cited by document link so a reader can reach the primary record
without this repository republishing an individual's contact details.

## Where the real records should live

A separate, access-logged internal workspace, not this repository. The public site must not
link to it, because a link is itself a disclosure about where the records are. See proposal
SG-09 on the suggestions page.
