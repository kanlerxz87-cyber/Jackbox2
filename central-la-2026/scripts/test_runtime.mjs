#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.cwd();
const pages = [
  'index.html', 'tenant-analysis.html', 'market-trade-area.html', 'hazards-risk.html',
  'lease-calendar.html', 'calculator.html', 'decision-gates.html', 'questions-gaps.html',
  'suggestions.html', 'advisor-summary.html', 'flagged-review.html'
];

function createMiniDom(html, pathname) {
  const elementsById = new Map();
  const listeners = { DOMContentLoaded: [] };
  const store = new Map();

  function makeEl(id, tag, attrs = {}) {
    const el = {
      id,
      tagName: tag.toUpperCase(),
      type: attrs.type || '',
      value: attrs.value !== undefined ? attrs.value : '',
      checked: false,
      className: '',
      textContent: '',
      _innerHTML: '',
      style: {},
      classList: { toggle() {}, add() {}, remove() {} },
      listeners: {},
      set innerHTML(v) { this._innerHTML = String(v); },
      get innerHTML() { return this._innerHTML; },
      addEventListener(ev, fn) {
        this.listeners[ev] = this.listeners[ev] || [];
        this.listeners[ev].push(fn);
      },
      trigger(ev, extra = {}) {
        (this.listeners[ev] || []).forEach((fn) => fn({ target: el, ...extra }));
      },
      getAttribute(k) { return attrs[k] || null; },
      querySelectorAll() { return []; }
    };
    return el;
  }

  // Parse all elements with id="..." in HTML
  const tagRe = /<([a-z0-9-]+)([^>]*?)\bid=["']([^"']+)["']([^>]*)>/gi;
  let m;
  while ((m = tagRe.exec(html)) !== null) {
    const tag = m[1];
    const allAttrs = (m[2] + ' ' + m[4]);
    const id = m[3];
    const attrs = {};
    const valM = allAttrs.match(/\bvalue=["']([^"']*)["']/i);
    if (valM) attrs.value = valM[1];
    const typeM = allAttrs.match(/\btype=["']([^"']*)["']/i);
    if (typeM) attrs.type = typeM[1];
    elementsById.set(id, makeEl(id, tag, attrs));
  }

  const document = {
    getElementById(id) { return elementsById.get(id) || null; },
    addEventListener(ev, fn) {
      listeners[ev] = listeners[ev] || [];
      listeners[ev].push(fn);
    },
    createElement(tag) {
      return { ...makeEl('', tag), click() {} };
    }
  };

  const sandbox = {
    console,
    Math,
    Date,
    Number,
    String,
    Array,
    Object,
    JSON,
    parseFloat,
    parseInt,
    isNaN,
    Blob: class { constructor(parts) { this.parts = parts; } },
    URL: { createObjectURL: () => 'blob:test', revokeObjectURL: () => {} },
    localStorage: {
      getItem: (k) => (store.has(k) ? store.get(k) : null),
      setItem: (k, v) => store.set(k, String(v)),
      removeItem: (k) => store.delete(k)
    },
    document,
    location: { pathname: '/' + pathname },
    alert: (msg) => { throw new Error('Unexpected alert: ' + msg); }
  };
  sandbox.window = sandbox;
  return { sandbox, elementsById, fireReady: () => (listeners.DOMContentLoaded || []).forEach((fn) => fn()) };
}

let failures = 0;

for (const page of pages) {
  const html = fs.readFileSync(path.join(root, page), 'utf8');
  const { sandbox, elementsById, fireReady } = createMiniDom(html, page);
  const ctx = vm.createContext(sandbox);

  // Execute external local scripts referenced by the page
  const scriptTagRe = /<script([^>]*)>([\s\S]*?)<\/script>/gi;
  let sm;
  try {
    while ((sm = scriptTagRe.exec(html)) !== null) {
      const attrs = sm[1];
      const inlineCode = sm[2];
      const srcM = attrs.match(/\bsrc=["']([^"']+)["']/i);
      if (srcM) {
        const scriptPath = path.join(root, srcM[1]);
        const code = fs.readFileSync(scriptPath, 'utf8');
        vm.runInContext(code, ctx, { filename: srcM[1] });
      } else if (inlineCode.trim()) {
        vm.runInContext(inlineCode, ctx, { filename: `${page}:inline` });
      }
    }
    fireReady();

    // Verify shell rendered
    if (!elementsById.get('app-sidebar')?.innerHTML.includes('index.html')) {
      throw new Error('Sidebar failed to render');
    }
    if (!elementsById.get('app-topbar')?.innerHTML.includes('Zero PII')) {
      throw new Error('Topbar failed to render');
    }

    // Verify dynamic tbodies rendered rows and every row has an https:// source link
    let rowTotal = 0;
    for (const [id, el] of elementsById.entries()) {
      if (id.endsWith('-tbody')) {
        const rows = el.innerHTML.match(/<tr[\s>]/gi) || [];
        if (rows.length === 0) {
          throw new Error(`Dynamic table body #${id} rendered 0 rows`);
        }
        rowTotal += rows.length;
        const trBlocks = el.innerHTML.split(/<tr[\s>]/i).slice(1);
        trBlocks.forEach((trHtml, idx) => {
          if (!trHtml.includes('https://')) {
            throw new Error(`Row ${idx} in #${id} is missing an https:// official source link`);
          }
        });
      }
    }

    // Extra calculator functional test
    if (page === 'calculator.html') {
      elementsById.get('btn-load-sandbox').trigger('click');
      const bov = elementsById.get('bov-results').innerHTML;
      const atx = elementsById.get('aftertax-results').innerHTML;
      const mod = elementsById.get('model-results').innerHTML;
      const sen = elementsById.get('sensitivity-results').innerHTML;
      if (!bov.includes('Short-Lease Discount') || !atx.includes('NET AFTER-TAX CASH PROCEEDS') || !mod.includes('IRC §1031') || !sen.includes('Exit Cap')) {
        throw new Error('Calculator sandbox render incomplete');
      }
      // Test Measure ULA $5.5M dead zone warning
      elementsById.get('overrideSalePrice').value = '5500000';
      elementsById.get('inLaCity').value = 'yes';
      elementsById.get('overrideSalePrice').trigger('input');
      if (!elementsById.get('aftertax-results').innerHTML.includes('MEASURE ULA 4.0% DEAD ZONE')) {
        throw new Error('Measure ULA 4.0% dead zone alert did not trigger at $5,500,000');
      }
      // Test Wipe Inputs clears back to pending
      elementsById.get('btn-wipe-inputs').trigger('click');
      if (!elementsById.get('calc-status-banner').innerHTML.includes('DECISION PENDING VERIFIED PRIVATE INPUTS')) {
        throw new Error('Wipe inputs did not restore pending state');
      }
    }

    // Extra notice calendar functional test
    if (page === 'lease-calendar.html') {
      elementsById.get('nc-expiration-date').value = '2032-06-30';
      elementsById.get('nc-notice-days').value = '180';
      elementsById.get('nc-expiration-date').trigger('change');
      if (!elementsById.get('nc-output').innerHTML.includes('2032-06-30') || !elementsById.get('nc-output').innerHTML.includes('HARD CONTRACTUAL OPTION NOTICE DEADLINE')) {
        throw new Error('Notice calendar tool did not render milestones');
      }
    }

    console.log(`PASS  ${page.padEnd(26)} (${rowTotal} dynamic table rows verified)`);
  } catch (err) {
    console.error(`FAIL  ${page}: ${err.message}`);
    failures++;
  }
}

if (failures > 0) {
  process.exit(1);
}
console.log('ALL 11 PAGES PASSED RUNTIME DOM, TABLE SOURCE & CALCULATOR TESTS.');
