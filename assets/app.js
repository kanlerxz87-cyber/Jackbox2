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
    const t15 = num('in-t15', 0.15), t20 = num('in-t20', 0.20), t25 = num('in-t25', 0.25);
    const niit = num('in-niit', 0.038), ca = num('in-ca', 0.093);
    const otherOrd = num('in-ord', 0.24);     // ordinary rate on rental income (illustrative)

    // HOLD: NPV of escalating NNN rent, then terminal value at cap rate
    let holdNPV = 0;
    for(let y=1;y<=years;y++){ holdNPV += (rent*Math.pow(1+esc,y-1)) / Math.pow(1+disc,y); }
    const terminalRent = renewalRent*Math.pow(1+esc,years-1);
    const terminalValue = capRate>0 ? terminalRent/capRate : 0;
    holdNPV += terminalValue / Math.pow(1+disc,years);

    // SELL NOW: after-tax proceeds
    const grossGain = Math.max(0, price - basis);
    const recapture = Math.min(dep, grossGain);
    const ltcg = Math.max(0, grossGain - recapture);
    // Simplified tiering: user sets blended LTCG rate via t15/t20 inputs; default uses t15.
    const tax = recapture*t25 + ltcg*t15 + grossGain*niit + grossGain*ca;
    const sellNet = price*(1-costs) - tax;

    // Short-lease discount sensitivity: value if sold with <5y remaining vs long lease
    const shortDisc = num('in-shortdisc', 0.10);
    const shortPrice = price*(1-shortDisc);

    const out = $('calc-result');
    if(!out) return;
    out.innerHTML =
      `<p><b>Hold NPV (${years}y, ${Math.round(disc*100)}% discount):</b> ${money(holdNPV)} <span class="muted">(rent NPV + terminal ${money(terminalValue)} at ${Math.round(capRate*100)}% cap)</span></p>`+
      `<p><b>Sell now, after-tax (illustrative):</b> ${money(sellNet)} <span class="muted">(gross ${money(price)} − costs ${money(price*costs)} − tax ${money(tax)}; gain ${money(grossGain)}, recapture ${money(recapture)})</span></p>`+
      `<p><b>Short-lease sensitivity:</b> at ${Math.round(shortDisc*100)}% discount, price ≈ ${money(shortPrice)}.</p>`+
      `<p><b>Gap (Hold NPV − Sell net):</b> ${money(holdNPV - sellNet)} <span class="muted">— positive favours hold on these inputs; negative favours sell. Not a recommendation until verified inputs exist.</span></p>`+
      `<p class="muted">Tax rates default to IRS Topic 409 (2025): 15% LTCG tier, 25% §1250 recapture, 3.8% NIIT. CA rate is illustrative — confirm with CPA. This tool is not tax advice.</p>`;
  }
  document.addEventListener('DOMContentLoaded', ()=>{
    const form = $('calc-form');
    if(form){ form.addEventListener('input', calc); calc(); }
  });
})();
