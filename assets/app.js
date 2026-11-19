// Evidentall — comportements de la maquette (sans dépendance).
(function () {
  var app = document.querySelector('.app');
  var head = document.querySelector('.page-head');
  var root = document.documentElement;

  // 1. Hauteur réelle de l'en-tête de page : sert à coller l'en-tête des tableaux juste dessous.
  function measure() {
    if (!head) return;
    var sticky = getComputedStyle(head).position === 'sticky';
    root.style.setProperty('--head-h', (sticky ? head.offsetHeight : 0) + 'px');
  }

  // 2. L'en-tête de page se compacte et prend une ombre dès qu'on fait défiler.
  function onScroll() {
    if (!head) return;
    var stuck = window.scrollY > 24;
    if (stuck !== head.classList.contains('is-stuck')) {
      head.classList.toggle('is-stuck', stuck);
      measure();
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', measure);
  measure();
  onScroll();

  // 3. Menu latéral : réduit sur ordinateur, tiroir sur mobile.
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-action]');
    if (!t) return;
    if (t.dataset.action === 'collapse') { app.classList.toggle('is-collapsed'); measure(); }
    if (t.dataset.action === 'menu') app.classList.toggle('menu-open');
    if (t.dataset.action === 'clear') {
      document.querySelectorAll('tbody input[type="checkbox"], th input[type="checkbox"]').forEach(function (c) { c.checked = false; });
      syncBulk();
    }
  });

  // 4. Barre d'actions groupées : visible seulement quand des lignes sont cochées.
  var bulk = document.querySelector('.bulkbar');
  function syncBulk() {
    if (!bulk) return;
    var n = document.querySelectorAll('tbody input[type="checkbox"]:checked').length;
    bulk.classList.toggle('is-on', n > 0);
    var out = bulk.querySelector('[data-count]');
    if (out) out.textContent = n + (n > 1 ? ' sélectionnées' : ' sélectionnée');
  }
  document.addEventListener('change', function (e) {
    if (!e.target.matches('input[type="checkbox"]')) return;
    if (e.target.closest('th')) {
      var table = e.target.closest('table');
      table.querySelectorAll('tbody input[type="checkbox"]').forEach(function (c) { c.checked = e.target.checked; });
    }
    syncBulk();
  });

  // 5. Filtres et sélecteurs à choix unique (pastilles, périodes).
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.chips .chip, .seg button');
    if (!b) return;
    b.parentElement.querySelectorAll('[aria-pressed]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
    b.setAttribute('aria-pressed', 'true');
  });

  // 6. Ctrl K : place le curseur dans la recherche globale.
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      var s = document.querySelector('.search input');
      if (s) s.focus();
    }
  });
})();
