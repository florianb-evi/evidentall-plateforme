// Evidentall — comportements de la maquette (sans dépendance).
// Tout est simulé : aucune donnée n'est envoyée ni enregistrée.
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var text = function (el) { return (el.textContent || '').replace(/\s+/g, ' ').trim(); };
  var norm = function (s) { return s.toLowerCase().replace(/s\b/g, ''); };
  var app = $('.app'), head = $('.page-head'), root = document.documentElement;

  /* ---------- En-tête collé ---------- */
  function measure() {
    if (!head) return;
    var sticky = getComputedStyle(head).position === 'sticky';
    root.style.setProperty('--head-h', (sticky ? head.offsetHeight : 0) + 'px');
  }
  function onScroll() {
    if (!head) return;
    var stuck = window.scrollY > 24;
    if (stuck !== head.classList.contains('is-stuck')) { head.classList.toggle('is-stuck', stuck); measure(); }
    closePop();
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', measure);

  /* ---------- Messages de confirmation ---------- */
  var toasts = document.createElement('div');
  toasts.className = 'toasts';
  toasts.setAttribute('role', 'status');
  toasts.setAttribute('aria-live', 'polite');
  document.body.appendChild(toasts);
  function toast(msg) {
    var t = document.createElement('div');
    t.className = 'toast';
    t.textContent = msg;
    toasts.appendChild(t);
    setTimeout(function () { t.remove(); }, 3200);
  }

  /* ---------- Menus déroulants ---------- */
  var MENUS = {
    aide: ['Visite guidée de cette page', 'Visite complète de la plateforme', 'Guide d’utilisation', 'Demander à Elia>messagerie.html#onglet-2'],
    lang: ['Français', 'English', 'עברית', 'Русский', 'العربية', '中文'],
    notifs: ['1 ticket critique en attente>service-client.html', '2 sites refusent la veille des prix>comparateur-prix.html', '7 créneaux 24h à valider>24h-dentaire.html'],
    compte: ['Mon profil>parametres.html#onglet-1', 'Paramètres>parametres.html', 'Ma journée et mes absences>rh.html', '!Se déconnecter'],
    org: ['Votre société', 'Entité 2', 'Entité 3', 'Gérer les entités>parametres.html#onglet-3'],
    row: ['Voir le détail', 'Modifier', 'Dupliquer', 'Imprimer', '!Supprimer']
  };
  var OPTIONS = {
    'Période': ['ce mois', 'aujourd’hui', 'cette semaine', 'mois dernier', '3 mois', 'cette année', 'personnalisée…'],
    'Canal': ['tous', 'Direct', 'Site internet', 'Place de marché'],
    'Paiement': ['tous', 'Payée', 'Impayée', 'Paiement partiel'],
    'Type': ['tous', 'Cabinet', 'Centre', 'Laboratoire', 'Appel', 'Visite', 'E-mail', 'Technique', 'Livraison'],
    'Commercial': ['tous', 'Florian Bonnet', 'Sans commercial'],
    'Assigné': ['tous', 'Non assigné', 'D. Yan', 'S. Peretti'],
    'Entité': ['toutes', 'Dental Groupe', 'Oofti', 'Safe Implant'],
    'Transporteur': ['tous', 'Transporteur 24 h', 'Coursier'],
    'Zone': ['toutes', 'Paris Est', 'Lyon', 'Marseille'],
    'Relance': ['toutes', 'En retard', 'Aujourd’hui']
  };
  var pop = null;
  function closePop() { if (pop) { pop.remove(); pop = null; } }
  function openPop(anchor, items, onPick, current) {
    closePop();
    pop = document.createElement('div');
    pop.className = 'pop';
    pop.setAttribute('role', 'menu');
    items.forEach(function (raw) {
      var danger = raw.charAt(0) === '!';
      var parts = raw.replace(/^!/, '').split('>');
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'menuitem');
      b.textContent = parts[0];
      if (danger) b.className = 'danger';
      if (current && parts[0] === current) b.setAttribute('aria-checked', 'true');
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        closePop();
        if (parts[1]) { window.location.href = parts[1]; return; }
        if (danger) { confirmBox(parts[0]); return; }
        onPick(parts[0]);
      });
      pop.appendChild(b);
    });
    document.body.appendChild(pop);
    var r = anchor.getBoundingClientRect();
    var left = Math.min(r.left, window.innerWidth - pop.offsetWidth - 12);
    var top = r.bottom + 6;
    if (top + pop.offsetHeight > window.innerHeight - 12) top = Math.max(12, r.top - pop.offsetHeight - 6);
    pop.style.left = Math.max(12, left) + 'px';
    pop.style.top = top + 'px';
    pop.querySelector('button').focus();
  }

  /* ---------- Fenêtres ---------- */
  function dialogEl(cls, html) {
    var d = document.createElement('dialog');
    d.className = 'modal ' + cls;
    d.innerHTML = html;
    document.body.appendChild(d);
    return d;
  }
  var confirmDlg = dialogEl('sm', '<form method="dialog"><header><h2></h2></header><div class="modal-body"><p>Cette action ne peut pas être annulée.</p></div>' +
    '<footer><button class="btn btn-ghost" value="cancel">Annuler</button><button class="btn btn-danger" value="ok">Confirmer</button></footer></form>');
  function confirmBox(label) {
    $('h2', confirmDlg).textContent = label + ' ?';
    confirmDlg.dataset.done = label + ' : fait (simulation)';
    confirmDlg.showModal();
  }
  var byLabel = {};
  function bindDialog(d) {
    (d.dataset.for || '').split('|').forEach(function (l) { if (l) byLabel[l] = d; });
    d.addEventListener('close', function () { if (d.returnValue === 'ok') toast(d.dataset.done || 'Enregistré (simulation)'); d.returnValue = ''; });
    d.addEventListener('click', function (e) { if (e.target === d) d.close('cancel'); });
  }
  $$('dialog.modal').forEach(bindDialog);

  /* ---------- Recherche globale (Ctrl K) ---------- */
  var palette = dialogEl('', '<form method="dialog"><div style="padding:16px 16px 0"><label class="search" style="max-width:none">' +
    '<input type="search" aria-label="Rechercher une page ou une action" placeholder="Aller à une page, un client, une commande…"></label></div>' +
    '<nav class="palette-list" aria-label="Résultats"></nav></form>');
  var links = $$('.side .nav a[href$=".html"]').map(function (a) { return [text(a).replace(/\d+$/, '').trim(), a.getAttribute('href')]; });
  links.push(['Nouvelle commande', 'commande-nouvelle.html'], ['Point de vente', 'ventes.html#onglet-5'], ['Fiche client : Dr Camille Renaud', 'client-fiche.html'], ['Factures', 'ventes.html#onglet-3']);
  $('.palette-list', palette).innerHTML = links.map(function (l) { return '<a href="' + l[1] + '">' + l[0] + '</a>'; }).join('');
  function filterPalette() {
    var q = norm($('input', palette).value), first = true;
    $$('.palette-list a', palette).forEach(function (a) {
      var ok = norm(text(a)).indexOf(q) !== -1;
      a.hidden = !ok;
      a.classList.toggle('is-first', ok && first);
      if (ok) first = false;
    });
  }
  $('input', palette).addEventListener('input', filterPalette);
  $('form', palette).addEventListener('submit', function (e) {
    var a = $('.palette-list a.is-first', palette);
    if (a) { e.preventDefault(); window.location.href = a.getAttribute('href'); }
  });
  palette.addEventListener('click', function (e) { if (e.target === palette) palette.close(); });
  function openPalette() { if (palette.open) return; $('input', palette).value = ''; filterPalette(); palette.showModal(); }

  /* ---------- Panneau de détail d'une ligne ---------- */
  var drawer = document.createElement('aside');
  drawer.className = 'drawer';
  drawer.setAttribute('aria-label', 'Détail');
  drawer.innerHTML = '<header><h2></h2><button type="button" class="btn btn-sm" data-action="drawer-close">Fermer</button></header><div class="drawer-body"></div><footer></footer>';
  document.body.appendChild(drawer);
  function openDrawer(title, pairs, actions) {
    $('h2', drawer).textContent = title;
    $('.drawer-body', drawer).innerHTML = '<dl>' + pairs.map(function (p) { return '<dt>' + p[0] + '</dt><dd>' + p[1] + '</dd>'; }).join('') + '</dl>';
    $('footer', drawer).innerHTML = actions.map(function (a, i) { return '<button type="button" class="btn ' + (i === actions.length - 1 ? 'btn-primary' : '') + '">' + a + '</button>'; }).join('');
    drawer.classList.add('is-on');
  }
  function rowDrawer(link) {
    var tr = link.closest('tr'), heads = $$('th', tr.closest('table')).map(text), pairs = [];
    $$('td', tr).forEach(function (td, i) {
      var h = heads[i], v = (td.innerText || '').trim().replace(/\s*\n+\s*/g, ' · ');
      if (h && v && !/action/i.test(h) && !td.querySelector('input')) pairs.push([h, v]);
    });
    var acts = $$('.row-actions .btn:not(.btn-icon)', tr).map(text);
    openDrawer(text(link), pairs, ['Imprimer', 'Modifier'].concat(acts));
  }

  /* ---------- Onglets ---------- */
  var primary = $('.head-row .btn-primary'), primaryDefault = primary ? text(primary) : '';
  function showTab(i, silent) {
    var tabs = $$('.tabs [role="tab"]');
    if (!tabs.length || !$('.panel[data-panel="' + i + '"]')) return;
    tabs.forEach(function (t) { t.setAttribute('aria-selected', t.dataset.tab === String(i) ? 'true' : 'false'); });
    $$('.panel').forEach(function (p) { p.hidden = p.dataset.panel !== String(i); });
    var panel = $('.panel[data-panel="' + i + '"]');
    if (primary) {
      var lab = panel.dataset.primary;
      primary.hidden = lab === '';
      primary.style.display = lab === '' ? 'none' : '';
      (primary.querySelector('span') || primary).textContent = lab || primaryDefault;
    }
    if (!silent) { try { history.replaceState(null, '', '#onglet-' + i); } catch (err) { /* ouverture en fichier local */ } }
    syncBulk();
    measure();
  }
  function tabFromHash() {
    var m = /#onglet-(\d+)/.exec(window.location.hash);
    if (m) showTab(m[1], true);
  }
  window.addEventListener('hashchange', tabFromHash);

  /* ---------- Filtres de liste ---------- */
  function applyFilters(card) {
    var q = norm(($('.filters input[type="search"]', card) || {}).value || '');
    var chip = $('.chips .chip[aria-pressed="true"]', card);
    var key = chip && chip !== chip.parentElement.firstElementChild ? norm(text(chip).replace(/[\d\s]+$/, '')) : '';
    var extra = (card.dataset.pick || '');
    var rows = $$('tbody tr', card), shown = 0;
    rows.forEach(function (tr) {
      if (tr.classList.contains('no-result')) return;
      var t = norm(text(tr));
      var ok = t.indexOf(q) !== -1 && t.indexOf(key) !== -1 && t.indexOf(extra) !== -1;
      tr.hidden = !ok;
      if (ok) shown++;
    });
    var body = $('tbody', card);
    if (!body) return;
    var none = $('.no-result', body);
    if (!shown && !none) {
      none = document.createElement('tr');
      none.className = 'no-result';
      none.innerHTML = '<td colspan="20"><div class="empty" style="padding:28px"><h2>Aucun résultat</h2><p>Modifiez la recherche ou les filtres.</p></div></td>';
      body.appendChild(none);
    }
    if (none) none.hidden = shown > 0;
  }
  document.addEventListener('input', function (e) {
    var card = e.target.matches('.filters input[type="search"]') && e.target.closest('.card');
    if (card) applyFilters(card);
  });

  /* ---------- Sélection et actions groupées ---------- */
  function syncBulk() {
    var panel = $('.panel:not([hidden])') || document;
    $$('.bulkbar').forEach(function (bulk) {
      var mine = bulk.closest('.panel') === panel || !bulk.closest('.panel');
      var n = mine ? $$('tbody input[type="checkbox"]:checked', panel).length : 0;
      bulk.classList.toggle('is-on', n > 0);
      var out = $('[data-count]', bulk);
      if (out) out.textContent = n + (n > 1 ? ' sélectionnées' : ' sélectionnée');
    });
  }
  function clearChecks() { $$('table input[type="checkbox"]').forEach(function (c) { c.checked = false; }); syncBulk(); }
  document.addEventListener('change', function (e) {
    if (!e.target.matches('table input[type="checkbox"]')) return;
    if (e.target.closest('th')) $$('tbody input[type="checkbox"]', e.target.closest('table')).forEach(function (c) { c.checked = e.target.checked; });
    syncBulk();
  });

  /* ---------- Pointage ---------- */
  var clocked = false;
  try { clocked = localStorage.getItem('ev-clock') === '1'; } catch (err) { /* stockage indisponible */ }
  function paintClock() {
    $$('[data-action="clock"]').forEach(function (b) { (b.querySelector('span') || b).textContent = clocked ? 'Terminer ma journée' : 'Démarrer ma journée'; });
  }

  /* ---------- Un seul écouteur pour tous les clics ---------- */
  document.addEventListener('click', function (e) {
    if (pop && !e.target.closest('.pop')) closePop();
    var el = e.target.closest('button, a, [data-action]');
    if (!el || el.closest('dialog') || el.closest('.pop')) return;
    var act = el.dataset.action, lab = text(el);

    if (act === 'collapse') { e.preventDefault(); app.classList.toggle('is-collapsed'); measure(); return; }
    if (act === 'menu') { app.classList.toggle('menu-open'); return; }
    if (act === 'clear') { clearChecks(); return; }
    if (act === 'drawer-close') { drawer.classList.remove('is-on'); return; }
    if (act === 'palette') { e.preventDefault(); openPalette(); return; }
    if (act === 'theme') {
      var dark = root.dataset.theme !== 'dark';
      if (dark) root.dataset.theme = 'dark'; else delete root.dataset.theme;
      try { localStorage.setItem('ev-theme', dark ? 'dark' : 'light'); } catch (err) { /* stockage indisponible */ }
      el.setAttribute('aria-label', dark ? 'Activer le mode jour' : 'Activer le mode nuit');
      toast(dark ? 'Mode nuit activé' : 'Mode jour activé');
      return;
    }
    if (act === 'clock') {
      clocked = !clocked;
      try { localStorage.setItem('ev-clock', clocked ? '1' : '0'); } catch (err) { /* stockage indisponible */ }
      paintClock();
      toast(clocked ? 'Journée démarrée. Bon courage !' : 'Journée terminée. À demain !');
      return;
    }
    if (el.matches('[role="tab"]')) { showTab(el.dataset.tab); return; }
    if (el.matches('.chips .chip, .seg button')) {
      $$('[aria-pressed]', el.parentElement).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      el.setAttribute('aria-pressed', 'true');
      var c = el.closest('.card');
      if (c) applyFilters(c);
      return;
    }
    // Bouton « … » d'une ligne : menu d'actions par défaut
    if (el.matches('.btn-icon') && !el.dataset.menu && el.closest('.row-actions, td, .item, .card-head')) el.dataset.menu = 'row';
    if (el.dataset.menu) {
      e.stopPropagation();
      var items = MENUS[el.dataset.menu] || el.dataset.menu.split('|');
      openPop(el, items, function (choice) {
        if (el.dataset.menu === 'lang') { $('span', el).textContent = { 'Français': 'FR', 'English': 'EN', 'עברית': 'HE', 'Русский': 'RU', 'العربية': 'AR', '中文': 'ZH' }[choice]; toast('Langue : ' + choice); return; }
        if (el.dataset.menu === 'org') { $('b', el).textContent = choice; toast('Société active : ' + choice); return; }
        var tr = el.closest('tr'), ref = tr && $('a', tr);
        if (choice === 'Voir le détail' && ref) { rowDrawer(ref); return; }
        toast(choice + (ref ? ' · ' + text(ref) : '') + ' (simulation)');
      });
      return;
    }
    if (el.matches('.filters .btn') && lab.indexOf(' : ') !== -1) {
      e.stopPropagation();
      var name = lab.split(' : ')[0], cur = lab.split(' : ')[1];
      openPop(el, OPTIONS[name] || ['tous', 'toutes'], function (choice) {
        el.firstChild.textContent = name + ' : ' + choice;
        var card = el.closest('.card');
        if (!card) return;
        var k = /^tou/.test(choice) ? '' : norm(choice);
        var hit = k && $$('tbody tr', card).some(function (tr) { return norm(text(tr)).indexOf(k) !== -1; });
        card.dataset.pick = hit ? k : '';
        applyFilters(card);
      }, cur);
      return;
    }
    if (byLabel[lab]) {
      e.preventDefault();
      var d = byLabel[lab], tr2 = el.closest('tr, .item'), who = tr2 && $('a, b', tr2);
      var sub = $('[data-context]', d);
      if (sub) sub.textContent = who ? text(who) : '';
      d.showModal();
      return;
    }
    if (el.closest('.bulkbar')) {
      var n = $$('tbody input[type="checkbox"]:checked', $('.panel:not([hidden])') || document).length;
      toast(lab + ' : ' + n + ' élément' + (n > 1 ? 's' : '') + ' (simulation)');
      clearChecks();
      return;
    }
    if (el.matches('.slot')) {
      var st = text(el).replace(/^\d+ h/, '').trim();
      openDrawer('Créneau de ' + $('b', el).textContent, [['État', st], ['Produit', st === 'Libre' ? 'Aucun produit' : 'Produit du créneau'], ['Prix promo', st === 'Libre' ? '—' : 'Voir la fiche'], ['Seuil d’achat', '10 acheteurs']],
        st === 'À valider' ? ['Changer de produit', 'Valider'] : st === 'Libre' ? ['Choisir un produit'] : ['Voir le produit']);
      return;
    }
    if (el.matches('.mail-item')) {
      e.preventDefault();
      $$('.mail-item', el.parentElement).forEach(function (x) { x.removeAttribute('aria-current'); });
      el.setAttribute('aria-current', 'true');
      return;
    }
    var href = el.getAttribute('href');
    if (el.tagName === 'A' && href && href !== '#') return; // vrai lien : navigation normale
    if (el.tagName === 'A') e.preventDefault();
    if (el.tagName === 'A' && el.closest('td') && el.closest('tr') && !el.closest('.row-actions')) { rowDrawer(el); return; }
    var row = el.closest('tr, .item'), ref2 = row && $('a, b', row);
    if (el.type === 'submit' && el.form) return;
    toast((lab || el.getAttribute('aria-label') || 'Action') + (ref2 && ref2 !== el ? ' · ' + text(ref2) : '') + ' (simulation)');
  });

  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openPalette(); }
    if (e.key === 'Escape') { closePop(); drawer.classList.remove('is-on'); app.classList.remove('menu-open'); }
  });
  document.addEventListener('focusin', function (e) { if (e.target.matches('.topbar .search input')) { e.target.blur(); openPalette(); } });
  $$('form:not([method="dialog"])').forEach(function (f) { f.addEventListener('submit', function (e) { e.preventDefault(); toast('Enregistré (simulation)'); }); });

  var first = $('.tabs [role="tab"][aria-selected="true"]');
  if (first) showTab(first.dataset.tab, true);
  paintClock();
  measure();
  onScroll();
  tabFromHash();
})();
