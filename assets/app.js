'use strict';
const form = document.querySelector('#calculator');
if (form) {
  const results = document.querySelector('#results');
  const box = document.querySelector('.result-box');
  const heading = box.querySelector('h3');
  const description = box.querySelector('p');
  const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const values = Object.fromEntries(new FormData(form).entries());
    if (Object.values(values).some(v => v.trim() === '' || !Number.isFinite(Number(v)))) return;
    const price = Number(values.price), cost = Number(values.cost), debt = Number(values.debt), tax = Number(values.tax);
    const cash = Number(values.cash), terminal = Number(values.terminal), years = Number(values.years), rate = Number(values.rate) / 100;
    if (!Number.isInteger(years) || years < 1 || years > 50 || rate < 0 || rate > 1 || [price,cost,debt,tax].some(v => v < 0)) return;
    const sale = price - cost - debt - tax;
    let hold = terminal / Math.pow(1 + rate, years);
    for (let year = 1; year <= years; year++) hold += cash / Math.pow(1 + rate, year);
    if (![sale,hold].every(Number.isFinite)) { heading.textContent = 'Values out of range'; results.textContent = ''; return; }
    heading.textContent = 'Illustrative comparison';
    description.textContent = 'Based solely on the inputs entered; not a recommendation.';
    results.replaceChildren();
    [['Sale net cash today', sale], ['Hold present value', hold], ['Hold minus sale', hold - sale]].forEach(([label, amount]) => {
      const row = document.createElement('div'); row.className = 'result-row';
      row.append(document.createTextNode(label)); const value = document.createElement('strong'); value.textContent = currency.format(amount); row.append(value); results.append(row);
    });
  });
  form.addEventListener('reset', () => { results.replaceChildren(); heading.textContent = 'Awaiting verified inputs'; description.textContent = 'Results appear here only. No data is stored.'; });
}
