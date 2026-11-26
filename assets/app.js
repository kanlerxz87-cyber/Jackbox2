/* Jack in the Box — Central LA decision dashboard
 * Private sell-vs-renew calculator. Runs entirely in the browser.
 * Nothing entered here is transmitted anywhere: no fetch, no XHR, no beacon, no storage.
 *
 * Tax rules implemented (each linked to its official source on the page):
 *   - Federal LTCG tiers 0/15/20% ............ IRS Topic 409 (+ Rev. Proc. 2024-40 thresholds)
 *   - Unrecaptured §1250 gain, max 25% ....... IRS Topic 409
 *   - NIIT 3.8% .............................. IRS Topic 559
 *   - California: no preferential LTCG rate .. CA FTB 540 rate schedules (2024)
 *   - Measure ULA + City base transfer tax ... LA Office of Finance, ULA FAQ
 * Unverified or user-supplied inputs are labelled as such in the output.
 */
(function () {
  'use strict';

  var $ = function (id) { return document.getElementById(id); };

  /* ---------- helpers ---------- */
  function num(id) {
    var el = $(id);
    if (!el) return null;
    var raw = String(el.value == null ? '' : el.value).trim();
    if (raw === '') return null;
    // Accept "6" or "6%" for rate fields, and "1,250,000" for money fields.
    var cleaned = raw.replace(/[,\s$]/g, '');
    var pct = cleaned.slice(-1) === '%';
    if (pct) cleaned = cleaned.slice(0, -1);
    var v = parseFloat(cleaned);
    if (!isFinite(v)) return null;
    if (pct) v = v / 100;
    return v;
  }
  function rate(id) {
    // Rates are typed as percent by humans: "6" means 6%, "0.06" means 0.06%.
    var v = num(id);
    return v === null ? null : v / 100;
  }
  function money(n) {
    if (n === null || !isFinite(n)) return '—';
    var sign = n < 0 ? '-' : '';
    return sign + '$' + Math.abs(Math.round(n)).toLocaleString('en-US');
  }
  function pctTxt(r) {
    if (r === null || !isFinite(r)) return '—';
    return (r * 100).toFixed(2).replace(/\.00$/, '') + '%';
  }
  function row(label, value, cls, note) {
    return '<div class="row"><span>' + label + '</span><span class="' + (cls || '') + '">' +
      value + (note ? ' <span class="muted">' + note + '</span>' : '') + '</span></div>';
  }
  function missing(list) {
    return '<div class="callout danger" style="margin-top:12px"><b>Cannot compute a comparison yet.</b> ' +
      'These required inputs are blank or invalid: <b>' + list.join(', ') + '</b>. ' +
      'Leave unknowns blank rather than guessing — a guessed input produces a confident wrong answer.</div>';
  }

  /* ---------- 2025 federal long-term capital gain brackets ----------
   * Source: IRS Topic 409 (https://www.irs.gov/taxtopics/tc409) for the 0/15/20
   * structure and the $48,350 / $533,400 single / $96,700 / $600,050 joint
   * thresholds for tax year 2025. Those are the figures the IRS publishes for
   * 2025. Other taxable-income amounts are entered by the user, never assumed.
   */
  var LTCG = {
    single:             { z0: 48350,  z15: 533400 },
    marriedJoint:       { z0: 96700,  z15: 600050 },
    marriedSeparate:    { z0: 48350,  z15: 300000 },
    headOfHousehold:    { z0: 64750,  z15: 566700 }
  };

  /* Blended federal LTCG rate for a given amount of gain stacked on top of
   * other taxable income, using the statutory tier boundaries. */
  function blendedLtcgRate(filingStatus, otherTaxableIncome, gain) {
    var b = LTCG[filingStatus] || LTCG.single;
    if (gain <= 0) return 0;
    var start = Math.max(0, otherTaxableIncome);
    var end = start + gain;
    var bands = [
      { from: 0,        to: b.z0,  rate: 0.00 },
      { from: b.z0,     to: b.z15, rate: 0.15 },
      { from: b.z15,    to: Infinity, rate: 0.20 }
    ];
    var tax = 0;
    for (var i = 0; i < bands.length; i++) {
      var lo = Math.max(start, bands[i].from);
      var hi = Math.min(end, bands[i].to);
      if (hi > lo) tax += (hi - lo) * bands[i].rate;
    }
    return tax / gain;
  }
  /* The highest tier the gain reaches — the rate on the last dollar of gain. */
  function marginalLtcgRate(filingStatus, otherTaxableIncome, gain) {
    var b = LTCG[filingStatus] || LTCG.single;
    var top = otherTaxableIncome + Math.max(0, gain || 0);
    if (top <= b.z0) return 0.00;
    if (top <= b.z15) return 0.15;
    return 0.20;
  }

  /* ---------- Measure ULA + City of LA base transfer tax ----------
   * Source: LA Office of Finance, "Real Property Transfer Tax and Measure ULA FAQ"
   * https://finance.lacity.gov/faq/measure-ula
   * Base tax $2.25 per $500 (0.45%), rounded UP to the next $500.
   * ULA: 4% over $5,400,000 and under $10,900,000; 5.5% at $10,900,000 or more
   * (thresholds effective for closings after 30 June 2026).
   * ULA is percentage-based and is NOT rounded to $500.
   * These thresholds are CPI-indexed annually — re-check the FAQ before relying on them.
   */
  var ULA_LOW = 5400000, ULA_HIGH = 10900000;
  function ulaRate(price) {
    if (price == null || price <= 0) return 0;
    if (price >= ULA_HIGH) return 0.055;
    if (price > ULA_LOW) return 0.04;
    return 0;
  }
  function cityLaTransferTax(price, inCityOfLa) {
    if (!inCityOfLa || price == null || price <= 0) return { base: 0, ula: 0, total: 0, rate: 0 };
    var units = Math.ceil(price / 500);
    var base = units * 2.25;
    var ula = price * ulaRate(price);
    return { base: base, ula: ula, total: base + ula, rate: (base + ula) / price };
  }

  /* ---------- core comparison ---------- */
  function calc() {
    var out = $('calc-result');
    if (!out) return;

    var askingRent   = num('c-rent');          // current NNN rent, $/yr
    var escRate      = rate('c-esc');          // annual escalation
    var yearsLeft    = num('c-term');          // years left on lease at decision
    var renewalRent  = num('c-renew-rent');    // negotiated renewal rent, $/yr
    var renewalTerm  = num('c-renew-term');    // years of renewal term
    var capRate      = rate('c-cap');          // exit cap rate on renewal
    var discRate     = rate('c-disc');         // discount rate
    var price        = num('c-price');         // gross sale price today
    var basis        = num('c-basis');         // adjusted basis
    var depTaken     = num('c-dep');           // accumulated depreciation (§1250)
    var sellCosts    = rate('c-costs');        // broker + closing, % of gross
    var otherTaxInc  = num('c-other-inc');     // other taxable income (for LTCG tiering)
    var filing       = ($('c-filing') && $('c-filing').value) || 'single';
    var caRate       = rate('c-ca-rate');      // owner's CA marginal rate (CPA supplied)
    var niitApplies  = $('c-niit') ? $('c-niit').checked : true;
    var inCityOfLa   = $('c-in-ula') ? $('c-in-ula').checked : false;
    var quotes       = num('c-quotes');        // short-lease discount from real broker quotes
    var rentLossMo   = num('c-rent-loss');     // months of lost rent to stress
    var repairCost   = num('c-repair');        // stress repair / TI cost
    var capStressBps = num('c-cap-stress');    // exit cap widening, basis points

    var required = [];
    if (askingRent === null) required.push('current annual NNN rent');
    if (price === null) required.push('gross sale price today');
    if (basis === null) required.push('adjusted basis');
    if (escRate === null) required.push('rent escalation');
    if (yearsLeft === null) required.push('years remaining on lease');
    if (discRate === null) required.push('discount rate');
    if (capRate === null) required.push('exit cap rate');
    if (sellCosts === null) required.push('selling costs');
    if (caRate === null) required.push('California marginal rate (from CPA)');
    if (required.length) { out.innerHTML = missing(required); return; }

    if (yearsLeft <= 0 || yearsLeft > 40) { out.innerHTML = missing(['years remaining on lease (must be 1–40)']); return; }
    if (discRate > 0.5 || capRate > 0.5) { out.innerHTML = missing(['discount rate or cap rate (enter as percent, e.g. 6 for 6%)']); return; }

    depTaken = depTaken === null ? 0 : Math.max(0, depTaken);
    otherTaxInc = otherTaxInc === null ? 0 : Math.max(0, otherTaxInc);
    renewalRent = (renewalRent === null || renewalRent <= 0) ? askingRent : renewalRent;
    renewalTerm = (renewalTerm === null || renewalTerm <= 0) ? 10 : renewalTerm;
    rentLossMo = rentLossMo === null ? 0 : Math.max(0, rentLossMo);
    repairCost = repairCost === null ? 0 : Math.max(0, repairCost);
    capStressBps = capStressBps === null ? 0 : Math.max(0, capStressBps);

    /* ===== SELL TODAY ===== */
    var grossProceeds = price * (1 - sellCosts);
    var gain = Math.max(0, grossProceeds - basis);
    var recapture = Math.min(depTaken, gain);
    var ltcg = Math.max(0, gain - recapture);
    var fedRecap = recapture * 0.25;
    var fedLtcg = ltcg * blendedLtcgRate(filing, otherTaxInc, ltcg);
    var niit = niitApplies ? gain * 0.038 : 0;
    var caTax = gain * caRate;            // CA has no preferential capital-gain rate
    var xfer = cityLaTransferTax(price, inCityOfLa);
    var totalTax = fedRecap + fedLtcg + niit + caTax;
    var sellNet = grossProceeds - totalTax - xfer.total;

    /* ===== HOLD + RENEW (unlevered, pre-income-tax rent stream) =====
     * Rent continues at the current lease through the remaining term, then at
     * the negotiated renewal rent for the renewal term, then exit at cap rate.
     * Rent is shown PRE- income tax: ordinary income tax on rent is an owner
     * -specific input not verified here, and is deliberately excluded rather
     * than guessed. The comparison is therefore biased TOWARD hold. */
    var cashflows = [];
    var t = 0, rent = askingRent, pvRent = 0, totalRent = 0;
    var leaseYears = Math.round(yearsLeft);
    for (var y = 1; y <= leaseYears; y++) {
      t++; pvRent += rent / Math.pow(1 + discRate, t); totalRent += rent;
      cashflows.push({ year: t, rent: rent, phase: 'current lease' });
      rent = rent * (1 + escRate);
    }
    rent = renewalRent;
    for (var k = 1; k <= renewalTerm; k++) {
      t++; pvRent += rent / Math.pow(1 + discRate, t); totalRent += rent;
      cashflows.push({ year: t, rent: rent, phase: 'renewal term' });
      rent = rent * (1 + escRate);
    }
    var exitRent = renewalRent * Math.pow(1 + escRate, renewalTerm - 1);
    var stressedCap = capRate + capStressBps / 10000;
    var exitValue = stressedCap > 0 ? exitRent / stressedCap : 0;
    var pvExit = exitValue / Math.pow(1 + discRate, t);
    var holdNpv = pvRent + pvExit;

    /* ===== STRESS: rent loss + repairs applied inside the hold case ===== */
    var rentLossCost = rentLossMo > 0 ? (askingRent / 12) * rentLossMo : 0;
    var stressDrag = rentLossCost + repairCost;
    var holdStressed = holdNpv - stressDrag;

    /* ===== SHORT-LEASE DISCOUNT (from real quotes) ===== */
    var longLeaseValue = capRate > 0 ? askingRent / capRate : 0;
    var quoteValue = quotes === null ? null : longLeaseValue * (1 - quotes / 100);
    var impliedDiscount = (quotes === null || longLeaseValue <= 0) ? null
      : quotes / 100;

    /* ===== RENDER ===== */
    var gap = holdNpv - sellNet;
    var gapStressed = holdStressed - sellNet;
    var verdict = gap > 0 ? 'Hold/renew leads' : (gap < 0 ? 'Sell leads' : 'Tied');
    var verdictCls = gap > 0 ? 'win' : (gap < 0 ? 'lose' : 'neutral');
    var vStress = gapStressed > 0 ? 'Hold/renew leads' : (gapStressed < 0 ? 'Sell leads' : 'Tied');
    var vStressCls = gapStressed > 0 ? 'win' : (gapStressed < 0 ? 'lose' : 'neutral');

    var html = '';
    html += '<div class="row"><span><b>SELL TODAY — net after tax</b></span><span class="big">' + money(sellNet) + '</span></div>';
    html += row('Gross price', money(price));
    html += row('Less selling costs (' + pctTxt(sellCosts) + ')', '−' + money(price * sellCosts));
    html += row('Taxable gain', money(gain), '', '(proceeds − basis)');
    html += row('  unrecaptured §1250 @ 25%', '−' + money(fedRecap));
    html += row('  long-term capital gain @ ' + pctTxt(ltcg > 0 ? fedLtcg / ltcg : 0) + ' blended',
      '−' + money(fedLtcg), '', ltcg > 0 ? '(top tier ' + pctTxt(marginalLtcgRate(filing, otherTaxInc, ltcg)) + ')' : '');
    html += row('  NIIT 3.8%' + (niitApplies ? '' : ' (off)'), '−' + money(niit));
    html += row('  California @ ' + pctTxt(caRate), '−' + money(caTax));
    if (inCityOfLa) {
      html += row('  LA City transfer tax (base + Measure ULA)', '−' + money(xfer.total),
        '', '(' + pctTxt(xfer.rate) + ' effective)');
    } else {
      html += row('  LA City transfer tax', 'not applied', '', '(parcel marked outside City of LA)');
    }
    html += row('Total tax + transfer tax', '−' + money(totalTax + xfer.total));

    html += '<div class="row" style="margin-top:8px"><span><b>HOLD + RENEW — present value</b></span><span class="big">' + money(holdNpv) + '</span></div>';
    html += row('PV of contract rent, ' + leaseYears + ' yr', money(pvRent),
      '', 'pre-income-tax');
    html += row('Renewal rent', money(renewalRent) + '/yr for ' + renewalTerm + ' yr');
    html += row('Exit value', money(exitValue), '',
      '(' + pctTxt(stressedCap) + ' cap' + (capStressBps > 0 ? ', +' + capStressBps + ' bps stress' : '') + ')');
    html += row('PV of exit', money(pvExit));
    html += row('Undiscounted rent received', money(totalRent));

    html += '<div class="row" style="margin-top:8px"><span><b>STRESSED HOLD</b> <span class="muted">(' +
      rentLossMo + ' mo rent loss + ' + money(repairCost) + ' repairs)</span></span><span class="big">' +
      money(holdStressed) + '</span></div>';
    html += row('Rent-loss drag', '−' + money(rentLossCost));
    html += row('Repair / TI drag', '−' + money(repairCost));

    html += '<div class="row" style="margin-top:8px"><span><b>Gap: hold − sell</b></span>' +
      '<span class="big ' + verdictCls + '">' + money(gap) + ' · ' + verdict + '</span></div>';
    html += '<div class="row"><span><b>Gap under stress</b></span>' +
      '<span class="big ' + vStressCls + '">' + money(gapStressed) + ' · ' + vStress + '</span></div>';

    if (quoteValue === null) {
      html += '<div class="row"><span>Short-lease discount</span><span class="neutral">not priced — no verified broker quotes entered</span></div>';
    } else {
      html += '<div class="row"><span>Value at quoted ' + quotes + '% short-lease discount</span><span>' +
        money(quoteValue) + ' <span class="muted">(long-lease value ' + money(longLeaseValue) + ' at ' + pctTxt(capRate) + ' cap)</span></span></div>';
    }

    html += '<p class="muted" style="margin:12px 0 0">Reading this: the gap is <b>not a recommendation</b>. ' +
      'It shows which case wins on the inputs you entered. Where an input is an assumption rather than a verified ' +
      'document (asking price, cap rate, discount rate, CA rate), the answer is only as good as that assumption — ' +
      'check each one against the Flagged for Review list before any commitment. Rent is shown pre-income-tax, ' +
      'which flatters the hold case; the sell case already carries full tax. A comparison is only final when a CPA ' +
      'has supplied basis, depreciation and the California rate, and at least two brokers have quoted the short-lease ' +
      'discount in writing.</p>';

    if (verdict === 'Sell leads' && vStress === 'Sell leads') {
      html += '<div class="callout ok" style="margin-top:12px"><b>Direction:</b> on these inputs the after-tax sale ' +
        'beats both the base and stressed hold case. That is still a sensitivity result, not a green light — it becomes ' +
        'actionable only once the lease abstract, CPA run and broker quotes are attached.</div>';
    } else if (verdict === 'Hold/renew leads' && vStress === 'Hold/renew leads') {
      html += '<div class="callout info" style="margin-top:12px"><b>Direction:</b> on these inputs holding and renewing ' +
        'beats selling after tax, even under stress. Note that rent here is pre-income-tax, so verify with a CPA before ' +
        'treating the hold case as superior.</div>';
    } else {
      html += '<div class="callout" style="margin-top:12px"><b>Direction flips under stress.</b> The base and stressed ' +
        'cases disagree, which means the decision hinges on hazard and vacancy assumptions rather than on price. ' +
        'Resolve the stress inputs before choosing.</div>';
    }

    out.innerHTML = html;
  }

  function reset() {
    var form = $('calc-form');
    if (form) form.reset();
    var out = $('calc-result');
    if (out) out.innerHTML = '<p class="muted">Inputs cleared. Enter verified documents only.</p>';
  }

  /* Print the comparison the reader actually built. */
  function printResult() {
    var out = $('calc-result');
    if (!out || !out.textContent.trim()) return;
    window.print();
  }

  /* Export the comparison as a local file (nothing is uploaded). */
  function exportResult() {
    var out = $('calc-result');
    if (!out) return;
    var lines = ['Jack in the Box — Central LA — sell vs hold comparison',
      'Generated locally in the browser on ' + new Date().toISOString().slice(0, 10),
      'ANONYMOUS WORKING COPY — no parcel, owner or lease identifiers', ''];
    var rows = out.querySelectorAll('.row');
    for (var i = 0; i < rows.length; i++) {
      lines.push(rows[i].textContent.replace(/\s+/g, ' ').trim());
    }
    lines.push('', 'Tax rules: IRS Topic 409 (LTCG 0/15/20, §1250 max 25%), IRS Topic 559 (NIIT 3.8%),',
      'CA FTB 540 schedules (no preferential capital-gain rate), LA Office of Finance ULA FAQ',
      '(4% over $5.4M, 5.5% at/above $10.9M, base 0.45%). Verify all rates before relying on this.');
    var blob = new Blob([lines.join('\n')], { type: 'text/plain' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'jackbox-sell-vs-hold-anonymous.txt';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  }

  function init() {
    var form = $('calc-form');
    if (form) {
      form.addEventListener('submit', function (e) { e.preventDefault(); calc(); });
      form.addEventListener('input', calc);
      form.addEventListener('change', calc);
      var b = $('calc-run'); if (b) b.addEventListener('click', function (e) { e.preventDefault(); calc(); });
      var r = $('calc-reset'); if (r) r.addEventListener('click', function (e) { e.preventDefault(); reset(); });
      var x = $('calc-export'); if (x) x.addEventListener('click', function (e) { e.preventDefault(); exportResult(); });
      var p = $('calc-print'); if (p) p.addEventListener('click', function (e) { e.preventDefault(); printResult(); });
      calc();
    }
    // Print buttons anywhere on the site.
    var btns = document.querySelectorAll('[data-print]');
    for (var i = 0; i < btns.length; i++) {
      btns[i].addEventListener('click', function (e) { e.preventDefault(); window.print(); });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }

  // Exposed for the test harness only.
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { blendedLtcgRate: blendedLtcgRate, ulaRate: ulaRate, cityLaTransferTax: cityLaTransferTax };
  }
})();
