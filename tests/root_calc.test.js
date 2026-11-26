'use strict';
// Regression coverage for the superseded legacy root calculator: the supported
// replacement cannot silently invent inputs or apply a universal tax rate.
const assert = require('node:assert/strict');
const calc = require('../assets/app.js');
const valid = { salePrice: '100', saleCosts: '0', debtPayoff: '0', saleTax: '0', terminalEquity: '0', discountRate: '0', cashFlows: '0' };
assert.equal(calc.compare(valid).saleNet, 100);
assert.equal(calc.compare(valid).holdPV, 0);
assert.equal(calc.compare({ ...valid, saleTax: '25' }).saleNet, 75);
assert.equal(calc.compare({ ...valid, terminalEquity: '-20', cashFlows: '-10' }).holdPV, -30);
assert.throws(() => calc.compare({ ...valid, saleTax: '' }), /required/);
assert.throws(() => calc.compare({ ...valid, cashFlows: '0\n\n0' }), /required/);
assert.throws(() => calc.compare({ ...valid, discountRate: '-100' }), /discount rate/i);
assert.ok(Math.abs(calc.quoteDiscount({ longQuote: '200', shortQuote: '180' }).percent - 10) < 1e-10);
assert.ok(calc.quoteDiscount({ longQuote: '200', shortQuote: '220' }).percent < 0);
console.log('Root worksheet regression: no assumed rates, explicit zeros and negative cash-flow handling passed.');
