/* ==========================================================================
   W-03 Decision-Gate Board, Notice Calendar Tool & Suggestions Review State
   100% client-side localStorage (optional) with one-click reset & JSON export.
   ========================================================================== */
(function () {
  const GATES_KEY = 'jackbox_w03_gate_statuses_v1';
  const SUG_KEY = 'jackbox_suggestions_review_v1';

  function loadStore(key) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : {};
    } catch (_) {
      return {};
    }
  }

  function saveStore(key, obj) {
    try { localStorage.setItem(key, JSON.stringify(obj)); } catch (_) {}
  }

  // ---- W-03 Decision-Gate Progress Board ----
  function initGatesBoard() {
    const tbody = document.getElementById('gates-tbody');
    if (!tbody || !window.JACKBOX_DATA) return;

    const gates = window.JACKBOX_DATA.gates.gates;
    const saved = loadStore(GATES_KEY);

    function render() {
      let doneCount = 0;
      tbody.innerHTML = gates.map((g) => {
        const cur = saved[g.gateId] || g.defaultStatus;
        if (cur === 'done') doneCount++;
        return `
          <tr>
            <td><strong>${App.escapeHtml(g.gateId)}</strong></td>
            <td><strong>${App.escapeHtml(g.phase)}</strong><br><span class="field-hint">${App.escapeHtml(g.ownerRole)}</span></td>
            <td>
              <select class="select-input gate-status-select" data-gate="${App.escapeHtml(g.gateId)}" aria-label="Status for ${App.escapeHtml(g.gateId)}">
                <option value="blocked" ${cur === 'blocked' ? 'selected' : ''}>Blocked — Missing Private Data</option>
                <option value="in_progress" ${cur === 'in_progress' ? 'selected' : ''}>In Progress</option>
                <option value="done" ${cur === 'done' ? 'selected' : ''}>Verified &amp; Complete</option>
              </select>
              <div style="margin-top:6px;">${App.renderStatusBadge(cur)}</div>
            </td>
            <td>${App.escapeHtml(g.blockingItems)}</td>
            <td>${App.escapeHtml(g.exitCriteria)}</td>
            <td>${App.renderSourceLink(g.sourceUrl, g.sourceLabel)}</td>
          </tr>
        `;
      }).join('');

      const pct = Math.round((doneCount / gates.length) * 100);
      const bar = document.getElementById('gates-progress-fill');
      const lbl = document.getElementById('gates-progress-label');
      const gate5Banner = document.getElementById('gate5-readiness-banner');
      if (bar) bar.style.width = pct + '%';
      if (lbl) lbl.textContent = `${doneCount} of ${gates.length} gates verified (${pct}%)`;
      if (gate5Banner) {
        if (doneCount === gates.length) {
          gate5Banner.className = 'banner banner-verified';
          gate5Banner.innerHTML = '<strong>ALL DECISION GATES VERIFIED:</strong> Ready for formal Gate-5 advisor sign-off and binding strategic commitment.';
        } else {
          gate5Banner.className = 'banner banner-warn';
          gate5Banner.innerHTML = `<strong>DECISION HOLD ACTIVE (${gates.length - doneCount} Gates Incomplete):</strong> Do NOT execute a binding sale, listing, §1031 commitment, or lease extension until Gates 0–4 are verified offline with qualified advisors.`;
        }
      }

      tbody.querySelectorAll('.gate-status-select').forEach((sel) => {
        sel.addEventListener('change', (ev) => {
          const gid = ev.target.getAttribute('data-gate');
          saved[gid] = ev.target.value;
          saveStore(GATES_KEY, saved);
          render();
        });
      });
    }

    const resetBtn = document.getElementById('btn-reset-gates');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        Object.keys(saved).forEach((k) => delete saved[k]);
        try { localStorage.removeItem(GATES_KEY); } catch (_) {}
        render();
      });
    }

    render();
  }

  // ---- Notice Calendar Reconciliation Tool (lease-calendar.html) ----
  function initNoticeCalendar() {
    const expInput = document.getElementById('nc-expiration-date');
    const noticeDaysInput = document.getElementById('nc-notice-days');
    const out = document.getElementById('nc-output');
    if (!expInput || !noticeDaysInput || !out) return;

    function addMonths(d, delta) {
      const copy = new Date(d.getTime());
      copy.setMonth(copy.getMonth() + delta);
      return copy;
    }

    function addDays(d, delta) {
      const copy = new Date(d.getTime());
      copy.setDate(copy.getDate() + delta);
      return copy;
    }

    function fmtDate(d) {
      return d.toISOString().slice(0, 10);
    }

    function render() {
      const raw = expInput.value;
      const noticeDays = parseInt(noticeDaysInput.value, 10);
      if (!raw) {
        out.innerHTML = `<p class="card-sub">Enter your private primary lease expiration date (from your attorney lease abstract — placeholder window 2030–2035) and required written option notice period (days) to generate your backward milestone calendar locally.</p>`;
        return;
      }
      const exp = new Date(raw + 'T00:00:00');
      if (isNaN(exp.getTime())) return;
      const days = Number.isFinite(noticeDays) && noticeDays > 0 ? noticeDays : 180;
      const noticeDeadline = addDays(exp, -days);
      const today = new Date('2026-11-25T00:00:00');
      const yrsRemaining = ((exp - today) / (1000 * 60 * 60 * 24 * 365.25)).toFixed(2);

      const milestones = [
        { label: 'Target Early Strategy & Lease Abstract Audit (-48 mos)', date: addMonths(exp, -48), action: 'Complete Gates 0–2 (Lease abstract, W-01 trade area, W-04 hazards, Phase I ESA).' },
        { label: 'Short-Lease Valuation Check / 3 Broker BOVs (-36 mos)', date: addMonths(exp, -36), action: 'Price current WALT vs. 10–15 yr blend-and-extend before entering <5–7 yr lender discount zone.' },
        { label: 'Negotiate Blend-and-Extend OR Launch Sale / §1031 (-24 mos)', date: addMonths(exp, -24), action: 'Commit to either formal lease extension talks or listing/marketing while sufficient WALT remains.' },
        { label: 'Pre-Notice Final Decision Checkpoint (-6 mos before Notice Deadline)', date: addMonths(noticeDeadline, -6), action: 'Finalize renewal counter-offer, re-tenanting broker RFP, or §1031 Qualified Intermediary setup.' },
        { label: `HARD CONTRACTUAL OPTION NOTICE DEADLINE (-${days} days)`, date: noticeDeadline, action: 'Reconcile certified-mail / overnight-courier delivery rules with real estate attorney.' },
        { label: 'PRIMARY LEASE EXPIRATION DATE', date: exp, action: 'Option term commences OR property reverts vacant to landlord.' }
      ];

      out.innerHTML = `
        <div class="banner banner-privacy" style="margin-bottom:12px;">
          <strong>Local-Only Calendar Computed:</strong> Implied remaining WALT as of 2026-11-25 is <strong>${yrsRemaining} years</strong>.
          This date is held only in your browser and never sent over any network.
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Milestone</th><th>Target Date</th><th>Required Action</th><th>Status vs. 2026-11-25</th></tr></thead>
            <tbody>
              ${milestones.map((m) => {
                const passed = m.date < today;
                const badge = passed
                  ? '<span class="badge badge-unverified">Past / Immediate Action</span>'
                  : '<span class="badge badge-verified">Upcoming</span>';
                return `<tr><td><strong>${App.escapeHtml(m.label)}</strong></td><td class="num"><strong>${fmtDate(m.date)}</strong></td><td>${App.escapeHtml(m.action)}</td><td>${badge}</td></tr>`;
              }).join('')}
            </tbody>
          </table>
        </div>
      `;
    }

    expInput.addEventListener('change', render);
    noticeDaysInput.addEventListener('input', render);
    render();
  }

  // ---- Site Suggestions Review Selector (suggestions.html) ----
  function initSuggestions() {
    const tbody = document.getElementById('suggestions-tbody');
    if (!tbody || !window.JACKBOX_DATA) return;
    const list = window.JACKBOX_DATA.qaSuggestions.siteSuggestions;
    const saved = loadStore(SUG_KEY);

    function render() {
      let approve = 0, defer = 0, reject = 0;
      tbody.innerHTML = list.map((s) => {
        const dec = saved[s.id] || 'review';
        if (dec === 'approve') approve++;
        else if (dec === 'defer') defer++;
        else if (dec === 'reject') reject++;
        return `
          <tr data-category="${App.escapeHtml(s.category)}">
            <td><strong>${App.escapeHtml(s.id)}</strong><br><span class="badge badge-neutral">${App.escapeHtml(s.category)}</span></td>
            <td><strong>${App.escapeHtml(s.title)}</strong><br><span class="field-hint">${App.escapeHtml(s.description)}</span></td>
            <td>${App.escapeHtml(s.decisionBenefit)}<br><span class="field-hint"><strong>Privacy:</strong> ${App.escapeHtml(s.privacyImpact)}</span></td>
            <td><strong>${App.escapeHtml(s.effort)}</strong><br><span class="field-hint">Prereq: ${App.escapeHtml(s.prerequisites)}</span></td>
            <td>
              <select class="select-input sug-select" data-sug="${App.escapeHtml(s.id)}" aria-label="Review status for ${App.escapeHtml(s.id)}">
                <option value="review" ${dec === 'review' ? 'selected' : ''}>Pending Review</option>
                <option value="approve" ${dec === 'approve' ? 'selected' : ''}>Approve for Next Phase</option>
                <option value="defer" ${dec === 'defer' ? 'selected' : ''}>Defer / Later</option>
                <option value="reject" ${dec === 'reject' ? 'selected' : ''}>Do Not Implement</option>
              </select>
            </td>
            <td>${App.renderSourceLink(s.sourceUrl, s.sourceLabel)}</td>
          </tr>
        `;
      }).join('');

      const summary = document.getElementById('suggestions-summary');
      if (summary) {
        summary.textContent = `Local Review Tally — Approved: ${approve} · Deferred: ${defer} · Rejected: ${reject} · Pending: ${list.length - approve - defer - reject}`;
      }

      tbody.querySelectorAll('.sug-select').forEach((sel) => {
        sel.addEventListener('change', (ev) => {
          saved[ev.target.getAttribute('data-sug')] = ev.target.value;
          saveStore(SUG_KEY, saved);
          render();
        });
      });
    }

    const btnExport = document.getElementById('btn-export-suggestions');
    if (btnExport) {
      btnExport.addEventListener('click', () => {
        const out = list.map((s) => ({ id: s.id, title: s.title, decision: saved[s.id] || 'review' }));
        const blob = new Blob([JSON.stringify(out, null, 2)], { type: 'application/json' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'site-suggestions-selection.json';
        a.click();
        URL.revokeObjectURL(a.href);
      });
    }

    const btnReset = document.getElementById('btn-reset-suggestions');
    if (btnReset) {
      btnReset.addEventListener('click', () => {
        Object.keys(saved).forEach((k) => delete saved[k]);
        try { localStorage.removeItem(SUG_KEY); } catch (_) {}
        render();
      });
    }

    render();
    App.wireTableFilter('sug-search', 'sug-cat-filter', 'suggestions-table');
  }

  document.addEventListener('DOMContentLoaded', () => {
    initGatesBoard();
    initNoticeCalendar();
    initSuggestions();
  });
})();
