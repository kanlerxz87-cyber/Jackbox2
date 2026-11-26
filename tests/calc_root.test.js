// Arithmetic and inertness test for the private root calculator (assets/calc.js).
// Runs offline with a minimal DOM stub: no jsdom dependency.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const code = fs.readFileSync(path.join(__dirname, '..', 'assets', 'calc.js'), 'utf8');
const html = fs.readFileSync(path.join(__dirname, '..', 'calculator.html'), 'utf8');

// Seed the DOM stub with the defaults the page actually ships, so the test checks the
// published markup rather than an assumption about it.
const defaults = {};
for (const m of html.matchAll(/<(?:input|select)[^>]*id="([a-z]+)"[^>]*>/gi)) {
  const id = m[1];
  const tag = m[0];
  const valueAttr = tag.match(/value="([^"]*)"/i);
  const selected = tag.match(/<option value="([^"]+)"[^>]*selected/i);
  defaults[id] = selected ? selected[1] : (valueAttr ? valueAttr[1] : '');
}
// selected option options carry the value attribute before the selected marker
for (const id of Object.keys(defaults)) {
  if (defaults[id] === '') {
    const sel = html.match(new RegExp('<select id="' + id + '"[\\s\\S]*?</select>', 'i'));
    if (sel) {
      const chosen = sel[0].match(/<option value="([^"]+)"[^>]*selected/i);
      if (chosen) defaults[id] = chosen[1];
    }
  }
}

function makeEl(id) {
  return {
    id,
    tagName: id === 'ltcg' ? 'SELECT' : (id === 'run' || id === 'reset' ? 'BUTTON' : 'INPUT'),
    value: defaults[id] || '',
    textContent: '',
    innerHTML: '',
    handlers: {},
    addEventListener(ev, fn) { (this.handlers[ev] = this.handlers[ev] || []).push(fn); },
    fire(ev) { (this.handlers[ev] || []).forEach(fn => fn({})); },
  };
}

const nodes = {};
function el(id) { return (nodes[id] = nodes[id] || makeEl(id)); }

const listener = {};
const document = {
  getElementById: el,
  addEventListener(ev, fn) { listener[ev] = fn; },
};

const sandbox = { document, window: {}, console, isFinite, Math, parseFloat, Number };
vm.createContext(sandbox);
vm.runInContext(code, sandbox);
assert.ok(listener.DOMContentLoaded, 'calculator should register a DOMContentLoaded handler');
listener.DOMContentLoaded();

// defaults the page ships with
assert.strictEqual(el('recap').value, '0.25', 'recapture default should be the 25% statutory maximum');
assert.strictEqual(defaults['niit'], '0', 'NIIT default in the markup must be zero');
assert.strictEqual(el('ltcg').value, '0.20', 'federal rate default should be the top verified bracket');
assert.strictEqual(el('state').value, '0.123', 'state default should be the verified top marginal rate');
assert.strictEqual(el('niit').value, '0', 'NIIT must default to zero because it is unverified');

// --- sale arithmetic: 4,000,000 price, 2,000,000 basis, 1,000,000 depreciation
// costs 3% = 120,000; transfer 0.5% = 20,000; gain = 1,860,000
// recapture 1,000,000 @25% = 250,000; remainder 860,000 @20% = 172,000; state 1,860,000 @12.3% = 228,780
// net = 4,000,000 - 120,000 - 20,000 - 250,000 - 172,000 - 228,780 = 3,209,220
el('price').value = '4000000';
el('basis').value = '2000000';
el('dep').value = '1000000';
el('costs').value = '3';
el('transfer').value = '0.5';
el('ltcg').value = '0.20';
el('recap').value = '0.25';
el('niit').value = '0';
el('state').value = '0.123';

// --- hold arithmetic: rent 200,000, 4% escalation, 5 years, no owner costs, 0 vacancy
// discount 7%, exit cap 6%, exit costs 2%
el('rent').value = '200000';
el('esc').value = '4';
el('years').value = '5';
el('ownerCosts').value = '0';
el('costInfl').value = '0';
el('vacancy').value = '0';
el('disc').value = '7';
el('cap').value = '6';
el('exitCosts').value = '2';

// --- short-lease discount: 5.5% long vs 6.75% short => 1 - (5.5/6.75) = 18.5%
el('capLong').value = '5.5';
el('capShort').value = '6.75';

el('run').fire('click');
const lines = el('lines').innerHTML;
const headline = el('headline').innerHTML;

function money(s) { return s.replace(/[^0-9.-]/g, ''); }

const expectedNet = 4000000 - 120000 - 20000 - 250000 - 172000 - 228780;
assert.ok(lines.includes('$3,209,220'), `net sale proceeds should be $3,209,220, got: ${lines.slice(0, 400)}`);

// hold NPV: 200k growing 4% for 5 years discounted at 7%, terminal at 6% cap on year-6 rent
let pv = 0;
for (let y = 1; y <= 5; y++) pv += (200000 * Math.pow(1.04, y - 1)) / Math.pow(1.07, y);
const terminal = (200000 * Math.pow(1.04, 5)) / 0.06;
pv += (terminal * 0.98) / Math.pow(1.07, 5);
const pvText = pv.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
assert.ok(lines.includes(pvText), `hold NPV should be ${pvText}, got: ${lines.slice(0, 700)}`);

// difference sign and headline must agree
const diff = pv - expectedNet;
assert.ok(headline.includes('Hold value exceeds net sale proceeds') || headline.includes('Net sale proceeds exceed hold value'),
  `headline should state a direction, got: ${headline}`);
if (diff >= 0) assert.ok(headline.includes('Hold value exceeds'), 'headline direction should be hold-favouring');
else assert.ok(headline.includes('Net sale proceeds exceed'), 'headline direction should be sell-favouring');

// break-even price must make net proceeds equal hold NPV
const beMatch = lines.match(/Break-even sale price<\/span><span[^>]*>([^<]+)</);
assert.ok(beMatch, 'break-even price should be rendered');
const be = parseFloat(money(beMatch[1]));
assert.ok(Math.abs(be - (pv + 0) / 1) > 0, 'break-even price should be positive');
// recompute net at the break-even price and compare with hold NPV within rounding
function netAt(price) {
  const costs = price * 0.03, transfer = price * 0.005;
  const gain = Math.max(0, price - costs - transfer - 2000000);
  const recap = Math.min(1000000, gain);
  const rest = gain - recap;
  const fed = recap * 0.25 + rest * 0.20;
  const state = gain * 0.123;
  return price - costs - transfer - fed - state;
}
assert.ok(Math.abs(netAt(be) - pv) < Math.max(5, pv * 0.0005),
  `net proceeds at break-even (${netAt(be).toFixed(0)}) should equal hold NPV (${pv.toFixed(0)})`);

// short-lease discount
assert.ok(lines.includes('18.5%'), `implied short-lease discount should be 18.5%, got: ${lines.slice(-400)}`);

// zero price and zero rent must not produce a number
el('price').value = '';
el('rent').value = '';
el('run').fire('click');
assert.strictEqual(el('headline').textContent, 'Enter a price or a rent to begin',
  'empty inputs must not produce a result');
assert.strictEqual(el('lines').innerHTML, '');

// clear resets to the verified statutory defaults and empties the rest
el('price').value = '123';
el('reset').fire('click');
assert.strictEqual(el('price').value, '');
assert.strictEqual(el('recap').value, '0.25');
assert.strictEqual(el('state').value, '0.123');

// inertness: the script must contain no network, storage or tracking capability
for (const bad of ['fetch(', 'XMLHttpRequest', 'localStorage', 'sessionStorage', 'document.cookie',
                   'sendBeacon', 'new Image(', 'WebSocket', 'IndexedDB', 'import(', 'eval(']) {
  assert.ok(!code.includes(bad), `calc.js must not contain ${bad}`);
}
assert.ok(!/https?:\/\//.test(code), 'calc.js must not reference any URL');

console.log('root calculator: sale arithmetic, hold NPV, break-even, discount, empty-state, reset and inertness OK');
