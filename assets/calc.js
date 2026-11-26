/*
 * Anonymous adviser worksheet, version 2.0.0 (2026-11-26).
 * Deliberately no network, storage, tax-rate defaults, automatic rankings or
 * parcel identifiers. Outputs are arithmetic on adviser-supplied inputs only.
 */
(function (root) {
  'use strict';

  const VERSION = '2.0.0';
  const MAX_AMOUNT = 1e12;

  function amount(raw, label, options) {
    const limits = options || {};
    if (raw === undefined || raw === null || String(raw).trim() === '') {
      throw new Error(label + ' is required; blank is not zero.');
    }
    const text = String(raw).trim();
    if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(text)) {
      throw new Error(label + ' must be a plain number without commas.');
    }
    const n = Number(text);
    if (!Number.isFinite(n) || Math.abs(n) > MAX_AMOUNT) {
      throw new Error(label + ' is outside the supported range.');
    }
    if (limits.nonnegative && n < 0) throw new Error(label + ' cannot be negative.');
    if (limits.positive && n <= 0) throw new Error(label + ' must be greater than zero.');
    return n;
  }

  function annualFlows(raw) {
    if (typeof raw !== 'string' || raw.trim() === '') {
      throw new Error('Enter a verified after-tax cash flow for every year.');
    }
    const rows = raw.trim().split(/\r?\n/);
    if (rows.length > 30) throw new Error('The worksheet supports at most 30 years.');
    return rows.map((row, index) => amount(row, 'Year ' + (index + 1) + ' cash flow'));
  }

  function compare(inputs) {
    const salePrice = amount(inputs.salePrice, 'Sale price', { positive: true });
    const costs = amount(inputs.saleCosts, 'Sale costs', { nonnegative: true });
    const debt = amount(inputs.debtPayoff, 'Debt payoff', { nonnegative: true });
    // A negative amount is allowed only when a tax professional has supported
    // an incremental benefit. Tax is not computed by this worksheet.
    const tax = amount(inputs.saleTax, 'Incremental sale tax');
    const terminal = amount(inputs.terminalEquity, 'Terminal after-tax equity');
    const discount = amount(inputs.discountRate, 'Annual discount rate');
    if (discount <= -100 || discount > 1000) {
      throw new Error('Annual discount rate must be above -100% and no more than 1000%.');
    }
    const flows = annualFlows(inputs.cashFlows);
    const factor = 1 + discount / 100;
    let holdPV = 0;
    for (let i = 0; i < flows.length; i += 1) {
      holdPV += flows[i] / Math.pow(factor, i + 1);
    }
    holdPV += terminal / Math.pow(factor, flows.length);
    const saleNet = salePrice - costs - debt - tax;
    if (![holdPV, saleNet, holdPV - saleNet].every(Number.isFinite)) {
      throw new Error('The result exceeds the supported numerical range.');
    }
    return { saleNet, holdPV, difference: holdPV - saleNet, years: flows.length };
  }

  function quoteDiscount(inputs) {
    const long = amount(inputs.longQuote, 'Extended-lease quote', { positive: true });
    const short = amount(inputs.shortQuote, 'Short-lease quote', { positive: true });
    const percent = (1 - short / long) * 100;
    if (!Number.isFinite(percent)) throw new Error('Quote difference exceeds the supported range.');
    return { percent, difference: long - short };
  }

  const api = { VERSION, compare, quoteDiscount, annualFlows };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (!root || !root.document) return;

  const doc = root.document;
  const $ = (id) => doc.getElementById(id);
  const money = (v) => new Intl.NumberFormat('en-US', {
    style: 'currency', currency: 'USD', maximumFractionDigits: 0
  }).format(v);
  const fields = ['sale-price', 'sale-costs', 'debt-payoff', 'sale-tax',
    'terminal-equity', 'discount-rate', 'cash-flows'];
  const quoteFields = ['long-quote', 'short-quote'];

  function resultLine(label, value) {
    const p = doc.createElement('p');
    const strong = doc.createElement('strong');
    strong.textContent = label + ' ';
    p.appendChild(strong);
    p.appendChild(doc.createTextNode(value));
    return p;
  }

  function updateComparison() {
    const output = $('comparison-output');
    if (!output) return;
    output.replaceChildren();
    try {
      const result = compare({
        salePrice: $('sale-price').value,
        saleCosts: $('sale-costs').value,
        debtPayoff: $('debt-payoff').value,
        saleTax: $('sale-tax').value,
        terminalEquity: $('terminal-equity').value,
        discountRate: $('discount-rate').value,
        cashFlows: $('cash-flows').value
      });
      output.appendChild(resultLine('Sale proceeds today:', money(result.saleNet)));
      output.appendChild(resultLine('Hold present value:', money(result.holdPV)));
      output.appendChild(resultLine('Difference (hold minus sale):', money(result.difference)));
      const note = doc.createElement('p');
      note.className = 'result-note';
      note.textContent = result.years + '-year illustration; not a tax calculation, appraisal, forecast, or recommendation. Both paths must use consistent after-tax equity assumptions.';
      output.appendChild(note);
    } catch (error) {
      output.appendChild(resultLine('Not calculated.', error.message));
    }
  }

  function updateQuote() {
    const output = $('quote-output');
    if (!output) return;
    output.replaceChildren();
    try {
      const result = quoteDiscount({ longQuote: $('long-quote').value, shortQuote: $('short-quote').value });
      const label = result.percent < 0 ? 'Short-lease premium:' : 'Short-lease discount:';
      output.appendChild(resultLine(label, Math.abs(result.percent).toFixed(2) + '% (' + money(Math.abs(result.difference)) + ')'));
      const note = doc.createElement('p');
      note.className = 'result-note';
      note.textContent = 'A paired quote comparison, not an independently verified market discount. Keep other terms consistent and review actual offers.';
      output.appendChild(note);
    } catch (error) {
      output.appendChild(resultLine('Not calculated.', error.message));
    }
  }

  function clearAll() {
    fields.concat(quoteFields).forEach((id) => { const el = $(id); if (el) el.value = ''; });
    updateComparison();
    updateQuote();
  }

  function init() {
    fields.forEach((id) => { const el = $(id); if (el) el.addEventListener('input', updateComparison); });
    quoteFields.forEach((id) => { const el = $(id); if (el) el.addEventListener('input', updateQuote); });
    const clear = $('clear-worksheet');
    if (clear) clear.addEventListener('click', clearAll);
    updateComparison();
    updateQuote();
  }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', init);
  else init();
  root.addEventListener('pagehide', clearAll);
})(typeof window === 'undefined' ? null : window);
