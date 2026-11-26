'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const model = require('../assets/app.js');

const valid = {
  salePrice: '1000000', saleCosts: '60000', debtPayoff: '100000', saleTax: '200000',
  terminalEquity: '800000', discountRate: '10', cashFlows: '50000\n-20000\n30000'
};
const result = model.compare(valid);
const expectedHold = 50000 / 1.1 - 20000 / 1.1 ** 2 + (30000 + 800000) / 1.1 ** 3;
assert.equal(result.saleNet, 640000);
assert.ok(Math.abs(result.holdPV - expectedHold) < 1e-7);
assert.ok(Math.abs(result.difference - (expectedHold - 640000)) < 1e-7);
assert.equal(result.years, 3);
assert.equal(model.compare({ ...valid, discountRate: '0', cashFlows: '0\n-10', terminalEquity: '0' }).holdPV, -10);
assert.equal(model.compare({ ...valid, saleTax: '-100', debtPayoff: '0' }).saleNet, 940100);
for (const field of ['salePrice', 'saleCosts', 'debtPayoff', 'saleTax', 'terminalEquity', 'discountRate', 'cashFlows']) {
  assert.throws(() => model.compare({ ...valid, [field]: '' }), undefined, `${field} must not default to zero`);
}
assert.throws(() => model.compare({ ...valid, cashFlows: '1\n\n2' }));
assert.throws(() => model.compare({ ...valid, cashFlows: '1,000' }));
assert.throws(() => model.compare({ ...valid, cashFlows: Array(31).fill('1').join('\n') }));
assert.throws(() => model.compare({ ...valid, salePrice: 'Infinity' }));
assert.throws(() => model.compare({ ...valid, saleCosts: '-1' }));
assert.throws(() => model.compare({ ...valid, debtPayoff: '-1' }));
assert.throws(() => model.compare({ ...valid, discountRate: '-100' }));
assert.throws(() => model.compare({ ...valid, discountRate: '1001' }));
const discountedQuote = model.quoteDiscount({ longQuote: '100', shortQuote: '90' });
assert.ok(Math.abs(discountedQuote.percent - 10) < 1e-10);
assert.equal(discountedQuote.difference, 10);
assert.equal(model.quoteDiscount({ longQuote: '100', shortQuote: '110' }).difference, -10);
assert.throws(() => model.quoteDiscount({ longQuote: '', shortQuote: '90' }));
assert.throws(() => model.quoteDiscount({ longQuote: '0', shortQuote: '90' }));

const code = fs.readFileSync(require.resolve('../assets/app.js'), 'utf8');
assert.doesNotMatch(code, /\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon|localStorage|sessionStorage|indexedDB)\b|document\s*\.\s*cookie/);

// Minimal browser harness exercises blank state, live updates, quote module and pagehide clearing.
class Element {
  constructor() { this.value = ''; this.children = []; this.events = {}; this._text = ''; this.className = ''; }
  set textContent(v) { this._text = String(v); this.children = []; }
  get textContent() { return this._text + this.children.map((c) => c.textContent).join(''); }
  appendChild(child) { this.children.push(child); return child; }
  replaceChildren() { this.children = []; this._text = ''; }
  addEventListener(type, fn) { this.events[type] = fn; }
  fire(type) { this.events[type]?.(); }
}
const ids = ['sale-price', 'sale-costs', 'debt-payoff', 'sale-tax', 'terminal-equity', 'discount-rate', 'cash-flows', 'long-quote', 'short-quote', 'comparison-output', 'quote-output', 'clear-worksheet'];
const elements = Object.fromEntries(ids.map((id) => [id, new Element()]));
const document = {
  readyState: 'complete', getElementById: (id) => elements[id] || null,
  createElement: () => new Element(), createTextNode: (text) => { const e = new Element(); e.textContent = text; return e; }
};
const events = {};
const window = { document, addEventListener: (type, fn) => { events[type] = fn; } };
vm.runInNewContext(code, { window, Intl, Number, Math });
assert.match(elements['comparison-output'].textContent, /Not calculated/);
assert.match(elements['quote-output'].textContent, /Not calculated/);
const mapping = { 'sale-price': 'salePrice', 'sale-costs': 'saleCosts', 'debt-payoff': 'debtPayoff', 'sale-tax': 'saleTax', 'terminal-equity': 'terminalEquity', 'discount-rate': 'discountRate', 'cash-flows': 'cashFlows' };
for (const [id, key] of Object.entries(mapping)) elements[id].value = valid[key];
elements['sale-price'].fire('input');
assert.match(elements['comparison-output'].textContent, /\$640,000/);
assert.match(elements['comparison-output'].textContent, /not a tax calculation/i);
elements['long-quote'].value = '100'; elements['short-quote'].value = '90';
elements['short-quote'].fire('input');
assert.match(elements['quote-output'].textContent, /10\.00%/);
events.pagehide();
assert.equal(elements['sale-price'].value, '');
assert.equal(elements['short-quote'].value, '');
assert.match(elements['comparison-output'].textContent, /Not calculated/);
console.log('Root worksheet: like-for-like arithmetic, incomplete inputs, quotes, privacy and browser behavior passed.');
