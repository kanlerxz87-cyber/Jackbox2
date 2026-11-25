// Version 1.0. No network, storage, tracking or automatic transmission.
(() => {
  const ids = ['salePrice','sellingCosts','debt','saleTax','cash','growth','years','discount','exit'];
  const $ = id => document.getElementById(id);
  const format = value => value.toLocaleString('en-US', {style:'currency', currency:'USD'});
  $('runCalc').addEventListener('click', () => {
    const result = $('result');
    result.textContent = '';
    if (ids.some(id => $(id).value.trim() === '' || !Number.isFinite(Number($(id).value)))) {
      result.textContent = 'All fields are required. Enter zero explicitly where applicable; missing is not zero.'; return;
    }
    const values = Object.fromEntries(ids.map(id => [id, Number($(id).value)]));
    const {salePrice, sellingCosts, debt, saleTax, cash, growth, years, discount, exit} = values;
    if ([salePrice, sellingCosts, debt, saleTax, discount].some(n => n < 0) || growth < -100 || !Number.isInteger(years) || years < 1 || years > 30) {
      result.textContent = 'Check inputs: nonnegative sale amounts and discount rate, growth at least −100%, and whole years from 1 to 30 are required.'; return;
    }
    const sale = salePrice - sellingCosts - debt - saleTax;
    let hold = 0;
    for (let year=1; year<=years; year++) hold += cash * (1 + growth / 100)**(year-1) / (1 + discount / 100)**year;
    hold += exit / (1 + discount / 100)**years;
    if (!Number.isFinite(sale) || !Number.isFinite(hold)) {result.textContent = 'Inputs are too large to calculate reliably.'; return;}
    result.textContent = `Illustrative sale net equity: ${format(sale)}. Illustrative after-tax hold equity PV: ${format(hold)}. Sale minus hold PV: ${format(sale-hold)}. No winner selected: assumptions and tax estimates require review.`;
  });
  $('resetCalc').addEventListener('click', () => { ids.forEach(id => $(id).value = ''); $('result').textContent = ''; });
})();
