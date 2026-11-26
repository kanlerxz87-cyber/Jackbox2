'use strict';
// The previous suite asserted default tax rates and compared pre-tax hold value
// to after-tax sale proceeds. It is superseded by these tests of the actual
// generated worksheet and its like-for-like adviser-supplied inputs.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'calculator.html'), 'utf8');
const src = fs.readFileSync(path.join(root, 'assets/app.js'), 'utf8');
const generated = fs.readFileSync(path.join(root, 'assets/calc.js'), 'utf8');
assert.equal(generated, src, 'generated calculator must match its reviewed source');
assert.match(html, /<script src="assets\/calc\.js" defer><\/script>/);
assert.doesNotMatch(html, /<form\b/i, 'the worksheet has no submission form');
for (const id of ['sale-price', 'sale-costs', 'debt-payoff', 'sale-tax', 'terminal-equity', 'discount-rate', 'cash-flows', 'long-quote', 'short-quote']) {
  const field = html.match(new RegExp('<(?:input|textarea)\\b[^>]*id="' + id + '"[^>]*>', 'i'));
  assert.ok(field, `missing ${id}`);
  assert.doesNotMatch(field[0], /\b(?:value|name|placeholder)\s*=/i, `${id} must start blank and cannot submit`);
  assert.match(html, new RegExp('<label[^>]+for="' + id + '"', 'i'), `${id} needs a label`);
}
assert.doesNotMatch(src, /\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon|localStorage|sessionStorage|indexedDB)\b|document\s*\.\s*cookie/);
const calc = require('../assets/calc.js');
assert.equal(calc.VERSION, '2.0.0');
const inputs = { salePrice: '1200000', saleCosts: '50000', debtPayoff: '100000', saleTax: '220000', terminalEquity: '800000', discountRate: '10', cashFlows: '50000\n-10000' };
const out = calc.compare(inputs);
assert.equal(out.saleNet, 830000);
assert.ok(Math.abs(out.holdPV - (50000 / 1.1 + 790000 / 1.1 ** 2)) < 1e-7);
assert.ok(Math.abs(out.difference - (out.holdPV - out.saleNet)) < 1e-7);
for (const key of Object.keys(inputs)) assert.throws(() => calc.compare({ ...inputs, [key]: '' }), undefined, `${key} cannot default to zero`);
console.log('Published root worksheet: identical safe engine, blank markup, no submission, and after-tax cash flows verified.');
