const assert = require('node:assert/strict');

const ids = [
  'in-rent', 'in-esc', 'in-years', 'in-disc', 'in-price', 'in-basis', 'in-dep',
  'in-cap', 'in-renewal', 'in-costs', 'in-t15', 'in-t25', 'in-niit', 'in-ca',
  'in-ord', 'in-shortdisc', 'calc-result', 'calc-form'
];

const values = {
  'in-rent': '200000',
  'in-esc': '0',
  'in-years': '1',
  'in-disc': '0',
  'in-price': '4000000',
  'in-basis': '1000000',
  'in-dep': '500000',
  'in-cap': '0.05',
  'in-renewal': '200000',
  'in-costs': '0.05',
  'in-t15': '0.20',
  'in-t25': '0.25',
  'in-niit': '0.038',
  'in-ca': '0.10',
  'in-ord': '0.25',
  'in-shortdisc': '0.10'
};

const listeners = {};
const elements = Object.fromEntries(ids.map((id) => [
  id,
  {
    value: values[id] ?? '',
    innerHTML: '',
    addEventListener(ev, fn) { listeners[id + ':' + ev] = fn; }
  }
]));

global.document = {
  getElementById: (id) => elements[id],
  addEventListener: (ev, fn) => { listeners['doc:' + ev] = fn; }
};

require('../assets/app.js');
listeners['doc:DOMContentLoaded']();

const out = elements['calc-result'].innerHTML;
// Hold (1y, 0% disc, 25% ord tax, 5% exit cost on 4,000,000 terminal = 3,800,000 + 150,000 rent = 3,950,000)
assert.match(out, /\$3,950,000/);
// Sell: 4,000,000 * 0.95 = 3,800,000 amount realized; gain = 2,800,000; recapture = 500,000 * 0.25 = 125,000;
// ltcg = 2,300,000 * 0.20 = 460,000; niit = 2,800,000 * 0.038 = 106,400; ca = 2,800,000 * 0.10 = 280,000;
// total tax = 971,400; sellNet = 3,800,000 - 971,400 = 2,828,600.
assert.match(out, /\$2,828,600/);
assert.match(out, /\$1,121,400/);
console.log('Root calculator after-tax & IRC 1001 arithmetic: OK');
