// Private browser-only sell-vs-hold calculator. No data leaves the device.
// All tax parameters default to IRS Topic 409 (2025) and are user-editable.
(function(){
  const $ = id => document.getElementById(id);
  function num(id, def){ const v = parseFloat($(id)?.value); return isFinite(v) ? v : def; }
  function money(n){ return n.toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}); }
  function calc(){
    const rent = num('in-rent', 0);           // current annual NNN rent
    const esc = num('in-esc', 0.02);          // annual rent escalation
    const years = Math.max(1, Math.min(30, Math.round(num('in-years', 10))));
    const disc = num('in-disc', 0.06);        // discount rate
    const price = num('in-price', 0);         // gross sale price today
    const basis = num('in-basis', 0);         // adjusted basis
    const dep = num('in-dep', 0);             // unrecaptured §1250 gain
    const capRate = num('in-cap', 0.06);      // cap rate for renewal value
    const renewalRent = num('in-renewal', rent); // negotiated renewal rent
    const costs = num('in-costs', 0.03);      // selling costs % of price
    const ltcgRate = num('in-t15', 0.15), t25 = num('in-t25', 0.25);
    const niit = num('in-niit', 0.038), ca = num('in-ca', 0.093);
    const otherOrd = num('in-ord', 0.24);     // combined ordinary rate on rental income (illustrative)

    // HOLD: Pre-tax and after-tax NPV of escalating NNN rent + net terminal value at cap rate
    let holdPreTaxNPV = 0;
    let holdAfterTaxNPV = 0;
    for(let y=1;y<=years;y++){
      const rY = rent * Math.pow(1+esc, y-1);
      const df = Math.pow(1+disc, y);
      holdPreTaxNPV += rY / df;
      holdAfterTaxNPV += (rY * (1 - otherOrd)) / df;
    }
    const terminalRent = renewalRent * Math.pow(1+esc, years-1);
    const terminalGross = capRate > 0 ? terminalRent / capRate : 0;
    const terminalNetOfCosts = terminalGross * (1 - costs);
    holdPreTaxNPV += terminalGross / Math.pow(1+disc, years);
    holdAfterTaxNPV += terminalNetOfCosts / Math.pow(1+disc, years);

    // SELL NOW: IRC §1001 amount realized (gross price minus selling costs) and after-tax proceeds
    const amountRealized = Math.max(0, price * (1 - costs));
    const grossGain = Math.max(0, amountRealized - basis);
    const recapture = Math.min(dep, grossGain);
    const ltcg = Math.max(0, grossGain - recapture);
    const tax = recapture*t25 + ltcg*ltcgRate + grossGain*niit + grossGain*ca;
    const sellNet = amountRealized - tax;

    // Short-lease discount sensitivity: value if sold with <5y remaining vs long lease
    const shortDisc = num('in-shortdisc', 0.10);
    const shortPrice = price*(1-shortDisc);

    const out = $('calc-result');
    if(!out) return;
    out.innerHTML =
      `<p><b>Hold NPV — after-tax rent + net exit (${years}y, ${Math.round(disc*100)}% discount):</b> ${money(holdAfterTaxNPV)} <span class="muted">(pre-tax NPV ${money(holdPreTaxNPV)}; terminal gross ${money(terminalGross)} at ${Math.round(capRate*100)}% cap less ${Math.round(costs*100)}% exit costs; future terminal exit tax not modeled here)</span></p>`+
      `<p><b>Sell now, after-tax (illustrative):</b> ${money(sellNet)} <span class="muted">(gross ${money(price)} − costs ${money(price*costs)} = amount realized ${money(amountRealized)} − tax ${money(tax)}; gain ${money(grossGain)}, §1250 recapture ${money(recapture)})</span></p>`+
      `<p><b>Short-lease sensitivity:</b> at ${Math.round(shortDisc*100)}% discount, gross price ≈ ${money(shortPrice)}.</p>`+
      `<p><b>Gap (After-tax Hold NPV − Sell net):</b> ${money(holdAfterTaxNPV - sellNet)} <span class="muted">— positive favours hold on these inputs; negative favours sell. Not a recommendation until verified inputs exist.</span></p>`+
      `<p class="muted">Federal tax defaults use IRS Topic 409 (2025): 0%/15%/20% LTCG, 25% max §1250 recapture, 3.8% NIIT. CA taxes gains as ordinary income (up to 13.3%). For Measure ULA ($5.4M/$10.9M) and IRC §1031 modeling, use the full W-02 calculator in central-la-2026/calculator.html. Not tax advice.</p>`;
  }
  document.addEventListener('DOMContentLoaded', ()=>{
    const form = $('calc-form');
    if(form){ form.addEventListener('input', calc); calc(); }
  });
})();
