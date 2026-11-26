#!/usr/bin/env python3
"""Build the canonical, static root dashboard. No network or private data required.

The source ledger below is deliberately explicit. A link on a workflow/question
row is a contextual reference, not proof of an answer about the subject parcel.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = {
    'sec23': ('SEC · FY2023 10-K', 'https://www.sec.gov/Archives/edgar/data/807882/000080788223000020/jack-20231001.htm'),
    'sec25': ('SEC · FY2025 10-K', 'https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm'),
    'secq425': ('SEC · Q4 FY2025 release', 'https://www.sec.gov/Archives/edgar/data/807882/000080788225000070/ex991-q425earningsrelease.htm'),
    'q126': ('Issuer · Q1 FY2026 release', 'https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-First-Quarter-2026-Earnings/default.aspx'),
    'q226': ('SEC · Q2 FY2026 release', 'https://www.sec.gov/Archives/edgar/data/807882/000080788226000066/ex991-q226earningsrelease.htm'),
    'q326': ('SEC · Q3 FY2026 release', 'https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm'),
    'q32610q': ('SEC · Q3 FY2026 10-Q', 'https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm'),
    'edgar': ('SEC · issuer filings', 'https://www.sec.gov/edgar/browse/?CIK=807882'),
    'schedule': ('Issuer · October announcement', 'https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Announces-Fourth-Quarter-and-Full-Year-2026-Earnings-Webcast/default.aspx'),
    'schedule2': ('Issuer · reference calendar', 'https://investors.jackinthebox.com/resources/commonly-referenced-info/default.aspx'),
    'census': ('Census · county population', 'https://www.census.gov/newsroom/press-releases/2026/2025-popest-metro-micro-counties.html'),
    'acs': ('Census · ACS comparison guidance', 'https://www.census.gov/help/topics/faq.what-are-some-general-guidelines-for-using-the-acs.html'),
    'acsdata': ('Census · ACS 5-year data', 'https://www.census.gov/programs-surveys/acs/data.html'),
    'income': ('Census via Federal Reserve · SAIPE', 'https://fred.stlouisfed.org/series/MHICA06037A052NCEN'),
    'bls': ('BLS · LA metro data', 'https://www.bls.gov/regions/west/ca_losangeles_msa.htm'),
    'school': ('CA Education · DataQuest', 'https://www.cde.ca.gov/ds/ad/dataquest.asp'),
    'traffic': ('Caltrans · traffic census', 'https://dot.ca.gov/programs/traffic-operations/census'),
    'planning': ('LA Planning · case reports', 'https://planning.lacity.gov/resources/case-reports'),
    'quake': ('USGS · regional earthquake model', 'https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area'),
    'cgs': ('CA Geological Survey · EQ Zapp', 'https://www.conservation.ca.gov/cgs/geohazards/eq-zapp'),
    'fema': ('FEMA · flood maps', 'https://www.fema.gov/locations/risk-reduction/california'),
    'fire': ('CAL FIRE · hazard zones', 'https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones'),
    'irs': ('IRS · capital gains', 'https://www.irs.gov/taxtopics/tc409'),
    'exchange': ('IRS · Form 8824 instructions', 'https://www.irs.gov/instructions/i8824'),
    'ftb': ('CA FTB · real-estate withholding', 'https://www.ftb.ca.gov/forms/misc/1016.html'),
    'ula': ('LA Finance · Measure ULA', 'https://finance.lacity.gov/faq/measure-ula'),
    'privacy': ('NIST · privacy framework', 'https://www.nist.gov/privacy-framework'),
    'diversify': ('SEC · diversification', 'https://www.investor.gov/introduction-investing/getting-started/asset-allocation'),
}

NAV = [
    ('Overview', [ ('index.html','Dashboard'), ('executive-summary.html','Executive summary'), ('decision-gates.html','Decision gates') ]),
    ('Research', [ ('trade-area.html','Market & trade area'), ('tenant.html','Tenant health'), ('hazards.html','Hazard screening'), ('risks.html','Risk scenarios') ]),
    ('Decision tools', [ ('sell-vs-hold.html','Sell vs. hold'), ('projection.html','Projection method'), ('questions.html','Open questions'), ('suggestions.html','Suggestions'), ('printable-summary.html','Advisor brief') ]),
    ('Accountability', [ ('flagged.html','Flagged for review'), ('sources.html','Source library'), ('privacy.html','Privacy') ]),
]


def src(key, label=None):
    name, url = S[key]
    return f'<a href="{escape(url, quote=True)}" rel="noopener noreferrer" referrerpolicy="no-referrer">{escape(label or name)} ↗</a>'


def sources(keys):
    return ' · '.join(src(key) for key in keys)


def table(headings, rows):
    # Rows = (cells, source keys); all public rows have at least one real source.
    head = ''.join(f'<th scope="col">{escape(h)}</th>' for h in [*headings, 'Official source / reference'])
    body = []
    for cells, keys in rows:
        if not keys or len(cells) != len(headings):
            raise ValueError(f'Incomplete row in {headings}: {cells}')
        body.append('<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + f'<td>{sources(keys)}</td></tr>')
    return '<div class="table-wrap" tabindex="0"><table><thead><tr>' + head + '</tr></thead><tbody>' + '\n'.join(body) + '</tbody></table></div>'


def nav(active):
    groups = []
    for label, items in NAV:
        groups.append(f'<div class="nav-label">{escape(label)}</div>')
        for href, title in items:
            current = ' aria-current="page"' if href == active else ''
            groups.append(f'<a href="{href}"{current}>{escape(title)}</a>')
    return '<nav class="side-nav" aria-label="Site navigation">' + ''.join(groups) + '</nav>'


def heading(kicker, title, description, status=''):
    return f'<div class="page-heading"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lead">{description}</p>{status}</div>'


def section(title, description, contents, link=''):
    extra = f'<a href="{link[0]}">{link[1]} →</a>' if link else ''
    return f'<section class="section"><div class="section-head"><div><h2>{title}</h2><p>{description}</p></div>{extra}</div>{contents}</section>'


def card_link(icon, title, text, url, label):
    return f'<a class="card card-link" href="{url}"><span class="card-icon" aria-hidden="true">{icon}</span><h3>{title}</h3><p>{text}</p><span class="card-arrow">{label} →</span></a>'


def page(filename, title, body, script=False, print_page=False):
    n = nav(filename)
    script_tag = '<script src="assets/app.js" defer></script>' if script else ''
    cls = 'content print-sheet' if print_page else 'content'
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer"><title>{escape(title)} · Property Decision Brief</title><link rel="stylesheet" href="assets/style.css">{script_tag}</head>
<body><a class="skip" href="#main">Skip to content</a><div class="app">
<aside class="sidebar"><a class="logo" href="index.html"><span class="logo-mark" aria-hidden="true">◇</span><span class="logo-name">Decision brief<small>Property research</small></span></a>{n}<div class="side-note"><strong>Private by design</strong>No parcel identifiers or owner records are published here. Private evidence belongs with authorized advisers.</div></aside>
<div class="workspace"><header class="topbar"><div class="breadcrumb">PROPERTY RESEARCH &nbsp; / &nbsp; <span>{escape(title)}</span></div><div class="top-status"><span class="pill">Privacy first</span><span class="updated">Evidence reviewed 26 Nov 2026</span></div><details class="mobile-nav"><summary>Browse the workspace</summary>{n}</details></header>
<main id="main" class="{cls}">{body}
<footer><span>Anonymous decision workspace · Not legal, tax, or investment advice.</span><span><a href="privacy.html">Privacy</a> · <a href="sources.html">Sources</a> · <a href="flagged.html">Review flags</a></span></footer></main></div></div></body></html>'''
    (ROOT / filename).write_text(html + '\n', encoding='utf-8')


BLANK = '<span class="empty" aria-label="Unverified, value blank">—<small>Unverified</small></span>'
PENDING = '<span class="pill warn">Not evidenced</span>'
PROPOSED = '<span class="pill neutral">Proposed</span>'


def build():
    # Dashboard
    body = '''<div class="hero"><div><p class="eyebrow">An evidence-led property decision</p><h1>Clarity before commitment.</h1><p>A privacy-first workspace for weighing a possible sale against a negotiated renewal of an anonymous quick-service property.</p><div class="actions"><a class="button light" href="executive-summary.html">Read the decision brief →</a><a class="button ghost" href="decision-gates.html">View decision gates</a></div></div><div class="hero-panel"><span class="mini-label">Current position</span><h2>Keep both paths open.</h2><p>No sale or renewal winner can be supported without a private lease abstract, real quotes, tax calculations, and parcel-specific risk screening.</p></div></div>'''
    body += section('The evidence at a glance', 'Public benchmarks are context, not a valuation of this property.', '''<div class="stat-grid">
<div class="stat"><div class="mini-label">Brand · latest checked quarter</div><div class="stat-value">−1.1%</div><p>System same-store sales, Q3 FY2026 (12 weeks). ''' + src('q326', 'SEC filing') + '''</p></div>
<div class="stat"><div class="mini-label">Brand · restaurants</div><div class="stat-value">2,115</div><p>System restaurant count at July 5, 2026. ''' + src('q326', 'SEC filing') + '''</p></div>
<div class="stat"><div class="mini-label">LA metro · unemployment</div><div class="stat-value">4.4%</div><p>September 2026, preliminary; not a local-tract estimate. ''' + src('bls', 'BLS') + '''</p></div>
<div class="stat"><div class="mini-label">Property decision</div><div class="stat-value">Pending</div><p>Terms, taxes, trade area and parcel risks remain unverified. <a href="flagged.html">Review open items →</a></p></div></div>''')
    gates = '''<div class="card"><div class="gate-list"><div class="gate"><span class="gate-num">01</span><div><strong>Confirm the lease</strong><small>Private abstract and notice calendar</small></div><span class="pill warn">Not evidenced</span></div><div class="gate"><span class="gate-num">02</span><div><strong>Price both paths</strong><small>Written short-lease and renewal quotes</small></div><span class="pill warn">Not evidenced</span></div><div class="gate"><span class="gate-num">03</span><div><strong>Understand the downside</strong><small>Parcel hazards, insurance and liquidity</small></div><span class="pill warn">Not evidenced</span></div></div></div>'''
    focus = '''<div class="card"><span class="mini-label">Recommended next step</span><h3 style="margin-top:10px">Protect the option to choose.</h3><p>Have counsel reconcile all notice rights first. In parallel, request private broker opinions and a CPA-prepared after-tax comparison.</p><a class="card-arrow" href="questions.html">See the discovery plan →</a></div>'''
    body += section('Decision readiness', 'Statuses reflect only evidence available to this public site; they are not confirmations of private work.', '<div class="split">' + gates + focus + '</div>', ('decision-gates.html', 'All gates'))
    body += section('Explore the workspace', 'Follow the questions, not assumptions.', '<div class="card-grid">' + card_link('↗', 'Market & trade area', 'What regional data says, and what only a private local study can answer.', 'trade-area.html', 'Explore market evidence') + card_link('≋', 'Compare the paths', 'An optional, blank-by-default after-tax worksheet for authorized advisers.', 'sell-vs-hold.html', 'Open the worksheet') + card_link('◇', 'Risks & resilience', 'Ordinary risks and joint disaster, rent-loss and exit-liquidity stresses.', 'risks.html', 'Review scenarios') + '</div>')
    body += '<div class="note warning"><strong>Privacy boundary.</strong> The public site is not an access-controlled workspace. Do not publish an address, parcel number, owner information, lease, financial details, local search results, or adviser documents here. <a href="privacy.html">Read the privacy policy →</a></div>'
    page('index.html', 'Dashboard', body)

    # Executive summary
    body = heading('01 · Decision brief', 'The decision, in plain language', 'For an anonymous Jack in the Box property described as having a triple-net lease expiring in the 2030–2035 window. The lease and exact location have not been verified.', '<span class="pill warn">No winner selected</span>')
    body += '''<div class="card"><span class="mini-label">Interim recommendation</span><h2 style="margin:9px 0">Preserve optionality; verify before committing.</h2><p>Do not choose a sale or renewal on regional indicators alone. Ask counsel to commission a private lease abstract and reconcile every notice right; simultaneously obtain comparable short-lease and renewal quotes, an accountant’s tax analysis, and a parcel-specific hazard and insurance review. This is a process recommendation, not a valuation or individualized financial advice.</p><p>Only after those inputs exist should the owner and advisers compare after-tax sale equity with the present value of after-tax hold cash flows, alongside liquidity, concentration, estate needs and acceptable downside.</p></div>'''
    rows = [
        (['Lease description and expiry window', 'NNN and 2030–2035 were supplied in the brief; the exact contract is not available.', BLANK, 'Counsel: abstract all amendments and reconcile notices before negotiating.'], ['sec25']),
        (['Brand operating trend', 'FY2025 system same-store sales −4.2%; Q3 FY2026 −1.1%.', 'Verified issuer disclosures', 'Monitor tenant and guarantor separately; brand results do not prove this location’s sales.'], ['secq425','q326']),
        (['Local demand', 'City/county and metro statistics are broader than a trade area.', BLANK, 'Privately define a consistent catchment, then obtain tract, traffic, school and competition evidence.'], ['acs','traffic','school']),
        (['Tax and liquidity', 'Rules depend on ownership, basis, income, jurisdiction and transaction terms.', BLANK, 'CPA prepares the incremental tax and net-equity figures for each path.'], ['irs','ftb','ula']),
        (['Physical risk', 'Earthquake, flood and wildfire maps exist; a map is not an engineering report.', BLANK, 'Obtain current parcel zones, an engineer’s review and insurance quotes privately.'], ['cgs','fema','fire']),
    ]
    body += section('What is known—and what is not', 'References on missing-input rows are guidance, not evidence of the property’s facts.', table(['Topic','Public evidence','Subject result','Next action'], rows))
    body += section('How to make the eventual choice', 'Use the same date, after-tax equity basis and risk limits for each case.', '''<div class="card-grid two"><div class="card"><h3>A sale may be preferable if…</h3><p>Executable after-tax proceeds and a realistic reinvestment plan meet the owner’s liquidity and diversification goals and compare favorably with a risk-adjusted hold case.</p></div><div class="card"><h3>A renewal may be preferable if…</h3><p>A signed, credit-supported renewal and realistic downside stresses justify keeping concentrated exposure and compare favorably with after-tax sale proceeds.</p></div></div><div class="note">A larger modeled value is not automatically the best personal decision. Match the owner’s documented risk tolerance, cash needs and time horizon; no personal objectives are available here.</div>''')
    page('executive-summary.html', 'Executive summary', body)

    # Decision gates
    body = heading('W-03 · Progress board', 'Decision gates', 'A public progress view without private documents. “Not evidenced” means no verified private attestation was supplied to this site; it does not prove the task has not been done.')
    gates = [
        (['00 · Privacy controls', PENDING, 'Authorized advisers keep identifiers and records in an access-controlled, offline workflow; approve any aggregate publication.'], ['privacy']),
        (['01 · Lease & notices', PENDING, 'Counsel commissions a private abstract; verifies expiry, options, service rules, deadlines, guaranty, repairs and transfer restrictions; reconciles a private calendar.'], ['sec25']),
        (['02 · Local evidence', PENDING, 'Select a consistent catchment privately and document tracts, vintage, margins of error, traffic, schools, competition and planning.'], ['acs','traffic','school','planning']),
        (['03 · Quotes & renewal terms', PENDING, 'Obtain comparable written opinions for current short term and a negotiated extension, plus real renewal terms and costs.'], ['sec25']),
        (['04 · Taxes & owner objectives', PENDING, 'CPA calculates incremental tax, debt payoff and closing costs; owner and adviser assess liquidity, concentration and estate constraints privately.'], ['irs','ftb','diversify']),
        (['05 · Hazard & insurance', PENDING, 'Geologist/engineer and broker confirm parcel map status, structural vulnerability, policy limits, deductibles and interruption coverage.'], ['cgs','fema','fire']),
        (['06 · Joint stress & decision', PENDING, 'Back-test when sufficient history exists; compare after-tax cases and joint downside, document assumptions and only then authorize a commitment.'], ['diversify','irs']),
    ]
    body += section('Gates before a binding commitment', 'A source explains the topic or process; it does not attest that an adviser has completed the gate.', table(['Gate','Public status','Evidence needed privately'], gates))
    body += section('Notice-calendar reconciliation', 'Dates are deliberately blank: they can only come from the governing lease and amendments.', table(['Calendar item','Date','Private verification'], [
        (['Base-term expiry', BLANK, 'Counsel identifies the controlling executed provision and amendments.'], ['sec25']),
        (['Earliest and latest option-notice dates', BLANK, 'Calculate from the actual clause; verify whether the option is exercisable and by whom.'], ['sec25']),
        (['Delivery method and recipients', BLANK, 'Confirm address, delivery method, business-day rules and evidence of receipt with counsel.'], ['sec25']),
        (['Internal lead time and escalation', BLANK, 'Authorized advisers set reminders and reconcile them independently; do not guess a notice period.'], ['sec25']),
    ]))
    body += '<div class="note warning">No abstract has been commissioned, no notice calendar has been reconciled, and no private adviser has been contacted by this website.</div>'
    page('decision-gates.html', 'Decision gates', body)

    # Market and neighborhood
    body = heading('W-01 · Local economics', 'Market & trade area', 'Official regional observations provide a backdrop only. The trade area, its Census tracts and nearby competitors cannot be selected without a secure parcel workflow.')
    body += section('Verified regional context', 'Census values are county-wide; BLS observations cover the Los Angeles–Long Beach–Anaheim metro.', table(['Measure','Value','Period / interpretation'], [
        (['LA County population', '9,748,868 → 9,694,934', 'July 2024 and July 2025, respectively; both from Census Vintage 2025.'], ['census']),
        (['LA County median household income', '$90,757', '2024 SAIPE estimate, annual nominal dollars; not a tract estimate or the ACS five-year measure.'], ['income']),
        (['LA metro unemployment', '4.4%', 'September 2026, preliminary, not seasonally adjusted.'], ['bls']),
        (['LA metro payroll growth', '+0.9%', 'October 2026, preliminary 12-month change; metro-wide.'], ['bls']),
    ]))
    body += '<div class="note">Census revises an entire population series with each vintage; use the same vintage for comparisons. The SAIPE income measure is not interchangeable with a five-year ACS median. Regional results do not establish local demand or a property price.</div>'
    body += section('Neighborhood evidence still needed', 'Every subject-specific value is blank. Do not put a tract number, address or map result on the public site.', table(['Factor','Subject value','Private discovery route'], [
        (['Trade-area boundary and tracts', BLANK, 'Authorized analyst defines an appropriate catchment and consistent tract boundaries, then records vintage and uncertainty privately.'], ['acsdata','acs']),
        (['Population and household-income trend', BLANK, 'Extract tract estimates and margins of error for consistent, non-overlapping ACS five-year periods; do not average tract medians.'], ['acs','acsdata']),
        (['Employment / daytime population', BLANK, 'Use appropriately bounded local employment data plus metro BLS as context; document geography and vintage.'], ['bls','acsdata']),
        (['Traffic, access and visibility', BLANK, 'Use local street counts and field review; Caltrans counts are for the state highway system, not all local streets.'], ['traffic']),
        (['Schools and enrollment', BLANK, 'Identify schools serving the catchment privately; check enrollment and performance in DataQuest without inferring property sales.'], ['school']),
        (['Planning, zoning and redevelopment', BLANK, 'First verify jurisdiction; then review the applicable local land-use rules, applications and access restrictions privately.'], ['planning']),
        (['Competing restaurants / openings', BLANK, 'Use a private field inventory and dated local records; distinguish confirmed facts from assumptions and proprietary observations.'], ['planning']),
        (['Parcel-level projection', BLANK, 'Collect sufficiently long, comparable verified history and validate the model described in the projection method.'], ['acs','bls']),
    ]))
    body += section('How to interpret tract trends', 'Keep observations, uncertainty and assumptions separate.', '''<div class="card-grid two"><div class="card"><h3>Consistent boundaries</h3><p>Use non-overlapping ACS five-year periods, account for boundary changes and report margins of error. A period estimate is not a single-year reading.</p></div><div class="card"><h3>No false precision</h3><p>Do not treat a county average, arbitrary radius, school score or traffic count as this location’s sales or value. Review the catchment and source limitations with a qualified analyst.</p></div></div>''')
    page('trade-area.html', 'Market & trade area', body)

    # Tenant operating series
    body = heading('Tenant health · SEC evidence', 'A longer view of the brand', 'System-level operating disclosures can inform tenant diligence, but they do not identify the lease counterparty, guarantee, or performance of the subject restaurant.')
    body += section('Annual Jack in the Box brand series', 'Same-store sales are year-over-year system changes; rental revenue is the Jack in the Box segment, not the owner’s rent.', table(['Fiscal year','System same-store sales','Ending units','Closures','Franchise rental revenue'], [
        (['2022', '+0.9%', '2,181', '54', '$335.936 million'], ['sec23']),
        (['2023', '+7.3%', '2,186', '15', '$351.283 million'], ['sec23']),
        (['2024', '−1.3%', '2,191', '25', '$347.227 million'], ['sec25']),
        (['2025', '−4.2%', '2,136', '86', '$332.735 million'], ['sec25','secq425']),
        (['2026 full year', BLANK, BLANK, BLANK, BLANK], ['edgar','schedule']),
    ]))
    body += section('Recent quarterly observations', 'Fiscal Q1 has 16 weeks; Q2 and Q3 have 12 weeks. Quarters should not be added to produce annual same-store sales.', table(['Period','System same-store sales','Ending units','Openings / closures'], [
        (['Q1 FY2026 · Jan 18', '−6.7%', '2,128', '6 / 14'], ['q126']),
        (['Q2 FY2026 · Apr 12', '−3.8%', '2,128', '9 / 9'], ['q226']),
        (['Q3 FY2026 · Jul 5', '−1.1%', '2,115', '4 / 17'], ['q326']),
    ]))
    body += '<div class="note">The issuer reported 40-week franchise rental revenue of $242.526 million versus $260.254 million in the prior-year period. These are company-level figures, not rent paid on this property. The issuer also reported the sale of Del Taco and recast discontinued operations; check comparability before using consolidated series. ' + src('q32610q') + ' · ' + src('q126') + '</div>'
    body += '<div class="note warning"><strong>Upcoming results:</strong> the October 26 issuer announcement schedules FY2026 results for December 9, 2026. An issuer reference calendar separately lists November 18, 2026. The conflict is <a href="flagged.html">flagged for review</a>; verify the actual filing when available. ' + src('schedule') + ' · ' + src('schedule2') + '</div>'
    page('tenant.html', 'Tenant health', body)

    # Parcel hazard screening
    body = heading('W-04 · Physical risk', 'Screen the parcel—not the region', 'Map designations, structural vulnerability and insurance coverage are different questions. All subject-specific results remain private and unverified.')
    body += section('Hazard screening register', 'The linked sources explain the screening tools; they do not establish this parcel’s zone or insured loss.', table(['Exposure','Parcel status','Private next step'], [
        (['Earthquake fault rupture', BLANK, 'Use current California Geological Survey regulatory layers; obtain an engineering/geotechnical assessment where appropriate.'], ['cgs']),
        (['Liquefaction / landslide', BLANK, 'Check current CGS zones and whether the area has been evaluated; assess ground conditions and foundation privately.'], ['cgs']),
        (['Ground shaking / building resilience', BLANK, 'Ask a licensed engineer for a building-specific assessment; regional event probability is not a building damage probability.'], ['quake','cgs']),
        (['Flood', BLANK, 'Check the current effective FEMA map, map date and amendments; discuss coverage and exclusions with an insurance broker.'], ['fema']),
        (['Wildfire / smoke / access', BLANK, 'Check the adopted local or state responsibility area map, plus building exposure, access and business interruption.'], ['fire']),
        (['Insurance, deductibles and rent loss', BLANK, 'Obtain actual property, earthquake, flood and loss-of-rents terms, limits, exclusions, deductibles and premiums.'], ['fema','fire']),
    ]))
    body += '<div class="note warning"><strong>Map limitations:</strong> CGS says its maps do not show every hazard and do not replace site-specific investigations. CAL FIRE distinguishes hazard from risk. A location outside a mapped zone is not proof of zero loss.</div>'
    body += section('Stress the combined loss', 'An event may affect income and the ability to sell at the same time.', '''<div class="card-grid"><div class="card"><span class="mini-label">01 · Income</span><h3>Loss of rent</h3><p>Review abatement, interruption coverage, tenant obligations, repair time and uninsured downtime together.</p></div><div class="card"><span class="mini-label">02 · Cost</span><h3>Repairs &amp; deductibles</h3><p>Include structural repairs, deductibles, uncovered expenses and financing needs in the same scenario.</p></div><div class="card"><span class="mini-label">03 · Exit</span><h3>Liquidity shock</h3><p>Consider delayed sale, weaker pricing and insurance availability after the same event. Do not assume independence.</p></div></div>''')
    body += '<div class="note">Use downloaded official layers offline where practical. If an adviser uses an online lookup, the external service may receive or log the location; follow the adviser’s privacy policy and do not paste the result into this site.</div>'
    page('hazards.html', 'Hazard screening', body)

    # Decision options and downside
    body = heading('Risk & resilience', 'Understand the trade-offs', 'A useful decision considers routine events, tail events and the owner’s ability to absorb loss. No risk score or event probability is assigned without evidence.')
    body += section('Decision-path risk matrix', 'These are prospective possibilities, not claims that any outcome will occur.', table(['Path','Potential benefit','Key risks / verification needed'], [
        (['Sell before expiry', 'Potential liquidity and reduced single-property concentration.', 'Short remaining term may affect bids; tax, selling costs, debt payoff and replacement-investment risk remain unknown.'], ['irs','diversify']),
        (['Negotiate an early renewal', 'Could preserve rent and extend the contractual income stream if agreed.', 'Tenant may decline or demand concessions; guarantee, notice rights, capex and future credit require verification.'], ['sec25']),
        (['Hold through expiry', 'Keeps future leasing or use options open.', 'Vacancy, rent loss, re-leasing cost and uncertain market rent can coincide; review legal rights and reserves.'], ['sec25','diversify']),
        (['Qualifying §1031 exchange', 'May defer eligible gain when all requirements are satisfied.', 'Replacement-property availability, timing, boot, financing and future taxes are material; CPA and qualified intermediary required.'], ['exchange','ftb']),
        (['Refinance / borrow', 'Could provide liquidity while retaining the asset.', 'Debt service, maturity, covenants and refinancing risk can magnify loss. No financing terms are known.'], ['diversify']),
        (['Re-tenant or redevelop', 'May create optionality if allowed and economically feasible.', 'Zoning, approvals, environmental conditions, construction cost, vacancy and demand are unknown.'], ['planning','cgs']),
        (['Do nothing / miss notice', 'No transaction cost today.', 'Inaction can eliminate an option or create an unintended holdover; verify the actual contract and dates.'], ['sec25']),
    ]))
    body += section('Stress events together', 'The inputs and probability of each event are unknown. These are tests to design with advisers, not predictions.', table(['Scenario','Joint effects to model','Data to obtain'], [
        (['Business-as-usual slowdown', 'Weaker sales and credit, rent renegotiation, higher expenses and longer marketing time.', 'Private unit sales, guaranty, comparable offers and insurance renewal terms.'], ['q326','bls']),
        (['Earthquake / ground failure', 'Rent interruption + repairs/deductible + reduced exit liquidity in one scenario.', 'CGS zones, structural report, loss-of-rent policy and contractor estimates.'], ['cgs','quake']),
        (['Wildfire, smoke or power interruption', 'Access restrictions + lost rent + coverage limits + difficult sale or financing.', 'Adopted hazard map, local access, utility and actual business-interruption policy terms.'], ['fire']),
        (['Flood / severe weather', 'Physical repair + tenant interruption + insurance gap + lower sale liquidity.', 'Effective FEMA map, property condition and coverage/exclusions.'], ['fema']),
        (['Tenant failure / credit shock', 'Default or restructuring + vacancy + capital to re-lease + market repricing.', 'Signed lease, guarantor financial strength and unit performance; do not infer a default.'], ['sec25','q326']),
        (['Tax or interest-rate shock', 'Higher financing or transaction friction + lower buyer liquidity at the intended exit.', 'Time-specific CPA advice, lender terms and written market quotes.'], ['irs','ula','diversify']),
    ]))
    body += '<div class="note">Compare stressed after-tax equity and required reserves against the owner’s private liquidity needs and loss tolerance. Diversification can reduce concentration risk, but it does not guarantee against loss. ' + src('diversify') + '</div>'
    page('risks.html', 'Risk scenarios', body)

    # Calculator, no form submissions and no default values
    body = heading('W-02 · Optional adviser worksheet', 'Sell vs. hold, after tax', 'No input is needed to browse this site. This optional worksheet accepts adviser-prepared numbers only; it does not calculate taxes, appraise the property, validate inputs, or select a winner.', '<span class="pill warn">Blank until verified inputs exist</span>')
    body += '''<div class="note warning"><strong>Private by design, not a secure vault.</strong> The worksheet code has no network or storage functions and has no submission form. Inputs stay in the current page’s memory, but the hosting provider, browser, extensions, device and external sites have their own privacy risks. Use a trusted device and, where practical, a trusted offline copy. Do not enter names, addresses, lease text or identifiers. Clear the page when finished.</div>'''
    body += '''<div class="card-grid two"><div class="card"><h3>Sale, today</h3><p>Gross sale price − transaction/transfer costs − debt payoff − CPA-calculated incremental income tax = after-tax sale equity today. Avoid double-counting taxes or costs.</p></div><div class="card"><h3>Hold, same valuation date</h3><p>Present value of each year’s after-tax cash flow plus terminal after-tax sale equity. Annual flows and terminal equity must already include the relevant tax, costs and debt, with no double count.</p></div></div>'''
    body += section('What the tax professional must determine', 'General rules are not a calculation of this owner’s tax.', table(['Item','What must be reviewed','Subject amount'], [
        (['Basis, gains and depreciation', 'Adjusted basis, selling costs, holding period and applicable gain character are fact-specific. Unrecaptured §1250 gain may be subject to a maximum 25% federal rate.', BLANK], ['irs']),
        (['Federal and California income tax', 'CPA calculates incremental tax using entity, income, losses, credits, withholding and applicable rules; withholding is not automatically the final tax.', BLANK], ['irs','ftb']),
        (['Transfer tax and Measure ULA', 'Jurisdiction, timing, exemptions, consideration and allocation need verification. ULA applies only within the City of Los Angeles when applicable.', BLANK], ['ula']),
        (['Deferred exchange', 'A qualified exchange may defer gain; identification and receipt deadlines and California reporting require specialized advice.', BLANK], ['exchange','ftb']),
    ]))
    body += section('Optional, local-only arithmetic', 'All fields are intentionally empty. Enter explicit zero only where a verified input is actually zero.', '''<div class="card"><div class="field-grid">
<div><div class="field"><label for="sale-price">Sale price today ($)</label><input id="sale-price" type="number" inputmode="decimal" step="any" autocomplete="off"><p class="hint">Private broker offer or supported scenario.</p></div>
<div class="field"><label for="sale-costs">Sale and transfer costs ($)</label><input id="sale-costs" type="number" inputmode="decimal" step="any" autocomplete="off"><p class="hint">Include transaction/transfer taxes here, once.</p></div>
<div class="field"><label for="debt-payoff">Debt payoff and prepayment costs ($)</label><input id="debt-payoff" type="number" inputmode="decimal" step="any" autocomplete="off"></div>
<div class="field"><label for="sale-tax">Incremental income tax on sale ($)</label><input id="sale-tax" type="number" inputmode="decimal" step="any" autocomplete="off"><p class="hint">CPA’s total; a negative amount must be a substantiated incremental tax benefit.</p></div></div>
<div><div class="field"><label for="cash-flows">Hold cash flows: one year per line ($)</label><textarea id="cash-flows" inputmode="decimal" autocomplete="off" spellcheck="false" aria-describedby="flows-help"></textarea><p class="hint" id="flows-help">Year 1 first; use plain numbers with no commas, up to 30 years. After-tax, after debt service, including each year’s costs. Losses may be negative.</p></div>
<div class="field"><label for="terminal-equity">Terminal after-tax sale equity ($)</label><input id="terminal-equity" type="number" inputmode="decimal" step="any" autocomplete="off"><p class="hint">Net of terminal costs, debt and taxes; exclude the final operating cash flow above.</p></div>
<div class="field"><label for="discount-rate">After-tax annual discount rate (%)</label><input id="discount-rate" type="number" inputmode="decimal" step="any" autocomplete="off"><p class="hint">Adviser-supplied, consistent with nominal cash flows and the alternative use of funds.</p></div></div></div>
<div id="comparison-output" class="result" aria-live="polite"><p>Not calculated. Verified inputs are required.</p></div><p class="hint" style="margin-top:12px">End-of-year flows and terminal equity are discounted to today. Comparing a current sale with a hold present value uses the discount rate as the opportunity-cost assumption; it is not a separate reinvestment forecast. Risk, liquidity and different future outcomes require additional analysis.</p>
<noscript><p>JavaScript is required for this optional arithmetic; no information is sent by the page.</p></noscript></div>''')
    body += section('Short-lease discount from paired quotes', 'Obtain written opinions on comparable terms. A difference in quotes is not an independently verified market discount.', '''<div class="card"><div class="field-grid"><div class="field"><label for="long-quote">Extended-lease quote ($)</label><input id="long-quote" type="number" inputmode="decimal" step="any" autocomplete="off"></div><div class="field"><label for="short-quote">Current short-lease quote ($)</label><input id="short-quote" type="number" inputmode="decimal" step="any" autocomplete="off"></div></div><p class="formula">Paired difference = (1 − short-lease quote ÷ extended-lease quote) × 100. A negative result is a premium, not a discount.</p><div id="quote-output" class="result" aria-live="polite"><p>Not calculated. Two quotes are required.</p></div><p style="margin-top:14px"><button id="clear-worksheet" type="button" class="button secondary">Clear all worksheet inputs</button></p></div>''')
    body += '<p class="lead" style="margin-top:16px">Model version 2.0.0 · Illustrative arithmetic only · No property inputs, assumptions or quotes are supplied by the site. A separate, independently validated model and professional advice are required for a decision.</p>'
    page('sell-vs-hold.html', 'Sell vs. hold', body, script=True)

    # Forecasting method
    body = heading('Research design · Version 0.1', 'A projection system, not a prediction', 'No reliable parcel forecast or back-test is possible with the available evidence. This specification sets out what must exist before a model is built and used.')
    steps = [
        (['1 · Define the outcome', 'Choose a private target—after-tax equity cash flow, closed-sale price or tenant performance—with clear units, time horizon and decision date.', 'No target series supplied.'], ['irs','sec25']),
        (['2 · Freeze geography and data', 'Privately document the catchment, tract boundaries, source vintage, release date, margin of error and transformations; separate observed inputs from assumptions.', 'Parcel and tracts not supplied.'], ['acs','acsdata']),
        (['3 · Assemble consistent history', 'Collect sufficiently long lease, rent, vacancy, comparable transaction, traffic, local employment and hazard/insurance histories without future information leaking into past training dates.', 'Comparable and property history not supplied.'], ['traffic','bls','cgs']),
        (['4 · Establish baselines', 'Compare against transparent no-change and simple historical benchmarks before fitting a more complex model. Do not derive a local forecast from metro averages.', 'No baseline fitted.'], ['acs','bls']),
        (['5 · Walk-forward back-test', 'Train only on data available at each past decision date, test on later observations, and retain a final untouched test period; check changing vintages and sample selection.', 'Back-test not performed.'], ['acs','census']),
        (['6 · Evaluate and stress', 'Report errors in dollars and, only when meaningful, percentages; evaluate interval coverage and regime failures. Stress correlated rent loss, repair costs and liquidity.', 'No validated error or range available.'], ['quake','fema','fire']),
        (['7 · Version and govern', 'Record model version, source dates, transformations, assumptions, reviewer, limitations and change log; revalidate on new data before a binding decision.', 'Specification only; no model deployed.'], ['privacy','diversify']),
    ]
    body += section('Minimum model-development protocol', 'Source links support the data or risk topic; the methodology itself is a proposed analytical design.', table(['Stage','Method','Status'], steps))
    body += '<div class="note warning"><strong>Do not fill the gap with fabricated certainty.</strong> Without verified parcel inputs and sufficient comparable history, the site supplies no 2030–2035 forecast, target price, probability of renewal, or estimated short-lease discount.</div>'
    page('projection.html', 'Projection method', body)

    # Questions and discovery
    body = heading('Decision intelligence', 'Questions before any decision', 'Every answer below is blank because the source evidence is not available to this public site. A linked official reference supplies context, not the private answer.')
    questions = [
        ('Q01 · When does the base lease end?', 'Attorney obtains the executed lease and every amendment; records the exact date privately.', ['sec25']),
        ('Q02 · Who controls renewal options?', 'Attorney identifies each option, conditions, rent-setting method and whether the right remains exercisable.', ['sec25']),
        ('Q03 · What are the notice deadlines and delivery rules?', 'Counsel calculates dates from the actual contract, confirms recipient and service method, and reconciles an independent private calendar.', ['sec25']),
        ('Q04 · Who is the tenant and who guarantees rent?', 'Counsel checks the contracting entity, guaranty, assignments and estoppel; do not infer from the brand.', ['sec25']),
        ('Q05 · What rent and escalation actually apply?', 'Reconcile the rent roll, amendments, payment history and any percentage-rent clause privately.', ['sec25']),
        ('Q06 · What does NNN really allocate?', 'Abstract taxes, insurance, common expenses, roof, structure, HVAC, environmental and capital obligations.', ['sec25']),
        ('Q07 · What happens after casualty or interruption?', 'Review restoration, rent abatement, termination, insurance proceeds and repair responsibility in the lease.', ['cgs','fema']),
        ('Q08 · What restrictions affect sale or financing?', 'Counsel reviews assignment, consent, first-offer rights, easements, use restrictions, title and existing loan terms.', ['sec25']),
        ('Q09 · How healthy is the actual restaurant?', 'Request permitted unit-level sales, rent coverage and guarantor financial information privately; compare with system disclosures.', ['q326']),
        ('Q10 · What renewal could actually be negotiated?', 'Obtain a non-binding written proposal including rent, term, guarantee, options, concessions and capital obligations.', ['sec25']),
        ('Q11 · What are executable short- and long-lease prices?', 'Obtain multiple contemporaneous, written, matched broker opinions; document terms, comps and uncertainty.', ['sec25']),
        ('Q12 · What is the owner’s adjusted basis and tax?', 'CPA reconciles acquisition records, improvements, depreciation, entity, losses, income and federal/state consequences privately.', ['irs','ftb']),
        ('Q13 · What debt and exit costs are due?', 'Review payoff, prepayment, brokerage, transfer tax, escrow and the relevant sale-date jurisdiction.', ['ula','ftb']),
        ('Q14 · Is an exchange viable?', 'CPA and qualified intermediary assess eligibility, replacement supply, financing and identification/receipt deadlines before any closing.', ['exchange','ftb']),
        ('Q15 · What liquidity and risk tolerance are appropriate?', 'Adviser documents cash needs, concentration, investment horizon, estate aims and acceptable loss privately.', ['diversify']),
        ('Q16 · What is the relevant catchment?', 'A trusted analyst uses the withheld location to set a consistent trade area and tracts without publishing the location.', ['acsdata','acs']),
        ('Q17 · How have local income and population changed?', 'Retrieve matching non-overlapping tract estimates and margins of error; document boundary and price-level changes.', ['acs']),
        ('Q18 · What is the local employment and traffic picture?', 'Combine appropriately bounded employment evidence with city street counts or relevant state highway counts.', ['bls','traffic']),
        ('Q19 · What schools and competitors affect the catchment?', 'Use CDE and a dated private competitor survey; avoid treating school metrics as proof of restaurant demand.', ['school','planning']),
        ('Q20 · What land use, transit or development changes apply?', 'Confirm jurisdiction, zoning, access and official plans; distinguish proposals from approved or completed work.', ['planning']),
        ('Q21 · What is the parcel’s earthquake exposure?', 'Check CGS zones and commissioning of a building-specific engineering and ground assessment.', ['cgs']),
        ('Q22 · What are the flood and fire designations?', 'Review the effective FEMA and adopted local/state fire maps privately; record map date and limitations.', ['fema','fire']),
        ('Q23 · What insurance and reserves exist?', 'Obtain policy limits, exclusions, deductibles, loss-of-rent terms and actual quotes; compare with repair and downtime estimates.', ['fema','fire']),
        ('Q24 · What happens in a compound disaster?', 'Stress lost rent, uncovered repairs and weaker exit liquidity together; compare with private reserve capacity.', ['quake','fema','fire']),
        ('Q25 · Is a projection actually reliable?', 'Collect sufficient compatible history, freeze versions and run a genuine walk-forward back-test before using projections.', ['acs','census']),
    ]
    body += section('Open questions and discovery routes', 'All answers are unverified; the role/action describes a suggested way to obtain them privately.', table(['Question','Answer','Suggested discovery action'], [([q, BLANK, action], keys) for q, action, keys in questions]))
    body += '<div class="note warning">No advisers have been commissioned or contacted by this site. Some missing facts cannot be discovered safely from public regional data and require authorized access to private records.</div>'
    page('questions.html', 'Open questions', body)

    # Suggestions and review-before-change
    body = heading('Review before implementation', 'Suggestions & next paths', 'A decision backlog for review—not a record that private work or a site change has already been approved.')
    body += section('Choose a research path', 'These are proposed approaches. The recommendation is to assemble decision-grade inputs before committing, not to choose sale or renewal.', table(['Path','Scope','Trade-off','Status'], [
        (['A · Minimum', 'Lease and notice abstract, actual bids and CPA sale/renewal comparison.', 'Fastest starting point, but local and disaster evidence remains incomplete.', PROPOSED], ['sec25','irs']),
        (['B · Decision-grade', 'Path A plus private trade-area, hazard, insurance and joint stress review.', 'Recommended process for a balanced decision; requires adviser work and verified records.', PROPOSED], ['acs','cgs','fema']),
        (['C · Evidence-grade', 'Path B plus versioned, walk-forward model and continued comparable collection.', 'More analytical depth, but only credible if enough reliable history exists.', PROPOSED], ['acs','census']),
    ]))
    suggestions = [
        (['S01 · Commission lease abstract', 'Protect option deadlines and reconcile the private calendar before negotiating.', 'Attorney', PROPOSED], ['sec25']),
        (['S02 · Matched broker quotes', 'Get separate short-lease and extension opinions on the same assumptions; retain actual quotes privately.', 'Broker / adviser', PROPOSED], ['sec25']),
        (['S03 · Professional tax comparison', 'Compare current-sale equity, negotiated renewal and feasible exchange on a consistent after-tax basis.', 'CPA / qualified intermediary', PROPOSED], ['irs','exchange','ftb']),
        (['S04 · Local evidence pack', 'Define tract boundaries privately; include ACS uncertainty, traffic, schools and planning, not only regional proxies.', 'Local analyst', PROPOSED], ['acs','traffic','school','planning']),
        (['S05 · Engineering and insurance', 'Verify adopted parcel zones and coverage; quantify downtime, repairs and financing needs together.', 'Engineer / insurance broker', PROPOSED], ['cgs','fema','fire']),
        (['S06 · Back-tested projection', 'Only after sufficient verified history, implement the versioned validation protocol; publish non-identifying summaries.', 'Analyst / independent reviewer', PROPOSED], ['acs','census']),
        (['S07 · Source freshness review', 'Recheck tenant filings and each external source when material decisions or new releases occur.', 'Research reviewer', PROPOSED], ['edgar','schedule']),
        (['S08 · Privacy and accessibility review', 'Independently test disclosure risk, keyboard use and print output before future publishing.', 'Privacy / accessibility reviewer', PROPOSED], ['privacy']),
    ]
    body += section('Suggestions awaiting review', 'Each item stays proposed until the authorized reviewer decides whether to act.', table(['Suggestion','Why it could help','Suggested owner','Status'], suggestions))
    body += '<div class="note">Choose among the paths with authorized advisers after reviewing cost, timing, privacy and evidence quality. No approval mechanism or private task tracker is provided by the public site.</div>'
    page('suggestions.html', 'Suggestions', body)

    # Flag register
    body = heading('Transparency & exceptions', 'Flagged for review', 'Unverified values are blank. These items remain visible and are not reasons to invent an answer. A reference helps investigate the topic; it is not proof of the subject result.', '<span class="pill warn">Review required</span>')
    flags = [
        (['F01 · Exact lease and notice terms', BLANK, 'Brief says NNN and 2030–2035; controlling contract, expiry and notice dates were not provided.', 'Private counsel abstract and reconciled calendar.'], ['sec25']),
        (['F02 · Tenant / guarantor / store sales', BLANK, 'Brand filings do not establish the identity or credit of this lease counterparty or unit.', 'Review executed documents and permitted unit data privately.'], ['q326','sec25']),
        (['F03 · Trade area and tract trends', BLANK, 'Location withheld; regional data cannot be relabeled as parcel-level evidence.', 'Authorized analyst defines catchment and obtains consistent ACS data and margins.'], ['acs','acsdata']),
        (['F04 · Parcel hazards and insurance', BLANK, 'Fault, flood, fire, structure and coverage are not known.', 'Use current official layers, engineering and actual private policies/quotes.'], ['cgs','fema','fire']),
        (['F05 · Real broker quotes / discount', BLANK, 'No short-lease or extended-lease bids have been obtained.', 'Request matched written opinions; do not substitute a default discount.'], ['sec25']),
        (['F06 · Owner tax, debt and objectives', BLANK, 'Basis, income, ownership, payoff and acceptable loss are private and unavailable.', 'CPA and owner/adviser calculate the incremental after-tax cases privately.'], ['irs','ftb','diversify']),
        (['F07 · Private workspace / commissioning', BLANK, 'This is a public static site, not an access-controlled internal workspace; no advisers were contacted.', 'Use a separately controlled adviser workspace and authorize private work.'], ['privacy']),
        (['F08 · Historical calculator inconsistency', BLANK, 'The former root calculator compared pre-tax hold value against after-tax sale proceeds and used defaults. The canonical root worksheet was replaced; other historical dashboards have not been fully audited and may still contain assumptions or inconsistent calculators.', 'Use only the blank-by-default root worksheet with CPA-prepared inputs; separately audit legacy materials.'], ['irs']),
        (['F09 · Historical dashboards / row provenance', BLANK, 'Several prior dashboards are retained in the repository; some historical table rows lack per-row external citations and may use older data. They are not the canonical reviewed dashboard.', 'Re-verify each historical row and calculator before relying on it; do not treat an archive as current.'], ['edgar','acs']),
        (['F10 · FY2026 release date discrepancy', BLANK, 'The October 26 announcement says December 9; the issuer reference calendar lists November 18. Neither establishes that full-year results are available as of this review.', 'Check EDGAR and issuer updates for the actual release.'], ['schedule','schedule2','edgar']),
        (['F11 · Tax jurisdiction and ULA', BLANK, 'Central Los Angeles in the brief does not establish the City boundary, tax application or an exemption.', 'Counsel/CPA verify jurisdiction and time-specific transfer tax rules.'], ['ula']),
        (['F12 · Validated forecast', BLANK, 'No sufficient comparable history, back-test, prediction interval or property-specific model has been supplied.', 'Follow the staged protocol; do not publish a fabricated target.'], ['acs','census']),
        (['F13 · Census income source access', BLANK, 'QuickFacts could not be opened directly during this review. The root site uses separately accessible SAIPE county income instead of treating the ACS five-year value as verified here.', 'Manually check QuickFacts / ACS and preserve the differing program and vintage definitions.'], ['acs','income']),
    ]
    body += section('Open items and irregularities', 'Review status is a public evidence status; it does not disclose or attest to private work.', table(['Item','Subject value','Finding','Resolution'], flags))
    page('flagged.html', 'Flagged for review', body)

    # One page printable brief
    body = '''<div class="print-meta"><div><p class="eyebrow">W-10 · Adviser handout</p><h1>Decision brief</h1><p class="lead">Anonymous quick-service property · Evidence reviewed 26 November 2026</p></div><div class="no-print"><button class="button secondary" type="button" onclick="window.print()">Print / save PDF</button></div></div>
<div class="note warning"><strong>Current posture:</strong> Keep sale and renewal options open. No winner is supportable until private lease, market, tax, insurance and owner-objective inputs are verified.</div>'''
    body += section('Verified public context', 'Regional and brand figures—not parcel evidence.', table(['Observation','Value / limitation'], [
        (['Brand same-store sales', 'FY2025 −4.2%; Q3 FY2026 −1.1%.'], ['secq425','q326']),
        (['Brand restaurant count', '2,115 at July 5, 2026; Q3 had 4 openings and 17 closures.'], ['q326']),
        (['LA County population', '9,748,868 (2024) → 9,694,934 (2025), Census Vintage 2025.'], ['census']),
        (['LA metro unemployment', '4.4% preliminary, September 2026; not a trade-area result.'], ['bls']),
    ]))
    body += section('Priority questions for authorized advisers', 'Private records and answers must remain outside this public site.', '''<div class="card-grid two"><div class="card"><h3>Legal + market</h3><p>Abstract the executed lease and reconcile option and notice dates. Verify guaranty, rent, repairs and restrictions. Obtain matched short-term sale and negotiated renewal quotes.</p></div><div class="card"><h3>Tax + risk</h3><p>Calculate after-tax sale and hold equity; verify basis, debt, liquidity and tax jurisdiction. Privately screen earthquake, flood and fire; obtain engineering and insurance terms.</p></div></div>''')
    body += '<p style="margin-top:12px;font-size:11px">The brief’s NNN lease and 2030–2035 window are unverified. No abstract, quote, private workspace or adviser engagement is evidenced here. The worksheet is not a tax engine or investment recommendation. <a href="flagged.html">Open the review register.</a></p>'
    page('printable-summary.html', 'Advisor brief', body, print_page=True)

    # Source library
    body = heading('Source library', 'Read the underlying evidence', 'Official agency, SEC and issuer-primary references used by the canonical dashboard. Reviewed 26 November 2026; dynamic sources may change. A link on a workflow row is context, not proof of a private fact.')
    source_rows = [
        (['FY2023 annual filing', 'Same-store sales, system units, closures and Jack in the Box franchise rental revenue.'], ['sec23']),
        (['FY2025 annual filing', 'FY2024–2025 Jack in the Box segment performance and company lease portfolio context.'], ['sec25']),
        (['FY2025 earnings release', 'FY2025 and Q4 system sales changes and closures.'], ['secq425']),
        (['Q1 FY2026 release', 'Issuer-primary quarterly same-store sales, openings, closures and unit count.'], ['q126']),
        (['Q2 FY2026 release', 'SEC-filed quarterly sales change and unit count.'], ['q226']),
        (['Q3 FY2026 release', 'SEC-filed quarterly sales change, restaurant count and closures.'], ['q326']),
        (['Q3 FY2026 10-Q', 'Company rental-revenue series and comparative disclosures.'], ['q32610q']),
        (['SEC issuer filing index', 'Check for subsequently filed reports; no future filing is assumed.'], ['edgar']),
        (['FY2026 release scheduling', 'Issuer-primary October announcement and reference calendar conflict; see F10.'], ['schedule','schedule2']),
        (['Census population release', 'County population estimates with the same Vintage 2025 series and revision guidance.'], ['census']),
        (['Census ACS data and guidance', 'Small-area estimates, five-year comparison and uncertainty.'], ['acsdata','acs']),
        (['Census SAIPE via Federal Reserve', 'Annual LA County median household income estimate, not an ACS tract value.'], ['income']),
        (['Bureau of Labor Statistics', 'LA metro unemployment and nonfarm payroll data, including preliminary labels.'], ['bls']),
        (['California Department of Education', 'Public school and enrollment data.'], ['school']),
        (['Caltrans traffic census', 'State-highway traffic counts and guidance for local roads.'], ['traffic']),
        (['LA City Planning', 'City planning cases and maps; applicable jurisdiction is not established.'], ['planning']),
        (['USGS and California Geological Survey', 'Regional earthquake context and parcel hazard-zone screening limitations.'], ['quake','cgs']),
        (['FEMA flood maps', 'Flood map research and risk reduction resources.'], ['fema']),
        (['CAL FIRE / State Fire Marshal', 'Fire Hazard Severity Zone context and current map resources.'], ['fire']),
        (['IRS capital gains', 'Federal basis and capital-gain rules; not an owner-specific computation.'], ['irs']),
        (['IRS like-kind exchange instructions', 'Form 8824 requirements and timing; verify applicability with specialists.'], ['exchange']),
        (['California Franchise Tax Board', 'Real-estate withholding and like-kind reporting guidance.'], ['ftb']),
        (['LA transfer tax / Measure ULA', 'City-specific rates, boundaries, exemptions and annual threshold adjustment.'], ['ula']),
        (['NIST Privacy Framework', 'Privacy risk management and data protection context.'], ['privacy']),
        (['SEC investor education', 'Risk tolerance, time horizon and diversification.'], ['diversify']),
    ]
    body += section('Evidence ledger', 'External links open only when selected; external websites have their own privacy practices.', table(['Reference','What it supports'], source_rows))
    page('sources.html', 'Source library', body)

    # Privacy policy
    body = heading('Highest priority', 'Privacy comes first', 'This public site contains only broad, non-identifying context and placeholders. It is not an internal document repository or a substitute for access controls.')
    body += section('What belongs where', 'Never upload private property evidence to this repository or a public issue, pull request, comment, screenshot or deployment.', table(['Information','Public site','Private workflow'], [
        (['Owner and parcel identifiers', 'Withheld.', 'Keep names, address, parcel number, contact details and identifying maps with authorized advisers only.'], ['privacy']),
        (['Lease, title, tax and finances', 'Withheld.', 'Keep originals, extracts, tax returns, basis, debt and quotes in a separately controlled workspace.'], ['privacy','irs']),
        (['Local research', 'Only aggregate, non-identifying findings after disclosure review.', 'Use the actual location only for authorized tract, planning, traffic, school, competitor and hazard research.'], ['privacy','acs']),
        (['Optional browser worksheet', 'No default values or submission form; code does not intentionally transmit or persist inputs.', 'Use a trusted device; browser extensions, device history, hosting logs and external sites may pose separate risks.'], ['privacy']),
        (['External map and source links', 'Loaded only after a user selects a link.', 'A third-party site may receive/log search data. Download data for offline use when practical and follow adviser policy.'], ['privacy','cgs']),
    ]))
    body += '''<div class="note warning"><strong>Important limits:</strong> GitHub Pages is public. Accessing it may reveal ordinary connection metadata to the host. This site cannot provide encryption, access control, secure backup or confidentiality for private records; no separate private workspace has been created or verified.</div>'''
    page('privacy.html', 'Privacy', body)


if __name__ == '__main__':
    build()
    print('Built 15 canonical static pages from official-source references; no private inputs used.')
