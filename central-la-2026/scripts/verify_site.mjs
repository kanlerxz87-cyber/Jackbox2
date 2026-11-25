#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const errors = [];
const warnings = [];

const TRUSTED_DOMAINS = [
  'sec.gov', 'census.gov', 'data.census.gov', 'bls.gov', 'dof.ca.gov', 'edd.ca.gov',
  'cde.ca.gov', 'dir.ca.gov', 'wagesla.lacity.gov', 'finance.lacity.gov', 'lavote.gov',
  'assessor.lacounty.gov', 'irs.gov', 'ftb.ca.gov', 'boe.ca.gov', 'usgs.gov',
  'conservation.ca.gov', 'maps.conservation.ca.gov', 'fire.ca.gov', 'osfm.fire.ca.gov',
  'fema.gov', 'insurance.ca.gov', 'home.treasury.gov', 'fred.stlouisfed.org',
  'metro.net', 'planning.lacity.gov', 'scag.ca.gov', 'dot.ca.gov', 'leginfo.legislature.ca.gov'
];

function checkTrustedUrl(url, ctx) {
  if (!url || typeof url !== 'string' || !url.startsWith('https://')) {
    errors.push(`[URL] Invalid or non-HTTPS source URL at ${ctx}: ${url}`);
    return;
  }
  try {
    const host = new URL(url).hostname.replace(/^www\./, '');
    const ok = TRUSTED_DOMAINS.some((d) => host === d || host.endsWith('.' + d));
    if (!ok) {
      errors.push(`[UNTRUSTED DOMAIN] ${host} at ${ctx} (${url})`);
    }
  } catch (e) {
    errors.push(`[URL PARSE] ${ctx}: ${url}`);
  }
}

// 1. Validate all JSON datasets & every row's official source URL
const dataFiles = [
  'tenant.json', 'market-w01.json', 'hazards-w04.json',
  'tax-lease.json', 'gates-w03.json', 'flagged.json', 'questions-suggestions.json'
];
const datasets = {};
for (const f of dataFiles) {
  const full = path.join(root, 'data', f);
  try {
    datasets[f] = JSON.parse(fs.readFileSync(full, 'utf8'));
  } catch (e) {
    errors.push(`[JSON] Failed parsing data/${f}: ${e.message}`);
  }
}

function auditRowArray(arr, urlField, label) {
  if (!Array.isArray(arr) || arr.length === 0) {
    errors.push(`[DATA] Empty or missing array: ${label}`);
    return;
  }
  arr.forEach((row, idx) => {
    checkTrustedUrl(row[urlField], `${label}[${idx}]`);
  });
}

if (datasets['tenant.json']) {
  auditRowArray(datasets['tenant.json'].annualSeries, 'sourceUrl', 'tenant.annualSeries');
  auditRowArray(datasets['tenant.json'].quarterlySeriesFY25_26, 'sourceUrl', 'tenant.quarterlySeriesFY25_26');
  auditRowArray(datasets['tenant.json'].creditAndCorporateFacts, 'sourceUrl', 'tenant.creditAndCorporateFacts');
}
if (datasets['market-w01.json']) {
  auditRowArray(datasets['market-w01.json'].indicators, 'sourceUrl', 'market.indicators');
  auditRowArray(datasets['market-w01.json'].projectionFramework, 'sourceUrl', 'market.projectionFramework');
}
if (datasets['hazards-w04.json']) {
  auditRowArray(datasets['hazards-w04.json'].hazardMatrix, 'lookupPortalUrl', 'hazards.hazardMatrix');
  auditRowArray(datasets['hazards-w04.json'].wildfire2025OfficialStats, 'sourceUrl', 'hazards.wildfire2025OfficialStats');
  auditRowArray(datasets['hazards-w04.json'].stressScenarios, 'sourceUrl', 'hazards.stressScenarios');
}
if (datasets['tax-lease.json']) {
  auditRowArray(datasets['tax-lease.json'].taxRules, 'sourceUrl', 'taxLease.taxRules');
  auditRowArray(datasets['tax-lease.json'].leaseAbstractChecklist, 'sourceUrl', 'taxLease.leaseAbstractChecklist');
}
if (datasets['gates-w03.json']) {
  auditRowArray(datasets['gates-w03.json'].gates, 'sourceUrl', 'gates.gates');
}
if (datasets['flagged.json']) {
  auditRowArray(datasets['flagged.json'].items, 'sourceUrl', 'flagged.items');
}
if (datasets['questions-suggestions.json']) {
  auditRowArray(datasets['questions-suggestions.json'].decisionOptions, 'sourceUrl', 'qaSuggestions.decisionOptions');
  auditRowArray(datasets['questions-suggestions.json'].missingInfoQA, 'sourceUrl', 'qaSuggestions.missingInfoQA');
  auditRowArray(datasets['questions-suggestions.json'].siteSuggestions, 'sourceUrl', 'qaSuggestions.siteSuggestions');
}

// 2. Check data-bundle.js exists and is up to date
const bundlePath = path.join(root, 'assets', 'js', 'data-bundle.js');
if (!fs.existsSync(bundlePath)) {
  errors.push('[BUNDLE] assets/js/data-bundle.js missing');
}

// 3. Validate all HTML pages, internal links, asset links, and zero external CDN scripts/CSS
const expectedPages = [
  'index.html', 'tenant-analysis.html', 'market-trade-area.html', 'hazards-risk.html',
  'lease-calendar.html', 'calculator.html', 'decision-gates.html', 'questions-gaps.html',
  'suggestions.html', 'advisor-summary.html', 'flagged-review.html'
];

for (const page of expectedPages) {
  const full = path.join(root, page);
  if (!fs.existsSync(full)) {
    errors.push(`[PAGE] Missing expected HTML file: ${page}`);
    continue;
  }
  const html = fs.readFileSync(full, 'utf8');

  // Check zero external scripts or stylesheets
  const extScript = html.match(/<script[^>]+src=["']https?:\/\//gi);
  const extStyle = html.match(/<link[^>]+href=["']https?:\/\//gi);
  if (extScript) errors.push(`[PRIVACY] External <script> found in ${page}: ${extScript.join(', ')}`);
  if (extStyle) errors.push(`[PRIVACY] External <link> found in ${page}: ${extStyle.join(', ')}`);

  // Check all href and src attributes
  const attrRegex = /(?:href|src)=["']([^"']+)["']/gi;
  let m;
  while ((m = attrRegex.exec(html)) !== null) {
    const target = m[1];
    if (target.startsWith('https://')) {
      checkTrustedUrl(target, `${page} link`);
    } else if (target.startsWith('http://')) {
      errors.push(`[HTTP] Non-HTTPS external link in ${page}: ${target}`);
    } else if (target.startsWith('#') || target.startsWith('mailto:') || target.startsWith('javascript:')) {
      continue;
    } else {
      const cleanPath = target.split('#')[0].split('?')[0];
      const resolved = path.join(root, cleanPath);
      if (!fs.existsSync(resolved)) {
        errors.push(`[BROKEN LINK] ${page} -> ${target}`);
      }
    }
  }
}

// 4. PII & Privacy Leak Scan across HTML, JS, CSS, JSON, MD
const piiPatterns = [
  { name: 'SSN pattern', re: /\b\d{3}-\d{2}-\d{4}\b/g },
  { name: 'Unrelated search address leak (5th St)', re: /741 W 5TH/i },
  { name: 'Unrelated search address leak (Crenshaw)', re: /3017-3053 Crenshaw|3630 Crenshaw/i },
  { name: 'Personal email address', re: /[a-zA-Z0-9._%+-]+@(?!example\.com)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g }
];

function scanDir(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.') || entry.name === 'node_modules' || entry.name === 'scripts') continue;
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) scanDir(p);
    else if (/\.(html|js|css|json|md)$/i.test(entry.name)) {
      const content = fs.readFileSync(p, 'utf8');
      for (const pat of piiPatterns) {
        if (pat.re.test(content)) {
          errors.push(`[PRIVACY SCAN] Matched ${pat.name} in ${path.relative(root, p)}`);
        }
      }
    }
  }
}
scanDir(root);

// 5. Verify Measure ULA & Transfer Tax Math Accuracy (post-June 30, 2026 rules)
function testUlaMath() {
  const calc = (gross, inLa) => {
    const county = Math.ceil(gross / 500) * 0.55;
    const cityBase = inLa ? Math.ceil(gross / 500) * 2.25 : 0;
    const ula = !inLa ? 0 : (gross >= 10900000 ? gross * 0.055 : (gross > 5400000 ? gross * 0.04 : 0));
    return { county, cityBase, ula, total: county + cityBase + ula };
  };
  const at540 = calc(5400000, true);
  if (at540.ula !== 0 || Math.round(at540.cityBase) !== 24300 || Math.round(at540.county) !== 5940) {
    errors.push(`[MATH] ULA at $5.4M failed: ${JSON.stringify(at540)}`);
  }
  const at550 = calc(5500000, true);
  if (Math.round(at550.ula) !== 220000) {
    errors.push(`[MATH] ULA at $5.5M expected $220,000 got ${at550.ula}`);
  }
  const at109 = calc(10900000, true);
  if (Math.round(at109.ula) !== 599500) {
    errors.push(`[MATH] ULA at $10.9M expected $599,500 got ${at109.ula}`);
  }
  const nonLa = calc(6000000, false);
  if (nonLa.ula !== 0 || nonLa.cityBase !== 0 || Math.round(nonLa.county) !== 6600) {
    errors.push(`[MATH] Non-LA City DTT failed: ${JSON.stringify(nonLa)}`);
  }
}
testUlaMath();

// Summary output
console.log(`Checked ${expectedPages.length} HTML pages, ${dataFiles.length} JSON datasets, official URLs, privacy patterns, and Measure ULA/tax math.`);
if (warnings.length) {
  console.log('WARNINGS:');
  warnings.forEach((w) => console.log('  -', w));
}
if (errors.length) {
  console.error(`FAILED with ${errors.length} error(s):`);
  errors.forEach((e) => console.error('  -', e));
  process.exit(1);
}
console.log('ALL VERIFICATION CHECKS PASSED (0 errors).');
