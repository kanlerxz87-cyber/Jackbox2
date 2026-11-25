/* ==========================================================================
   Shared Dashboard Shell, Table Utilities & SVG Charts
   Zero external requests. Pure vanilla JS.
   ========================================================================== */
(function () {
  const NAV_GROUPS = [
    {
      label: 'Overview',
      items: [
        { href: 'index.html', title: 'Executive Summary', tag: 'HOME' },
        { href: 'advisor-summary.html', title: 'Advisor 1-Page Brief', tag: 'W-10' }
      ]
    },
    {
      label: 'Verified Research',
      items: [
        { href: 'tenant-analysis.html', title: 'Tenant Series (JACK)', tag: 'SEC' },
        { href: 'market-trade-area.html', title: 'Trade Area & Economy', tag: 'W-01' },
        { href: 'hazards-risk.html', title: 'Parcel Hazards & Risks', tag: 'W-04' },
        { href: 'lease-calendar.html', title: 'Lease, Notice & Tax Rules', tag: 'LEGAL' }
      ]
    },
    {
      label: 'Decision Tools (Local Only)',
      items: [
        { href: 'calculator.html', title: 'Sell vs. Hold Calculator', tag: 'W-02' },
        { href: 'decision-gates.html', title: 'Decision-Gate Board', tag: 'W-03' }
      ]
    },
    {
      label: 'Gaps, Review & Roadmap',
      items: [
        { href: 'questions-gaps.html', title: 'Missing Info & Q&A', tag: 'Q&A' },
        { href: 'suggestions.html', title: 'Site Suggestions', tag: 'IDEAS' },
        { href: 'flagged-review.html', title: 'Flagged for Review', tag: 'AUDIT', flag: true }
      ]
    }
  ];

  function currentPage() {
    const p = window.location.pathname.split('/').pop();
    return p && p.endsWith('.html') ? p : 'index.html';
  }

  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderValueOrBlank(val, customLabel) {
    if (val === null || val === undefined || val === '') {
      return `<span class="blank-cell">${escapeHtml(customLabel || 'BLANK — UNVERIFIED')}</span>`;
    }
    return escapeHtml(val);
  }

  function renderSourceLink(url, label) {
    if (!url) return `<span class="blank-cell">NO SOURCE</span>`;
    return `<a class="source-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(label || 'Official Source')} &#8599;</a>`;
  }

  function renderStatusBadge(status) {
    const map = {
      verified: ['badge-verified', 'Verified'],
      unverified: ['badge-unverified', 'Unverified / Blank'],
      unverified_parcel: ['badge-unverified', 'Parcel Unverified'],
      verified_proxy_only: ['badge-proxy', 'Regional Proxy Only'],
      flagged_reconcile: ['badge-flagged', 'Flagged — Reconcile'],
      blocked: ['badge-unverified', 'Blocked'],
      in_progress: ['badge-flagged', 'In Progress'],
      done: ['badge-verified', 'Verified & Done']
    };
    const [cls, text] = map[status] || ['badge-neutral', status || 'Review'];
    return `<span class="badge ${cls}">${escapeHtml(text)}</span>`;
  }

  function injectShell() {
    const active = currentPage();
    const sidebar = document.getElementById('app-sidebar');
    if (sidebar) {
      let navHtml = `
        <div class="sidebar-brand">
          <span class="brand-kicker">Anonymous Research Workspace</span>
          <h1>Central LA NNN QSR<br>Decision Dashboard</h1>
          <div class="brand-sub">Lease Window: 2030–2035 (Placeholder)<br>Parcel ID: [REDACTED]</div>
        </div>
      `;
      NAV_GROUPS.forEach((g) => {
        navHtml += `<div class="nav-section"><div class="nav-label">${escapeHtml(g.label)}</div><ul class="nav-list">`;
        g.items.forEach((it) => {
          const isActive = active === it.href ? 'active' : '';
          const tagCls = it.flag ? 'nav-tag flag' : 'nav-tag';
          navHtml += `<li><a href="${it.href}" class="${isActive}"><span>${escapeHtml(it.title)}</span><span class="${tagCls}">${escapeHtml(it.tag)}</span></a></li>`;
        });
        navHtml += `</ul></div>`;
      });
      navHtml += `
        <div class="sidebar-footer">
          <strong>Privacy First:</strong> Zero PII published. Zero analytics or external calls. Private inputs remain in your browser only.<br><br>
          <strong>Verified Date:</strong> 2026-11-25
        </div>
      `;
      sidebar.innerHTML = navHtml;
    }

    const topbar = document.getElementById('app-topbar');
    if (topbar) {
      topbar.innerHTML = `
        <div class="topbar-left">
          <button type="button" class="menu-toggle" id="menu-toggle-btn" aria-label="Toggle Menu">&#9776; Menu</button>
          <span class="privacy-pill">&#128274; Anonymized Public Summary · Zero PII</span>
          <span class="decision-pill">&#9888; No Winner Selected Until Private Inputs Verified</span>
        </div>
        <div class="topbar-meta">
          Official Sources Verified: <strong>2026-11-25</strong> · <a href="flagged-review.html">Flagged Audit Log</a>
        </div>
      `;
      const btn = document.getElementById('menu-toggle-btn');
      if (btn && sidebar) {
        btn.addEventListener('click', () => sidebar.classList.toggle('open'));
      }
    }
  }

  function wireTableFilter(inputId, selectId, tableId) {
    const input = document.getElementById(inputId);
    const select = selectId ? document.getElementById(selectId) : null;
    const table = document.getElementById(tableId);
    if (!table) return;

    function apply() {
      const q = input ? input.value.trim().toLowerCase() : '';
      const cat = select ? select.value.trim().toLowerCase() : '';
      const rows = table.querySelectorAll('tbody tr');
      rows.forEach((tr) => {
        const text = tr.textContent.toLowerCase();
        const rowCat = (tr.getAttribute('data-category') || '').toLowerCase();
        const matchQ = !q || text.includes(q);
        const matchCat = !cat || rowCat === cat || text.includes(cat);
        tr.style.display = matchQ && matchCat ? '' : 'none';
      });
    }

    if (input) input.addEventListener('input', apply);
    if (select) select.addEventListener('change', apply);
  }

  function formatCurrency(num) {
    if (num === null || num === undefined || isNaN(num)) return '—';
    const abs = Math.abs(num);
    const sign = num < 0 ? '-' : '';
    return sign + '$' + Math.round(abs).toLocaleString('en-US');
  }

  function formatPct(num, digits = 2) {
    if (num === null || num === undefined || isNaN(num)) return '—';
    return (num * 100).toFixed(digits) + '%';
  }

  window.App = {
    escapeHtml,
    renderValueOrBlank,
    renderSourceLink,
    renderStatusBadge,
    injectShell,
    wireTableFilter,
    formatCurrency,
    formatPct
  };

  document.addEventListener('DOMContentLoaded', injectShell);
})();
