'use strict';
const form = document.querySelector('#calc');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  const fields = ['price', 'costs', 'debt', 'tax', 'hold'];
  const vals = fields.map(id => document.getElementById(id).value.trim());
  const out = document.querySelector('#result');
  if (vals.some(v => v === '' || !Number.isFinite(Number(v)) || Number(v) < 0)) {
    out.textContent = 'All five non-negative amounts are required. No estimate has been calculated.'; return;
  }
  const [price,costs,debt,tax,hold] = vals.map(Number);
  const proceeds = price-costs-debt-tax;
  const fmt = n => new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(n);
  out.textContent = `Illustrative net sale cash: ${fmt(proceeds)}. Difference versus supplied hold present value: ${fmt(proceeds-hold)}. This is not a valuation or a tax calculation.`;
});
