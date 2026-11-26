// Unit tests for the root dashboard's calculator engine (assets/app.js).
// Verifies the tax rules the page cites, so a later edit cannot silently break them.
// Run from the repository root: node tests/calc_root.test.js
const assert = require('node:assert/strict');

global.document = {
  readyState: 'complete',
  addEventListener() {},
  getElementById() { return null; },
  querySelectorAll() { return []; }
};
global.window = { print() {}, addEventListener() {} };

const m = require('../assets/app.js');

/* ---- Federal long-term capital gain tiers (IRS Topic 409, 2025) ---- */
// Gain wholly inside the 0% band.
assert.equal(m.blendedLtcgRate('single', 0, 40000), 0);
// Single filer: 0% to $48,350, 15% to $533,400. A $100,000 gain from zero income
// spans both bands, so the blended rate must be (51,650 * 15%) / 100,000.
assert.ok(Math.abs(m.blendedLtcgRate('single', 0, 100000) - (51650 * 0.15) / 100000) < 1e-12);
// Gain wholly inside the 15% band.
assert.equal(m.blendedLtcgRate('single', 200000, 100000), 0.15);
// Gain straddling the 15%/20% boundary at $533,400.
assert.ok(Math.abs(m.blendedLtcgRate('single', 500000, 100000) - (33400 * 0.15 + 66600 * 0.20) / 100000) < 1e-12);
// Married filing jointly has wider bands: a $50,000 gain stays in the 0% band.
assert.equal(m.blendedLtcgRate('marriedJoint', 0, 50000), 0);
// Income already above the top band means the whole gain is at 20%.
assert.equal(m.blendedLtcgRate('single', 700000, 1000), 0.20);
// A zero gain must not divide by zero.
assert.equal(m.blendedLtcgRate('single', 0, 0), 0);

/* ---- Measure ULA (LA Office of Finance, closings after 30 Jun 2026) ---- */
// 4% applies to "over $5,400,000": exactly at the threshold is not over it.
assert.equal(m.ulaRate(5000000), 0);
assert.equal(m.ulaRate(5400000), 0);
assert.equal(m.ulaRate(5400001), 0.04);
assert.equal(m.ulaRate(10899999), 0.04);
// 5.5% applies "at $10,900,000 or more".
assert.equal(m.ulaRate(10900000), 0.055);
assert.equal(m.ulaRate(20000000), 0.055);
// No price, no tax.
assert.equal(m.ulaRate(0), 0);
assert.equal(m.ulaRate(null), 0);

/* ---- City of Los Angeles real property transfer tax ---- */
// Base tax is $2.25 per $500 of value, with the value rounded UP to the next $500.
let t = m.cityLaTransferTax(1000000, true);
assert.equal(t.base, 2000 * 2.25);
assert.equal(t.ula, 0);
assert.equal(t.total, t.base);

t = m.cityLaTransferTax(500001, true);
assert.equal(t.base, 1001 * 2.25);          // rounded up, not 1000

t = m.cityLaTransferTax(6000000, true);
assert.equal(t.base, 12000 * 2.25);
assert.equal(Math.round(t.ula), 240000);    // 4% of gross, not of gain

t = m.cityLaTransferTax(11000000, true);
assert.equal(Math.round(t.ula), 605000);    // 5.5% of gross

// Outside the City of Los Angeles, neither the base tax nor ULA applies.
t = m.cityLaTransferTax(6000000, false);
assert.equal(t.total, 0);
assert.equal(t.rate, 0);

// The effective rate the page displays must equal total / price.
t = m.cityLaTransferTax(9000000, true);
assert.ok(Math.abs(t.rate - t.total / 9000000) < 1e-12);

/* ---- The calculator must stay offline and stateless ---- */
const fs = require('fs');
const src = fs.readFileSync(require.resolve('../assets/app.js'), 'utf8');
for (const banned of ['XMLHttpRequest', 'localStorage', 'sessionStorage', 'indexedDB',
                      'document.cookie', 'sendBeacon']) {
  assert.ok(!src.includes(banned), `assets/app.js must not use ${banned}`);
}
assert.ok(!/\bfetch\s*\(/.test(src), 'assets/app.js must not call fetch()');

console.log('Root calculator engine: tax tiers, Measure ULA thresholds, transfer-tax rounding, '
            + 'and offline/stateless behaviour all verified.');
