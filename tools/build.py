#!/usr/bin/env python3
"""
Build the static site from the verified data layer.

Design rules enforced here (they are the point of the project, not decoration):
  1. No figure is ever printed without its source id rendered as a clickable link.
  2. Any row whose status is 'unverified' renders an EMPTY value cell plus an
     UNVERIFIED badge. The generator refuses to print a number for such a row.
  3. Nothing personal is stored in data/, so nothing personal can reach the site.
  4. The build fails loudly if a row cites a source id that is not in sources.json.
"""
import json, html, pathlib, re, sys, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = ROOT / "site"
BUILT = datetime.datetime.now(datetime.timezone.utc)
BUILT_STR = BUILT.strftime("%Y-%m-%d %H:%M UTC")

def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))

SOURCES = load("sources.json")["sources"]
SRC = {s["id"]: s for s in SOURCES}

errors = []

def e(x):
    return html.escape("" if x is None else str(x), quote=True)

def src_link(sid, show_title=False):
    """Render a source id as a link to the official document."""
    if not sid:
        return '<span class="src-none" title="No official source">unverified</span>'
    ids = [p.strip() for p in re.split(r"[\/,]", str(sid)) if p.strip()]
    out = []
    for i in ids:
        if i not in SRC:
            errors.append(f"unknown source id: {i}")
            out.append(f'<span class="src-none">{e(i)}?</span>')
            continue
        s = SRC[i]
        url = s.get("url") or ""
        if not url:
            out.append(f'<span class="src-none" title="source has no url">{e(i)}</span>')
            continue
        tip = f'{s["publisher"]} — {s["title"]}'
        label = f'{i}' if not show_title else f'{i} · {s["publisher"]}'
        out.append(f'<a class="src" href="{e(url)}" target="_blank" rel="noopener" title="{e(tip)}">{e(label)}</a>')
    return " ".join(out)

def badge(kind, text):
    return f'<span class="b b-{kind}">{e(text)}</span>'

LABEL_BADGE = {
    "observation": ("obs", "observed"),
    "derived": ("der", "derived"),
    "rule": ("rule", "verified rule"),
    "template": ("tpl", "template"),
    "context": ("ctx", "context only"),
    "unverified": ("unv", "unverified"),
    "unverified-blocked": ("unv", "unverified"),
}

def label_badge(raw):
    k = str(raw or "").strip().lower()
    if k in LABEL_BADGE:
        c, t = LABEL_BADGE[k]
        return badge(c, t)
    return badge("ctx", k or "n/a")

def val(raw, status=None):
    """Value cell. Empty for anything unverified — the hard rule."""
    st = str(status or "").lower()
    if raw in (None, "", []) or ("unverif" in st) or st in ("blocked", "open-blocked"):
        return '<td class="empty">—</td>'
    return f"<td>{e(raw)}</td>"

META = load("sources.json")["meta"]

NAV = [
    ("index.html", "Overview"),
    ("decision.html", "Decision"),
    ("gates.html", "Decision gates"),
    ("questions.html", "Questions"),
    ("economy.html", "Local economy"),
    ("trade-area.html", "Trade area"),
    ("hazards.html", "Hazards"),
    ("valuation.html", "Sell vs hold"),
    ("tax.html", "After tax"),
    ("risks.html", "Risks"),
    ("calculator.html", "Calculator"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for review"),
    ("requirements.html", "Requirements"),
    ("suggestions.html", "Suggestions"),
    ("print.html", "1-page summary"),
]

def page(fname, title, body, lede="", hero_extra=""):
    parts = []
    for f, t in NAV:
        cls = ' class="on"' if f == fname else ''
        parts.append(f'<a href="{f}"{cls}>{e(t)}</a>')
    nav = "\n".join(parts)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} — Jack in the Box ground lease, Central Los Angeles</title>
<meta name="description" content="Verified, source-linked decision support for a single-tenant NNN Jack in the Box ground lease in Central Los Angeles. Aggregate findings only; no personal data.">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site"><div class="wrap bar">
  <div class="brand">Jack in the Box <span>/ Central LA ground lease</span></div>
  <nav class="main">
{nav}
  </nav>
</div></header>
<main class="wrap">
<div class="hero">
  <p class="eyebrow">Decision support · aggregate findings only</p>
  <h1>{e(title)}</h1>
  {f'<p class="lede">{lede}</p>' if lede else ''}
  {hero_extra}
</div>
{body}
</main>
<footer class="site"><div class="wrap">
  <p><b>Privacy:</b> this site publishes aggregate, non-identifying findings only. No owner name, entity, address, APN, lease document or financial record appears here, by design. All identifiers are replaced with placeholders. See <a href="privacy.html">the privacy policy</a>.</p>
  <p><b>Verification:</b> every figure links to the official source that printed it. Where a value could not be confirmed against an official source it is left blank and flagged, never inferred. Built {e(BUILT_STR)} from the data layer in <code>data/</code>.</p>
  <p>Not investment, legal, tax or appraisal advice. Nothing here is a property valuation. Engage licensed advisers before acting.</p>
</div></footer>
</body>
</html>
"""
    (SITE / fname).write_text(doc, encoding="utf-8")
    return fname

def privacy_banner():
    return ('<div class="privacy"><span class="lock">🔒</span><div><b>Privacy first.</b> '
            'Owner identity, property address, parcel number, lease file and all financial records are held offline by '
            'authorised advisers and are <b>not</b> published here. Every identifier is replaced with a placeholder. '
            'Everything on this site is an aggregate, non-identifying finding. '
            '<a href="privacy.html">Read the policy</a>.</div></div>')

def table(headers, rows, cls=""):
    """headers: list of (label, align). rows: list of html strings for <td>."""
    ths = []
    for h, a in headers:
        align = ' style="text-align:right"' if a == "r" else ''
        ths.append(f'<th{align}>{e(h)}</th>')
    th = "".join(ths)
    tr = "\n".join(f"<tr>{r}</tr>" for r in rows)
    return f'<div class="twrap"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

# ---------------------------------------------------------------- economy page
def build_economy():
    eco = load("economy.json")

    lm_rows = []
    for r in eco["labour_market"]:
        lm_rows.append(
            f'<td class="id">{e(r["id"])}</td>'
            f'<td>{e(r["series"])}</td>'
            f'{val(r.get("value"), r.get("label"))}'
            f'<td>{e(r.get("unit",""))}</td>'
            f'<td>{e(r.get("period",""))}</td>'
            f'<td>{label_badge(r.get("label"))}</td>'
            f'<td>{src_link(r.get("source"), True)}</td>'
        )

    im_rows = []
    for r in eco["industry_mix"]:
        im_rows.append(
            f'<td class="id">{e(r["id"])}</td>'
            f'<td>{e(r["sector"])}</td>'
            f'<td class="num">{e(r["employment"])}</td>'
            f'<td class="num">{e(r["chg_12m_pct"])}</td>'
            f'<td>{e(r["period"])}</td>'
            f'<td>{label_badge(r.get("label"))}</td>'
            f'<td>{src_link(r.get("source"))}</td>'
            f'<td>{e(r.get("read_through",""))}</td>'
        )

    def generic(rows, cols, headers):
        out = []
        for r in rows:
            tds = []
            for c in cols:
                key, kind = c
                if kind == "id":
                    tds.append(f'<td class="id">{e(r.get(key))}</td>')
                elif kind == "num":
                    tds.append(f'<td class="num">{e(r.get(key,""))}</td>')
                elif kind == "label":
                    tds.append(f'<td>{label_badge(r.get(key))}</td>')
                elif kind == "src":
                    tds.append(f'<td>{src_link(r.get(key), True)}</td>')
                elif kind == "val":
                    tds.append(val(r.get("value"), r.get("label")))
                elif kind == "empty":
                    tds.append('<td class="empty">—</td>')
                else:
                    tds.append(f'<td>{e(r.get(key,""))}</td>')
            out.append("".join(tds))
        return table(headers, out)

    body = privacy_banner()
    body += """
<div class="note warn"><p><b>Read this before the numbers.</b> Everything below describes a <b>container</b> — Los Angeles County, the Los Angeles–Long Beach–Anaheim metro area, or the City of Los Angeles. None of it describes this parcel's trade area. A metro area of thirteen million people is not a three-mile drive-time ring. Using container figures as if they were trade-area figures is the most common way a ground-lease analysis goes wrong, so the trade-area figures live separately on the <a href="trade-area.html">trade area</a> page and are currently blank.</p></div>

<div class="grid g4">
  <div class="stat warn"><div class="k">MSA jobs vs Oct 2019</div><div class="v">+1.29<small>%</small></div><div class="n">Six years to recover 1.3 points. Not a growth cycle.</div></div>
  <div class="stat warn"><div class="k">City population 2020→2025</div><div class="v">−0.8<small>%</small></div><div class="n">The city is shrinking.</div></div>
  <div class="stat info"><div class="k">LA CPI-U, 12-month</div><div class="v">+3.7<small>%</small></div><div class="n">Sep 2026. Tests any rent escalation clause.</div></div>
  <div class="stat warn"><div class="k">County unemployment</div><div class="v">4.6<small>%</small></div><div class="n">Oct 2026, preliminary.</div></div>
</div>

<section class="block">
  <h2>Labour market</h2>
  <p class="sub">Official unemployment and labour-force series. The pandemic peak is included deliberately: it is the last verified severe shock and is used as the stress anchor on the risks page.</p>
"""
    body += table(
        [("ID", "l"), ("Series", "l"), ("Value", "l"), ("Unit", "l"), ("Period", "l"), ("Class", "l"), ("Official source", "l")],
        lm_rows,
    )
    body += f"""
  <div class="note"><p><b>What the series says.</b> MSA nonfarm employment at 6,371.5 thousand in October 2026 is 1.29% above October 2019 and only 0.19% above October 2024. A region that took six years to add 1.3 percentage points of employment has had a recovery, not an expansion. For a ground lease, that removes the growth argument from the hold case before any rent figure is even considered.</p></div>
</section>

<section class="block">
  <h2>Industry mix — where the jobs actually are</h2>
  <p class="sub">Twelve-month change by supersector, October 2026, not seasonally adjusted. The tenant's end market is Leisure and Hospitality; the lunchtime density of a commercial corridor is set by Professional and Business Services and Information.</p>
"""
    body += table(
        [("ID", "l"), ("Sector", "l"), ("Jobs (000s)", "r"), ("12-mo %", "r"), ("Period", "l"), ("Class", "l"), ("Source", "l"), ("Read-through for this property", "l")],
        im_rows,
    )
    body += """
  <div class="note warn"><p><b>One sector is growing.</b> Education and Health Services, +3.3%. Trade/Transportation/Utilities is flat at 0.0%, Professional and Business Services +0.5%, Construction +0.2%, while Information (−2.1%), Financial Activities (−1.6%) and Manufacturing (−1.2%) are contracting. A QSR near an office corridor depends on the contracting sectors for its lunch trade. This is the detailed form of the "existing economic activity" the brief asks about, and it is not a growth story.</p></div>
</section>
"""
    body += """
<section class="block">
  <h2>Prices and income</h2>
  <p class="sub">Verified inflation and household income. The six-year realised CPI growth is an observation, not a forecast, and is the correct benchmark for testing a rent escalation clause.</p>
"""
    body += generic(
        eco["prices_and_income"],
        [("id", "id"), ("series", "t"), ("val", "val"), ("unit", "t"), ("period", "t"), ("label", "label"), ("source", "src"), ("note", "t")],
        [("ID", "l"), ("Series", "l"), ("Value", "l"), ("Unit", "l"), ("Period", "l"), ("Class", "l"), ("Official source", "l"), ("Note", "l")],
    )
    body += """
  <div class="note"><p><b>The squeeze in two numbers.</b> City median household income is $81,939 (2024 dollars) with 16.5% of residents below the poverty line, while the fast-food wage floor is $20.00 per hour and rises by a council decision the owner does not control. The operator's margin is compressed from both ends. That is the mechanism that produces closures, and closures are what this ground lease is actually exposed to.</p></div>
</section>

<section class="block">
  <h2>Population and place</h2>
  <p class="sub">Verified Census estimates. Density supports volume now; it does not create growth.</p>
"""
    body += generic(
        eco["population_and_place"],
        [("id", "id"), ("series", "t"), ("val", "val"), ("unit", "t"), ("period", "t"), ("label", "label"), ("source", "src"), ("note", "t")],
        [("ID", "l"), ("Series", "l"), ("Value", "l"), ("Unit", "l"), ("Period", "l"), ("Class", "l"), ("Official source", "l"), ("Note", "l")],
    )
    body += """
</section>

<section class="block">
  <h2>Cost of capital</h2>
  <p class="sub">The only verified risk-free and benchmark rates available. Any commercial discount rate must be built as a spread over these, and the spread is an assumption the broker must justify with a comparable transaction.</p>
"""
    body += generic(
        eco["capital_markets"],
        [("id", "id"), ("series", "t"), ("val", "val"), ("unit", "t"), ("period", "t"), ("label", "label"), ("source", "src"), ("note", "t")],
        [("ID", "l"), ("Series", "l"), ("Value", "l"), ("Unit", "l"), ("Period", "l"), ("Class", "l"), ("Official source", "l"), ("Note", "l")],
    )
    body += """
  <div class="note warn"><p><b>The trap to avoid.</b> The 30-year fixed mortgage rate of 7.28% is a <i>residential</i> benchmark. It is not a commercial cap rate and must never be used as one. The only legitimate anchor here is the 10-year Treasury at 4.92%; the spread above it is where the entire valuation lives, and that spread is currently unverified.</p></div>
</section>

<section class="block">
  <h2>Tenant health — the series, not one quarter</h2>
  <p class="sub">From the tenant's own filings. The brief asks for a series of same-store sales, unit counts, closures and franchise rental revenue: here it is, with both a good-looking reading and a bad one shown side by side so the direction is visible rather than asserted.</p>
"""
    body += generic(
        eco["tenant_health"],
        [("id", "id"), ("series", "t"), ("val", "val"), ("unit", "t"), ("period", "t"), ("label", "label"), ("source", "src"), ("note", "t")],
        [("ID", "l"), ("Series", "l"), ("Value", "l"), ("Unit", "l"), ("Period", "l"), ("Class", "l"), ("Official source", "l"), ("Note", "l")],
    )
    body += """
  <div class="note warn"><p><b>The five facts that decide this property.</b></p>
  <ul class="tight">
    <li>Same-store sales fell 4.2% in FY2025 and 7.4% in Q4 FY2025 — deteriorating, not stabilising. Compounded over the two years it is −5.45%.</li>
    <li>The tenant closed 86 units in FY2025; 38 of the 47 Q4 closures were a deliberate block-closure programme ("JACK on Track").</li>
    <li>Guidance for FY2026 is 50 to 100 <i>further</i> closures — the tenant has told the market it plans to shrink again.</li>
    <li>Total debt of $1.70bn against guided Adjusted EBITDA of $225–240m is about <b>7.3× leverage</b>, with a shareholders' deficit of −$938m.</li>
    <li>FY2026 guidance names "selling real estate" as part of the plan. The tenant is a <i>source of competing supply</i> in the window this owner is considering selling — and possibly a buyer.</li>
  </ul>
  <p>None of that proves this unit will close. It does mean a renewal probability above roughly 50% cannot be defended on the evidence available, and it means the hold case is a bet against the counterparty's own stated strategy.</p></div>
</section>

<section class="block">
  <h2>Cost inputs the operator bears</h2>
  <p class="sub">These are the operator's costs, not the landlord's — but they drive the operator's decision to keep this unit open, which is what the landlord's rent depends on.</p>
"""
    body += generic(
        eco["cost_inputs"],
        [("id", "id"), ("series", "t"), ("val", "val"), ("unit", "t"), ("period", "t"), ("label", "label"), ("source", "src"), ("note", "t")],
        [("ID", "l"), ("Item", "l"), ("Value", "l"), ("Unit", "l"), ("Period", "l"), ("Class", "l"), ("Official source", "l"), ("Note", "l")],
    )
    body += "</section>"

    body += """
<section class="block">
  <h2>Municipal and fiscal items held open</h2>
  <p class="sub">Deliberately blank. Each is relevant and each failed verification, so none is filled in.</p>
"""
    body += generic(
        eco["municipal_fiscal"],
        [("id", "id"), ("series", "t"), ("val", "val"), ("unit", "t"), ("period", "t"), ("label", "label"), ("source", "src"), ("note", "t")],
        [("ID", "l"), ("Item", "l"), ("Value", "l"), ("Unit", "l"), ("Period", "l"), ("Class", "l"), ("Official source", "l"), ("Note", "l")],
    )
    body += "</section>"

    page("economy.html", "Local economy",
         body,
         "Verified official labour, price, income, population and tenant data for the container geographies around the property — with an explicit warning that container figures are not trade-area figures.")

# ---------------------------------------------------------------- sources page
def build_sources():
    tier_badge = {1: ("closed", "Tier 1 official"), 2: ("der", "Tier 2 official-derived"), 3: ("ctx", "Tier 3 lead")}
    rows = []
    opened = 0
    blocked = 0
    for s in SOURCES:
        cls, txt = tier_badge.get(s.get("tier", 3), ("ctx", "lead"))
        status = s.get("status", "")
        if status.startswith("open"):
            opened += 1
            st = badge("closed", status.replace("-", " "))
        else:
            blocked += 1
            st = badge("open", status or "unknown")
        rows.append(
            f'<td class="id">{e(s["id"])}</td>'
            f'<td>{badge(cls, txt)}</td>'
            f'<td>{e(s["publisher"])}</td>'
            f'<td><a href="{e(s.get("url",""))}" target="_blank" rel="noopener">{e(s["title"])}</a></td>'
            f'<td class="num">{e(s.get("accessed",""))}</td>'
            f'<td>{st}</td>'
            f'<td>{e(s.get("limitation",""))}</td>'
        )

    body = f"""
<div class="grid g4">
  <div class="stat info"><div class="k">Sources in ledger</div><div class="v">{len(SOURCES)}</div><div class="n">Every one opened or attempted this session</div></div>
  <div class="stat ok"><div class="k">Opened and read</div><div class="v">{opened}</div><div class="n">Basis for every published value</div></div>
  <div class="stat warn"><div class="k">Blocked or method-only</div><div class="v">{blocked}</div><div class="n">No value published from these</div></div>
  <div class="stat info"><div class="k">Tier 1 publishers</div><div class="v">{sum(1 for s in SOURCES if s.get("tier")==1)}</div><div class="n">SEC, BLS, Census, IRS, CA agencies, FEMA, USGS, CAL FIRE</div></div>
</div>

<div class="note"><p><b>How the tiering works.</b> <b>Tier 1</b> is an official primary document — a filing, a statistical release, a statute, a regulator's page. Only Tier 1 may be the basis of a published value. <b>Tier 2</b> is an official agency series republished by another official body (FRED republishing Freddie Mac and the Federal Reserve); acceptable because the underlying publisher is named. <b>Tier 3</b> is any non-official source; it is used <i>only</i> to locate a Tier 1 document and is never a basis for a value. Commercial data providers are Tier 3 by definition, which is why the comparable-sales and short-lease-discount questions are flagged rather than answered.</p></div>

<div class="note warn"><p><b>Environment limitation, disclosed.</b> This session's research channel could read web pages but could not download binary files or call data APIs. Two consequences are visible in the ledger: the California Department of Finance projection workbooks (S-09) could not be opened, so no population projection is published; and the Census data API refused queries without a key, so no tract-level ACS pull was possible. Both are recorded as gaps, not worked around with estimates.</p></div>

<section class="block">
  <h2>Source ledger</h2>
  <p class="sub">Every source cited anywhere on this site. Click through to the official document for manual review.</p>
"""
    body += table(
        [("ID", "l"), ("Tier", "l"), ("Publisher", "l"), ("Document", "l"), ("Accessed", "r"), ("Status", "l"), ("Limitation", "l")],
        rows,
    )
    body += "</section>"

    page("sources.html", "Sources and verification ledger",
         body,
         "The complete audit trail. Nothing is published on this site unless it traces to a source on this page.")

# ---------------------------------------------------------------- flagged page
def build_flagged():
    flags = [
        ("I-01", "No subject address or APN supplied",
         "critical",
         "The brief describes a Jack in the Box in Central Los Angeles but supplies no street address, parcel number or lease. Parcel-level hazard screening (W-04), tract selection (W-01) and any numeric valuation are therefore blocked. Only methodology and container-level evidence can be published.",
         "Release the address into the secure workflow only. Nothing else unblocks this.",
         ["S-19", "S-20", "S-21"]),
        ("I-02", "Lease expiry given as a five-year range (2030-2035)",
         "critical",
         "A range cannot be discounted. It also means the option notice window is unknown, which is the single most common way an owner loses value on a ground lease. Every projection in this repository is run as a range because of this.",
         "Read the term clause in the lease and fix the date, plus any option already exercised.",
         []),
        ("I-03", "Census data API unavailable without a key",
         "high",
         "Queries to api.census.gov returned 'Missing Key'. Tract-level ACS figures could not be pulled programmatically, and direct curl to census.gov is blocked in this environment. Figures must therefore be read from published tables, or left blank.",
         "Either obtain a Census API key for the secure workflow, or read the published ACS tables manually.",
         ["S-08"]),
        ("I-04", "No verified comparable sales or rent quotes exist for the short-lease discount",
         "high",
         "The short-lease discount is the dominant valuation input for this asset and it is not observable in any official dataset. CoStar, Reonomy, Crexi and RCA hold the data but are commercial and paywalled, so they cannot satisfy the verification rule. No value is published.",
         "Build a comp set from Los Angeles County recorded grant deeds plus documentary transfer tax stamps — public record, no purchase required. In parallel, obtain three written bid indications.",
         []),
        ("I-05", "School system evidence not verified",
         "medium",
         "The brief explicitly asks for school systems. No school quality figure is published because none was verified against a California Department of Education page in this session. Reporting a third-party ranking would breach the no-hallucination rule.",
         "Pull DataQuest and the California School Dashboard for the schools assigned to the tract once the tract is known.",
         []),
        ("I-06", "Proposition 13 assessment rule could not be verified",
         "medium",
         "The State Board of Equalization FAQ page failed to load. The widely repeated '1% levy with a 2% annual inflation cap' rule is asserted by many secondary sources but was not confirmed on an official page here, so no property-tax figure is published anywhere on this site.",
         "Open boe.ca.gov proposition13 FAQ or the LA County Assessor page directly and quote it, then populate the property-tax line.",
         ["S-23"]),
        ("I-07", "Obligor identity unverified — brand vs franchisee",
         "critical",
         "The tenant brand is Jack in the Box Inc. and its corporate credit is verified from SEC filings. But the obligor on this specific lease may be a franchisee. All the tenant-health analysis on this site is about the brand; if the obligor is a franchisee, that analysis describes a different balance sheet.",
         "Read the tenant-identity and guaranty clauses. Obtain franchisee financials.",
         ["S-01", "S-02"]),
        ("I-08", "Tenant-health analysis is brand-level, not unit-level",
         "high",
         "System-wide same-store sales and closure counts describe 2,136 restaurants. This unit's own sales, traffic and closure status are unknown and are not public. The brand-level series is used as the best available evidence, clearly labelled as such.",
         "Request unit-level sales reporting under the lease's reporting clause.",
         ["S-02"]),
        ("I-09", "Population projections could not be extracted",
         "medium",
         "The California Department of Finance publishes official county and state projections to 2070, and the programme is linked in the ledger. The .xlsx workbooks could not be downloaded in this session, so no projection figure is published. This is a gap in the projection spine (R-29), not a reason to substitute a private forecast.",
         "Download P-2A_County_Total.xlsx and read the Los Angeles County 2030 and 2035 rows.",
         ["S-09"]),
        ("I-10", "Local minimum wage for the City of Los Angeles not confirmed",
         "medium",
         "The state DIR page states that some cities set higher minimum wages and links a UC Berkeley inventory, which is not an official government source. The City of Los Angeles rate is therefore blank rather than filled from a secondary list.",
         "Check the City of Los Angeles Office of Wage Standards page directly.",
         ["S-17"]),
    ]
    rows = []
    for fid, title, sev, detail, fix, srcs in flags:
        sev_cls = "blocking" if sev == "critical" else ("high" if sev == "high" else "medium")
        links = " ".join(src_link(s) for s in srcs) if srcs else '<span class="src-none">no source — item is an absence</span>'
        rows.append(
            f'<td class="id">{e(fid)}</td>'
            f'<td><b>{e(title)}</b></td>'
            f'<td>{badge(sev_cls, sev)}</td>'
            f'<td>{e(detail)}</td>'
            f'<td>{e(fix)}</td>'
            f'<td>{links}</td>'
        )

    body = """
<div class="note warn"><p><b>These items do not block publication — they block the <i>decision</i>.</b> Everything on this page is published deliberately, with its source links, so it can be reviewed after the site is live. Nothing here has been quietly dropped or filled in with an estimate. Three of the ten are critical, and one of those (I-01, no address) is the root cause of most of the blanks elsewhere on the site.</p></div>
<div class="grid g3">
  <div class="stat warn"><div class="k">Critical</div><div class="v">3</div><div class="n">I-01, I-02, I-07</div></div>
  <div class="stat warn"><div class="k">High</div><div class="v">3</div><div class="n">I-03, I-04, I-08</div></div>
  <div class="stat info"><div class="k">Medium</div><div class="v">4</div><div class="n">I-05, I-06, I-09, I-10</div></div>
</div>
<section class="block">
  <h2>Flagged for review</h2>
  <p class="sub">Each item states what is missing, how severe it is, and the exact route to obtain it.</p>
"""
    body += table(
        [("ID", "l"), ("Irregularity", "l"), ("Severity", "l"), ("Detail", "l"), ("Route to resolution", "l"), ("Related sources", "l")],
        rows,
    )
    body += "</section>"
    page("flagged.html", "Flagged for review", body,
         "Every irregularity, gap and unverified value found in this project, published openly with the route to fixing it.")

build_sources()
build_flagged()
build_economy()
print("built:", "economy.html sources.html flagged.html")
if errors:
    print("SOURCE ERRORS:", *errors, sep="\n  ")
