/* ==========================================================================
   W-02 · Private Browser Sell-vs-Hold & After-Tax Calculator (v1.0.0-2026.11)
   100% client-side. Zero network calls. No winner declared without verified inputs.
   ========================================================================== */
(function () {
  const MODEL_VERSION = 'v1.0.0-2026.11';
  const TREASURY_10Y = 4.91; // Verified 2026-11-24 U.S. Treasury Par Yield Curve
  const ULA_TIER1 = 5400000; // Effective after June 30, 2026 (LA Office of Finance)
  const ULA_TIER2 = 10900000;

  const FIELD_IDS = [
    'noi', 'remainingWalt', 'annualEscalation', 'debtBalance', 'prepayPenalty',
    'inLaCity', 'adjustedBasis', 'accumDep', 'fedLtcgRate', 'fedRecapRate', 'niitRate', 'caTaxRate',
    'brokerCommPct', 'otherClosingPct',
    'bov1CurCap', 'bov2CurCap', 'bov3CurCap',
    'bov1ExtCap', 'bov2ExtCap', 'bov3ExtCap',
    'overrideSalePrice',
    'reinvestAfterTaxYield', 'exchangeYield', 'exchangeGrowth',
    'renewalRentPct', 'renewalTiLc', 'renewalExitCap',
    'holdDowntimeMonths', 'holdReleasingCost', 'holdReplacementRentPct', 'holdLandFloor', 'holdExitCap',
    'discountRate', 'ordinaryTaxOnRent', 'verifiedAttestation'
  ];

  // Illustrative anonymized sandbox values (explicitly flagged as NOT real parcel data)
  const SANDBOX_EXAMPLE = {
    noi: 275000,
    remainingWalt: 6.0,
    annualEscalation: 2.0,
    debtBalance: 0,
    prepayPenalty: 0,
    inLaCity: 'yes',
    adjustedBasis: 1200000,
    accumDep: 650000,
    fedLtcgRate: 20.0,
    fedRecapRate: 25.0,
    niitRate: 3.8,
    caTaxRate: 13.3,
    brokerCommPct: 3.5,
    otherClosingPct: 0.5,
    bov1CurCap: 6.25,
    bov2CurCap: 6.50,
    bov3CurCap: 6.75,
    bov1ExtCap: 5.50,
    bov2ExtCap: 5.75,
    bov3ExtCap: 5.85,
    overrideSalePrice: '',
    reinvestAfterTaxYield: 4.5,
    exchangeYield: 5.75,
    exchangeGrowth: 2.0,
    renewalRentPct: 95,
    renewalTiLc: 150000,
    renewalExitCap: 6.0,
    holdDowntimeMonths: 15,
    holdReleasingCost: 450000,
    holdReplacementRentPct: 100,
    holdLandFloor: 3200000,
    holdExitCap: 6.5,
    discountRate: 7.5,
    ordinaryTaxOnRent: 38.0,
    verifiedAttestation: false
  };

  function valNum(id) {
    const el = document.getElementById(id);
    if (!el || el.value === '' || el.value === null) return null;
    const n = parseFloat(el.value);
    return Number.isFinite(n) ? n : null;
  }

  function valStr(id) {
    const el = document.getElementById(id);
    return el ? el.value : '';
  }

  function valBool(id) {
    const el = document.getElementById(id);
    return el ? !!el.checked : false;
  }

  function avgNonNull(arr) {
    const valid = arr.filter((x) => x !== null && x > 0);
    if (!valid.length) return null;
    return valid.reduce((a, b) => a + b, 0) / valid.length;
  }

  function computeTransferTaxes(grossPrice, netOfAssumedLiens, inLaCity) {
    if (!grossPrice || grossPrice <= 0) {
      return { countyDtt: 0, cityBase: 0, ulaTax: 0, ulaRate: 0, total: 0, ulaCliffWarning: '' };
    }
    // LA County DTT: $0.55 per $500 (rounded up to nearest $500)
    const countyUnits = Math.ceil(netOfAssumedLiens / 500);
    const countyDtt = countyUnits * 0.55;

    let cityBase = 0;
    let ulaTax = 0;
    let ulaRate = 0;
    let ulaCliffWarning = '';

    if (inLaCity === 'yes') {
      const cityUnits = Math.ceil(netOfAssumedLiens / 500);
      cityBase = cityUnits * 2.25;
      if (grossPrice >= ULA_TIER2) {
        ulaRate = 0.055;
        ulaTax = grossPrice * 0.055;
        if (grossPrice < 11550000) {
          ulaCliffWarning = `MEASURE ULA 5.5% CLIFF ZONE: At ${App.formatCurrency(grossPrice)}, the 5.5% ULA tax (${App.formatCurrency(ulaTax)}) applies to the ENTIRE gross price. Selling at $10,899,999 incurs 4.0% ($436,000) instead — a $163,500+ jump at the $10.9M boundary.`;
        }
      } else if (grossPrice > ULA_TIER1) {
        ulaRate = 0.04;
        ulaTax = grossPrice * 0.04;
        if (grossPrice < 5640000) {
          const netHere = grossPrice - ulaTax;
          const netAtCap = ULA_TIER1;
          ulaCliffWarning = `MEASURE ULA 4.0% DEAD ZONE: At ${App.formatCurrency(grossPrice)}, the 4.0% ULA tax (${App.formatCurrency(ulaTax)}) leaves ${App.formatCurrency(netHere)} before other costs — LESS than selling at $5,400,000 (${App.formatCurrency(netAtCap)} with $0 ULA)!`;
        }
      }
    }

    return {
      countyDtt,
      cityBase,
      ulaTax,
      ulaRate,
      total: countyDtt + cityBase + ulaTax,
      ulaCliffWarning
    };
  }

  function computeAfterTaxSale(grossPrice, params) {
    const brokerFee = grossPrice * (params.brokerCommPct / 100);
    const otherClosing = grossPrice * (params.otherClosingPct / 100);
    const tx = computeTransferTaxes(grossPrice, grossPrice, params.inLaCity);
    const totalSellingCosts = brokerFee + otherClosing + tx.total;

    const amountRealized = grossPrice - totalSellingCosts;
    const totalGain = Math.max(0, amountRealized - params.adjustedBasis);
    const sec1250Gain = Math.min(totalGain, Math.max(0, params.accumDep));
    const remLtcg = Math.max(0, totalGain - sec1250Gain);

    const fedRecapTax = sec1250Gain * (params.fedRecapRate / 100);
    const fedLtcgTax = remLtcg * (params.fedLtcgRate / 100);
    const niitTax = totalGain * (params.niitRate / 100);
    const caTax = totalGain * (params.caTaxRate / 100);
    const totalIncomeTax = fedRecapTax + fedLtcgTax + niitTax + caTax;

    const debtOutflow = params.debtBalance + params.prepayPenalty;
    const netAfterTaxCash = amountRealized - debtOutflow - totalIncomeTax;
    const net1031Equity = amountRealized - debtOutflow; // 1031 defers income tax, NOT closing/transfer/ULA taxes

    return {
      grossPrice,
      brokerFee,
      otherClosing,
      tx,
      totalSellingCosts,
      amountRealized,
      totalGain,
      sec1250Gain,
      remLtcg,
      fedRecapTax,
      fedLtcgTax,
      niitTax,
      caTax,
      totalIncomeTax,
      debtOutflow,
      netAfterTaxCash,
      net1031Equity
    };
  }

  function runTenYearModel(sale, params, extendedValue) {
    const H = 10;
    const rDisc = params.discountRate / 100;
    const taxOnRent = params.ordinaryTaxOnRent / 100;
    const esc = params.annualEscalation / 100;

    // 1) Sell Now (Taxable Cash Out -> Reinvest)
    const yReinv = params.reinvestAfterTaxYield / 100;
    const sellTaxableFV = sale.netAfterTaxCash * Math.pow(1 + yReinv, H);
    const sellTaxableNPV = sellTaxableFV / Math.pow(1 + rDisc, H);

    // 2) Sell Now (1031 Exchange -> Diversified Replacement Real Estate)
    // Models annual after-tax cash flow + Year-10 terminal equity (net of standard 4% selling costs; deferred basis noted)
    const yExch = params.exchangeYield / 100;
    const gExch = params.exchangeGrowth / 100;
    let exchCashFV = 0;
    let exchNPV = 0;
    let curExchCF = sale.net1031Equity * yExch;
    for (let t = 1; t <= H; t++) {
      const afterTaxCF = curExchCF * (1 - taxOnRent * 0.65); // partial depreciation shelter note
      exchCashFV += afterTaxCF * Math.pow(1 + yReinv, H - t);
      exchNPV += afterTaxCF / Math.pow(1 + rDisc, t);
      curExchCF *= (1 + gExch);
    }
    const exchTerminalGross = sale.net1031Equity * Math.pow(1 + gExch, H);
    const exchTerminalNetPreTax = exchTerminalGross * 0.96; // 4% future exit cost (deferred tax liability noted!)
    const exchTotalFV = exchCashFV + exchTerminalNetPreTax;
    const exchTotalNPV = exchNPV + exchTerminalNetPreTax / Math.pow(1 + rDisc, H);

    // 3) Negotiated Early Renewal / Blend-and-Extend
    let renCashFV = -params.renewalTiLc * Math.pow(1 + yReinv, H);
    let renNPV = -params.renewalTiLc;
    let renNoi = params.noi * (params.renewalRentPct / 100);
    for (let t = 1; t <= H; t++) {
      const atCF = renNoi * (1 - taxOnRent);
      renCashFV += atCF * Math.pow(1 + yReinv, H - t);
      renNPV += atCF / Math.pow(1 + rDisc, t);
      renNoi *= (1 + esc);
    }
    const renTermGross = renNoi / (params.renewalExitCap / 100);
    const renTermSale = computeAfterTaxSale(renTermGross, params);
    const renTotalFV = renCashFV + renTermSale.netAfterTaxCash;
    const renTotalNPV = renNPV + renTermSale.netAfterTaxCash / Math.pow(1 + rDisc, H);

    // 4) Hold to Expiration & Re-Tenant / Dark-Value Stress
    let holdCashFV = 0;
    let holdNPV = 0;
    let curNoi = params.noi;
    const expYear = Math.max(1, Math.min(H, Math.round(params.remainingWalt)));
    const downYrs = params.holdDowntimeMonths / 12;
    let reTenantedNoi = params.noi * (params.holdReplacementRentPct / 100);

    for (let t = 1; t <= H; t++) {
      let cf = 0;
      if (t <= expYear) {
        cf = curNoi * (1 - taxOnRent);
        curNoi *= (1 + esc);
      } else {
        const yrsPast = t - expYear;
        if (yrsPast <= Math.floor(downYrs)) {
          // Full vacancy year: zero rent, negative carry (~1.3% property tax + insurance carry on land floor)
          cf = -(params.holdLandFloor * 0.015);
          if (yrsPast === 1) cf -= params.holdReleasingCost;
        } else if (yrsPast === Math.floor(downYrs) + 1) {
          const fracDown = downYrs - Math.floor(downYrs);
          const fracActive = 1 - fracDown;
          cf = (reTenantedNoi * fracActive) * (1 - taxOnRent) - (params.holdLandFloor * 0.015 * fracDown);
          if (Math.floor(downYrs) === 0) cf -= params.holdReleasingCost;
          reTenantedNoi *= (1 + esc);
        } else {
          cf = reTenantedNoi * (1 - taxOnRent);
          reTenantedNoi *= (1 + esc);
        }
      }
      holdCashFV += cf * Math.pow(1 + yReinv, H - t);
      holdNPV += cf / Math.pow(1 + rDisc, t);
    }
    const holdIncomeExitGross = reTenantedNoi / (params.holdExitCap / 100);
    const holdTermGross = Math.max(holdIncomeExitGross, params.holdLandFloor * Math.pow(1 + 0.02, H));
    const holdTermSale = computeAfterTaxSale(holdTermGross, params);
    const holdTotalFV = holdCashFV + holdTermSale.netAfterTaxCash;
    const holdTotalNPV = holdNPV + holdTermSale.netAfterTaxCash / Math.pow(1 + rDisc, H);

    return {
      sellTaxable: { fv: sellTaxableFV, npv: sellTaxableNPV, day1: sale.netAfterTaxCash },
      sell1031: { fv: exchTotalFV, npv: exchTotalNPV, day1: sale.net1031Equity, note: 'Deferred tax liability carries over unless held to IRC §1014 step-up' },
      renew: { fv: renTotalFV, npv: renTotalNPV, day1: extendedValue ? (extendedValue - params.renewalTiLc) : null, termGross: renTermGross },
      holdStress: { fv: holdTotalFV, npv: holdTotalNPV, day1: params.holdLandFloor, termGross: holdTermGross }
    };
  }

  function renderEmptyState() {
    document.getElementById('calc-status-banner').className = 'banner banner-warn';
    document.getElementById('calc-status-banner').innerHTML = `
      <strong>STATUS: DECISION PENDING VERIFIED PRIVATE INPUTS (Model ${MODEL_VERSION}).</strong>
      All private parcel fields start intentionally blank so no unverified numbers are fabricated.
      Enter your CPA-, attorney-, and broker-verified private figures below (100% local in your browser), OR click
      <em>"Load Illustrative Anonymized Sandbox"</em> to test how the math responds.
    `;
    document.getElementById('bov-results').innerHTML = `<p class="card-sub">Enter current NOI and at least one broker BOV cap rate (or a custom sale price) to compute the short-lease discount.</p>`;
    document.getElementById('aftertax-results').innerHTML = `<p class="card-sub">Enter private NOI/price, adjusted tax basis, and cumulative depreciation to generate the single net after-tax comparison number.</p>`;
    document.getElementById('model-results').innerHTML = `<p class="card-sub">Complete inputs above to run the 10-year Sell-vs-1031-vs-Renew-vs-Hold comparison and sensitivity grid.</p>`;
    document.getElementById('sensitivity-results').innerHTML = '';
  }

  function recalculate() {
    const noi = valNum('noi');
    const overridePrice = valNum('overrideSalePrice');
    const curAvgCap = avgNonNull([valNum('bov1CurCap'), valNum('bov2CurCap'), valNum('bov3CurCap')]);
    const extAvgCap = avgNonNull([valNum('bov1ExtCap'), valNum('bov2ExtCap'), valNum('bov3ExtCap')]);

    const grossPrice = overridePrice || (noi && curAvgCap ? noi / (curAvgCap / 100) : null);
    const extendedValue = (noi && extAvgCap) ? noi / (extAvgCap / 100) : null;

    if (!grossPrice || grossPrice <= 0) {
      renderEmptyState();
      return;
    }

    const params = {
      noi: noi || 0,
      remainingWalt: valNum('remainingWalt') ?? 6,
      annualEscalation: valNum('annualEscalation') ?? 2,
      debtBalance: valNum('debtBalance') ?? 0,
      prepayPenalty: valNum('prepayPenalty') ?? 0,
      inLaCity: valStr('inLaCity') || 'yes',
      adjustedBasis: valNum('adjustedBasis') ?? 0,
      accumDep: valNum('accumDep') ?? 0,
      fedLtcgRate: valNum('fedLtcgRate') ?? 20.0,
      fedRecapRate: valNum('fedRecapRate') ?? 25.0,
      niitRate: valNum('niitRate') ?? 3.8,
      caTaxRate: valNum('caTaxRate') ?? 13.3,
      brokerCommPct: valNum('brokerCommPct') ?? 3.5,
      otherClosingPct: valNum('otherClosingPct') ?? 0.5,
      reinvestAfterTaxYield: valNum('reinvestAfterTaxYield') ?? 4.5,
      exchangeYield: valNum('exchangeYield') ?? 5.75,
      exchangeGrowth: valNum('exchangeGrowth') ?? 2.0,
      renewalRentPct: valNum('renewalRentPct') ?? 100,
      renewalTiLc: valNum('renewalTiLc') ?? 0,
      renewalExitCap: valNum('renewalExitCap') ?? (extAvgCap || curAvgCap || 6.0),
      holdDowntimeMonths: valNum('holdDowntimeMonths') ?? 12,
      holdReleasingCost: valNum('holdReleasingCost') ?? 0,
      holdReplacementRentPct: valNum('holdReplacementRentPct') ?? 100,
      holdLandFloor: valNum('holdLandFloor') ?? 0,
      holdExitCap: valNum('holdExitCap') ?? (curAvgCap || 6.5),
      discountRate: valNum('discountRate') ?? 7.5,
      ordinaryTaxOnRent: valNum('ordinaryTaxOnRent') ?? 38.0
    };

    const isVerified = valBool('verifiedAttestation');
    const banner = document.getElementById('calc-status-banner');
    if (isVerified) {
      banner.className = 'banner banner-verified';
      banner.innerHTML = `
        <strong>VERIFIED PRIVATE INPUT MODE ACTIVE (Model ${MODEL_VERSION}):</strong>
        User attested inputs come from verified lease abstract, CPA basis schedule, and written broker BOV quotes.
        All calculations remain 100% local in browser memory — export to your offline vault before closing.
      `;
    } else {
      banner.className = 'banner banner-warn';
      banner.innerHTML = `
        <strong>ILLUSTRATIVE / UNVERIFIED SANDBOX OUTPUT (Model ${MODEL_VERSION}) — NO WINNER DECLARED:</strong>
        Do NOT make a binding sale or renewal commitment until inputs are attested from verified lease, CPA, and broker BOV documents.
      `;
    }

    // 1) Short-lease discount panel
    const spreadCur = curAvgCap ? (curAvgCap - TREASURY_10Y).toFixed(2) + '%' : '—';
    const spreadExt = extAvgCap ? (extAvgCap - TREASURY_10Y).toFixed(2) + '%' : '—';
    const discountBps = (curAvgCap && extAvgCap) ? Math.round((curAvgCap - extAvgCap) * 100) : null;
    const discountDollars = (extendedValue && grossPrice) ? (extendedValue - grossPrice) : null;

    document.getElementById('bov-results').innerHTML = `
      <div class="kpi-grid" style="margin-bottom:0;">
        <div class="kpi-card">
          <div class="kpi-label">Implied Sale Price (Current WALT)</div>
          <div class="kpi-value">${App.formatCurrency(grossPrice)}</div>
          <div class="kpi-sub">Avg Cap: ${curAvgCap ? curAvgCap.toFixed(2) + '%' : 'Custom Override'} (Spread vs. 4.91% 10Y: ${spreadCur})</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Extended-WALT Implied Value</div>
          <div class="kpi-value">${extendedValue ? App.formatCurrency(extendedValue) : '—'}</div>
          <div class="kpi-sub">Avg Cap: ${extAvgCap ? extAvgCap.toFixed(2) + '%' : 'Enter Ext. BOVs'} (Spread vs. 10Y: ${spreadExt})</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Short-Lease Discount (Penalty)</div>
          <div class="kpi-value ${discountDollars > 0 ? 'warn' : ''}">${discountDollars !== null ? App.formatCurrency(discountDollars) : '—'}</div>
          <div class="kpi-sub">${discountBps !== null ? '+' + discountBps + ' bps cap-rate penalty for shorter WALT' : 'Enter both Current & Extended BOV quotes'}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Verified Risk-Free Benchmark</div>
          <div class="kpi-value">4.91%</div>
          <div class="kpi-sub">U.S. 10-Yr Treasury (Nov 24, 2026)</div>
        </div>
      </div>
    `;

    // 2) After-Tax Sale Panel
    const sale = computeAfterTaxSale(grossPrice, params);
    const ulaWarningHtml = sale.tx.ulaCliffWarning
      ? `<div class="banner banner-danger" style="margin-top:12px;margin-bottom:0;"><strong>&#9888; ${App.escapeHtml(sale.tx.ulaCliffWarning)}</strong></div>`
      : '';

    const effTaxDragPct = grossPrice > 0 ? ((sale.totalSellingCosts + sale.totalIncomeTax) / grossPrice) * 100 : 0;

    document.getElementById('aftertax-results').innerHTML = `
      <div class="kpi-grid">
        <div class="kpi-card" style="border-color:#1e40af;background:#eff6ff;">
          <div class="kpi-label">Net After-Tax Sale Proceeds (One Number)</div>
          <div class="kpi-value">${App.formatCurrency(sale.netAfterTaxCash)}</div>
          <div class="kpi-sub">Taxable cash-out net of ALL selling, transfer/ULA, debt & income taxes (${effTaxDragPct.toFixed(1)}% total friction)</div>
        </div>
        <div class="kpi-card" style="border-color:#065f46;background:#ecfdf5;">
          <div class="kpi-label">IRC §1031 Reinvestable Equity</div>
          <div class="kpi-value pos">${App.formatCurrency(sale.net1031Equity)}</div>
          <div class="kpi-sub">Defers ${App.formatCurrency(sale.totalIncomeTax)} income tax; closing + ULA (${App.formatCurrency(sale.totalSellingCosts)}) still paid</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Transfer Taxes (LA County + City + ULA)</div>
          <div class="kpi-value ${sale.tx.ulaTax > 0 ? 'neg' : ''}">${App.formatCurrency(sale.tx.total)}</div>
          <div class="kpi-sub">County: ${App.formatCurrency(sale.tx.countyDtt)} · City Base: ${App.formatCurrency(sale.tx.cityBase)} · ULA (${(sale.tx.ulaRate * 100).toFixed(1)}%): ${App.formatCurrency(sale.tx.ulaTax)}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Total Income & Recapture Taxes</div>
          <div class="kpi-value neg">${App.formatCurrency(sale.totalIncomeTax)}</div>
          <div class="kpi-sub">Fed 1250: ${App.formatCurrency(sale.fedRecapTax)} · Fed LTCG: ${App.formatCurrency(sale.fedLtcgTax)} · NIIT: ${App.formatCurrency(sale.niitTax)} · CA: ${App.formatCurrency(sale.caTax)}</div>
        </div>
      </div>
      ${ulaWarningHtml}
      <div class="table-wrap" style="margin-top:14px;">
        <table>
          <thead><tr><th>After-Tax Sale Waterfall Line Item</th><th>Classification</th><th class="num">Amount</th><th>Official Statutory Basis</th></tr></thead>
          <tbody>
            <tr><td>Gross Sale Price (BOV Average / Override)</td><td><span class="tag-priv">PRIVATE QUOTE</span></td><td class="num"><strong>${App.formatCurrency(sale.grossPrice)}</strong></td><td><a class="source-link" href="https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=202611" target="_blank" rel="noopener noreferrer">U.S. Treasury 10Y Floor &#8599;</a></td></tr>
            <tr><td>Less: Brokerage Commission (${params.brokerCommPct}%) &amp; Other Closing (${params.otherClosingPct}%)</td><td><span class="tag-assump">ASSUMPTION</span></td><td class="num">-${App.formatCurrency(sale.brokerFee + sale.otherClosing)}</td><td><a class="source-link" href="https://www.irs.gov/publications/p550" target="_blank" rel="noopener noreferrer">IRS Pub 550 Selling Costs &#8599;</a></td></tr>
            <tr><td>Less: LA County DTT ($0.55/$500) + LA City Base ($2.25/$500)</td><td><span class="tag-obs">OBSERVED LAW</span></td><td class="num">-${App.formatCurrency(sale.tx.countyDtt + sale.tx.cityBase)}</td><td><a class="source-link" href="https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info" target="_blank" rel="noopener noreferrer">LA County RRCC &#8599;</a></td></tr>
            <tr><td>Less: City of LA Measure ULA Special Tax (${(sale.tx.ulaRate * 100).toFixed(1)}% on Gross)</td><td><span class="tag-obs">OBSERVED LAW</span></td><td class="num">-${App.formatCurrency(sale.tx.ulaTax)}</td><td><a class="source-link" href="https://finance.lacity.gov/faq/measure-ula" target="_blank" rel="noopener noreferrer">LA Finance ULA &#8599;</a></td></tr>
            <tr><td><strong>Amount Realized (Net Sales Proceeds Before Debt &amp; Income Tax)</strong></td><td><span class="tag-obs">FORMULA</span></td><td class="num"><strong>${App.formatCurrency(sale.amountRealized)}</strong></td><td><a class="source-link" href="https://www.irs.gov/taxtopics/tc409" target="_blank" rel="noopener noreferrer">IRS Topic 409 &#8599;</a></td></tr>
            <tr><td>Less: Existing Debt Payoff &amp; Prepayment Penalty</td><td><span class="tag-priv">PRIVATE INPUT</span></td><td class="num">-${App.formatCurrency(sale.debtOutflow)}</td><td><a class="source-link" href="https://www.irs.gov/pub/irs-pdf/i8824.pdf" target="_blank" rel="noopener noreferrer">IRS Form 8824 Debt Relief &#8599;</a></td></tr>
            <tr><td><strong>Reinvestable Equity Under IRC §1031 Exchange (Deferred Tax)</strong></td><td><span class="tag-obs">OBSERVED LAW</span></td><td class="num"><strong>${App.formatCurrency(sale.net1031Equity)}</strong></td><td><a class="source-link" href="https://www.irs.gov/pub/irs-pdf/i8824.pdf" target="_blank" rel="noopener noreferrer">IRS Form 8824 &#8599;</a></td></tr>
            <tr><td>Taxable Gain Breakdown (Total Gain ${App.formatCurrency(sale.totalGain)}: Sec 1250 ${App.formatCurrency(sale.sec1250Gain)} + LTCG ${App.formatCurrency(sale.remLtcg)})</td><td><span class="tag-priv">CPA BASIS</span></td><td class="num">${App.formatCurrency(sale.totalGain)}</td><td><a class="source-link" href="https://www.irs.gov/publications/p550" target="_blank" rel="noopener noreferrer">IRS Pub 550 &#8599;</a></td></tr>
            <tr><td>Less: Federal Sec 1250 (${params.fedRecapRate}%) + Federal LTCG (${params.fedLtcgRate}%) + NIIT (${params.niitRate}%)</td><td><span class="tag-obs">OBSERVED LAW</span></td><td class="num">-${App.formatCurrency(sale.fedRecapTax + sale.fedLtcgTax + sale.niitTax)}</td><td><a class="source-link" href="https://www.irs.gov/newsroom/questions-and-answers-on-the-net-investment-income-tax" target="_blank" rel="noopener noreferrer">IRS Topic 409 / NIIT &#8599;</a></td></tr>
            <tr><td>Less: California Income &amp; Behavioral Health Services Tax (${params.caTaxRate}%)</td><td><span class="tag-obs">OBSERVED LAW</span></td><td class="num">-${App.formatCurrency(sale.caTax)}</td><td><a class="source-link" href="https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html" target="_blank" rel="noopener noreferrer">CA FTB &#8599;</a></td></tr>
            <tr style="background:#eff6ff;"><td><strong>NET AFTER-TAX CASH PROCEEDS (TAXABLE SALE)</strong></td><td><span class="tag-obs">OUTPUT</span></td><td class="num"><strong>${App.formatCurrency(sale.netAfterTaxCash)}</strong></td><td><a class="source-link" href="https://www.irs.gov/taxtopics/tc409" target="_blank" rel="noopener noreferrer">IRS / CA FTB / ULA &#8599;</a></td></tr>
          </tbody>
        </table>
      </div>
    `;

    // 3) 10-Year Multi-Path Cash-Flow Model
    const m = runTenYearModel(sale, params, extendedValue);
    document.getElementById('model-results').innerHTML = `
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Strategic Path (10-Yr Horizon · ${MODEL_VERSION})</th>
              <th class="num">Day-1 Net Capital / Value</th>
              <th class="num">Year-10 Projected Wealth (FV)</th>
              <th class="num">Present Value (NPV @ ${params.discountRate}%)</th>
              <th>Primary Risk &amp; Tax Caveat</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>1. Sell Now — Taxable Cash Out</strong></td>
              <td class="num">${App.formatCurrency(m.sellTaxable.day1)}</td>
              <td class="num">${App.formatCurrency(m.sellTaxable.fv)}</td>
              <td class="num"><strong>${App.formatCurrency(m.sellTaxable.npv)}</strong></td>
              <td>Zero single-asset LA/JACK risk post-close; highest immediate tax drag.</td>
            </tr>
            <tr>
              <td><strong>2. Sell Now — IRC §1031 Exchange</strong></td>
              <td class="num">${App.formatCurrency(m.sell1031.day1)}</td>
              <td class="num">${App.formatCurrency(m.sell1031.fv)} *</td>
              <td class="num"><strong>${App.formatCurrency(m.sell1031.npv)} *</strong></td>
              <td>*Pre-deferred-tax terminal value (tax deferred until future taxable sale or IRC §1014 step-up); eliminates single-site LA risk if diversified out of state.</td>
            </tr>
            <tr>
              <td><strong>3. Negotiated Early Renewal / Blend-and-Extend</strong></td>
              <td class="num">${m.renew.day1 !== null ? App.formatCurrency(m.renew.day1) : '—'}</td>
              <td class="num">${App.formatCurrency(m.renew.fv)}</td>
              <td class="num"><strong>${App.formatCurrency(m.renew.npv)}</strong></td>
              <td>After-tax terminal value net of future exit tax/ULA; retains LA seismic &amp; JACK 2031–32 debt refinancing exposure.</td>
            </tr>
            <tr>
              <td><strong>4. Hold to Expiration &amp; Re-Tenant / Dark Stress</strong></td>
              <td class="num">${App.formatCurrency(m.holdStress.day1)} (Land Floor)</td>
              <td class="num">${App.formatCurrency(m.holdStress.fv)}</td>
              <td class="num"><strong>${App.formatCurrency(m.holdStress.npv)}</strong></td>
              <td>Includes ${params.holdDowntimeMonths} mo vacancy + ${App.formatCurrency(params.holdReleasingCost)} re-leasing cost; terminal exit floored by escalated land value.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="chart-caption">
        ${isVerified
          ? 'Note: Compare NPVs alongside non-financial risk tolerances (single-asset LA earthquake/wildfire exposure, JACK credit concentration, and liquidity needs) before making a Gate-5 commitment.'
          : 'NO WINNER DECLARED: Above figures reflect unverified sandbox/assumption inputs. Re-run after Gates 1–4 verify actual lease, CPA basis, and 3 broker BOV quotes.'}
      </p>
    `;

    // 4) Sensitivity Grid: Hold-to-Expiry Exit Cap Rate vs. Vacancy Downtime Months
    const capSteps = [-0.75, -0.25, 0, +0.50, +1.00];
    const downSteps = [0, 6, 12, 18, 24];
    let gridHtml = `<div class="table-wrap"><table><thead><tr><th>Hold Path NPV (${params.discountRate}% disc.)<br>Exit Cap \\ Vacancy Downtime</th>`;
    downSteps.forEach((d) => { gridHtml += `<th class="num">${d} mo dark</th>`; });
    gridHtml += `</tr></thead><tbody>`;
    capSteps.forEach((dc) => {
      const cap = Math.max(3.5, params.holdExitCap + dc);
      gridHtml += `<tr><td><strong>${cap.toFixed(2)}% Exit Cap</strong></td>`;
      downSteps.forEach((dm) => {
        const subP = Object.assign({}, params, { holdExitCap: cap, holdDowntimeMonths: dm });
        const subRes = runTenYearModel(sale, subP, extendedValue);
        const deltaVsSell = subRes.holdStress.npv - m.sellTaxable.npv;
        const cls = deltaVsSell >= 0 ? 'pos' : 'neg';
        gridHtml += `<td class="num"><span style="font-weight:600;">${App.formatCurrency(subRes.holdStress.npv)}</span><br><span style="font-size:11px;" class="${cls}">${deltaVsSell >= 0 ? '+' : ''}${App.formatCurrency(deltaVsSell)} vs Tax Sale</span></td>`;
      });
      gridHtml += `</tr>`;
    });
    gridHtml += `</tbody></table></div>`;
    document.getElementById('sensitivity-results').innerHTML = gridHtml;
  }

  function loadValues(obj) {
    FIELD_IDS.forEach((id) => {
      const el = document.getElementById(id);
      if (!el || !(id in obj)) return;
      if (el.type === 'checkbox') el.checked = !!obj[id];
      else el.value = obj[id];
    });
    recalculate();
  }

  function wipeInputs() {
    FIELD_IDS.forEach((id) => {
      const el = document.getElementById(id);
      if (!el) return;
      if (el.type === 'checkbox') el.checked = false;
      else if (el.tagName === 'SELECT') el.value = 'yes';
      else if (['fedLtcgRate', 'fedRecapRate', 'niitRate', 'caTaxRate'].includes(id)) {
        const defaults = { fedLtcgRate: 20.0, fedRecapRate: 25.0, niitRate: 3.8, caTaxRate: 13.3 };
        el.value = defaults[id];
      } else {
        el.value = '';
      }
    });
    try { localStorage.removeItem('jackbox_w02_private'); } catch (_) {}
    recalculate();
  }

  function exportJson() {
    const payload = {
      modelVersion: MODEL_VERSION,
      exportedAt: new Date().toISOString(),
      privacyWarning: 'CONFIDENTIAL OFFLINE WORKSPACE FILE — DO NOT UPLOAD TO PUBLIC REPOSITORY',
      inputs: {}
    };
    FIELD_IDS.forEach((id) => {
      const el = document.getElementById(id);
      if (!el) return;
      payload.inputs[id] = el.type === 'checkbox' ? el.checked : el.value;
    });
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `private-w02-scenario-${MODEL_VERSION}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function init() {
    if (!document.getElementById('w02-calculator-form')) return;
    FIELD_IDS.forEach((id) => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', recalculate);
        el.addEventListener('change', recalculate);
      }
    });

    const btnSandbox = document.getElementById('btn-load-sandbox');
    if (btnSandbox) btnSandbox.addEventListener('click', () => loadValues(SANDBOX_EXAMPLE));

    const btnWipe = document.getElementById('btn-wipe-inputs');
    if (btnWipe) btnWipe.addEventListener('click', wipeInputs);

    const btnExport = document.getElementById('btn-export-json');
    if (btnExport) btnExport.addEventListener('click', exportJson);

    const importInput = document.getElementById('input-import-json');
    if (importInput) {
      importInput.addEventListener('change', (ev) => {
        const file = ev.target.files && ev.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          try {
            const parsed = JSON.parse(String(reader.result));
            if (parsed && parsed.inputs) loadValues(parsed.inputs);
          } catch (e) {
            alert('Invalid scenario JSON file.');
          }
        };
        reader.readAsText(file);
      });
    }

    renderEmptyState();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
