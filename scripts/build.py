from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
sources = {
 'census': ('Census QuickFacts', 'https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,ca'),
 'county': ('Census · county QuickFacts', 'https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia,ca'),
 'acs': ('Census · ACS release', 'https://www.census.gov/programs-surveys/acs/news/data-releases/2024/release.html'),
 'bls': ('BLS · metro unemployment', 'https://www.bls.gov/opub/ted/2026/unemployment-rates-lower-in-226-metro-areas-from-september-2025-to-september-2026.htm'),
 'jack': ('Jack in the Box · FY2025 results', 'https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Reports-Fourth-Quarter-and-Full-Year-2025-Earnings/default.aspx'),
 'irs': ('IRS · basis', 'https://www.irs.gov/publications/p551'),
 'sale': ('IRS · dispositions', 'https://www.irs.gov/publications/p544'),
 'exchange': ('IRS · Form 8824 instructions', 'https://www.irs.gov/pub/irs-prior/i8824--2025.pdf'),
 'eq': ('California Geological Survey', 'https://www.conservation.ca.gov/cgs/Pages/_Maps-and-Data-Home.aspx'),
 'flood': ('FEMA · flood maps', 'https://www.fema.gov/flood-maps'),
 'fire': ('CAL FIRE · hazard maps', 'https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones'),
 'planning': ('LA City Planning · ZIMAS', 'https://planning.lacity.gov/blog/how-do-i-receive-information-proposed-projects'),
 'schools': ('CA Department of Education', 'https://www.cde.ca.gov/ds/'),
 'traffic': ('Caltrans · traffic counts', 'https://dot.ca.gov/programs/traffic-operations/census'),
 'privacy': ('FTC · data security', 'https://www.ftc.gov/business-guidance/resources/start-security-guide-business'),
 'sec': ('SEC · investor risk', 'https://www.investor.gov/introduction-investing/investing-basics/investment-products/real-estate-investment-trusts-reits'),
}
def link(key):
 label,url=sources[key]
 return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label} ↗</a>'
def table(head, rows):
 return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+escape(x)+'</th>' for x in head)+ '<th>Source / method</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row[:-1])+'<td class="source">'+link(row[-1])+'</td></tr>' for row in rows)+'</tbody></table></div>'
def pill(text, kind='amber'): return f'<span class="pill {kind}"><span></span>{text}</span>'
def section(title,desc='',content=''): return f'<section class="section"><div class="section-head"><div><h2>{title}</h2>{("<p>"+desc+"</p>") if desc else ""}</div></div>{content}</section>'
def callout(title,text,cls=''): return f'<div class="callout {cls}"><div class="call-icon">!</div><div><strong>{title}</strong><p>{text}</p></div></div>'
nav=[('index.html','Overview','◫'),('market.html','Market evidence','◈'),('decisions.html','Decision paths','⇄'),('gates.html','Decision gates','▦'),('calculator.html','Private calculator','▤'),('suggestions.html','Suggestions','✧'),('review.html','Flagged for review','⚑')]
def page(file,title,eyebrow,subtitle,body,action=''):
 links=''.join(f'<a class="nav-link {"active" if file==url else ""}" href="{url}"><span class="nav-icon">{icon}</span>{name}</a>' for url,name,icon in nav)
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="no-referrer"><title>{title} | Property Decision Desk</title><link rel="stylesheet" href="assets/style.css"><script defer src="assets/app.js"></script></head><body><a class="skip" href="#main">Skip to content</a><div class="layout"><aside class="sidebar"><a class="brand" href="index.html"><span class="brand-mark">▧</span><span>PROPERTY<span class="brand-sub">DECISION DESK</span></span></a><div class="workspace"><span class="workspace-icon">◇</span><span><strong>Advisory workspace</strong><small>ANONYMOUS CASE STUDY</small></span></div><div class="nav-label">WORKSPACE</div><nav aria-label="Main navigation">{links}</nav><div class="sidebar-foot"><span class="shield">◇</span><div><strong>Privacy first</strong><p>Public findings only. Sensitive records stay offline.</p></div></div></aside><div class="content"><header class="topbar"><span>PROPERTY INTELLIGENCE <span class="top-sep">/</span> <b>{title.upper()}</b></span><span class="top-right"><span class="green-dot"></span> PUBLIC · ANONYMIZED</span></header><main id="main"><div class="page-head"><div><div class="eyebrow"><span></span>{eyebrow}</div><h1>{title}</h1><p class="subtitle">{subtitle}</p></div>{action}</div>{body}<footer><span>PROPERTY DECISION DESK <span class="footer-dot">•</span> RESEARCH BRIEF</span><span>Sources reviewed November 25, 2026 · Not investment, legal or tax advice</span></footer></main></div></div></body></html>'''
 (ROOT/file).write_text(html)

# Public context observations, not estimates of the unidentified location.
market=table(['Indicator','Published figure','Scope & interpretation'],[
 ('Population estimate','3,869,089','Los Angeles city; July 1, 2025. Not the trade area.','census'),
 ('Median household income','$81,939','Los Angeles city; ACS 2020–2024, 2024 dollars. Not parcel income.','census'),
 ('Median household income','$90,112','Los Angeles County; ACS 2020–2024, 2024 dollars. Not parcel income.','county'),
 ('Unemployment','5.5% → 4.4%','LA–Long Beach–Anaheim metro; September 2025 → September 2026, not seasonally adjusted. Not job growth.','bls'),
 ('System same-store sales','−1.3% → −4.2%','Jack in the Box system, FY2024 → FY2025; not this restaurant.','jack'),
 ('Restaurant count','2,191 → 2,136','Jack in the Box system, end of FY2024 → end of FY2025.','jack'),
 ('Openings / closures','31 / 86','Jack in the Box system, FY2025. Not a site-specific closure prediction.','jack'),
 ('Franchise rental revenue','$375.428m → $368.643m','Company-wide consolidated, FY2024 → FY2025; includes both segments, not site rent.','jack'),
])
questions=table(['Question','Known / answer','Missing & next step'],[
 ('What is the exact lease term and notice window?','Reported NNN; expiry somewhere in 2030–2035, unverified.','Counsel to abstract signed lease and amendments; reconcile notice dates and delivery rules privately.','planning'),
 ('Who pays what and who guarantees rent?','NNN is a user description, not verified lease language.','Confirm landlord obligations, guarantor, assignment, defaults, options, rent steps and estoppel.','sale'),
 ('What can each path yield after tax?','No property or taxpayer figures supplied.','CPA to verify basis, depreciation, debt, selling costs, federal and California tax and timing.','irs'),
 ('What is the short-lease discount?','No verified bids or comparable transactions.','Solicit dated, comparable as-is and renewal-contingent broker opinions / bids; reconcile terms.','sale'),
 ('Is the neighborhood strengthening?','City and metro measures are context only.','Privately define a trade area and consistent tracts; compare ACS vintages and margins of error.','acs'),
 ('Are earthquake, flood or fire zones applicable?','Parcel location and zone status not supplied.','Private map checks plus engineering, insurance and coverage review; record map dates.','eq'),
 ('What level of risk is manageable?','Owner liquidity, concentration and goals are unknown.','Adviser to document reserves, income needs, diversification and loss tolerance offline.','sec'),
])
flags=table(['Item','Status','Why it matters / resolution'],[
 ('Lease expiry and NNN allocation',pill('Unverified'),'Reported 2030–2035 is not a date or legal conclusion. Obtain signed documents and legal abstract.','sale'),
 ('Parcel, trade area and tract',pill('Not available'),'No parcel identifier or boundary was provided. No tract, site geography, schools, traffic or competitor claims are possible.','acs'),
 ('Earthquake, fire and flood status',pill('Not screened'),'Do not interpret regional maps as a parcel determination. An authorized professional must check current maps privately.','eq'),
 ('Valuation, quotes and short-lease discount',pill('Not available'),'No actual bids, comparable lease terms, concessions or appraisal. Do not invent a cap rate or discount.','sale'),
 ('Tax and owner circumstances',pill('Not available'),'Basis, depreciation, debt, taxpayer profile, liquidity and objectives are unknown. CPA must calculate taxes privately.','irs'),
 ('Projection and back-test',pill('Not ready'),'No verified asset cash flows or sufficient comparable history. No forecast or confidence interval can be justified.','acs'),
 ('Public-company indicators',pill('Context only','blue'),'Company-wide historical results do not establish the local operator’s credit, site sales or likelihood of renewal.','jack'),
 ('Private workflow',pill('External dependency'),'This public repository and website are not an access-controlled records system. No adviser has been commissioned.','privacy'),
])
gates=table(['Gate','Status','Evidence to clear / responsible party'],[
 ('01 · Privacy & authority',pill('Open'),'Owner and counsel: designate authorized advisers and an offline, access-controlled file location.','privacy'),
 ('02 · Lease & notice',pill('Open'),'Real-estate counsel: signed lease, amendments and estoppel; independently reconcile a dated notice calendar before commitment.','sale'),
 ('03 · Local demand',pill('Open'),'Analyst: privately define trade area, consistent tract vintages and ACS uncertainty; validate planning, schools, traffic and competitors.','acs'),
 ('04 · Condition & hazards',pill('Open'),'Engineer and insurance broker: parcel maps, building condition, deductibles, limits, exclusions and rent interruption.','eq'),
 ('05 · Market pricing',pill('Open'),'Broker/appraiser: dated comparable bids for existing term and negotiated renewal, with matched assumptions.','sale'),
 ('06 · Tax & alternatives',pill('Open'),'CPA and adviser: reconcile basis, tax, debt and after-tax cash flows for sale, renewal and alternatives.','irs'),
 ('07 · Decision & monitoring',pill('Blocked'),'Owner/advisers: approve documented assumptions, stress tests and notice dates; revisit when quotes or facts change.','sec'),
])
paths=table(['Path','Potential benefit','Material risk / diligence'],[
 ('Sell before expiration','Liquidity and reduced exposure to future vacancy.','Short remaining term may affect bids; taxes, debt payoff and reinvestment can reduce proceeds. Compare real quotes.','sale'),
 ('Negotiate renewal, then hold','Potential continuity of rent and longer lease term.','Renewal is not assured; concession, tenant credit, capital, inflation and concentration risk remain. Verify documents.','sec'),
 ('Renew, then sell','A longer term may affect marketability.','Negotiation takes time and may require concessions; compare firm net offers and tax consequences.','sale'),
 ('Hold through expiration / re-lease','Potential flexibility to change tenants or use.','Vacancy, downtime, tenant improvements, permitting and uncertain rent can erode returns. Confirm permissible use.','planning'),
 ('Redevelop / alternative use','May create different future uses if feasible.','Entitlement, construction, financing and delay risk; verify zoning, feasibility and capital needs.','planning'),
 ('Exchange under §1031','Potential tax deferral if requirements are met.','Not tax-free; replacement and execution risk, timing and eligibility require advance CPA and intermediary advice.','exchange'),
])
# Landing
body='''<div class="hero"><div class="hero-top"><div><div class="hero-kicker"><span class="pulse"></span> DECISION BRIEF <span class="hero-divider">/</span> CENTRAL LOS ANGELES AREA</div><h2>A clearer path to a<br><em>better decision.</em></h2><p>A privacy-first framework for evaluating a single-tenant property, its lease horizon, and the choices ahead.</p><div class="hero-actions"><a class="button light" href="gates.html">Explore decision gates <span>→</span></a><a class="text-link" href="advisor.html">Advisor summary ↗</a></div></div><div class="hero-graphic" aria-hidden="true"><div class="orbit orbit-a"></div><div class="orbit orbit-b"></div><div class="orbit orbit-c"></div><div class="graphic-center">◇</div><div class="graphic-tag tag-one">LEASE <b>2030–35*</b></div><div class="graphic-tag tag-two">DECISION <b>ON HOLD</b></div></div></div><div class="hero-bottom"><span><b>01</b> Asset <strong>Single-tenant NNN*</strong></span><span><b>02</b> Market <strong>Los Angeles area*</strong></span><span><b>03</b> Status <strong>Evidence gathering</strong></span></div></div><p class="fine">*User-reported context, not independently verified. No property has been identified or screened.</p>'''
body+=section('The decision at a glance','A recommendation on process—not a premature recommendation to sell or renew.', '''<div class="summary-grid"><article class="summary-card"><div class="card-icon">↗</div><h3>Current position</h3><p>Do not commit to a sale or renewal yet. First protect notice rights and obtain comparable, after-tax cases.</p><a href="decisions.html">Compare the paths →</a></article><article class="summary-card"><div class="card-icon">⌁</div><h3>What the data says</h3><p>Regional indicators and brand-wide results provide context, but cannot establish this location’s outlook.</p><a href="market.html">Review the evidence →</a></article><article class="summary-card"><div class="card-icon">▧</div><h3>What comes next</h3><p>Private lease abstraction, hazard screening, market quotes and a CPA-reviewed comparison are open gates.</p><a href="gates.html">See the checklist →</a></article></div>''')
body+=callout('The most important boundary','This is a public, anonymous research product—not a private document vault. Do not enter identifiers, lease documents, or financial records into this repository. See '+link('privacy')+'.')
body+=section('Evidence snapshot','The figures below are broad context, not observations about the property.',market)
body+=section('Questions before a commitment','The highest-priority gaps and a way to resolve each one.',questions)
page('index.html','Overview','A PRIVATE DECISION, A PUBLIC BRIEF','An evidence-led look at the sell-versus-renew decision.',body,'<a class="outline-button" href="advisor.html">↗ &nbsp; Advisor brief</a>')
body=callout('Geography is not a trade area','City, county and metro data cannot establish the conditions around an unidentified parcel. All local measures remain blank until the location is reviewed privately.')
body+=section('Verified public context','Primary sources; periods, geography and definitions are deliberately retained.','<p class="note">Government sources are official statistical series; Jack in the Box results are the company’s own primary-source disclosures, not government verification of the individual unit.</p>'+market)
body+=section('Trade-area research plan','No tract is selected and no parcel-based values are inferred.',table(['Evidence','Value','Private collection method'],[
 ('Population, income, housing & trend','— Unverified','Select consistent tract boundaries and ACS vintages; report margins of error, overlap and changes.','acs'),
 ('Job growth & labor market','— Unverified','Use applicable official employment series and geography; unemployment is not job growth.','bls'),
 ('Schools','— Unverified','Identify nearby schools and enrollment using state records; do not infer performance or demand.','schools'),
 ('Traffic, access & competition','— Unverified','Caltrans counts cover state highways only; obtain city street counts locally and field inventory. Distinguish count location, date, accessibility and competitor openings.','traffic'),
 ('Zoning & pipeline','— Unverified','Verify jurisdiction first; if within Los Angeles city, inspect ZIMAS and pending planning cases privately.','planning'),
 ('Earthquake zones','— Unverified','Privately check current CGS fault and seismic hazard maps; request engineering review.','eq'),
 ('Flood zone','— Unverified','Privately check the effective FEMA map and amendments; review coverage.','flood'),
 ('Fire hazard zone','— Unverified','Privately check applicable CAL FIRE and local jurisdiction maps; hazard zones are not loss probability.','fire'),
]))
body+=section('Projection discipline','A useful model comes after the evidence, not before it.', '<div class="prose-card"><h3>Build, validate, then use</h3><p>Version a dated cash-flow model with explicit observations, assumptions and sources. Use consistent geography and non-overlapping periods where possible. Assemble comparable history before fitting or back-testing; keep a holdout period, assess errors and report limitations. Run base, downside and severe scenarios; do not assign unsupported probabilities or extrapolate city averages to a specific site.</p></div>')
page('market.html','Market evidence','RESEARCH LIBRARY','What can be verified today—and what requires a secure, parcel-level investigation.',body)
body=callout('No winner selected','The decision cannot responsibly be personalized without verified lease terms, actual pricing, tax inputs, owner objectives and risk tolerance.')+section('Compare the alternatives','Potential outcomes are conditional, not recommendations or forecasts.',paths)
body+=section('Stress the whole picture','Test combined losses rather than treating each risk in isolation.',table(['Scenario','Possible impact','Review / mitigation'],[
 ('Business as usual','Rent, costs, rates and tenant credit may change.','Obtain rent steps, expense responsibilities, refinance assumptions and comparable prices.','sec'),
 ('Tenant default or nonrenewal','Lost rent, vacancy, legal costs, re-leasing and capital requirements.','Review guaranty, lease remedies, tenant credit and replacement-tenant costs.','sale'),
 ('Earthquake, flood or wildfire','Repairs, rent interruption, deductible and exit liquidity may occur together.','Screen each parcel zone and engineering vulnerabilities; review policy limits and exclusions.','flood'),
 ('Liquidity or capital-market shock','Fewer buyers, higher financing costs and delayed exit.','Use real bid ranges and a prolonged sale timeline; maintain reserves consistent with owner capacity.','sec'),
 ('Tax / regulatory change','Net proceeds, permissible use or replacement economics can change.','CPA and counsel to update rules and zoning before committing.','irs'),
]))
body+=section('Quote the lease discount','A practical protocol, not an invented percentage.', '<div class="prose-card"><p>Ask qualified brokers or buyers for dated, written indications on the <strong>same asset</strong>: (1) sale with the current remaining lease and (2) sale conditional on a specified signed renewal. Align sale date, rent, expenses, credit, contingencies and transaction costs. Difference in net quotes is an observed indication, not a causal estimate; reconcile with independent comparables. Keep all identifying materials offline.</p></div>')
page('decisions.html','Decision paths','STRATEGY & RISK','Compare alternatives on equal terms, including ordinary and severe downside.',body)
body=callout('All gates remain open','No lease, parcel record, binding offer or owner financial record was provided. Status reflects missing evidence, not completed work.')+section('Progress board','Clear these gates before making a sale or renewal commitment.',gates)+section('Questions & discovery','A working list for authorized advisers.',questions)
page('gates.html','Decision gates','DUE DILIGENCE','A practical sequence from privacy safeguards to a defensible decision.',body)
body=callout('No inputs are prefilled','Nothing has been verified for this property. This optional adviser tool runs only in this page’s browser memory. It does not transmit or save entries; use a trusted offline device and clear the form when finished. Do not enter names, addresses or identifiers.')
body+=section('Comparable after-tax cash flows','Enter CPA-reviewed totals only. Values are assumptions until verified; this is not a tax engine.', '''<div class="calc-layout"><form id="calculator" autocomplete="off"><div class="form-grid"><label>Sale price today ($)<input name="price" type="number" min="0" step="any" required></label><label>Selling costs today ($)<input name="cost" type="number" min="0" step="any" required></label><label>Debt payoff today ($)<input name="debt" type="number" min="0" step="any" required></label><label>CPA-estimated sale tax today ($)<input name="tax" type="number" min="0" step="any" required></label><label>Annual after-tax hold cash flow ($)<input name="cash" type="number" step="any" required></label><label>Terminal net sale proceeds after tax & debt ($)<input name="terminal" type="number" step="any" required></label><label>Holding horizon (whole years)<input name="years" type="number" min="1" max="50" step="1" required></label><label>Annual discount rate (%)<input name="rate" type="number" min="0" max="100" step="any" required></label></div><div class="form-actions"><button class="button dark" type="submit">Compare scenarios →</button><button class="outline-button" type="reset">Clear all</button></div></form><div class="result-box" aria-live="polite"><div class="mini-label">COMPARISON OUTPUT</div><h3>Awaiting verified inputs</h3><p>Results appear here only. No data is stored.</p><div id="results"></div></div></div><p class="note">The hold case assumes a constant annual after-tax cash flow received at each year-end and terminal net proceeds at the end of the horizon. Discount rate must be consistent with after-tax equity cash flows. Include the cost and tax of a future exit in terminal proceeds; avoid double-counting debt service or costs. Sale proceeds are today’s net cash, not an NPV of reinvestment. Compare an equivalent reinvestment case separately. CPA estimates—not an automatic tax-rate calculation—capture federal, state and taxpayer-specific rules. Negative annual and terminal net amounts are permitted.</p>''')
body+=section('Tax review checklist','CPA-reviewed inputs are essential; no single tax rate applies universally.',table(['Item','Treatment to verify','Official guidance'],[
 ('Adjusted basis','Acquisition and capital improvements, less allowable adjustments including depreciation.','irs'),
 ('Gain & depreciation treatment','Confirm amount realized, gain character, depreciation and any applicable federal / California taxes.','sale'),
 ('Debt and transaction costs','Separate debt payoff from taxable gain; reconcile costs and net cash with CPA.','sale'),
 ('Like-kind exchange','Potential deferral, not automatic elimination; generally 45-day identification and earlier of 180 days or tax return due date including extensions.','exchange'),
]))
page('calculator.html','Private calculator','SCENARIO WORKBENCH','A transparent starting point for advisers, not a valuation or tax opinion.',body)
body=section('Proposed improvements','Review and choose a path before implementation. None of these proposals is presented as completed.',table(['Priority','Suggestion','Decision / reason'],[
 ('01 · Critical','Establish offline access-controlled adviser workspace','Approve storage and access policy before collecting sensitive records; never place them on Pages.','privacy'),
 ('02 · Critical','Commission lease abstract and notice calendar','Authorize counsel and an independent cross-check before any commitment.','sale'),
 ('03 · High','Replace proxies with trade-area evidence','Select consistent tracts privately; publish only non-identifying aggregate results after disclosure review.','acs'),
 ('04 · High','Secure quote and insurance evidence','Request matched market bids and hazard/coverage review before estimating discount or loss.','flood'),
 ('05 · High','Add a versioned cash-flow and tax model','Have CPA and adviser validate a time-varying model, assumptions and back-test before publishing any output.','irs'),
 ('06 · Later','Add review workflow for future suggestions','Agree on priority, owner, approval and privacy policy before collecting any submissions.','privacy'),
]))
body+=callout('Review first, implement second','Suggestions are proposals. The public site does not collect votes, messages or personal information. Use an authorized offline process to choose and approve changes.')
page('suggestions.html','Suggestions','IMPROVEMENT BACKLOG','A dedicated place to consider improvements without automatically implementing them.',body)
body=section('Open items','Unverified items are visible here and are not represented as facts.',flags)+callout('Source links are starting points','A linked method or agency page does not verify a missing parcel-specific value. Official map checks and private records are still required.')
page('review.html','Flagged for review','TRANSPARENCY LOG','Missing evidence, limitations and irregularities requiring follow-up.',body)
body='''<div class="print-actions"><button class="outline-button" onclick="window.print()">Print / save PDF ↗</button></div><div class="advisor-sheet"><div class="advisor-head"><div><div class="eyebrow"><span></span> ONE-PAGE ADVISOR BRIEF</div><h2>Decision on hold.</h2><p>Anonymous single-tenant restaurant property · Los Angeles area</p></div><div class="sheet-status">EVIDENCE GATHERING</div></div><div class="advisor-grid"><div><h3>Situation</h3><p>Reported NNN lease; reported expiration range 2030–2035. Neither lease nor property has been independently verified.</p><h3>Recommended immediate action</h3><p>Do not commit to sell or renew. Engage counsel for a lease abstract and notice calendar; obtain matched sale and renewal quotes and a CPA-reviewed after-tax comparison.</p><h3>What is known</h3><p>Broad public indicators are context only. FY2025 system same-store sales declined 4.2%; this does not establish this unit’s performance. '''+link('jack')+'''</p></div><div><h3>Critical unknowns</h3><p>Exact dates and rights; tenant and guarantor; site performance; land-use and neighborhood trends; condition and parcel hazard zones; bids, debt, basis, tax and owner risk capacity.</p><h3>Downside to test</h3><p>Tenant nonrenewal, vacancy, capital costs, lower exit liquidity and compounded earthquake, fire or flood losses with rent interruption. Check maps, engineering and coverage privately. '''+link('flood')+'''</p><h3>Privacy boundary</h3><p>Public site contains no parcel identifiers or private records. Keep evidence and calculations on trusted devices with authorized advisers. '''+link('privacy')+'''</p></div></div><div class="sheet-foot">AS OF 25 NOV 2026 &nbsp; · &nbsp; NOT LEGAL, TAX OR INVESTMENT ADVICE &nbsp; · &nbsp; SEE FULL SITE FOR SOURCES AND FLAGS</div></div>'''
page('advisor.html','Advisor summary','PRINTABLE BRIEF','A concise, anonymous handoff for the people helping make the decision.',body)
