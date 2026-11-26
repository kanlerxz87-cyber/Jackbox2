// Shared navigation for the root dashboard pages.
// One source of truth so no page drifts and no link breaks.
(function () {
  var PAGES = [
    ['index.html',            'Dashboard'],
    ['executive-summary.html','Executive Summary'],
    ['decision-gates.html',   'Decision Gates'],
    ['trade-area.html',       'Trade Area'],
    ['hazards.html',          'Hazards'],
    ['sell-vs-hold.html',     'Sell vs Hold'],
    ['risks.html',            'Risks'],
    ['questions.html',        'Questions'],
    ['suggestions.html',      'Suggestions'],
    ['flagged.html',          'Flagged for Review'],
    ['printable-summary.html','Printable'],
    ['sources.html',          'Sources']
  ];
  function build() {
    var nav = document.getElementById('site-nav');
    if (!nav) return;
    var here = location.pathname.split('/').pop() || 'index.html';
    var html = '';
    for (var i = 0; i < PAGES.length; i++) {
      var active = (PAGES[i][0] === here) ? ' class="active"' : '';
      html += '<a' + active + ' href="' + PAGES[i][0] + '">' + PAGES[i][1] + '</a>';
    }
    nav.innerHTML = html;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();
})();
