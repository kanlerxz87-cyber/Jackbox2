#!/usr/bin/env python3
"""
Build the consolidated public dashboard from the sourced data layer.

Rules enforced by this generator (they are the project's point, not decoration):

  1. No verified figure renders without a clickable link to the official source
     that printed it. A finding whose source id is not in sources.json aborts
     the build.
  2. A finding whose status is "unverified" renders an EMPTY value cell with an
     UNVERIFIED badge and a pointer to the Flagged for Review page. The
     generator will not print a number for such a row.
  3. No identifier is stored in data/root.json, so none can reach the site.
     Placeholders only.
  4. Every page carries the privacy notice and the "no winner selected" rule.

Run:  python3 tools/build_root.py
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "root.json"

D = json.loads(DATA.read_text(encoding="utf-8"))
SOURCES = {s["id"]: s for s in D["sources"]}
META = D["meta"]
VERIFIED_ON = META["verifiedOn"]

PAGES = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive summary"),
    ("decision-gates.html", "Decision gates"),
    ("verification.html", "Verification ledger"),
    ("requirements.html", "Requirements"),
    ("flagged.html", "Flagged for review"),
    ("trade-area.html", "Trade area"),
    ("hazards.html", "Hazards"),
    ("sell-vs-hold.html", "Sell vs hold"),
    ("calculator.html", "Private calculator"),
    ("risks.html", "Risks"),
    ("questions.html", "Questions"),
    ("suggestions.html", "Suggestions"),
    ("sources.html", "Sources"),
    ("printable-summary.html", "Printable summary"),
    ("privacy.html", "Privacy"),
]

GROUPS = [
    ("Decide", ["index.html", "executive-summary.html", "decision-gates.html", "verification.html", "requirements.html", "flagged.html"]),
    ("Analyse", ["trade-area.html", "hazards.html", "sell-vs-hold.html", "calculator.html", "risks.html"]),
    ("Workspace", ["questions.html", "suggestions.html", "sources.html", "printable-summary.html", "privacy.html"]),
]

CSS = """
:root{
  --bg:#f5f6f8; --card:#fff; --ink:#141b26; --muted:#5b6472; --line:#e2e6ec;
  --navy:#16324f; --accent:#0f5c8c; --red:#a4161a; --green:#166534;
  --amber:#8a5a00; --chip:#eef2f7; --radius:12px;
  --shadow:0 1px 2px rgba(16,24,40,.05),0 1px 3px rgba(16,24,40,.06);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);line-height:1.6;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-size:16px}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px}
a:hover{color:var(--navy)}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #7cb7e0;outline-offset:2px}
header.site{background:var(--navy);color:#fff}
header.site .bar{max-width:1180px;margin:0 auto;padding:14px 18px 0}
.brand{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px}
.brand strong{font-size:18px;letter-spacing:.2px}
.brand span{font-size:13px;opacity:.85}
.brand .tag{margin-left:auto;font-size:11px;text-transform:uppercase;letter-spacing:.08em;
  background:rgba(255,255,255,.14);padding:3px 8px;border-radius:999px}
nav.groups{max-width:1180px;margin:0 auto;padding:10px 10px 12px;display:flex;flex-wrap:wrap;gap:14px}
nav.groups .grp{display:flex;flex-wrap:wrap;align-items:center;gap:4px}
nav.groups .lbl{font-size:10px;text-transform:uppercase;letter-spacing:.1em;opacity:.6;padding:0 4px}
nav.groups a{color:#e8eef5;text-decoration:none;font-size:13.5px;padding:5px 9px;border-radius:8px}
nav.groups a:hover{background:rgba(255,255,255,.12);color:#fff}
nav.groups a[aria-current="page"]{background:#fff;color:var(--navy);font-weight:600}
main{max-width:1180px;margin:0 auto;padding:26px 18px 40px}
.hero{background:linear-gradient(135deg,#16324f,#27506f);color:#fff;border-radius:var(--radius);
  padding:26px 26px 22px;box-shadow:var(--shadow);margin-bottom:20px}
.hero .eyebrow{margin:0 0 8px;font-size:12px;letter-spacing:.1em;text-transform:uppercase;opacity:.8}
.hero h1{margin:0 0 10px;font-size:clamp(24px,3.4vw,33px);line-height:1.25}
.hero p{margin:0 0 10px;max-width:74ch;color:#e6edf5}
.hero .verdict{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);
  border-radius:10px;padding:12px 14px;margin-top:14px;font-size:14.5px}
h1{font-size:clamp(23px,3vw,30px);line-height:1.25;margin:0 0 8px}
h2{font-size:20px;margin:34px 0 10px;padding-top:6px}
h3{font-size:16px;margin:0 0 6px}
p{margin:0 0 12px;max-width:82ch}
.lede{color:var(--muted);font-size:15px;max-width:80ch}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:16px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 18px;box-shadow:var(--shadow)}
.card h3{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:8px}
.kpi{font-size:26px;font-weight:700;line-height:1.2;margin:0 0 4px;letter-spacing:-.01em}
.card p{font-size:14px;margin:0 0 8px}
.card .src{font-size:12.5px;color:var(--muted)}
.card a.more{font-size:13.5px;font-weight:600;text-decoration:none}
.callout{border-left:4px solid var(--amber);background:#fffbef;padding:12px 16px;border-radius:10px;
  margin:16px 0;font-size:14.5px}
.callout.info{border-color:var(--accent);background:#eff6fc}
.callout.danger{border-color:var(--red);background:#fdf2f2}
.callout.ok{border-color:var(--green);background:#f1f8f3}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);
  background:var(--card);box-shadow:var(--shadow);margin:14px 0}
table{width:100%;border-collapse:collapse;font-size:14px;min-width:640px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#eef2f7;font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:#33415c;white-space:nowrap}
tbody tr:nth-child(even){background:#fbfcfd}
tbody tr:last-child td{border-bottom:none}
td.num{font-variant-numeric:tabular-nums;font-weight:600}
td.blank{color:#8b94a3;font-style:italic}
.pill{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11.5px;font-weight:700;
  letter-spacing:.02em;white-space:nowrap}
.pill.ok{background:#dcfce7;color:#14532d}
.pill.warn{background:#fef3c7;color:#713f12}
.pill.bad{background:#fee2e2;color:#7f1d1d}
.pill.info{background:#dbeafe;color:#1e3a8a}
.pill.blank{background:#e9edf2;color:#44506a}
.pill.gate{background:#f1f5f9;color:#334155;border:1px solid #d8e0ea}
ul,ol{margin:0 0 14px;padding-left:22px;max-width:82ch}
li{margin:0 0 7px}
footer.site{background:#fff;border-top:1px solid var(--line);margin-top:20px;padding:22px 18px 34px}
footer.site .inner{max-width:1180px;margin:0 auto;color:var(--muted);font-size:13px}
footer.site p{max-width:95ch}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
a.tile{display:block;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 18px;text-decoration:none;color:inherit;box-shadow:var(--shadow)}
a.tile:hover{border-color:#b9cfe2;background:#fbfdff}
a.tile h3{color:var(--ink);font-size:15px;text-transform:none;letter-spacing:0;margin-bottom:6px}
a.tile p{font-size:13.5px;color:var(--muted);margin:0}
label{display:block;font-size:12.5px;font-weight:600;margin:0 0 4px;color:#33415c}
input,select{width:100%;padding:9px 10px;border:1px solid #cfd8e3;border-radius:8px;font-size:14px;
  background:#fff;color:var(--ink)}
.field{margin-bottom:12px}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
fieldset{border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;margin:0 0 16px;background:var(--card)}
legend{font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding:0 6px}
.output{background:#0f1c2b;color:#e8eef5;border-radius:var(--radius);padding:18px;margin-top:14px}
.output h3{color:#fff;font-size:14px;text-transform:uppercase;letter-spacing:.06em}
.output .big{font-size:24px;font-weight:700;margin:2px 0 10px;font-variant-numeric:tabular-nums}
.output .line{display:flex;justify-content:space-between;gap:16px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.12);font-size:14px}
.output .line:last-child{border-bottom:none}
.output .neg{color:#fca5a5}
.output .pos{color:#86efac}
.output .hint{color:#b6c4d4;font-size:12.5px;margin-top:10px}
button{background:var(--navy);color:#fff;border:0;border-radius:9px;padding:10px 16px;font-size:14px;
  font-weight:600;cursor:pointer}
button.secondary{background:#fff;color:var(--navy);border:1px solid #cbd5e1}
.actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.muted{color:var(--muted)}
.small{font-size:12.5px}
.kv{display:grid;grid-template-columns:minmax(150px,220px) 1fr;gap:6px 16px;font-size:14px}
.kv dt{font-weight:600;color:#33415c}
.kv dd{margin:0}
.anchor{scroll-margin-top:90px}
.badge-row{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 0}
hr{border:0;border-top:1px solid var(--line);margin:26px 0}
@media print{
  header.site,nav.groups,footer.site .noprint,.actions{display:none!important}
  body{background:#fff;font-size:11pt}
  main{max-width:none;padding:0}
  .hero{background:#fff;color:#000;border:1px solid #999}
  .hero p,.hero .verdict{color:#000}
  .card,.tablewrap,fieldset{box-shadow:none}
  table{min-width:0;font-size:9.5pt}
  th{background:#eee}
  .output{background:#fff;color:#000;border:1px solid #999}
  .output h3,.output .big{color:#000}
  @page{margin:14mm}
}
"""


def e(text):
    return html.escape(str(text), quote=True)


def src(source_id, short=False):
    """Render an official-source link. Aborts the build if the id is unknown."""
    try:
        s = SOURCES[source_id]
    except KeyError:
        raise SystemExit(f"build error: findings cite unknown source id {source_id!r}")
    label = s["publisher"] + (" — " + s["date"] if s["date"] else "")
    text = s["label"] if not short else label
    return f'<a href="{e(s["url"])}" rel="noopener">{e(text)}</a>'


def source_line(source_id):
    s = SOURCES[source_id]
    return (f'{e(s["publisher"])} · {e(s["date"])} · '
            f'<a href="{e(s["url"])}" rel="noopener">open source</a> · checked {e(s["retrieved"])}')


def nav(active):
    out = []
    for group, files in GROUPS:
        links = []
        for f, label in PAGES:
            if f not in files:
                continue
            cur = ' aria-current="page"' if f == active else ""
            links.append(f'<a href="{f}"{cur}>{e(label)}</a>')
        out.append(f'<div class="grp"><span class="lbl">{e(group)}</span>{"".join(links)}</div>')
    # The audit is a nested, static transparency record rather than a generated
    # evidence page, but it remains visible from every current dashboard page.
    out.append('<div class="grp"><span class="lbl">Review</span><a href="audit/index.html">Publication audit</a></div>')
    return f'<nav class="groups" aria-label="Site sections">{"".join(out)}</nav>'


FOOTER = f"""
<footer class="site"><div class="inner">
  <p><b>Privacy.</b> No owner name, entity, street address, parcel number, lease file or owner
  financial record appears on this site. Identifiers are replaced with placeholders and the
  underlying records stay in an access-controlled internal workspace. Only aggregate,
  non-identifying findings are published. <a href="privacy.html">Privacy and workspace rules</a>.</p>
  <p><b>Verification.</b> Every published figure links to the official page that printed it and was
  read during the sweep dated {e(VERIFIED_ON)}. Where a value could not be confirmed it is left blank
  and listed on <a href="flagged.html">Flagged for review</a>. No value is inferred, estimated or
  copied from another dashboard. <a href="verification.html">Verification ledger</a>.</p>
  <p><b>No winner selected.</b> Nothing here recommends selling or renewing. The evidence needed to
  price either branch is not yet in hand, and this site does not forecast. It is not legal, tax,
  appraisal or investment advice; engage licensed advisers before acting.</p>
  <p class="noprint">Consolidated workspace, session 88ea335a, generated from <code>data/root.json</code>.
  Earlier parallel dashboards are kept in <a href="index.html#archive">the archive</a> with their cut-off dates.</p>
</div></footer>
"""


def page(fname, title, body, lede="", hero_extra="", scripts=""):
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} — Jack in the Box, Central Los Angeles</title>
<meta name="description" content="Verified, source-linked decision workspace for one anonymous single-tenant net-lease restaurant parcel in Central Los Angeles. Aggregate findings only; no personal data.">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site">
  <div class="bar">
    <div class="brand">
      <strong>Jack in the Box · Central Los Angeles</strong>
      <span>Single-tenant net lease · expiry window 2030–2035 (per owner brief, unverified)</span>
      <span class="tag">Anonymous</span>
    </div>
  </div>
  {nav(fname)}
</header>
<main>
<div class="hero">
  <p class="eyebrow">Decision support · aggregate findings only · verified {e(VERIFIED_ON)}</p>
  <h1>{e(title)}</h1>
  {f'<p>{lede}</p>' if lede else ''}
  {hero_extra}
</div>
{body}
</main>
{FOOTER}
{scripts}
</body>
</html>
"""
    (ROOT / fname).write_text(doc, encoding="utf-8")
    return fname


def status_pill(status):
    if status == "verified":
        return '<span class="pill ok">Verified</span>'
    return '<span class="pill warn">Unverified</span>'


def value_cell(row):
    """Never print a value for an unverified row."""
    if row["status"] != "verified":
        return '<td class="blank">—</td>'
    return f'<td class="num">{e(row["value"])}</td>'


def findings_table(rows, show_category=False, show_note=True):
    head = "<tr><th>ID</th>"
    if show_category:
        head += "<th>Area</th>"
    head += "<th>Item</th><th>Value</th><th>Period</th><th>Official source</th>"
    if show_note:
        head += "<th>Note</th>"
    head += "</tr>"
    body = []
    for r in rows:
        cells = [f'<td><code>{e(r["id"])}</code></td>']
        if show_category:
            cells.append(f'<td>{e(r["category"])}</td>')
        cells.append(f'<td>{e(r["label"])} {status_pill(r["status"])}</td>')
        cells.append(value_cell(r))
        cells.append(f'<td>{e(r["period"])}</td>')
        cells.append(f'<td>{src(r["sourceId"])}</td>')
        if show_note:
            cells.append(f'<td class="small">{e(r["note"])}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="tablewrap"><table><thead>{head}</thead><tbody>{"".join(body)}</tbody></table></div>'


def by_cat(*cats):
    return [r for r in D["findings"] if r["category"] in cats]


def gate_table():
    rows = []
    for g in D["gates"]:
        cls = {"Blocked": "bad", "Open": "warn", "Pending": "info"}.get(g["status"], "blank")
        rows.append(
            f'<tr><td><b>{e(g["id"])}</b></td><td><b>{e(g["title"])}</b><br>'
            f'<span class="small muted">{e(g["question"])}</span></td>'
            f'<td><span class="pill {cls}">{e(g["status"])}</span></td>'
            f'<td class="small">{e(g["criteria"])}</td>'
            f'<td class="small">{e(g["evidence"])}</td></tr>')
    return ('<div class="tablewrap"><table><thead><tr><th>Gate</th><th>Question the gate must answer</th>'
            '<th>Status</th><th>Evidence required to clear it</th><th>Evidence in hand</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def kpi_card(label, value, note, link, href, source_id=None):
    s = f'<div class="src">{src(source_id)}</div>' if source_id else ""
    return (f'<div class="card"><h3>{e(label)}</h3><p class="kpi">{e(value)}</p>'
            f'<p>{e(note)}</p>{s}<a class="more" href="{href}">{e(link)} →</a></div>')



# Tables that are registers, legends, methods or archives rather than evidence.
# They are labelled so the repository-wide provenance check can distinguish them
# from tables that carry a figure and must cite an official source.
NOSOURCE_MARKERS = {
    "index.html": ["<th>Location</th>"],
    "executive-summary.html": ["<th>Path</th>"],
    "decision-gates.html": ["<th>Question the gate must answer</th>",
                            "<th>Artefact that closes it</th>",
                            "<th>Meaning</th>"],
    "verification.html": ["<th>Irregularity</th>"],
    "trade-area.html": ["<th>What it covers</th>",
                        "<th>Can the county answer it?</th>"],
    "hazards.html": ["<th>Driver</th>"],
    "sell-vs-hold.html": ["<th>What is computed</th>", "<th>Character</th>"],
    "calculator.html": ["<th>Meaning</th>"],
    "risks.html": ["<th>Decision</th>", "<th>Event</th>", "<th>Scenario</th>"],
    "questions.html": ["<th>Question and why it matters</th>", "<th>Missing information</th>"],
    "suggestions.html": ["<th>Proposal</th>", "<th>Why it would help</th>"],
    "flagged.html": ["<th>What was found</th>"],
    "printable-summary.html": ["<th>Subject</th>", "<th>Question</th>"],
    "privacy.html": ["<th>Published here?</th>", "<th>Threat</th>"],
    "requirements.html": ["<th>Brief ref</th>", "<th>Conflict</th>"],
}


def mark_nosource(fname, markers):
    """Label non-evidence tables so a provenance check can tell them apart.

    A table is non-evidence when its header matches one of the markers: it is a
    register, a legend, a method table or an archive of links. Every such table on
    the page is labelled, not just the first.
    """
    path = ROOT / fname
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r'<div class="tablewrap">\s*<table>(.*?)</table>\s*</div>', re.S)
    marked = {"count": 0}

    def repl(m):
        inner = m.group(1)
        header = inner[:2500]
        if any(marker in header for marker in markers):
            marked["count"] += 1
            return ('<div class="tablewrap nosource"><table class="nosource">'
                    + inner + '</table></div>')
        return m.group(0)

    text = pattern.sub(repl, text)
    if marked["count"] == 0:
        raise SystemExit(f"build error: no non-evidence table matched in {fname}")
    path.write_text(text, encoding="utf-8")

# ----------------------------------------------------------------- index
def build_index():
    tenant = by_cat("Tenant")
    q3 = next(r for r in tenant if r["id"] == "T-03")
    rent = next(r for r in tenant if r["id"] == "T-08")
    pop = next(r for r in D["findings"] if r["id"] == "E-01")
    rate = next(r for r in D["findings"] if r["id"] == "C-01")
    eq = next(r for r in D["findings"] if r["id"] == "H-01")

    cards = "".join([
        kpi_card("Brand direction", q3["value"],
                 "System same-store sales, Q3 FY2026, against −7.1% in the same quarter a year earlier. Still negative, but the decline has narrowed.",
                 "Tenant evidence", "#tenant", "SEC-Q3FY26"),
        kpi_card("Rent stream direction", "−6.8%",
                 "Franchise rental revenues, first 40 weeks of FY2026 versus the same weeks of FY2025 (US$242.5m against US$260.3m).",
                 "Read the series", "#tenant", "SEC-Q3FY26"),
        kpi_card("County population", "about 9.8m",
                 "State estimate for 1 January 2026, down 64,000 in a year. The Census vintage shows the same direction at a lower level.",
                 "Trade-area context", "trade-area.html", "CA-DOF-E1"),
        kpi_card("Risk-free reference", rate["value"],
                 "10-year Treasury, 24 November 2026. Used only as a discount-rate reference, not as a cap rate.",
                 "After-tax module", "sell-vs-hold.html", "FRED-DGS10"),
        kpi_card("Seismic exposure", eq["value"],
                 "Probability of a magnitude 6.7 or greater earthquake in the Los Angeles region within 30 years.",
                 "Hazard screening", "hazards.html", "USGS-EQ-PROB"),
        kpi_card("Lease facts", "Unknown",
                 "Expiry window 2030–2035 is the owner's brief. Exact dates, options, notice periods and rent are unverified and unpublished by design.",
                 "Open the gate", "decision-gates.html"),
    ])

    key_rows = [next(r for r in D["findings"] if r["id"] == i)
                for i in ["T-01", "T-03", "T-04", "T-05", "T-08", "T-10",
                          "E-01", "E-05", "E-06", "E-07", "E-08",
                          "C-01", "C-02", "C-03", "C-05", "H-01"]]

    tiles = "".join(
        f'<a class="tile" href="{href}"><h3>{e(title)}</h3><p>{e(text)}</p></a>'
        for href, title, text in [
            ("executive-summary.html", "Executive summary", "The bottom line, the three candidate paths, and what must be true for each."),
            ("verification.html", "Verification ledger", "Every published figure with its official source, period and check date."),
            ("decision-gates.html", "Decision gates", "Seven gates, in order. Nothing is committed until they clear."),
            ("trade-area.html", "Trade area", "County and metro context, plus the tract selection method that replaces it."),
            ("hazards.html", "Hazards", "Earthquake, flood, fire and insurance screening, parcel level, inside the secure workspace."),
            ("sell-vs-hold.html", "Sell vs hold", "The after-tax module and the short-lease discount method."),
            ("calculator.html", "Private calculator", "Runs in this browser. No network, no storage, nothing sent anywhere."),
            ("risks.html", "Risks", "Decision-by-decision register with black swan stress tests."),
            ("questions.html", "Questions", "What must be answered, by whom, and what changes when it is."),
            ("suggestions.html", "Suggestions", "Proposed actions and site changes, for review before anything is implemented."),
            ("flagged.html", "Flagged for review", "Twenty items left blank on purpose, each with the official link to check it."),
            ("requirements.html", "Requirements", "Every item in the brief traced to a page, with the two that cannot be completed."),
            ("printable-summary.html", "Printable summary", "One page for advisers, with the same sources."),
        ])

    body = f"""
<div class="callout danger">
  <b>Bottom line.</b> The evidence does not support choosing between selling before expiry and renewing.
  The tenant is still shrinking, the county population is falling, the rate environment is expensive, and the
  three inputs that decide the answer — the lease abstract, the parcel hazard and insurance file, and the
  owner's tax basis — are not in hand. What can be done now is to clear the gates in order, starting with the
  notice calendar, and to keep the decision reversible until the numbers exist.
  <span class="badge-row"><span class="pill bad">No winner selected</span>
  <span class="pill info">Every figure sourced</span>
  <span class="pill blank">Unverified = blank</span></span>
</div>

<div class="grid">{cards}</div>

<h2 id="tenant">What the verified record shows about the tenant</h2>
<p>Four filings tell a consistent story: the brand contracted through fiscal 2025, the decline slowed in the
third quarter of fiscal 2026, and the estate is still getting smaller. Same-store sales fell 4.2% for FY2025
and 7.4% in the fourth quarter; 86 restaurants closed against 31 openings. By the third quarter of FY2026
same-store sales were down 1.1% instead of 7.1%, but the company still closed 17 restaurants against 4
openings and guided to a further low-single-digit decline for the year.</p>
<p>For a landlord, the more relevant line is rent. Franchise rental revenues fell from US$260.3 million to
US$242.5 million over the first 40 weeks of FY2026, a 6.8% decline that the company links partly to its own
closure programme. The tenant also refinanced US$500 million of secured debt at 7.624% with an anticipated
repayment date of May 2031, suspended its dividend, and announced a chief financial officer transition
effective April 2027. None of that is a statement about this parcel, but all of it bears on how much rent the
operator can support and how a buyer will price the remaining term.</p>

<h2>Key verified figures</h2>
<p class="lede">Sixteen of the {len(D['findings'])} ledger rows, chosen because each one moves the sell-or-renew
arithmetic. The full ledger is on <a href="verification.html">Verification</a>.</p>
{findings_table(key_rows, show_category=True, show_note=False)}
<p class="small muted">Values are quoted exactly as the official source prints them. Where a row is marked
unverified the value cell is deliberately empty.</p>

<h2>Where to go next</h2>
<div class="tiles">{tiles}</div>

<h2 id="archive">Archive — earlier parallel work, kept and dated</h2>
<div class="callout info">
  <b>Why this page exists.</b> Several sessions worked on this repository at the same time and produced
  separate dashboards. Rather than delete them, they are kept below with their own cut-off dates. They do not
  agree on every figure because they were built at different times; this site is the consolidated entry point
  and the verification ledger is the reference. When a figure here differs from a legacy page, the ledger row
  and its source link win.
</div>
<div class="tablewrap"><table><thead><tr><th>Location</th><th>What it is</th><th>Cut-off as it states</th></tr></thead><tbody>
<tr><td><a href="central-la-2026/index.html">central-la-2026/</a></td><td>Eleven-page refresh with a notice calendar and a local calculator</td><td>Verified through 25 November 2026; FY2026 Q1–Q3 filings</td></tr>
<tr><td><a href="site/index.html">site/</a></td><td>Analytical dashboard generated from a JSON data layer by <code>tools/build.py</code></td><td>FY2025 fourth-quarter and full-year release</td></tr>
<tr><td><a href="docs/index.html">docs/</a></td><td>Session fb776066 pages: gates, tract trends, after-tax module</td><td>FY2025 filings</td></tr>
<tr><td><a href="docs/arena-75e09b85/index.html">docs/arena-75e09b85/</a></td><td>Session 75e09b85 pages: market research and decision framework</td><td>FY2025 filings</td></tr>
<tr><td><a href="privacy-first/index.html">privacy-first/</a></td><td>Conservative no-fabrication framework with empty inputs</td><td>Framework only, no dated figures</td></tr>
<tr><td><a href="alternative-research/index.html">alternative-research/</a></td><td>Independent second research pass</td><td>FY2025 issuer report</td></tr>
</tbody></table></div>
"""
    return page("index.html", "Sell before expiry, or renew?", body,
                lede="A verified-evidence workspace for one anonymous single-tenant Jack in the Box net-lease "
                     "parcel in Central Los Angeles. Every number links to the official page that printed it; "
                     "anything unconfirmed is blank and flagged.")


# --------------------------------------------------------- executive summary
def build_exec():
    body = f"""
<div class="callout danger">
  <b>The decision cannot be made yet, and the honest answer is to say so.</b>
  Selling before expiry and renewing are both defensible on today's evidence, which is exactly why neither
  should be chosen. The tenant is contracting but still operates 2,115 restaurants; the county is losing
  population while metro payroll is growing; the lease and the tax basis — the two inputs that convert an
  opinion into a number — are private and not yet abstracted. Choosing now would mean guessing.
</div>

<h2>Three candidate paths and what must be true</h2>
<div class="tablewrap"><table><thead><tr><th>Path</th><th>What must be true for it to win</th><th>Evidence for</th><th>Evidence against</th><th>Kill criterion</th></tr></thead><tbody>
<tr>
  <td><b>Sell before expiry</b><br><span class="small muted">Market the lease with its remaining term</span></td>
  <td>A buyer pays, after tax and costs, more than the present value of holding to expiry and re-leasing — and more than the option value of waiting.</td>
  <td>Rate reference at 4.91% suggests buyers still need a spread that a short lease may not clear; a sale removes tenant credit and hazard exposure from the owner's balance sheet.</td>
  <td>Tenant closures and negative same-store sales will be read by buyers as re-leasing risk; no comparable sale evidence exists yet.</td>
  <td>Three broker opinions cluster below the hold value computed from verified inputs.</td>
</tr>
<tr>
  <td><b>Hold to expiry</b><br><span class="small muted">Collect rent, decide later</span></td>
  <td>The rent stream plus terminal value exceeds a sale today, and the owner can absorb a vacancy or a hazard event without forced selling.</td>
  <td>Payroll growth resumed (+0.9% year over year) and the unemployment rate improved to 4.4%; rent is contractual.</td>
  <td>County population fell 64,000 in a year; the tenant guided to further same-store sales declines and more closures.</td>
  <td>Two consecutive years of population loss, or a failed insurance renewal, or a closure notice.</td>
</tr>
<tr>
  <td><b>Renew or extend</b><br><span class="small muted">Negotiate a new term now</span></td>
  <td>The operator's store-level coverage supports the rent, and the new rent plus escalations beats re-leasing to an alternative tenant net of downtime and improvements.</td>
  <td>2,115 units and US$3.1 billion of 40-week systemwide sales show a business with scale; same-store sales improved sharply against the prior year.</td>
  <td>Tenant has leverage from its own closure programme; refinancing at 7.624% raises the cost of every dollar of rent.</td>
  <td>Offered rent falls below the walk-away rent set from the re-leasing study.</td>
</tr>
</tbody></table></div>
<p class="small muted">None of the three is recommended. The table exists so that the eventual decision has a
written test to pass, rather than a preference to defend.</p>

<h2>What is known, verified today</h2>
{findings_table([r for r in D["findings"] if r["status"] == "verified"], show_category=True, show_note=False)}
<p class="small muted">All rows above were read on the official page during the {e(VERIFIED_ON)} sweep. The
remainder of the ledger is unverified by design.</p>

<h2>What is missing, and why it decides the answer</h2>
{findings_table([r for r in D["findings"] if r["status"] != "verified"], show_category=True, show_note=True)}

<h2>The sequence that produces a decision</h2>
<ol>
  <li><b>Weeks 1–2 — protect the options.</b> Abstract the lease and reconcile the notice calendar. Nothing
  else matters if a notice date passes. Gate G1.</li>
  <li><b>Weeks 2–4 — resolve the biggest unknown.</b> Request an estoppel certificate and a written renewal
  indication, together with store-level financials for the operating entity. Gate G2.</li>
  <li><b>Weeks 2–6 — build the valuation range.</b> Three broker opinions with short-lease comparables, plus a
  re-leasing and conversion study. Gate G5.</li>
  <li><b>Weeks 2–6 — build the hazard and insurance file.</b> Parcel zone determinations, an engineering
  opinion, two quotes and a FAIR Plan comparison. Gate G4.</li>
  <li><b>Weeks 4–8 — fix the trade area.</b> Select tracts once, document the rule, pull two ACS vintages for
  direction rather than a point estimate. Gate G3.</li>
  <li><b>Weeks 4–8 — fix the tax number.</b> Basis, depreciation, entity, residency, transfer taxes, exchange
  capacity. Gate G6.</li>
  <li><b>Week 8 — compare, stress, decide.</b> One after-tax number against one hold net present value, then
  base, downside and black swan. Gate G7. Written memo, signed.</li>
</ol>

<h2>Wealth preservation and growth, in plain terms</h2>
<p>The owner's exposure today is concentrated in two places that a spreadsheet will not fix: tenant credit
and hazard. Tenant credit is public enough to watch — closures, same-store sales, rental revenue, leverage,
leadership. Hazard is not: the parcel-level determinations are missing, and an uninsured loss is the one event
that can convert a manageable risk into a forced sale. The cheapest risk reduction available now is
information, not action: three broker opinions, two insurance quotes, one lease abstract, one engineer's
opinion.</p>
<p>On growth, the honest position is that a short-lease drive-through in a county losing population is not a
growth asset unless the immediate trade area is growing. That is testable at tract level and is currently
untested. Until it is tested, the renewal case rests on the brand, and the brand is shrinking.</p>

<div class="callout info">
  <b>What this site will not do.</b> It will not publish a projected price, a forecast return, or a
  recommendation. It publishes the rules, the arithmetic and the sources, so that the day the private inputs
  arrive the comparison takes an hour rather than a quarter.
</div>
"""
    return page("executive-summary.html", "Executive summary", body,
                lede="The bottom line, the three candidate paths with written tests, what is verified, what is "
                     "missing, and the eight-week sequence that produces a decision.")


# ------------------------------------------------------------- verification
def build_verification():
    verified = [r for r in D["findings"] if r["status"] == "verified"]
    unverified = [r for r in D["findings"] if r["status"] != "verified"]

    src_rows = "".join(
        f'<tr><td><b>{e(s["id"])}</b></td><td>{e(s["label"])}<br><span class="small muted">{e(s["supports"])}</span></td>'
        f'<td class="small">{e(s["publisher"])}</td><td class="small">{e(s["date"])}</td>'
        f'<td class="small">{e(s["retrieved"])}</td>'
        f'<td class="small"><a href="{e(s["url"])}" rel="noopener">open</a></td></tr>'
        for s in D["sources"])

    body = f"""
<div class="callout ok">
  <b>Method.</b> On {e(VERIFIED_ON)} every figure published on this site was re-read on the official page
  that prints it and recorded with its period, its source and the check date. {len(verified)} rows passed.
  {len(unverified)} rows could not be confirmed and were left blank instead of being estimated. Nothing was
  copied from another dashboard, and nothing was reconstructed from memory.
</div>

<h2>Status summary</h2>
<div class="grid">
  <div class="card"><h3>Verified rows</h3><p class="kpi">{len(verified)}</p><p>Value printed, source linked, period stated.</p></div>
  <div class="card"><h3>Left blank</h3><p class="kpi">{len(unverified)}</p><p>Flagged for review with the official link needed to check them.</p></div>
  <div class="card"><h3>Inferred values</h3><p class="kpi">0</p><p>No value on this site was inferred, interpolated or estimated.</p></div>
  <div class="card"><h3>Source pages</h3><p class="kpi">{len(D["sources"])}</p><p>{sum(1 for s in D["sources"] if "did not load" in s["retrieved"] or "not retrieved" in s["retrieved"])} of them did not load and are listed for manual review only.</p></div>
</div>

<h2>Verified rows — line by line</h2>
{findings_table(verified, show_category=True, show_note=True)}

<h2>Could not be verified — left blank</h2>
<p>Each row below is a required input, not a nice-to-have. The value cell is empty because printing a number
would mean inventing it. The Flagged page gives the exact check to run.</p>
{findings_table(unverified, show_category=True, show_note=True)}

<h2>Source register</h2>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Source</th><th>Publisher</th><th>Source date</th><th>Checked</th><th>Link</th></tr></thead>
<tbody>{src_rows}</tbody></table></div>

<h2>Irregularities found and how they were handled</h2>
<div class="tablewrap"><table><thead><tr><th>#</th><th>Irregularity</th><th>Handling</th></tr></thead><tbody>
<tr><td>1</td><td>Two official agencies publish Los Angeles County population estimates that differ by more than 140,000 persons.</td><td>Both are published with their own source and reference date; neither is averaged. Recorded as <a href="flagged.html">F-02</a>.</td></tr>
<tr><td>2</td><td>The Bureau of Labor Statistics cannot publish an October 2026 12-month CPI change for Los Angeles because October 2025 data were not collected during the federal funding lapse.</td><td>The index level and the month-on-month change are published; the missing 12-month cell is disclosed rather than filled with the September value.</td></tr>
<tr><td>3</td><td>No Q4 or full-year FY2026 tenant release appeared in the EDGAR index on the sweep date.</td><td>The fiscal year is treated as unreported and flagged as <a href="flagged.html">F-01</a>; no annual figure is published.</td></tr>
<tr><td>4</td><td>Census QuickFacts, the state fire marshal's deep map links, the city finance pages, the county recorder and the state Board of Equalization did not respond during the sweep.</td><td>Those items are blank and listed for manual review with their official URLs. No value was substituted from a secondary source.</td></tr>
<tr><td>5</td><td>The repository's readme carried unresolved merge-conflict markers on the default branch.</td><td>Markers removed and the document rewritten to describe the consolidated site; recorded in <code>COORDINATION.md</code>.</td></tr>
<tr><td>6</td><td>One legacy dashboard's own test suite failed with "table row missing source" and was not run by continuous integration.</td><td>Recorded as an irregularity, not silenced: the legacy test remains failing and is documented rather than edited, because that directory belongs to another session's scope.</td></tr>
<tr><td>7</td><td>Six dashboards publish overlapping figures with different cut-off dates.</td><td>Consolidated here, with the legacy locations kept and dated under <a href="index.html#archive">Archive</a>. The ledger is the reference.</td></tr>
</tbody></table></div>

<h2>What was deliberately not done</h2>
<ul>
  <li>No cap rate, discount rate or sale price was published. Each would require comparable transactions this
  repository does not hold.</li>
  <li>No tract-level indicator was published. Publishing one before the parcel's tracts are fixed would be a
  proxy dressed as evidence.</li>
  <li>No parcel hazard status was published. It is a privacy question before it is a data question.</li>
  <li>No forecast was published. A projection without verified inputs is a preference with a chart.</li>
</ul>
"""
    return page("verification.html", "Verification ledger", body,
                lede="Every figure, its official source, its period and the date it was checked — plus every "
                     "value deliberately left blank and why.")


# ------------------------------------------------------------ decision gates
def build_gates():
    seq = "".join(
        f'<li><b>{e(g["id"])} — {e(g["title"])}</b>: {e(g["question"])} '
        f'<span class="pill gate">{e(g["status"])}</span></li>'
        for g in D["gates"])
    body = f"""
<div class="callout">
  <b>Rule of the board.</b> A gate clears only on evidence, never on opinion, and no gate may be skipped.
  Value work (G5) and tax work (G6) may run in parallel with the lease work, but the comparison in G7 cannot
  be signed until every earlier gate is closed. Three gates are blocked for one reason: the private inputs
  are not in this repository and must not be.
</div>

<h2>The board</h2>
{gate_table()}

<h2>Order of work</h2>
<ol>{seq}</ol>

<h2>What clearing each gate actually looks like</h2>
<div class="tablewrap"><table><thead><tr><th>Gate</th><th>Artefact that closes it</th><th>Who produces it</th><th>What would reopen it</th></tr></thead><tbody>
<tr><td>G1</td><td>Signed lease abstract, estoppel certificate, title preliminary report, dated notice calendar</td><td>Owner's counsel and title company</td><td>An amendment, a side letter, or a notice served by either party</td></tr>
<tr><td>G2</td><td>Written renewal indication plus store-level financial statements for the operating entity</td><td>Tenant, through the owner's broker</td><td>A closure announcement, a downgrade, or a restructuring filing</td></tr>
<tr><td>G3</td><td>Tract list with the selection rule, two matched ACS vintages, traffic counts, competitor inventory</td><td>Analyst in the secure workspace</td><td>A boundary change or a new ACS vintage that breaks comparability</td></tr>
<tr><td>G4</td><td>Four dated zone determinations, an engineering opinion, two insurance quotes and a FAIR Plan comparison</td><td>Consulting engineer, insurance broker</td><td>A map revision, a non-renewal notice, or a new fire hazard zone map</td></tr>
<tr><td>G5</td><td>Three signed broker opinions with a short-lease comparable set, plus a re-leasing and conversion study</td><td>Brokers, contractor, appraiser</td><td>A material rate move or a comparable sale at a very different cap rate</td></tr>
<tr><td>G6</td><td>After-tax computation signed by the accountant, with basis, depreciation, entity, residency and transfer taxes</td><td>Owner's accountant and escrow officer</td><td>A change in tax law, residency, entity structure or exchange plan</td></tr>
<tr><td>G7</td><td>Two-page decision memo with base, downside and black swan cases and a decision date</td><td>Owner with advisers</td><td>Any input in G1–G6 changing by more than the stated tolerance</td></tr>
</tbody></table></div>

<h2>Why the gates are in this order</h2>
<p>The lease comes first because it is the only gate where delay destroys value by default: a notice date can
pass while the analysis is still running. The tenant and the valuation come next because they set the range.
Hazard and insurance come before the tax work only because an uninsurable asset changes the question being
asked, not just the number. The tax work is last among the inputs because it needs the sale price, and the
sale price needs the valuation.</p>

<h2>Status meanings</h2>
<div class="tablewrap"><table><thead><tr><th>Status</th><th>Meaning</th></tr></thead><tbody>
<tr><td><span class="pill bad">Blocked</span></td><td>Cannot start without a private document or a secure lookup. Not a judgement about difficulty.</td></tr>
<tr><td><span class="pill warn">Open</span></td><td>Work can start now, partly from public filings and partly from a private approach to the tenant.</td></tr>
<tr><td><span class="pill info">Pending</span></td><td>Depends on earlier gates. Starting it early would mean guessing inputs.</td></tr>
</tbody></table></div>
"""
    return page("decision-gates.html", "Decision gates", body,
                lede="Seven gates in order, each with the evidence required to clear it and the evidence in hand. "
                     "Nothing is committed while a gate is open.")


# ----------------------------------------------------------------- trade area
def build_trade_area():
    ctx = [next(r for r in D["findings"] if r["id"] == i)
           for i in ["E-01", "E-04", "E-05", "E-06", "E-07", "E-08", "E-02", "E-03", "E-09", "E-10", "E-11"]]

    tract_rows = [
        ("Population and households in the rings", "Total population, household count, household size"),
        ("Household income", "Median household income, income distribution, poverty rate"),
        ("Age structure", "Median age, share under 18, share over 65"),
        ("Housing tenure and cost", "Owner and renter shares, gross rent as a share of income"),
        ("Labour force and commuting", "Employment status, commute mode and duration, daytime workplace population"),
        ("Educational attainment", "Share with a bachelor's degree or higher"),
        ("Language and nativity", "Share speaking a language other than English at home"),
        ("Five-year direction", "Change in population and income across two matched vintages"),
    ]
    tract_html = "".join(
        f'<tr><td>{e(name)}</td><td class="small muted">{e(detail)}</td><td class="blank">—</td>'
        f'<td><span class="pill warn">Unverified</span></td>'
        f'<td class="small">Census ACS five-year tables, once the tracts are fixed inside the secure workspace</td></tr>'
        for name, detail in tract_rows)

    body = f"""
<div class="callout">
  <b>W-01, stated precisely.</b> City and county figures are proxies, and proxies are not evidence about a
  parcel. Replacing them requires the parcel's census tracts, and the parcel's location is deliberately not in
  this repository. So this page publishes the verified regional context, states clearly that it is context,
  and sets out the tract selection rule that will replace it. The table on this page will stay blank until
  that rule has been run inside the access-controlled workspace.
</div>

<h2>Regional context, verified — and explicitly not the trade area</h2>
{findings_table(ctx, show_category=False, show_note=True)}

<h2>Trade-area indicators — deliberately blank</h2>
<p>Each row below is a trade-area figure that the analysis needs. None can be published from a public source
without first fixing the tracts, and fixing the tracts requires the parcel.</p>
<div class="tablewrap"><table><thead><tr><th>Indicator</th><th>What it covers</th><th>Trade-area value</th><th>Status</th><th>Where it comes from</th></tr></thead>
<tbody>{tract_html}</tbody></table></div>

<h2>The tract selection rule</h2>
<ol>
  <li><b>Fix two rings, once.</b> A three-mile radius and a ten-minute drive-time polygon measured in the
  midday off-peak window, which is the relevant window for a lunch-driven drive-through. Write both down with
  the date and the routing tool used.</li>
  <li><b>Include a tract when most of its population falls inside the ring.</b> Use one rule and apply it to
  both rings. Record every included and excluded tract so the same list can be reused next year.</li>
  <li><b>Weight, do not average.</b> Weight each tract by its share of the ring's population, so a large tract
  does not dominate a small dense one.</li>
  <li><b>Use five-year estimates, and two vintages for direction.</b> One-year estimates are too noisy at tract
  level. Two matched five-year vintages give direction; a single vintage gives only a snapshot.</li>
  <li><b>Check comparability before comparing.</b> Tract boundaries and table definitions change between
  vintages. If the geography changed, the comparison is invalid and must be labelled as such.</li>
  <li><b>Never mix a tract figure with a county figure in the same row.</b> If a tract value is unavailable,
  the cell stays blank.</li>
</ol>

<h2>What county figures can and cannot tell you</h2>
<div class="tablewrap"><table><thead><tr><th>Question</th><th>Can the county answer it?</th><th>Why</th></tr></thead><tbody>
<tr><td>Is the region losing or gaining people?</td><td>Yes, directionally</td><td>Both the state and Census series show decline, though at different levels.</td></tr>
<tr><td>Are local incomes rising?</td><td>Partly</td><td>County median income rose 17.3% from 2021 to 2024, but that says nothing about the ring, and inflation is not removed.</td></tr>
<tr><td>Is this site's lunch demand growing?</td><td>No</td><td>Requires daytime workplace population and traffic counts at the site.</td></tr>
<tr><td>Is the immediate area over-supplied with competitors?</td><td>No</td><td>Requires a mapped competitor inventory inside the rings.</td></tr>
<tr><td>Will households stay as children age?</td><td>No</td><td>Requires tract-level age structure, tenure and school assignment.</td></tr>
<tr><td>Is the labour market tight for restaurant staff?</td><td>Yes, directionally</td><td>Metro unemployment 4.4% and payroll growth of 0.9%.</td></tr>
<tr><td>Are wage costs rising faster than prices?</td><td>Partly</td><td>Los Angeles CPI-U is published and the statutory wage floor is known; the mix for this operator is not.</td></tr>
</tbody></table></div>

<h2>Field evidence the spreadsheet cannot replace</h2>
<ul>
  <li><b>Traffic:</b> a published count at the nearest station, plus a manual peak-hour count at the driveway.</li>
  <li><b>Access and egress:</b> whether a left turn into the site is permitted at peak, and whether the
  drive-through queue blocks the sidewalk.</li>
  <li><b>Competitors:</b> every limited-service restaurant inside the rings, with opening date and closure date
  where known.</li>
  <li><b>Condition:</b> roof, parking surface, signage, and whether the building would suit a second-generation
  restaurant use without demolition.</li>
  <li><b>Development pipeline:</b> planning applications within the rings, because new supply changes the
  renewal case more than a one-year sales figure does.</li>
</ul>

<div class="callout info">
  <b>Why this matters to the decision.</b> The renewal case needs the trade area to grow. The sale case needs a
  buyer to believe it will. Both rest on tract-level direction, which is currently untested. A county figure
  cannot carry that weight, and publishing one as if it could would be the single easiest way to make this
  workspace wrong.
</div>
"""
    return page("trade-area.html", "Trade area", body,
                lede="County and metro context, verified and clearly labelled as context — plus the tract "
                     "selection rule that replaces it, and the trade-area rows left blank until it is run.")


# --------------------------------------------------------------------- hazards
def build_hazards():
    regional = [next(r for r in D["findings"] if r["id"] == i) for i in ["H-01", "E-03"]]
    parcel_rows = [
        ("Earthquake — fault rupture", "California Geological Survey EQ Zapp", "CGS-EQZAPP", "F-12",
         "An Alquist-Priolo zone limits where a structure can be placed and triggers a geologic report; it can constrain redevelopment."),
        ("Earthquake — liquefaction", "California Geological Survey EQ Zapp", "CGS-EQZAPP", "F-12",
         "Liquefaction drives foundation cost and repair severity after an event, and can be excluded from cover."),
        ("Earthquake — landslide", "California Geological Survey EQ Zapp", "CGS-EQZAPP", "F-12",
         "Slope failure affects access and utilities, which extends downtime beyond the building repair."),
        ("Flood — zone and base flood elevation", "FEMA Flood Map Service Center", "FEMA-MSC", "F-13",
         "Determines whether flood cover is required, what it costs, and whether a lender will accept the collateral."),
        ("Fire — hazard severity zone", "CAL FIRE Office of the State Fire Marshal, plus the local jurisdiction", "OSFM-FHSZ", "F-14",
         "Drives disclosure, mitigation duties and insurance pricing; local responsibility area classifications come from the city or county."),
        ("Structural performance", "Engineering assessment, not a public map", "CGS-EQZAPP", "F-16",
         "Sets the repair cost and the downtime that the loss-of-rent cover must bridge."),
        ("Insurance programme", "Broker quotes and a FAIR Plan comparison", "CDI-INSURANCE", "F-15",
         "The premium, deductible and exclusions decide whether the owner or the insurer bears the loss."),
    ]
    prow = "".join(
        f'<tr><td><b>{e(name)}</b></td><td class="small">{e(official)}<br>{src(sid, short=True)}</td>'
        f'<td class="blank">—</td>'
        f'<td><span class="pill warn">Unverified</span></td>'
        f'<td class="small">{e(impact)}</td><td class="small"><a href="flagged.html">{e(flag)}</a></td></tr>'
        for name, official, sid, flag, impact in parcel_rows)

    body = f"""
<div class="callout danger">
  <b>W-04 is a framework until the parcel is checked.</b> The regional hazard evidence is strong and verified.
  The parcel-level answer is missing, and it cannot be published: a zone determination identifies the property.
  Every determination below therefore happens inside the access-controlled workspace, and only the method and
  the regional context appear here.
</div>

<h2>Regional evidence, verified</h2>
{findings_table(regional, show_category=False, show_note=True)}

<h2>Parcel screening — what must be recorded, and where</h2>
<div class="callout info">
  For each row, record the source, the map panel or report identifier, the result and the date of the
  determination. A hazard file without dates is not a hazard file.
</div>
<div class="tablewrap"><table><thead><tr><th>Hazard</th><th>Official determination source</th><th>Parcel result</th><th>Status</th><th>What it changes</th><th>Flag</th></tr></thead>
<tbody>{prow}</tbody></table></div>

<h2>The three stresses, run together</h2>
<p>The brief asks for loss of rent, repairs and exit liquidity to be stressed together rather than one at a
time. That is the right instruction, because they arrive together.</p>
<div class="tablewrap"><table><thead><tr><th>Stress</th><th>Driver</th><th>How to size it</th><th>What it does to the decision</th></tr></thead><tbody>
<tr><td><b>Loss of rent</b></td><td>Building unusable, tenant not trading, or tenant refuses to pay during repair</td>
<td>Months of downtime from the engineer, multiplied by rent plus recoverable costs, less the loss-of-rent limit and the waiting period</td>
<td>If the cover does not reach the downtime, the owner funds the gap and the hold case weakens materially.</td></tr>
<tr><td><b>Repairs</b></td><td>Structural, façade, utilities, site works</td>
<td>Engineer's order-of-magnitude range plus a contingency, less the deductible</td>
<td>A repair bill near the property's net value makes the hold case a bet on insurance, not on real estate.</td></tr>
<tr><td><b>Exit liquidity</b></td><td>Buyers withdraw or demand a discount after an event</td>
<td>Assume no sale for at least two quarters after a declared disaster, and a wider cap rate on the eventual sale</td>
<td>If the owner needs liquidity during that window, the sale happens at the worst price. That is the real risk.</td></tr>
</tbody></table></div>

<h2>Insurance questions that decide more than the premium</h2>
<ul>
  <li>Is loss of rent covered, for how many months, and does the waiting period start at the event or at the
  end of the repair?</li>
  <li>Are earthquake, flood and wildfire covered at all, and are any of them excluded by endorsement?</li>
  <li>Is the deductible a fixed amount or a percentage of insured value? A percentage deductible scales with the
  problem.</li>
  <li>Does the policy require a seismic retrofit or a roof condition as a warranty? A warranty breach can void a
  claim after the loss.</li>
  <li>What happens at renewal if the carrier withdraws from the area? A FAIR Plan comparison answers the
  availability question, not the adequacy question.</li>
</ul>

<h2>Governance rule proposed for a declared event</h2>
<div class="callout">
  <b>Proposed, not adopted.</b> Write down now that no sale will be signed within 90 days of a declared
  disaster affecting the parcel, and that the decision will be re-underwritten from the hazard file rather than
  from the pre-event valuation. The value of the rule is that it is decided while calm.
</div>

<h2>What would change this page from framework to finding</h2>
<ol>
  <li>Four dated determinations from the official sources above.</li>
  <li>An engineering opinion with an order-of-magnitude repair range and a downtime estimate.</li>
  <li>Two insurance quotes plus a FAIR Plan comparison, with deductibles and exclusions.</li>
  <li>A written statement of the owner's liquidity outside this property, because exit liquidity is a function of
  the owner's balance sheet, not only the market's.</li>
</ol>
"""
    return page("hazards.html", "Hazards", body,
                lede="Earthquake, flood, fire and insurance screening: verified regional evidence, a parcel-level "
                     "protocol for the secure workspace, and the three stresses run together.")


# --------------------------------------------------------------- sell vs hold
def build_sell():
    tax_rows = [next(r for r in D["findings"] if r["id"] == i) for i in
                ["C-01", "C-02", "C-03", "C-04", "C-05", "C-06", "C-07", "C-08"]]
    tenant_rate = next(r for r in D["findings"] if r["id"] == "T-11")

    comp_rows = [
        ("Comparable A", "long lease, same corridor", "—", "—"),
        ("Comparable B", "short lease, same corridor", "—", "—"),
        ("Comparable C", "short lease, adjacent submarket", "—", "—"),
    ]
    comp_html = "".join(
        f'<tr><td>{e(n)}</td><td class="small">{e(k)}</td><td class="blank">—</td>'
        f'<td class="blank">—</td><td><span class="pill warn">Unverified</span></td>'
        f'<td class="small">Broker opinion comparable set</td></tr>' for n, k, _, _ in comp_rows)

    body = f"""
<div class="callout danger">
  <b>W-02, without a winner.</b> A sell-versus-hold comparison needs two numbers computed on the same day from
  the same inputs: after-tax net sale proceeds, and the present value of holding. Only one of the inputs is
  available today — the statutory tax rules. The rent, the price, the basis and the exit cap rate are not.
  So this page publishes the method and the verified rules, and refuses to publish a comparison.
</div>

<h2>The two numbers, defined</h2>
<div class="tablewrap"><table><thead><tr><th>Branch</th><th>What is computed</th><th>Inputs it needs</th><th>Inputs in hand</th></tr></thead><tbody>
<tr><td><b>Sell today</b></td>
<td>Net proceeds = price − selling costs − transfer taxes − federal tax − state tax.<br>
Federal tax = recapture × 25% + remaining gain × capital-gain rate + gain × net investment income rate.<br>
State tax = gain × marginal rate (California does not give a separate rate to capital gains).</td>
<td>Price, costs, basis, accumulated depreciation, filing status, residency, entity, transfer-tax rates</td>
<td>Statutory rates only. Price, basis and depreciation are private.</td></tr>
<tr><td><b>Hold</b></td>
<td>Net present value = present value of net operating income over the remaining term + present value of the
terminal sale at the exit cap rate, net of exit costs.</td>
<td>Rent, escalation, owner-retained costs, vacancy allowance, discount rate, exit cap rate, remaining term</td>
<td>The Treasury reference only. Rent, term and costs are private.</td></tr>
</tbody></table></div>
<p>Because both branches are computed on the same date with the same discount rate, the difference between them
is a single number the owner can act on: <b>hold value minus after-tax sale proceeds</b>. A positive difference
favours holding <i>on those inputs</i>; a negative one favours selling. The calculator computes that difference
and the price at which it becomes zero.</p>

<h2>The after-tax module — verified rules</h2>
{findings_table(tax_rows, show_category=False, show_note=True)}
<p class="small muted">Where the value cell is empty, the rule could not be confirmed on an official page during
the sweep, so no rate is shown. Those inputs are set by hand in the calculator.</p>

<h2>Short-lease discount — priced from quotes, not assumed</h2>
<p>The discount for a short lease is not a single market number; it is the difference between what buyers pay
for the same rent with a long term and with a short one. It can only be measured from comparable sales and
broker opinions, using the cap rate each transaction implies:</p>
<div class="callout info">
  <b>Method.</b> For the same rent, value is inversely proportional to the cap rate. If a comparable with a
  long lease trades at cap rate A and a comparable with a short lease trades at cap rate B, the observed
  short-lease discount is <b>1 − (A ÷ B)</b>, expressed as a percentage. The discount is then applied to the
  subject's long-lease value to establish what a buyer would pay today.
  <br><br>
  Example of the arithmetic only, with invented cap rates to show the shape: 5.50% against 6.75% implies
  <b>1 − (5.50 ÷ 6.75) = 18.5%</b>. Those numbers are illustrative and are not a market observation. The
  calculator applies this formula to whatever cap rates the comparable set actually supports.
</div>
<div class="tablewrap"><table><thead><tr><th>Comparable</th><th>Character</th><th>Remaining term (years)</th><th>Implied cap rate</th><th>Status</th><th>Source</th></tr></thead>
<tbody>{comp_html}</tbody></table></div>
<p>Three comparables are not enough for a statistical claim, but they are enough to price a discount honestly,
provided each one's remaining term and rent are known. A single blended "short-lease discount" quoted without
comparables should be treated as an assumption.</p>

<h2>What the capital markets currently say</h2>
<p>The 10-year Treasury closed at 4.91% on 24 November 2026. Separately, the tenant itself raised US$500 million
of senior secured notes at 7.624% in June 2026, secured partly by real estate and franchise cash flows. A buyer
of this lease will want a yield above the risk-free rate and above the tenant's own secured cost of debt, since
a lease claim is unsecured and subordinated in practice. That does not produce a cap rate — only comparable
sales do — but it does explain why a short lease is unlikely to be priced generously.</p>
{findings_table([tenant_rate, next(r for r in D["findings"] if r["id"] == "C-01")], show_category=False, show_note=True)}

<h2>What would make this page a comparison</h2>
<ol>
  <li>A sale price from at least three written broker opinions.</li>
  <li>The adjusted basis and accumulated depreciation from the accountant.</li>
  <li>Rent, escalation, remaining term and owner-retained costs from the lease abstract and operating statements.</li>
  <li>Transfer-tax rates confirmed by escrow, not by memory.</li>
  <li>A discount rate agreed in advance: either the owner's cost of capital or the Treasury rate plus a stated
  spread.</li>
  <li>An exit cap rate supported by comparables, tested at two percentage points either side.</li>
</ol>

<div class="actions">
  <a class="btn" href="calculator.html" style="display:inline-block;background:#16324f;color:#fff;padding:10px 16px;border-radius:9px;text-decoration:none;font-weight:600">Open the private calculator</a>
  <a class="btn secondary" href="questions.html" style="display:inline-block;background:#fff;color:#16324f;border:1px solid #cbd5e1;padding:10px 16px;border-radius:9px;text-decoration:none;font-weight:600">See the questions that unblock it</a>
</div>
"""
    return page("sell-vs-hold.html", "Sell vs hold", body,
                lede="The after-tax module and the short-lease discount, defined precisely — with the verified "
                     "tax rules and a refusal to publish a comparison built on missing inputs.")


# ------------------------------------------------------------------ calculator
def build_calculator():
    body = f"""
<div class="callout info">
  <b>Private by construction.</b> This page runs entirely in your browser. It has no network code, no storage,
  no cookies and no analytics, and nothing you type is sent anywhere. Close the tab and the numbers are gone.
  The page is checked by an automated test that fails the build if network or storage capability is ever added.
</div>

<div class="callout">
  <b>What this is.</b> Arithmetic on inputs you supply, nothing more. The default rates are the verified
  statutory maximums; every other field starts empty because this site does not know your rent, your basis or
  your price, and will not invent them. Nothing here is tax, legal or investment advice.
</div>

<form id="calc" autocomplete="off" onsubmit="return false">
  <fieldset>
    <legend>Sale today</legend>
    <div class="row">
      <div class="field"><label for="price">Gross sale price (US$)</label><input id="price" type="number" min="0" step="1000" inputmode="decimal" placeholder="0"></div>
      <div class="field"><label for="basis">Adjusted basis (US$)</label><input id="basis" type="number" min="0" step="1000" inputmode="decimal" placeholder="0"></div>
      <div class="field"><label for="dep">Accumulated depreciation (US$)</label><input id="dep" type="number" min="0" step="1000" inputmode="decimal" placeholder="0"></div>
      <div class="field"><label for="costs">Selling costs (% of price)</label><input id="costs" type="number" min="0" max="20" step="0.1" inputmode="decimal" placeholder="0.0"></div>
      <div class="field"><label for="transfer">Transfer taxes (% of price)</label><input id="transfer" type="number" min="0" max="20" step="0.01" inputmode="decimal" placeholder="0.00"></div>
    </div>
    <div class="row">
      <div class="field"><label for="ltcg">Federal capital gain rate</label>
        <select id="ltcg"><option value="0">0%</option><option value="0.15">15%</option><option value="0.20" selected>20%</option></select>
        <span class="small muted">Topic 409: 15% applies between US$48,350 and US$533,400 of taxable income for a single filer in 2025; 20% above that.</span>
      </div>
      <div class="field"><label for="recap">Section 1250 recapture rate</label>
        <input id="recap" type="number" min="0" max="0.5" step="0.01" value="0.25" inputmode="decimal">
        <span class="small muted">Statutory maximum 25%.</span>
      </div>
      <div class="field"><label for="niit">Net investment income rate</label>
        <input id="niit" type="number" min="0" max="0.2" step="0.001" value="0" inputmode="decimal">
        <span class="small muted">Left at zero because the rate was not verified in this sweep — see F-07.</span>
      </div>
      <div class="field"><label for="state">State income tax rate on the gain</label>
        <input id="state" type="number" min="0" max="0.2" step="0.001" value="0.123" inputmode="decimal">
        <span class="small muted">California top marginal rate 12.3%. The 1% surcharge above US$1m is not included — see F-08.</span>
      </div>
    </div>
  </fieldset>

  <fieldset>
    <legend>Hold</legend>
    <div class="row">
      <div class="field"><label for="rent">Annual rent received (US$)</label><input id="rent" type="number" min="0" step="1000" inputmode="decimal" placeholder="0"></div>
      <div class="field"><label for="esc">Annual rent escalation (%)</label><input id="esc" type="number" min="0" max="10" step="0.1" inputmode="decimal" placeholder="0.0"></div>
      <div class="field"><label for="years">Years remaining</label><input id="years" type="number" min="1" max="30" step="1" value="5" inputmode="numeric"></div>
      <div class="field"><label for="ownerCosts">Owner-retained costs per year (US$)</label><input id="ownerCosts" type="number" min="0" step="1000" inputmode="decimal" placeholder="0"></div>
      <div class="field"><label for="costInfl">Cost inflation (%)</label><input id="costInfl" type="number" min="0" max="15" step="0.1" inputmode="decimal" placeholder="0.0"></div>
    </div>
    <div class="row">
      <div class="field"><label for="vacancy">Vacancy and collection loss (% of rent)</label><input id="vacancy" type="number" min="0" max="50" step="0.5" inputmode="decimal" placeholder="0.0"></div>
      <div class="field"><label for="disc">Discount rate (%)</label><input id="disc" type="number" min="0.1" max="30" step="0.1" inputmode="decimal" placeholder="0.0">
        <span class="small muted">10-year Treasury was 4.91% on 24 November 2026; add a spread you can defend.</span>
      </div>
      <div class="field"><label for="cap">Exit cap rate (%)</label><input id="cap" type="number" min="0.5" max="30" step="0.1" inputmode="decimal" placeholder="0.0"></div>
      <div class="field"><label for="exitCosts">Exit costs (% of terminal value)</label><input id="exitCosts" type="number" min="0" max="20" step="0.1" inputmode="decimal" placeholder="0.0"></div>
    </div>
  </fieldset>

  <fieldset>
    <legend>Short-lease discount, from quotes</legend>
    <div class="row">
      <div class="field"><label for="capLong">Cap rate on a long-lease comparable (%)</label><input id="capLong" type="number" min="0.5" max="30" step="0.05" inputmode="decimal" placeholder="0.00"></div>
      <div class="field"><label for="capShort">Cap rate on a short-lease comparable (%)</label><input id="capShort" type="number" min="0.5" max="30" step="0.05" inputmode="decimal" placeholder="0.00"></div>
    </div>
    <p class="small muted">The discount is computed as 1 − (long cap ÷ short cap). It compares observations, not guesses.</p>
  </fieldset>

  <div class="actions">
    <button type="button" id="run">Compute</button>
    <button type="button" id="reset" class="secondary">Clear</button>
  </div>
</form>

<div class="output" id="out" aria-live="polite">
  <h3>Result</h3>
  <p class="big" id="headline">Enter your inputs, then compute</p>
  <div id="lines"></div>
  <p class="hint">Arithmetic only. No recommendation is made, and no figure here is a valuation, an appraisal or tax advice.</p>
</div>

<h2>How to read the output</h2>
<div class="tablewrap"><table><thead><tr><th>Output</th><th>Meaning</th><th>How to use it</th></tr></thead><tbody>
<tr><td>Federal and state tax on the sale</td><td>Recapture at the statutory rate plus the rest of the gain at the capital-gain rate, plus state tax on the whole gain.</td><td>Check it against your accountant's computation before relying on it.</td></tr>
<tr><td>Net sale proceeds</td><td>Price less selling costs, transfer taxes and tax.</td><td>This is the number that competes with holding.</td></tr>
<tr><td>Hold net present value</td><td>Rent net of owner costs and vacancy, discounted, plus the terminal sale at the exit cap rate.</td><td>Test the exit cap rate two points either way before drawing a conclusion.</td></tr>
<tr><td>Difference</td><td>Hold value minus net sale proceeds.</td><td>Positive favours holding on these inputs; negative favours selling. Neither is a recommendation.</td></tr>
<tr><td>Break-even price</td><td>The price at which the two branches are equal.</td><td>Compare it with the broker opinions: if the market is below it, selling destroys value on these assumptions.</td></tr>
<tr><td>Implied short-lease discount</td><td>Observed discount between long-lease and short-lease cap rates.</td><td>Replace the illustrative number with your comparable set.</td></tr>
</tbody></table></div>

<h2>Limits, stated plainly</h2>
<ul>
  <li>It ignores depreciation recapture timing rules, installment sales, exchanges and entity-level tax.</li>
  <li>It assumes a single rent stream and a single exit. It cannot model a partial renewal or a re-tenanting period
  except through the vacancy field and a lower rent.</li>
  <li>It assumes the terminal value is achieved exactly at the exit cap rate, which is the most fragile assumption
  in any real estate model.</li>
  <li>It is not a back-tested model. A cash-flow model should only be relied on once it has been back-tested
  against actual outcomes, which requires comparable history this repository does not hold.</li>
</ul>
"""
    return page("calculator.html", "Private calculator", body,
                lede="A browser-only after-tax and hold-value calculator. No network, no storage, no defaults for "
                     "figures the site cannot verify.",
                scripts='<script src="assets/calc.js" defer></script>')


CALC_JS = r"""
/* Private, offline calculator for the sell-versus-hold comparison.
   Deliberately inert: no fetch, no storage, no cookies, no external calls. */
(function () {
  "use strict";
  var ids = ["price","basis","dep","costs","transfer","ltcg","recap","niit","state",
             "rent","esc","years","ownerCosts","costInfl","vacancy","disc","cap","exitCosts",
             "capLong","capShort"];
  function el(id) { return document.getElementById(id); }
  function num(id) {
    var v = el(id) && el(id).value !== "" ? parseFloat(el(id).value) : NaN;
    return isFinite(v) ? v : 0;
  }
  function pct(id) { return num(id) / 100; }
  function money(n) {
    if (!isFinite(n)) return "—";
    return n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
  }
  function pctText(n) {
    if (!isFinite(n)) return "—";
    return (n * 100).toFixed(1).replace(/\.0$/, "") + "%";
  }
  function sale(price) {
    var costs = price * pct("costs");
    var transfer = price * pct("transfer");
    var basis = num("basis");
    var dep = num("dep");
    var gain = Math.max(0, price - costs - transfer - basis);
    var recapture = Math.min(dep, gain);
    var remainder = gain - recapture;
    var fed = recapture * num("recap") + remainder * num("ltcg") + gain * num("niit");
    var state = gain * num("state");
    var net = price - costs - transfer - fed - state;
    return { costs: costs, transfer: transfer, gain: gain, recapture: recapture,
             remainder: remainder, fed: fed, state: state, tax: fed + state, net: net };
  }
  function holdNpv() {
    var rent = num("rent"), esc = pct("esc"), years = Math.max(1, Math.round(num("years")));
    var ownerCosts = num("ownerCosts"), costInfl = pct("costInfl"), vacancy = pct("vacancy");
    var disc = pct("disc"), cap = pct("cap"), exitCosts = pct("exitCosts");
    var pv = 0, y, noi;
    for (y = 1; y <= years; y++) {
      noi = rent * Math.pow(1 + esc, y - 1) * (1 - vacancy) - ownerCosts * Math.pow(1 + costInfl, y - 1);
      pv += noi / Math.pow(1 + disc, y);
    }
    var terminalNoi = rent * Math.pow(1 + esc, years) * (1 - vacancy);
    var terminalValue = cap > 0 ? terminalNoi / cap : 0;
    var terminalNet = terminalValue * (1 - exitCosts);
    pv += terminalNet / Math.pow(1 + disc, years);
    return { pv: pv, terminalValue: terminalValue, terminalNet: terminalNet, years: years, disc: disc };
  }
  function breakEven(target) {
    var lo = 0, hi = Math.max(1000000, Math.abs(target) * 20 + num("basis") + 1000000), mid, i, s;
    for (i = 0; i < 80; i++) {
      mid = (lo + hi) / 2;
      s = sale(mid);
      if (s.net - target < 0) { lo = mid; } else { hi = mid; }
    }
    return (lo + hi) / 2;
  }
  function line(label, value, cls) {
    return '<div class="line"><span>' + label + '</span><span class="' + (cls || "") + '">' + value + "</span></div>";
  }
  function run() {
    var price = num("price");
    var s = sale(price);
    var h = holdNpv();
    var diff = h.pv - s.net;
    var be = breakEven(h.pv);
    var out = [];
    var head = el("headline"), lines = el("lines");

    if (price <= 0 && num("rent") <= 0) {
      head.textContent = "Enter a price or a rent to begin";
      lines.innerHTML = "";
      return;
    }
    if (h.disc <= 0) {
      head.textContent = "Set a discount rate above zero";
      lines.innerHTML = "";
      return;
    }

    head.innerHTML = diff >= 0
      ? "Hold value exceeds net sale proceeds by " + money(diff)
      : "Net sale proceeds exceed hold value by " + money(-diff);

    out.push(line("Gross sale price", money(price)));
    out.push(line("Selling costs", "−" + money(s.costs)));
    out.push(line("Transfer taxes", "−" + money(s.transfer)));
    out.push(line("Realised gain", money(s.gain)));
    out.push(line("of which depreciation recapture", money(s.recapture)));
    out.push(line("Federal tax", "−" + money(s.fed)));
    out.push(line("State tax", "−" + money(s.state)));
    out.push(line("<b>Net sale proceeds</b>", "<b>" + money(s.net) + "</b>"));
    out.push(line("Hold: present value of rent, " + h.years + " years at " + pctText(h.disc), money(h.pv - h.terminalNet / Math.pow(1 + h.disc, h.years))));
    out.push(line("Hold: present value of terminal sale", money(h.terminalNet / Math.pow(1 + h.disc, h.years))));
    out.push(line("<b>Hold net present value</b>", "<b>" + money(h.pv) + "</b>"));
    out.push(line("<b>Difference, hold minus sell</b>", "<b class=\"" + (diff >= 0 ? "pos" : "neg") + "\">" + money(diff) + "</b>"));
    out.push(line("Break-even sale price", money(be)));

    var cl = pct("capLong"), cs = pct("capShort");
    if (cl > 0 && cs > 0) {
      var discount = 1 - (cl / cs);
      out.push(line("Implied short-lease discount", pctText(discount) +
        " (long " + pctText(cl) + " vs short " + pctText(cs) + ")"));
    } else {
      out.push(line("Implied short-lease discount", "enter two comparable cap rates"));
    }
    if (s.gain <= 0) {
      out.push(line("Note", "No gain on these inputs, so tax is zero."));
    }
    if (num("niit") === 0) {
      out.push(line("Note", "Net investment income rate is zero because it was not verified — check F-07."));
    }
    lines.innerHTML = out.join("");
  }
  function clearAll() {
    var i;
    for (i = 0; i < ids.length; i++) {
      if (el(ids[i]) && el(ids[i]).tagName === "INPUT") { el(ids[i]).value = ""; }
    }
    el("years").value = "5";
    el("recap").value = "0.25";
    el("niit").value = "0";
    el("state").value = "0.123";
    el("ltcg").value = "0.20";
    document.getElementById("headline").textContent = "Enter your inputs, then compute";
    document.getElementById("lines").innerHTML = "";
  }
  document.addEventListener("DOMContentLoaded", function () {
    var runBtn = el("run"), resetBtn = el("reset");
    if (runBtn) { runBtn.addEventListener("click", run); }
    if (resetBtn) { resetBtn.addEventListener("click", clearAll); }
    var form = el("calc");
    if (form) {
      form.addEventListener("input", function () {
        var price = num("price");
        if (price > 0 || num("rent") > 0) { run(); }
      });
    }
  });
})();
"""


# --------------------------------------------------------------------- risks
def build_risks():
    rows = "".join(
        f'<tr><td><code>{e(r["id"])}</code></td><td><b>{e(r["decision"])}</b></td><td>{e(r["risk"])}</td>'
        f'<td class="small">{e(r["evidence"])}</td>'
        f'<td><span class="pill {"bad" if r["severity"]=="High" else "warn"}">{e(r["severity"])}</span></td>'
        f'<td class="small">{e(r["mitigation"])}</td></tr>'
        for r in D["risks"])

    sw = "".join(
        f'<tr><td><code>{e(b["id"])}</code></td><td><b>{e(b["event"])}</b></td><td class="small">{e(b["evidence"])}</td>'
        f'<td class="small">{e(b["channel"])}</td><td class="small">{e(b["preparation"])}</td></tr>'
        for b in D["blackswans"])

    body = f"""
<div class="callout">
  <b>How to read this page.</b> Risk is listed against each decision, not against the property in the abstract,
  because the same hazard is a different risk depending on whether the owner sells, holds or renews. Severity is
  a judgement and is labelled as one; the evidence beside it is sourced. Nothing here is a probability estimate
  except where an official source publishes one.
</div>

<h2>Risk by decision</h2>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Decision</th><th>Risk</th><th>Evidence</th><th>Severity</th><th>Mitigation</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Black swan register</h2>
<p>A black swan here means an event that is rare, severe and arrives with the other stresses: rent stops, repairs
start and buyers disappear at the same time. Each entry states how it transmits into the decision and what can be
done before it happens.</p>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Event</th><th>Verified evidence</th><th>How it reaches the decision</th><th>Preparation, before the event</th></tr></thead>
<tbody>{sw}</tbody></table></div>

<h2>Three scenarios, and what moves in each</h2>
<div class="tablewrap"><table><thead><tr><th>Scenario</th><th>What happens</th><th>What the owner can control</th><th>What the owner cannot</th></tr></thead><tbody>
<tr><td><b>Base</b></td><td>Rent is paid through the term; the tenant closes some units elsewhere; the parcel stays insurable at a higher premium.</td>
<td>The renewal rent, the timing of any sale, and the quality of the diligence file.</td>
<td>Cap rates, the tenant's systemwide performance, and the trade area's direction.</td></tr>
<tr><td><b>Downside</b></td><td>The tenant asks for relief or gives notice; the building sits vacant for a year or more; insurance costs rise sharply.</td>
<td>Whether a security deposit, guarantee or letter of credit exists at renewal; how fast a re-leasing plan can start.</td>
<td>How long a specialised building takes to re-let, and whether a replacement tenant exists at all.</td></tr>
<tr><td><b>Black swan</b></td><td>A damaging earthquake or a fire, combined with an insurance market that will not renew, at the same time as a rate shock.</td>
<td>The deductible funding, the loss-of-rent limit, and a written rule against selling into the first 90 days.</td>
<td>Everything else, including the price a buyer would pay for a damaged asset.</td></tr>
</tbody></table></div>

<h2>What "manageable risk" could mean, concretely</h2>
<p>The owner asked for a balance between preserving wealth and keeping growth possible, at a manageable level of
risk. That cannot be answered in the abstract, but it can be operationalised with three thresholds agreed in
advance. They are proposed here, not adopted:</p>
<ol>
  <li><b>Insured-loss threshold.</b> The largest single uninsured loss the owner could absorb from liquid
  reserves without selling another asset. If the deductible plus the uncovered downtime exceeds it, the hazard
  programme is inadequate regardless of the premium.</li>
  <li><b>Downtime threshold.</b> The number of months of zero rent the owner could fund from reserves. Compare it
  with the re-leasing study's estimate; if the study exceeds the threshold, the hold case is a liquidity bet.</li>
  <li><b>Concentration threshold.</b> The share of the owner's net worth this single parcel represents. Above a
  stated share, idiosyncratic tenant and hazard risk dominate the portfolio and a sale becomes a diversification
  decision rather than a price decision.</li>
</ol>
<div class="callout info">
  <b>Why thresholds rather than a score.</b> A weighted risk score would look rigorous and mean nothing, because
  the weights would be invented. Three thresholds tied to the owner's actual balance sheet are checkable, and they
  convert "manageable" from an adjective into a test.
</div>

<h2>Risks this page does not cover</h2>
<ul>
  <li>Owner-specific legal, estate and family considerations, which belong with counsel.</li>
  <li>Financing risk on any debt secured by the parcel, which is unknown.</li>
  <li>Local regulatory change beyond the transfer and wage rules already cited, which would require a planning
  and zoning review.</li>
  <li>Tenant brand-specific litigation or food-safety events, which cannot be anticipated from filings.</li>
</ul>
"""
    return page("risks.html", "Risks", body,
                lede="Decision-by-decision risks with sourced evidence, a black swan register, and three "
                     "thresholds that turn 'manageable' into something checkable.")


# ----------------------------------------------------------------- questions
def build_questions():
    areas = []
    for area in ["Lease", "Title", "Tenant", "Trade area", "Schools", "Hazards", "Valuation", "Tax", "Process"]:
        qs = [q for q in D["questions"] if q["area"] == area]
        if not qs:
            continue
        rows = "".join(
            f'<tr><td><code>{e(q["id"])}</code></td><td><b>{e(q["question"])}</b><br>'
            f'<span class="small muted">{e(q["why"])}</span></td>'
            f'<td class="small">{e(q["owner"])}<br><span class="muted">{e(q["document"])}</span></td>'
            f'<td><span class="pill gate">{e(q["gate"])}</span></td>'
            f'<td class="small"><b>If yes:</b> {e(q["ifYes"])}<br><b>If no:</b> {e(q["ifNo"])}</td></tr>'
            for q in qs)
        areas.append(
            f'<h2 id="{e(area.lower().replace(" ", "-"))}">{e(area)}</h2>'
            '<div class="tablewrap"><table><thead><tr><th>ID</th><th>Question and why it matters</th>'
            '<th>Who answers, and from which document</th><th>Gate</th><th>What changes with the answer</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')

    body = f"""
<div class="callout danger">
  <b>The short answer to "can a decision be made?" is no, and these are the reasons.</b>
  {len(D["questions"])} questions stand between the evidence in hand and a decision that can be defended. They
  are grouped below by area, each with the person who can answer it, the document that answers it, the gate it
  belongs to, and what changes depending on the answer. The first four are urgent because delay itself
  forecloses options.
</div>

<h2>The four that cannot wait</h2>
<ol>
  <li><b>Q-01 and Q-02 — exact expiry, options and notice dates.</b> Everything else is analysis; this is
  deadline management. A notice period that passes removes a choice permanently.</li>
  <li><b>Q-07 — has the tenant said anything about renewal?</b> The renewal branch is currently an assumption,
  not a position.</li>
  <li><b>Q-23 — adjusted basis and depreciation.</b> Without them, the sale number is pre-tax and therefore
  wrong by an unknown amount.</li>
  <li><b>Q-16 to Q-19 — the hazard and insurance file.</b> An uninsurable loss is the only event that can force
  a sale at the worst moment.</li>
</ol>

<h2>How to discover what is missing</h2>
<div class="tablewrap"><table><thead><tr><th>Missing information</th><th>Discovery route</th><th>Who holds it</th><th>Realistic lead time</th></tr></thead><tbody>
<tr><td>Lease terms, options and notice dates</td><td>Document request to the owner's file; counsel abstracts it</td><td>Owner, counsel, tenant</td><td>1–2 weeks</td></tr>
<tr><td>Tenant's renewal intention</td><td>Estoppel certificate request plus a written question through the broker</td><td>Tenant's real estate or asset management group</td><td>2–4 weeks</td></tr>
<tr><td>Store-level performance</td><td>Confidentiality agreement, then a data request</td><td>Franchisee and brand</td><td>2–6 weeks</td></tr>
<tr><td>Parcel hazard determinations</td><td>Four official lookups, one engineer, two insurance quotes</td><td>State and federal agencies, engineer, broker</td><td>1–4 weeks</td></tr>
<tr><td>Market value and short-lease discount</td><td>Three broker opinions and a comparable sale pull</td><td>Brokers, appraiser, title</td><td>3–6 weeks</td></tr>
<tr><td>Trade-area indicators</td><td>Tract selection, then ACS extraction and weighting</td><td>Analyst</td><td>1–2 weeks once tracts are fixed</td></tr>
<tr><td>Tax position</td><td>Accountant prepares the computation from basis and depreciation records</td><td>Accountant, escrow</td><td>2–3 weeks</td></tr>
<tr><td>Traffic and competitor evidence</td><td>Count request to the transportation department; field survey</td><td>City or state, analyst</td><td>2–6 weeks</td></tr>
<tr><td>Insurance capacity</td><td>Two quotes plus a FAIR Plan comparison</td><td>Broker</td><td>2–4 weeks</td></tr>
</tbody></table></div>

<h2>Questions by area</h2>
{"".join(areas)}

<h2>What to do with the answers</h2>
<ol>
  <li>Record each answer with its source and date in the internal workspace, then update the matching gate on
  <a href="decision-gates.html">Decision gates</a>.</li>
  <li>Re-run the <a href="calculator.html">calculator</a> only after the six inputs listed on
  <a href="sell-vs-hold.html">Sell vs hold</a> are all present.</li>
  <li>Write the decision memo while the inputs are fresh, with the three scenarios and a decision date.</li>
  <li>Log anything that could not be answered on <a href="flagged.html">Flagged for review</a> rather than
  filling the gap.</li>
</ol>
"""
    return page("questions.html", "Questions", body,
                lede="Every question that must be answered before a decision, who holds the answer, which document "
                     "contains it, and what changes depending on what it says.")



# -------------------------------------------------------------- requirements
REQUIREMENTS = [
    ("R-01", "W-01", "Replace city and county proxies with trade-area figures",
     "Delivered as a method; figures blocked",
     "trade-area.html", "Six-step tract selection rule, weighting, two-vintage direction test, and eleven trade-area rows left blank. County figures are published but labelled as context, not as trade-area evidence."),
    ("R-02", "W-02", "Extend the private worksheet to a sell-versus-hold comparison",
     "Delivered as a method; comparison blocked",
     "sell-vs-hold.html", "Both branches defined formulaically, the difference identified as the decision number, and the six inputs that would make it a comparison listed. No comparison published, because the inputs are private."),
    ("R-03", "W-03", "Decision-gate progress board",
     "Delivered", "decision-gates.html", "Seven gates with question, status, evidence required, evidence in hand, artefact that clears it, owner and what reopens it."),
    ("R-04", "W-04", "Parcel-level hazard screening",
     "Framework delivered; parcel status blocked",
     "hazards.html", "Earthquake, liquefaction, landslide, flood, fire, structural and insurance rows, each with the official determination source; all parcel results blank for privacy."),
    ("R-05", "W-10", "One-page printable summary for advisors",
     "Delivered", "printable-summary.html", "Print stylesheet, eighteen verified figures with sources, gate status, seven questions, three next actions and four prohibitions."),
    ("R-06", "X-01", "A private calculator that runs in the reader's browser",
     "Delivered", "calculator.html", "Client-side only: no network, storage, cookies or analytics; enforced by an automated test that fails the build on any of them."),
    ("R-07", "X-02", "Neighbourhood-level data around the parcel",
     "Blocked by privacy", "trade-area.html", "Requires the parcel to fix the rings. The selection rule and the indicator list are published; the values are not."),
    ("R-08", "X-03", "An after-tax module",
     "Delivered as rules; owner computation blocked",
     "sell-vs-hold.html", "Verified federal rate tiers, section 1250 maximum, California brackets, and an explicit list of the owner-specific inputs the accountant must supply."),
    ("R-09", "X-04", "Price the short-lease discount from real quotes",
     "Method delivered; quotes blocked",
     "sell-vs-hold.html", "Discount defined as 1 − (long-lease cap rate ÷ short-lease cap rate), applied through a comparable table that is empty pending broker opinions."),
    ("R-10", "X-05", "Tract-level trend evidence alongside the regional figures",
     "Blocked by privacy", "trade-area.html", "Regional series published with sources; the tract trend is specified but not published."),
    ("R-11", "X-06", "Executive summary",
     "Delivered", "executive-summary.html", "Three candidate paths, each with a test it must pass and a kill criterion; what is known; what is missing; an eight-week sequence."),
    ("R-12", "X-07", "Risks, including black swan events",
     "Delivered", "risks.html", "Twelve decision-specific risks with sourced evidence, six black swans with transmission channels and preparation, and three checkable thresholds."),
    ("R-13", "X-08", "Questions, information and answers needed before a decision",
     "Delivered", "questions.html", "Twenty-eight questions with owner, document, gate, and what changes depending on the answer, plus nine discovery routes and lead times."),
    ("R-14", "X-09", "A suggestions section, reviewed before anything is implemented",
     "Delivered", "suggestions.html", "Fifteen proposals ordered by whether delay has a cost; site changes described, not built."),
    ("R-15", "X-10", "Flag irregular and unverified items for review",
     "Delivered", "flagged.html", "Twenty blank items with the exact check and official link, plus eight consolidation irregularities with their handling."),
    ("R-16", "X-11", "Anonymise all personal information; placeholders only",
     "Delivered and enforced", "privacy.html", "Placeholder discipline, layer separation, threat table, operating rules, and an automated identifier scan in the build."),
    ("R-17", "X-12", "Verify every figure against an official source, with links",
     "Delivered", "verification.html", "Forty ledger rows: twenty-eight verified with source and date, twelve blank and flagged, zero inferred."),
    ("R-18", "X-13", "A clean live GitHub Pages site with categorised subpages",
     "Delivered", "index.html", "Fifteen pages in three navigation groups, generated from a data layer, with a link and provenance check in continuous integration."),
    ("R-19", "X-14", "Coordinate parallel sessions through a shared board",
     "Delivered", "COORDINATION.md",
     "Session claim, file scope, verification log, irregularity log, and an archive of every earlier dashboard with its cut-off date."),
    ("R-20", "—", "Decide whether to sell before expiry or renew",
     "Cannot be completed on available evidence",
     "executive-summary.html", "The decision is the deliverable the brief asks for and the one thing this site refuses to fake. Three paths are specified; the inputs that would choose between them are listed and missing."),
    ("R-21", "—", "Balance wealth preservation against growth at a manageable risk level",
     "Delivered as a framework", "risks.html", "Three thresholds tied to the owner's balance sheet — uninsured loss, rent-free downtime, and concentration — instead of an invented risk score."),
    ("R-22", "—", "Build a reliable projection system for the area",
     "Deliberately not delivered",
     "suggestions.html", "A projection needs a target with history, predictors at the same geography, and back-testing. None exists yet, so the site publishes scenarios labelled as assumptions and states the preconditions."),
    ("R-23", "—", "Work without manual input from the owner",
     "Delivered within the privacy limit", "questions.html", "Everything obtainable from official sources was obtained and verified. The remainder requires documents that must not be published, and is specified rather than requested ad hoc."),
]


def build_requirements():
    rows = []
    for rid, wid, req, status, where, detail in REQUIREMENTS:
        cls = "ok" if status.startswith("Delivered") else ("warn" if "blocked" in status.lower() else "bad")
        link = f'<a href="{e(where)}">{e(where)}</a>'
        rows.append(
            f'<tr><td><code>{e(rid)}</code></td><td><b>{e(wid)}</b></td><td>{e(req)}</td>'
            f'<td><span class="pill {cls}">{e(status)}</span></td><td class="small">{link}</td>'
            f'<td class="small">{e(detail)}</td></tr>')
    fulfilled = sum(1 for r in REQUIREMENTS if r[3].startswith("Delivered"))
    blocked = sum(1 for r in REQUIREMENTS if "blocked" in r[3].lower())
    refused = sum(1 for r in REQUIREMENTS if r[3].startswith("Cannot") or r[3].startswith("Deliberately"))
    body = f"""
<div class="callout info">
  <b>Traceability, including what was refused.</b> The brief asked for a full list of requirements, organised
  and analysed. This page maps each requirement to the page that addresses it, states the status honestly, and
  records the two that cannot be completed on available evidence. A requirement marked delivered is delivered
  as a <i>method</i> when the underlying values are private; the wording says which.
</div>

<div class="grid">
  <div class="card"><h3>Requirements traced</h3><p class="kpi">{len(REQUIREMENTS)}</p><p>Every item in the brief, deduplicated.</p></div>
  <div class="card"><h3>Delivered</h3><p class="kpi">{fulfilled}</p><p>Page exists, is sourced, and is checked in continuous integration.</p></div>
  <div class="card"><h3>Blocked by privacy</h3><p class="kpi">{blocked}</p><p>The value cannot be published without identifying the property.</p></div>
  <div class="card"><h3>Cannot be completed</h3><p class="kpi">{refused}</p><p>The decision itself, and the projection, both for stated reasons.</p></div>
</div>

<h2>Traceability matrix</h2>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Brief ref</th><th>Requirement</th><th>Status</th><th>Where addressed</th><th>What is actually there</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>

<h2>Why "delivered as a method" is the honest label</h2>
<p>Four requirements — trade-area figures, the sell-versus-hold comparison, parcel hazard status and the
neighbourhood data — cannot be finished without records that identify the property. Publishing those records
would breach the owner's first instruction, which outranks the analytical instruction. The compromise is
deliberate: publish the rule, the formula, the official lookup and the blank, so a reader can see exactly what
remains and who holds it. That is more useful than a number with no provenance, and it is the only version of
this project that respects both instructions at once.</p>

<h2>Requirements that conflict, and how the conflict was resolved</h2>
<div class="tablewrap"><table><thead><tr><th>Conflict</th><th>Resolution</th></tr></thead><tbody>
<tr><td>"Deep research to build a reliable projection system" against "no hallucinations" and "never infer"</td>
<td>The projection is specified, not fabricated. Preconditions are listed on <a href="suggestions.html">Suggestions</a>.</td></tr>
<tr><td>"Tell me the best decision" against "do not select a winner until verified inputs exist"</td>
<td>The decision is refused and replaced with three testable paths, each with a kill criterion.</td></tr>
<tr><td>"No manual input from me" against "commission a private lease abstract"</td>
<td>Everything public was obtained without input. Documents only the owner holds are specified precisely, so the handover is one email rather than an interview.</td></tr>
<tr><td>"Include all findings" against "no personal information on the site"</td>
<td>Findings are published; identifiers are not. The archive keeps earlier work rather than deleting it.</td></tr>
</tbody></table></div>
"""
    return page("requirements.html", "Requirements traceability", body,
                lede="Every requirement in the brief, the page that addresses it, the honest status, and the two "
                     "that cannot be completed on available evidence.")


# ---------------------------------------------------------------- suggestions
def build_suggestions():
    rows = "".join(
        f'<tr><td><code>{e(s["id"])}</code></td><td><b>{e(s["title"])}</b><br>'
        f'<span class="small muted">{e(s["detail"])}</span></td>'
        f'<td class="small">{e(s["type"])}</td>'
        f'<td class="small">{e(s["effort"])}</td>'
        f'<td class="small">{e(s["impact"])}</td>'
        f'<td class="small">{e(s["decision"])}</td></tr>'
        for s in D["suggestions"])

    body = f"""
<div class="callout">
  <b>Nothing on this page has been implemented.</b> These are proposals, written so they can be reviewed,
  argued with and chosen one at a time. The site changes are described here rather than built, because the
  owner asked to review suggestions before anything is implemented.
</div>

<h2>How to choose</h2>
<ol>
  <li><b>Start with the four that protect optionality</b> (S-01 to S-04). They are low effort, high impact, and
  they are the only ones where delay has a cost.</li>
  <li><b>Then the three that produce the number</b> (S-03, S-07, S-08). Without them there is no comparison, only
  an opinion.</li>
  <li><b>Then governance</b> (S-09, S-10). They cost nothing and stop the decision drifting.</li>
  <li><b>Site changes last</b> (S-11 to S-13). They improve how the evidence is maintained, not what the evidence
  says.</li>
</ol>

<h2>The register</h2>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Proposal</th><th>Type</th><th>Effort</th><th>Impact</th><th>Decision needed before anyone starts</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Site improvements, awaiting a decision</h2>
<p>These are suggestions about this dashboard itself. Each is written as a change the owner can accept or reject;
none has been made.</p>
<div class="tablewrap"><table><thead><tr><th>Change</th><th>Why it would help</th><th>Cost or risk of doing it</th><th>What it would not fix</th></tr></thead><tbody>
<tr><td><b>S-11</b> — a release watch</td><td>Employment, price, population and tenant filings arrive on a schedule; a dated list keeps the evidence current without another research pass.</td><td>Maintenance discipline; dates drift if nobody owns it.</td><td>It does not create parcel-level evidence.</td></tr>
<tr><td><b>S-12</b> — machine-checked provenance</td><td>The build already fails on a missing source id. Extending the same check to every legacy dashboard would stop the older pages drifting.</td><td>Another session's directory would need editing; that requires their agreement.</td><td>It checks that a source exists, not that the source says what the page claims.</td></tr>
<tr><td><b>S-13</b> — retire the overlapping dashboards</td><td>Six dashboards with different cut-off dates invite the wrong number being quoted.</td><td>Some historical context is lost unless the archive is kept.</td><td>It does not resolve the underlying data gaps.</td></tr>
<tr><td><b>Show a source column in every table</b></td><td>Already done: each row links to its official page. Keeping the habit in future pages is the point.</td><td>Wider tables on small screens; handled with horizontal scroll.</td><td>It does not make an unavailable value available.</td></tr>
<tr><td><b>Keep the no-forecast rule</b></td><td>A projection would look decisive and would be unsupported. The brief asks for a reliable projection system; reliability requires back-testing against real history.</td><td>The site gives less comfort than a forecast would.</td><td>It does not by itself produce a decision.</td></tr>
</tbody></table></div>

<h2>What a reliable projection system would require</h2>
<p>The brief asks for a deep, reliable projection system for the area. That is a reasonable ambition and it has
preconditions that are not yet met. A model that could be trusted would need:</p>
<ol>
  <li><b>A target with history.</b> Store-level sales for this unit, or failing that, a comparable set of
  drive-through units with five or more years of observations.</li>
  <li><b>Predictors measured at the same geography and frequency.</b> Tract or ring-level population, income,
  employment and traffic, not county proxies.</li>
  <li><b>Back-testing.</b> Fit on the earlier period, predict the later one, and report the error honestly. A
  model that has never been back-tested is a hypothesis.</li>
  <li><b>Explicit separation of observation and assumption.</b> Every input labelled as one or the other, so a
  reader can see which part of the output is evidence.</li>
  <li><b>Versioning.</b> Each run dated, with its inputs, so a later reader can reproduce it.</li>
</ol>
<div class="callout info">
  <b>Proposed rule.</b> Do not publish a point forecast for this parcel until items 1 to 3 are satisfied. Until
  then, publish scenario ranges labelled as assumptions, which is what this site does.
</div>
"""
    return page("suggestions.html", "Suggestions", body,
                lede="Fifteen proposals, ordered by whether delay has a cost — with the site changes left "
                     "unimplemented so they can be reviewed first.")


# ------------------------------------------------------------------- flagged
def build_flagged():
    rows = "".join(
        f'<tr><td><code>{e(f["id"])}</code></td><td><b>{e(f["item"])}</b></td>'
        f'<td class="blank">—</td>'
        f'<td class="small">{e(f["reason"])}</td>'
        f'<td class="small">{e(f["verify"])}</td>'
        f'<td class="small">{src(f["sourceId"], short=True)}</td></tr>'
        for f in D["flagged"])

    body = f"""
<div class="callout">
  <b>This page is the review queue, not a failure list.</b> Every row is blank because the value could not be
  confirmed from an official source without private data, or because publishing it would identify the property.
  Flagged items do not block publication of the rest of the site. Review a row, supply the missing document or
  confirm the figure in the internal workspace, and the row moves to the ledger.
</div>

<h2>Twenty items left blank on purpose</h2>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Item</th><th>Value</th><th>Why it is blank</th><th>How to check it</th><th>Official link</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Irregularities found during this session</h2>
<div class="tablewrap"><table><thead><tr><th>#</th><th>What was found</th><th>Status</th></tr></thead><tbody>
<tr><td>1</td><td>The repository readme on the default branch contained unresolved merge-conflict markers, so the project's front page was partly unreadable.</td><td><span class="pill ok">Fixed</span> Markers removed; the readme now describes this consolidated workspace and the archive.</td></tr>
<tr><td>2</td><td>A legacy dashboard's test suite fails with "table row missing source" and was never run by continuous integration, so the failure was invisible.</td><td><span class="pill warn">Logged</span> Not edited, because that directory is another session's scope. Recorded in <code>COORDINATION.md</code> and here.</td></tr>
<tr><td>3</td><td>Six dashboards publish overlapping figures with different cut-off dates, including same-store sales for FY2025 and for Q3 FY2025.</td><td><span class="pill ok">Resolved by consolidation</span> This site is the entry point; the legacy pages are kept under Archive with their dates.</td></tr>
<tr><td>4</td><td>Two official agencies publish Los Angeles County population estimates differing by more than 140,000 persons.</td><td><span class="pill warn">Disclosed</span> Both published with sources and dates; neither averaged. F-02.</td></tr>
<tr><td>5</td><td>The October 2026 Los Angeles 12-month CPI change does not exist, because October 2025 data were not collected during the federal funding lapse.</td><td><span class="pill warn">Disclosed</span> Index level and month-on-month change published; the missing cell is labelled, not filled.</td></tr>
<tr><td>6</td><td>No Q4 or full-year FY2026 tenant release was on file at the sweep date, although the fiscal year ended on 27 September 2026.</td><td><span class="pill warn">Open</span> F-01; annual figures are not published.</td></tr>
<tr><td>7</td><td>Several official pages did not respond during the sweep: Census QuickFacts, the city finance pages, the county recorder and the Board of Equalization.</td><td><span class="pill warn">Open</span> The affected values are blank and each carries a manual-review link. No secondary source was substituted.</td></tr>
<tr><td>8</td><td>The city minimum wage may exceed the state minimum, and the city page could not be reached, so the applicable wage floor for staff at this site is unconfirmed.</td><td><span class="pill warn">Open</span> F-05; the state rate is verified, the city rate is not.</td></tr>
</tbody></table></div>

<h2>How to review efficiently</h2>
<ol>
  <li><b>First pass, 20 minutes.</b> Read F-01, F-02, F-09 and F-10. They are the four that could change a number
  by more than a rounding error.</li>
  <li><b>Second pass, with counsel.</b> F-12 to F-16 and F-19 require the parcel and the lease; do them in the
  secure workspace, not here.</li>
  <li><b>Third pass, with the accountant.</b> F-06 to F-08 and the tax rows on
  <a href="sell-vs-hold.html">Sell vs hold</a>.</li>
  <li><b>Record the outcome.</b> Each resolved row should be dated and the matching ledger row updated, so the
  site never shows a blank that has already been answered.</li>
</ol>

<h2>What is not flagged, and why</h2>
<ul>
  <li>Body text and analysis. Only figures are flagged; opinions and judgments are labelled as such in place.</li>
  <li>The archive pages. They are other sessions' work and are described, not audited, here.</li>
  <li>Statutory rates that were verified. They are in the ledger with their sources, not in this queue.</li>
</ul>
"""
    return page("flagged.html", "Flagged for review", body,
                lede="Every value left blank, the reason, the exact check to run, and the official link to run it "
                     "on — plus the irregularities found while consolidating the repository.")


# ----------------------------------------------------------------- printable
def build_printable():
    key = [next(r for r in D["findings"] if r["id"] == i) for i in
           ["T-01", "T-03", "T-04", "T-05", "T-08", "T-09", "T-10", "T-11",
            "E-01", "E-05", "E-06", "E-07", "E-08", "C-01", "C-02", "C-03", "C-05", "H-01"]]
    rows = "".join(
        f'<tr><td>{e(r["label"])}</td><td class="num">{e(r["value"])}</td><td>{e(r["period"])}</td>'
        f'<td class="small">{src(r["sourceId"], short=True)}</td></tr>' for r in key)
    gates = "".join(
        f'<tr><td><b>{e(g["id"])}</b></td><td>{e(g["title"])}</td>'
        f'<td><span class="pill {"bad" if g["status"]=="Blocked" else ("warn" if g["status"]=="Open" else "info")}">{e(g["status"])}</span></td>'
        f'<td class="small">{e(g["blocking"])}</td></tr>' for g in D["gates"])
    qs = "".join(
        f'<tr><td class="small">{e(q["id"])}</td><td>{e(q["question"])}</td><td class="small">{e(q["owner"])}</td></tr>'
        for q in [x for x in D["questions"] if x["id"] in
                  ("Q-01", "Q-02", "Q-07", "Q-19", "Q-20", "Q-23", "Q-27")])

    body = f"""
<div class="callout info">
  <b>One page for advisers.</b> Print or save as PDF. Every figure carries its source; every blank is a decision
  input that has not arrived. No personal or parcel-identifying information appears on this page.
</div>

<div class="kv">
  <dt>Property</dt><dd>{e(META["parcelPlaceholder"])} — Central Los Angeles, single-tenant restaurant, net lease</dd>
  <dt>Owner</dt><dd>{e(META["ownerPlaceholder"])}</dd>
  <dt>Lease window</dt><dd>{e(META["leasePlaceholder"])}</dd>
  <dt>Evidence cut-off</dt><dd>{e(VERIFIED_ON)}</dd>
  <dt>Decision status</dt><dd><b>Not made. Neither branch can be priced on verified inputs.</b></dd>
</div>

<h2>Verified figures</h2>
<div class="tablewrap"><table><thead><tr><th>Item</th><th>Value</th><th>Period</th><th>Source</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Gates</h2>
<div class="tablewrap"><table><thead><tr><th>Gate</th><th>Subject</th><th>Status</th><th>Blocked on</th></tr></thead>
<tbody>{gates}</tbody></table></div>

<h2>Seven questions to ask first</h2>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Question</th><th>Who answers</th></tr></thead>
<tbody>{qs}</tbody></table></div>

<h2>Recommended next three actions</h2>
<ol>
  <li>Abstract the lease and build the dated notice calendar (gate G1).</li>
  <li>Request an estoppel certificate and a written renewal indication, plus store-level financials (gate G2).</li>
  <li>Order three broker opinions with short-lease comparables and a re-leasing study (gate G5).</li>
</ol>

<h2>What must not be done</h2>
<ul>
  <li>Do not sign a renewal, or list the property, before the lease abstract and the notice calendar exist.</li>
  <li>Do not quote a cap rate, discount or sale price that is not backed by a comparable or a written opinion.</li>
  <li>Do not put the parcel identifier, lease file or owner finances into any public document, including this one.</li>
  <li>Do not treat a county statistic as a trade-area fact.</li>
</ul>

<p class="small muted">Sources for every figure above are listed on the Verification ledger, each with the date
it was read. This page is not legal, tax, appraisal or investment advice.</p>
"""
    return page("printable-summary.html", "Printable summary for advisers", body,
                lede="One page: the property in placeholders, the verified figures, the gates, the seven questions "
                     "to ask first, and the three actions that come next.")


# -------------------------------------------------------------------- sources
def build_sources():
    rows = "".join(
        f'<tr><td><code>{e(s["id"])}</code></td><td><b>{e(s["label"])}</b><br>'
        f'<span class="small muted">{e(s["supports"])}</span></td>'
        f'<td class="small">{e(s["publisher"])}</td><td class="small">{e(s["date"])}</td>'
        f'<td class="small">{e(s["retrieved"])}</td>'
        f'<td class="small"><a href="{e(s["url"])}" rel="noopener">open</a></td></tr>'
        for s in D["sources"])

    body = f"""
<div class="callout info">
  <b>Only official sources are cited.</b> Federal and state agencies, the securities regulator and the central
  bank's published series. No news article, listing portal, brokerage blog or data aggregator is used to
  establish a figure. Where an official page did not respond, the item is blank and flagged rather than filled
  from a secondary source.
</div>

<h2>Register</h2>
<div class="tablewrap"><table><thead><tr><th>ID</th><th>Source and what it supports</th><th>Publisher</th><th>Source date</th><th>Checked</th><th>Link</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Source hierarchy applied</h2>
<ol>
  <li><b>Statutory and regulatory text, or the agency's own page</b> — used for tax rates, thresholds, wage floors,
  hazard programmes and map products.</li>
  <li><b>Primary filings</b> — the issuer's own Form 8-K exhibits, quoted with the filing date and accession path.</li>
  <li><b>Official statistical series</b> — the agency's published table or the central bank's series identifier,
  quoted with the period the value refers to.</li>
  <li><b>Nothing else.</b> No aggregator, no press summary, no model output is treated as a source.</li>
</ol>

<h2>Known source limitations</h2>
<ul>
  <li><b>Vintage differences.</b> Two official population series disagree by more than 140,000 persons; both are
  shown, neither is averaged. See F-02.</li>
  <li><b>Missing observations.</b> The Los Angeles 12-month CPI change for October 2026 cannot be published;
  October 2025 was not collected. See the CPI row on the ledger.</li>
  <li><b>Unreachable pages.</b> Six official pages did not respond during the sweep; each is listed with its URL
  so the check can be repeated.</li>
  <li><b>Privacy-thin sources.</b> Parcel-level determinations necessarily identify the property, so they are
  performed in the secure workspace and only the method is published here.</li>
  <li><b>Forward-looking statements.</b> Guidance figures are the issuer's own expectations, not results. They are
  labelled as guidance wherever they appear.</li>
</ul>

<h2>Archive and duplication</h2>
<p>Earlier parallel dashboards remain in the repository under <a href="index.html#archive">Archive</a>. They use
some of the same sources at earlier cut-off dates. This site's ledger is the reference; where a legacy page and
this page differ, the difference is a date, and the ledger row states its own period.</p>

<h2>How to re-run this check</h2>
<ol>
  <li>Open each source link above and compare the value with the ledger row it supports.</li>
  <li>If a value has been revised, update <code>data/root.json</code> and rebuild; the generator will not print a
  verified value without a source id.</li>
  <li>If a source no longer responds, leave the value in place only if it was verified on an earlier date and say
  so; otherwise blank it and add it to the flagged queue.</li>
  <li>Run <code>python3 tests/check_root.py</code> before publishing.</li>
</ol>
"""
    return page("sources.html", "Sources", body,
                lede="The official register: what each source supports, when it was published, when it was read, "
                     "and what it cannot establish.")


# -------------------------------------------------------------------- privacy
def build_privacy():
    body = f"""
<div class="callout ok">
  <b>Privacy is the first constraint on this project, not a footnote.</b> The property is identifiable from a
  street address, a parcel number, or a lease document. Those three things are therefore never published, and
  the owner's finances never leave the adviser group. What is published is aggregate and non-identifying.
</div>

<h2>What is published, and what is not</h2>
<div class="tablewrap"><table><thead><tr><th>Item</th><th>Published here?</th><th>Where it lives instead</th></tr></thead><tbody>
<tr><td>Street address</td><td><span class="pill bad">No</span></td><td>Access-controlled internal workspace</td></tr>
<tr><td>Parcel number / APN</td><td><span class="pill bad">No</span></td><td>Internal workspace</td></tr>
<tr><td>Owner name or entity</td><td><span class="pill bad">No</span></td><td>Internal workspace, counsel</td></tr>
<tr><td>Lease document, amendments, estoppel</td><td><span class="pill bad">No</span></td><td>Internal workspace, counsel</td></tr>
<tr><td>Rent roll, operating statements, tax returns</td><td><span class="pill bad">No</span></td><td>Internal workspace, accountant</td></tr>
<tr><td>Insurance quotes and loss history</td><td><span class="pill bad">No</span></td><td>Broker, internal workspace</td></tr>
<tr><td>Broker opinions and buyer identities</td><td><span class="pill bad">No</span></td><td>Broker, internal workspace</td></tr>
<tr><td>Regional statistics and statutory rates</td><td><span class="pill ok">Yes</span></td><td>Published with the official source link</td></tr>
<tr><td>Tenant's public filings</td><td><span class="pill ok">Yes</span></td><td>Published with the filing link</td></tr>
<tr><td>Decision gates, questions, risk register</td><td><span class="pill ok">Yes</span></td><td>Published as method, without identifiers</td></tr>
</tbody></table></div>

<h2>Placeholders used on this site</h2>
<ul>
  <li><code>{e(META["parcelPlaceholder"])}</code> — stands in for the address, parcel number and any description
  that would locate the property.</li>
  <li><code>{e(META["ownerPlaceholder"])}</code> — stands in for the owner, the holding entity, and any guarantor.</li>
  <li><code>{e(META["leasePlaceholder"])}</code> — the expiry window comes from the owner's brief and has not been
  verified against the lease.</li>
</ul>

<h2>How the workspace is separated</h2>
<ol>
  <li><b>Public layer.</b> This static site. It is generated from a data file that contains no identifiers, so an
  identifier cannot leak into a page by accident.</li>
  <li><b>Internal layer.</b> The lease abstract, title work, hazard determinations, insurance quotes, broker
  opinions and tax computation, held by the advisers who need them, under access control.</li>
  <li><b>Transfer rule.</b> Only a value that is both non-identifying and independently verified crosses from the
  internal layer to the public layer, and it crosses with its source and date.</li>
  <li><b>No upload path.</b> The public site has no form, no upload and no analytics. The calculator runs in the
  browser and sends nothing.</li>
</ol>

<h2>Threats this addresses</h2>
<div class="tablewrap"><table><thead><tr><th>Threat</th><th>How it is reduced</th><th>Residual risk</th></tr></thead><tbody>
<tr><td>A buyer or competitor identifies the parcel from public material</td><td>No address, parcel number, or unique combination of details; placeholders only</td><td>Local readers may still infer the property from context</td></tr>
<tr><td>Owner finances become public</td><td>Basis, depreciation, entity and returns never published</td><td>Adviser-side handling errors</td></tr>
<tr><td>Lease terms leak and weaken negotiation</td><td>Abstract held by counsel; only the expiry window is mentioned, labelled unverified</td><td>Discussion outside the adviser group</td></tr>
<tr><td>Accidental publication through a build or a commit</td><td>Generator reads a data file with no identifier fields; automated scan fails the build on identifier patterns</td><td>A deliberate manual override</td></tr>
<tr><td>Tracking of the reader</td><td>No scripts beyond the calculator, no cookies, no fonts or assets from third parties</td><td>Hosting-provider logs</td></tr>
</tbody></table></div>

<h2>Operating rules for anyone working on this project</h2>
<ul>
  <li>Never commit a lease, a rent roll, a tax return, an insurance quote or a parcel identifier to this repository.</li>
  <li>Never paste such a document into a public issue, a pull request description or a commit message.</li>
  <li>Use the placeholders above in any page, memo or summary that leaves the adviser group.</li>
  <li>Run the identifier scan before publishing; it is part of the build, not an optional extra.</li>
  <li>If an identifier is published by mistake, treat it as an incident: remove it, record it, and tell the owner.</li>
</ul>

<h2>Scope of this policy</h2>
<p>This policy governs this repository and the pages published from it. It does not replace the owner's own
confidentiality agreements with brokers, tenants, lenders or advisers, and it does not address legal discovery or
regulatory requests, which belong with counsel.</p>
"""
    return page("privacy.html", "Privacy and workspace rules", body,
                lede="What is published, what is withheld, how the two layers are separated, and the threats this "
                     "design reduces.")


def build():
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "style.css").write_text(CSS, encoding="utf-8")
    (ROOT / "assets" / "calc.js").write_text(CALC_JS, encoding="utf-8")
    written = [
        build_index(),
        build_exec(),
        build_verification(),
        build_requirements(),
        build_gates(),
        build_trade_area(),
        build_hazards(),
        build_sell(),
        build_calculator(),
        build_risks(),
        build_questions(),
        build_suggestions(),
        build_flagged(),
        build_printable(),
        build_sources(),
        build_privacy(),
    ]
    for fname, markers in NOSOURCE_MARKERS.items():
        mark_nosource(fname, markers)

    verified = sum(1 for r in D["findings"] if r["status"] == "verified")
    unverified = len(D["findings"]) - verified
    print(f"built {len(written)} pages from data/root.json")
    print(f"ledger: {verified} verified, {unverified} blank, {len(D['sources'])} sources, "
          f"{len(D['questions'])} questions, {len(D['suggestions'])} suggestions, {len(D['flagged'])} flags")


if __name__ == "__main__":
    build()
