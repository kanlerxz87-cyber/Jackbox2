
/* Private, offline calculator for the sell-versus-hold comparison.
   Deliberately inert: no fetch, no storage, no cookies, no external calls. */
(function () {
  "use strict";
  var ids = ["price","basis","dep","costs","transfer","ltcg","recap","niit","state",
             "rent","esc","years","ownerCosts","costInfl","vacancy","disc","cap","exitCosts",
             "capLong","capShort"];
  function el(id) { return document.getElementById(id); }
  function num(id) {
    var v = el(id) && el(id).value !== "" ? parseFloat(el(id).value) : NaN;
    return isFinite(v) ? v : 0;
  }
  function pct(id) { return num(id) / 100; }
  function money(n) {
    if (!isFinite(n)) return "—";
    return n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
  }
  function pctText(n) {
    if (!isFinite(n)) return "—";
    return (n * 100).toFixed(1).replace(/\.0$/, "") + "%";
  }
  function sale(price) {
    var costs = price * pct("costs");
    var transfer = price * pct("transfer");
    var basis = num("basis");
    var dep = num("dep");
    var gain = Math.max(0, price - costs - transfer - basis);
    var recapture = Math.min(dep, gain);
    var remainder = gain - recapture;
    var fed = recapture * num("recap") + remainder * num("ltcg") + gain * num("niit");
    var state = gain * num("state");
    var net = price - costs - transfer - fed - state;
    return { costs: costs, transfer: transfer, gain: gain, recapture: recapture,
             remainder: remainder, fed: fed, state: state, tax: fed + state, net: net };
  }
  function holdNpv() {
    var rent = num("rent"), esc = pct("esc"), years = Math.max(1, Math.round(num("years")));
    var ownerCosts = num("ownerCosts"), costInfl = pct("costInfl"), vacancy = pct("vacancy");
    var disc = pct("disc"), cap = pct("cap"), exitCosts = pct("exitCosts");
    var pv = 0, y, noi;
    for (y = 1; y <= years; y++) {
      noi = rent * Math.pow(1 + esc, y - 1) * (1 - vacancy) - ownerCosts * Math.pow(1 + costInfl, y - 1);
      pv += noi / Math.pow(1 + disc, y);
    }
    var terminalNoi = rent * Math.pow(1 + esc, years) * (1 - vacancy);
    var terminalValue = cap > 0 ? terminalNoi / cap : 0;
    var terminalNet = terminalValue * (1 - exitCosts);
    pv += terminalNet / Math.pow(1 + disc, years);
    return { pv: pv, terminalValue: terminalValue, terminalNet: terminalNet, years: years, disc: disc };
  }
  function breakEven(target) {
    var lo = 0, hi = Math.max(1000000, Math.abs(target) * 20 + num("basis") + 1000000), mid, i, s;
    for (i = 0; i < 80; i++) {
      mid = (lo + hi) / 2;
      s = sale(mid);
      if (s.net - target < 0) { lo = mid; } else { hi = mid; }
    }
    return (lo + hi) / 2;
  }
  function line(label, value, cls) {
    return '<div class="line"><span>' + label + '</span><span class="' + (cls || "") + '">' + value + "</span></div>";
  }
  function run() {
    var price = num("price");
    var s = sale(price);
    var h = holdNpv();
    var diff = h.pv - s.net;
    var be = breakEven(h.pv);
    var out = [];
    var head = el("headline"), lines = el("lines");

    if (price <= 0 && num("rent") <= 0) {
      head.textContent = "Enter a price or a rent to begin";
      lines.innerHTML = "";
      return;
    }
    if (h.disc <= 0) {
      head.textContent = "Set a discount rate above zero";
      lines.innerHTML = "";
      return;
    }

    head.innerHTML = diff >= 0
      ? "Hold value exceeds net sale proceeds by " + money(diff)
      : "Net sale proceeds exceed hold value by " + money(-diff);

    out.push(line("Gross sale price", money(price)));
    out.push(line("Selling costs", "−" + money(s.costs)));
    out.push(line("Transfer taxes", "−" + money(s.transfer)));
    out.push(line("Realised gain", money(s.gain)));
    out.push(line("of which depreciation recapture", money(s.recapture)));
    out.push(line("Federal tax", "−" + money(s.fed)));
    out.push(line("State tax", "−" + money(s.state)));
    out.push(line("<b>Net sale proceeds</b>", "<b>" + money(s.net) + "</b>"));
    out.push(line("Hold: present value of rent, " + h.years + " years at " + pctText(h.disc), money(h.pv - h.terminalNet / Math.pow(1 + h.disc, h.years))));
    out.push(line("Hold: present value of terminal sale", money(h.terminalNet / Math.pow(1 + h.disc, h.years))));
    out.push(line("<b>Hold net present value</b>", "<b>" + money(h.pv) + "</b>"));
    out.push(line("<b>Difference, hold minus sell</b>", "<b class=\"" + (diff >= 0 ? "pos" : "neg") + "\">" + money(diff) + "</b>"));
    out.push(line("Break-even sale price", money(be)));

    var cl = pct("capLong"), cs = pct("capShort");
    if (cl > 0 && cs > 0) {
      var discount = 1 - (cl / cs);
      out.push(line("Implied short-lease discount", pctText(discount) +
        " (long " + pctText(cl) + " vs short " + pctText(cs) + ")"));
    } else {
      out.push(line("Implied short-lease discount", "enter two comparable cap rates"));
    }
    if (s.gain <= 0) {
      out.push(line("Note", "No gain on these inputs, so tax is zero."));
    }
    if (num("niit") === 0) {
      out.push(line("Note", "Net investment income rate is zero because it was not verified — check F-07."));
    }
    lines.innerHTML = out.join("");
  }
  function clearAll() {
    var i;
    for (i = 0; i < ids.length; i++) {
      if (el(ids[i]) && el(ids[i]).tagName === "INPUT") { el(ids[i]).value = ""; }
    }
    el("years").value = "5";
    el("recap").value = "0.25";
    el("niit").value = "0";
    el("state").value = "0.123";
    el("ltcg").value = "0.20";
    document.getElementById("headline").textContent = "Enter your inputs, then compute";
    document.getElementById("lines").innerHTML = "";
  }
  document.addEventListener("DOMContentLoaded", function () {
    var runBtn = el("run"), resetBtn = el("reset");
    if (runBtn) { runBtn.addEventListener("click", run); }
    if (resetBtn) { resetBtn.addEventListener("click", clearAll); }
    var form = el("calc");
    if (form) {
      form.addEventListener("input", function () {
        var price = num("price");
        if (price > 0 || num("rent") > 0) { run(); }
      });
    }
  });
})();
