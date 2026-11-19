#!/usr/bin/env python3
"""Génère les pages HTML de la maquette Evidentall à la racine du dépôt.

Usage : python3 tools/build.py
Le menu, la barre supérieure et l'en-tête de page sont définis une seule fois ici ;
chaque page ne décrit que son contenu. Toutes les données affichées sont fictives.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ICONS = {
    'grid': 'M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z',
    'chart': 'M4 20V10M10 20V4M16 20v-7M2 20h20',
    'mail': 'M3 6h18v12H3zM3 7l9 6 9-6',
    'cart': 'M3 4h2l2.4 11h10.2L20 7H6.2M9 20a1 1 0 1 0 0-2 1 1 0 0 0 0 2zM17 20a1 1 0 1 0 0-2 1 1 0 0 0 0 2z',
    'users': 'M16 20v-1.5a3.5 3.5 0 0 0-3.5-3.5h-5A3.5 3.5 0 0 0 4 18.5V20M10 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM20 20v-1.5a3.5 3.5 0 0 0-2.5-3.3M15.5 4.2a3.5 3.5 0 0 1 0 6.6',
    'target': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8z',
    'headset': 'M4 14v-2a8 8 0 0 1 16 0v2M4 14h3v5H5a1 1 0 0 1-1-1zM20 14h-3v5h2a1 1 0 0 0 1-1z',
    'box': 'M12 3l8 4.5v9L12 21l-8-4.5v-9zM4 7.5l8 4.5 8-4.5M12 12v9',
    'trend': 'M4 17l5-5 4 4 7-8M15 8h5v5',
    'book': 'M5 4h13v16H6.5A1.5 1.5 0 0 1 5 18.5zM5 18.5A1.5 1.5 0 0 1 6.5 17H18',
    'clock': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2',
    'bag': 'M5 8h14l-1 12H6zM9 8V6a3 3 0 0 1 6 0v2',
    'truck': 'M2 6h11v10H2zM13 9h4l4 4v3h-8zM6.5 19a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zM17.5 19a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z',
    'pin': 'M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11zM12 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z',
    'key': 'M8 15a4 4 0 1 1 3.9-5H21v3h-2v3h-3v-3h-4.1A4 4 0 0 1 8 15z',
    'folder': 'M3 6h6l2 2h10v11H3z',
    'team': 'M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1',
    'plus': 'M12 5v14M5 12h14',
    'search': 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM20 20l-4-4',
    'down': 'M12 4v11M7 10l5 5 5-5M4 20h16',
    'print': 'M7 8V4h10v4M5 8h14v8h-2v4H7v-4H5zM9 14h6',
    'more': 'M5 12h.01M12 12h.01M19 12h.01',
    'check': 'M5 12l5 5 9-10',
    'alert': 'M12 3l10 18H2zM12 10v5M12 18h.01',
    'help': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5M12 16.5h.01',
    'bell': 'M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 21h4',
    'play': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM10 8.5l5 3.5-5 3.5z',
    'menu': 'M4 7h16M4 12h16M4 17h16',
    'panel': 'M4 5h16v14H4zM9 5v14M15 10l-2 2 2 2',
    'gear': 'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM4 12h2M18 12h2M12 4v2M12 18v2M6.3 6.3l1.4 1.4M16.3 16.3l1.4 1.4M6.3 17.7l1.4-1.4M16.3 7.7l1.4-1.4',
    'pos': 'M3 6h18v12H3zM3 10h18M7 15h3',
    'send': 'M4 12l16-8-6 16-3-6z',
    'filter': 'M4 6h16M7 12h10M10 18h4',
    'upload': 'M12 16V5M7 10l5-5 5 5M4 20h16',
    'back': 'M15 6l-9 6 9 6',
    'globe': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM3 12h18M12 3c2.5 2.5 3.5 5.5 3.5 9s-1 6.5-3.5 9c-2.5-2.5-3.5-5.5-3.5-9s1-6.5 3.5-9z',
    'stop': 'M6 6h12v12H6z',
}

NAV = [
    ('Pilotage', [('dashboard', 'Tableau de bord', 'grid', 'index.html', '', ''),
                  ('stats', 'Statistiques', 'chart', 'statistiques.html', '', ''),
                  ('mail', 'Messagerie', 'mail', 'messagerie.html', '3', '')]),
    ('Commerce', [('ventes', 'Ventes', 'cart', 'ventes.html', '237', 'alert'),
                  ('clients', 'Clients', 'users', 'clients.html', '', ''),
                  ('prospection', 'Prospection', 'target', 'prospection.html', '3', ''),
                  ('sav', 'Service client', 'headset', 'service-client.html', '5', '')]),
    ('Catalogue', [('produits', 'Produits et stock', 'box', 'produits.html', '', ''),
                   ('prix', 'Comparateur de prix', 'trend', 'comparateur-prix.html', '50', ''),
                   ('partenaires', 'Catalogues partenaires', 'book', 'catalogues-partenaires.html', '', ''),
                   ('24h', '24h Dentaire', 'clock', '24h-dentaire.html', '7', '')]),
    ('Logistique', [('achats', 'Achats', 'bag', 'achats.html', '', ''),
                    ('expeditions', 'Expéditions', 'truck', 'expeditions.html', '', ''),
                    ('ramassage', 'Ramassage', 'pin', 'ramassage.html', '', ''),
                    ('locations', 'Locations', 'key', 'locations.html', '', '')]),
    ('Équipe et documents', [('rh', 'Ressources humaines', 'team', 'rh.html', '', ''),
                             ('docs', 'Documents', 'folder', 'documents.html', '', '')]),
]


# ---------- Briques ----------
def ico(n):
    return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS[n]}"/></svg>'


def btn(label, kind='', icon=None, href=None, sm=False, attrs=''):
    cls = 'btn' + (f' btn-{kind}' if kind else '') + (' btn-sm' if sm else '')
    inner = (ico(icon) if icon else '') + f'<span>{label}</span>'
    if href:
        return f'<a class="{cls}" href="{href}" {attrs}>{inner}</a>'
    return f'<button type="button" class="{cls}" {attrs}>{inner}</button>'


def kebab(label='Autres actions'):
    return f'<button type="button" class="btn btn-sm btn-icon" aria-label="{label}">{ico("more")}</button>'


def acts(label=None, kind='soft', more=True):
    a = btn(label, kind, sm=True) if label else ''
    return f'<div class="row-actions">{a}{kebab() if more else ""}</div>'


def badge(text, tone='', dot=True):
    return f'<span class="badge {tone}{" dot" if dot else ""}">{text}</span>'


def c(main, small=''):
    return f'<b>{main}</b>' + (f'<small>{small}</small>' if small else '')


def kpis(items):
    cells = ''.join(f'<div class="kpi"><span class="kpi-label">{l}</span><span class="kpi-value num">{v}</span>'
                    f'<span class="kpi-note">{n}</span></div>' for l, v, n in items)
    return f'<section class="kpis" aria-label="Indicateurs">{cells}</section>'


def tabs(items, active=0):
    out = ''
    for i, it in enumerate(items):
        label, count = it if isinstance(it, tuple) else (it, '')
        cur = ' aria-current="true"' if i == active else ''
        out += f'<a href="#"{cur}>{label}{f"<span class=count>{count}</span>" if count else ""}</a>'
    return f'<nav class="tabs" aria-label="Sections de la page">{out}</nav>'


def chips(items, label='Filtrer par statut'):
    out = ''
    for i, (l, n, state) in enumerate(items):
        cls = 'chip alert' if state == 'alert' else 'chip'
        out += f'<button type="button" class="{cls}" aria-pressed="{"true" if i == 0 else "false"}">{l}<b class="num">{n}</b></button>'
    return f'<div class="chips" role="group" aria-label="{label}">{out}</div>'


def filters(placeholder, selects=(), more=True):
    out = (f'<label class="search" style="flex:2 1 260px;max-width:none;background:#fff">{ico("search")}'
           f'<input type="search" aria-label="Rechercher" placeholder="{placeholder}"></label>')
    for s in selects:
        out += f'<button type="button" class="btn" style="flex:1 1 150px;justify-content:space-between">{s}{ico("filter")}</button>'
    if more:
        out += btn('Plus de filtres', 'ghost', 'filter')
    return f'<div class="filters">{out}</div>'


def table(cols, rows, check=False, name='la ligne'):
    head = '<th style="width:44px"><input type="checkbox" aria-label="Tout sélectionner"></th>' if check else ''
    for col in cols:
        label, align = col if isinstance(col, tuple) else (col, '')
        head += f'<th scope="col" class="{"right" if align else ""}">{label}</th>'
    body = ''
    for r in rows:
        body += '<tr>' + (f'<td><input type="checkbox" aria-label="Sélectionner {name}"></td>' if check else '')
        for col, cell in zip(cols, r):
            right = isinstance(col, tuple)
            body += f'<td class="{"right num" if right else ""}">{cell}</td>'
        body += '</tr>'
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def pager(text, page='Page 1 sur 12'):
    return (f'<div class="pager"><span>{text}</span><div>{btn("Précédent", sm=True)}<b>{page}</b>'
            f'{btn("Suivant", sm=True)}</div></div>')


def card(inner, pad=True, cls=''):
    return f'<section class="card {"card-pad" if pad else ""} {cls}">{inner}</section>'


def list_card(bar, tbl, foot=''):
    return card(f'<div class="card-bar">{bar}</div>{tbl}{foot}', pad=False)


def head(title, action=''):
    return f'<div class="card-head"><h2>{title}</h2>{action}</div>'


def empty(icon, title, text, cta=''):
    return f'<div class="empty"><span class="tile">{ico(icon)}</span><h2>{title}</h2><p>{text}</p>{cta}</div>'


def meter(pct, color=''):
    style = f'width:{pct}%' + (f';background:{color}' if color else '')
    return f'<div class="meter"><i style="{style}"></i></div>'


def bulkbar(primary, others=()):
    o = ''.join(btn(x, sm=True) for x in others)
    return (f'<div class="bulkbar" role="region" aria-label="Actions sur la sélection"><b data-count>0 sélectionnée</b>'
            f'{btn(primary, "primary", sm=True)}{o}'
            f'<button type="button" class="btn btn-sm btn-ghost" data-action="clear" style="color:#fff">Annuler</button></div>')


def item(title, small, right='', tone='', icon=None, soft=False):
    t = f'<span class="tile {tone}">{ico(icon)}</span>' if icon else ''
    return (f'<div class="item{" soft" if soft else ""}">{t}<div class="item-main"><b>{title}</b>'
            f'<small>{small}</small></div>{right}</div>')


# ---------- Gabarit ----------
def shell(slug, title, sub, actions, body, tab_html='', back=None):
    nav = ''
    for label, items in NAV:
        links = ''
        for sid, lab, icon, href, count, alert in items:
            cur = ' aria-current="page"' if sid == slug else ''
            cnt = f'<b class="count {alert}">{count}</b>' if count else ''
            links += f'<a href="{href}"{cur} title="{lab}">{ico(icon)}<span>{lab}</span>{cnt}</a>'
        nav += f'<div class="nav-group"><div class="nav-label">{label}</div>{links}</div>'
    backlink = f'<a href="{back[1]}" class="small" style="display:inline-flex;align-items:center;gap:4px">{ico("back")}{back[0]}</a>' if back else ''
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Evidentall</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap">
<link rel="icon" type="image/svg+xml" href="assets/logo-symbole.svg">
<link rel="stylesheet" href="assets/app.css">
</head>
<body>
<a class="sr" href="#contenu">Aller au contenu</a>
<div class="app">
<aside class="side">
<a class="logo" href="index.html" aria-label="Evidentall, tableau de bord"><img class="full" src="assets/logo-bleus.svg" alt="Evidentall, le pilotage intelligent" width="196" height="57"><img class="mark" src="assets/logo-symbole.svg" alt="" width="40" height="44"></a>
<button type="button" class="org">{ico("globe")}<span><small>Société active</small><b>Votre société</b></span></button>
<nav class="nav" aria-label="Navigation principale" style="display:flex;flex-direction:column;gap:16px">{nav}</nav>
<div class="side-foot nav">
<a href="#" title="Paramètres">{ico("gear")}<span>Paramètres</span></a>
<a href="#" data-action="collapse" title="Réduire le menu">{ico("panel")}<span>Réduire le menu</span></a>
</div>
</aside>
<div class="main">
<header class="topbar">
<button type="button" class="btn btn-icon menu-btn" data-action="menu" aria-label="Ouvrir le menu">{ico("menu")}</button>
<label class="search">{ico("search")}<input type="search" aria-label="Rechercher dans Evidentall" placeholder="Rechercher un client, une commande, un produit…"><span class="kbd hide-sm">Ctrl K</span></label>
<span class="spacer"></span>
<a class="btn hide-sm" href="rh.html" style="color:var(--ok-fg)">{ico("play")}<span style="color:var(--ink)">Démarrer ma journée</span></a>
<button type="button" class="btn hide-sm">{ico("help")}<span>Aide</span></button>
<button type="button" class="btn hide-sm" aria-label="Langue : français">{ico("globe")}<span>FR</span></button>
<button type="button" class="btn btn-icon" aria-label="Notifications : 3 nouvelles">{ico("bell")}</button>
<button type="button" class="btn btn-ghost" aria-label="Compte de Florian Bonnet" style="padding:0 6px"><span class="avatar">FB</span></button>
</header>
<div class="page-head">
<div class="head-row">
<div>{backlink}<h1>{title}</h1><p class="sub">{sub}</p></div>
<div class="actions">{actions}</div>
</div>
{tab_html}
</div>
<main class="content" id="contenu">
{body}
</main>
</div>
</div>
<script src="assets/app.js"></script>
</body>
</html>
'''


PAGES = {}


def page(file, *args, **kw):
    PAGES[file] = shell(*args, **kw)


ST = {'prep': badge('En préparation', 'info'), 'exp': badge('Expédiée', 'ok'), 'liv': badge('Livrée', 'ok'),
      'att': badge('En attente'), 'ret': badge('En retard', 'danger'), 'bro': badge('Brouillon')}
PAY = {'ok': badge('Payée', 'ok'), 'no': badge('Impayée', 'danger'), 'part': badge('Paiement partiel', 'warn')}

# ---------- 1. Tableau de bord ----------
months = [('Déc', 188), ('Jan', 172), ('Fév', 196), ('Mar', 224), ('Avr', 205), ('Mai', 214), ('Juin', 238),
          ('Juil', 190), ('Août', 141), ('Sep', 229), ('Oct', 221), ('Nov', 128)]
bars = ''.join(f'<div class="bar{" now" if i == 11 else ""}"><b class="num">{v}</b><div class="track">'
               f'<i style="height:{round(v * .8)}px"></i></div><span>{m}</span></div>' for i, (m, v) in enumerate(months))
chart = (head('Chiffre d’affaires sur 12 mois', '<a href="statistiques.html">Analyse détaillée</a>')
         + f'<div class="bars" role="img" aria-label="Chiffre d’affaires HT mensuel, en milliers d’euros">{bars}</div>'
         + '<p class="small muted">En milliers d’euros HT · mois en cours en bleu vif (partiel)</p>')
todo = head('À traiter aujourd’hui', badge('4', 'danger', False)) + '<div class="list">' + ''.join([
    item('517 factures échues', '81 200 € à recouvrer', btn('Relancer', 'soft', sm=True), 'danger', 'alert'),
    item('237 commandes en retard', 'Échéance dépassée', btn('Voir', 'soft', href='ventes.html', sm=True), 'warn', 'clock'),
    item('148 commandes à préparer', 'Dont 62 partielles', btn('Préparer', 'soft', href='expeditions.html', sm=True), '', 'box'),
    item('5 tickets service client', '1 ticket critique', btn('Ouvrir', 'soft', href='service-client.html', sm=True), '', 'headset'),
]) + '</div>'
orders = [('CMD-11682', 'Direct', 'Dr Camille Renaud', 'prep', 'no', '105,00 €'),
          ('CMD-11681', 'Site internet', 'Cabinet dentaire des Lilas', 'prep', 'ok', '127,58 €'),
          ('CMD-11680', 'Place de marché', 'Centrale Dentaire Exemple', 'exp', 'ok', '610,60 €'),
          ('CMD-11679', 'Site internet', 'SELARL Morel et Associés', 'prep', 'ok', '234,59 €'),
          ('CMD-11678', 'Direct', 'Centre dentaire Voltaire', 'ret', 'part', '1 840,00 €')]
last = head('Dernières commandes', btn('Tout voir', href='ventes.html', sm=True))
last_t = table(['Commande', 'Client', 'Statut', 'Paiement', ('Montant', 'r')],
               [[f'<a href="ventes.html">{r}</a><small>{ca}</small>', f'<b>{cl}</b>', ST[s], PAY[p], f'<b>{m}</b>'] for r, ca, cl, s, p, m in orders])
flow = (head('Suivi des commandes')
        + '<div class="split" role="img" aria-label="129 en attente, 148 en préparation, 397 expédiées, 237 en retard">'
          '<i style="flex:129;background:#B8C4D3"></i><i style="flex:148;background:#0077FD"></i>'
          '<i style="flex:397;background:#12925A"></i><i style="flex:237;background:#B3261E"></i></div><div class="list">'
        + ''.join(f'<a class="item soft" href="ventes.html" style="color:var(--ink)"><span class="item-main"><b>{l}</b></span>'
                  f'<b class="num {k}">{n}</b></a>' for l, n, k in
                  [('En attente', 129, ''), ('En préparation', 148, ''), ('Expédiées ce mois', 397, ''), ('En retard', 237, 'late')])
        + '</div><p class="small muted">Délai médian entre commande et expédition : <b>0,6 jour</b></p>')
dues = head('Factures à relancer', '<a href="#">Tout voir</a>') + '<div class="list">' + ''.join(
    item(n, f'<span class="{k}">{d}</span>', f'<b class="num">{m}</b>' + btn('Relancer', 'soft', sm=True), soft=True)
    for n, d, k, m in [('Laboratoire Prothésia', 'Échue depuis 4 jours', 'late', '2 100,00 €'),
                       ('SCM Dentaire du Parc', 'Échue depuis 4 jours', 'late', '1 315,00 €'),
                       ('Dr Sophie Marchand', 'Échéance aujourd’hui', '', '2 079,00 €')]) + '</div>'
top = head('Top 5 produits du mois') + '<div class="list" style="gap:14px">' + ''.join(
    f'<div><div class="total-line"><span>{n}</span><b class="num">{a}</b></div>{meter(p)}</div>' for n, a, p in
    [('Substitut osseux — boîte de 6', '66 400 €', 100), ('Journée de formation', '6 870 €', 22),
     ('Scanner intra-oral', '3 800 €', 14), ('Kit de chirurgie — carton de 10', '2 340 €', 10),
     ('Résine composite A3,5', '1 960 €', 8)]) + '</div>'
marge = (head('Marge brute', badge('À compléter', 'warn', False))
         + '<p>Votre marge ne peut pas encore être calculée : seul 1 % du chiffre d’affaires porte sur des produits dont le prix d’achat est renseigné.</p>'
         + meter(2, '#E08A00') + btn('Renseigner les prix d’achat', 'primary', href='produits.html'))
page('index.html', 'dashboard', 'Bonjour Florian', 'Jeudi 19 novembre 2026 · 4 points demandent votre attention',
     '<div class="seg" role="group" aria-label="Période"><button aria-pressed="false">Jour</button><button aria-pressed="false">Semaine</button>'
     '<button aria-pressed="true">Mois</button><button aria-pressed="false">Personnalisé</button></div>'
     + btn('Point de vente', icon='pos') + btn('Nouvelle commande', 'primary', 'plus', 'commande-nouvelle.html'),
     kpis([('Chiffre d’affaires HT', '128 400 €', '<span class="up">+8,3 %</span> vs octobre'),
           ('Encaissements', '112 900 €', '<span class="up">+3,0 %</span> · 78 % du facturé'),
           ('Reste à encaisser', '96 300 €', '<span class="late">38 % à plus de 90 jours</span>'),
           ('Commandes', '450', '<span class="down">−5,6 %</span> · panier moyen 315 €')])
     + f'<div class="cols"><div class="grow">{card(chart)}</div><div class="aside">{card(todo)}</div></div>'
     + f'<div class="cols"><div class="grow">{card(f"<div class=card-bar>{last}</div>{last_t}", pad=False)}</div><div class="aside">{card(flow)}</div></div>'
     + f'<div class="grid">{card(dues)}{card(top)}{card(marge)}</div>')

# ---------- 2. Statistiques ----------
page('statistiques.html', 'stats', 'Statistiques', 'Analyse détaillée de votre activité',
     btn('Ce mois : 1 au 30 nov.', icon='filter') + btn('Exporter', icon='down'),
     kpis([('Chiffre d’affaires HT', '128 400 €', 'Factures validées, avoirs déduits'), ('Commandes', '450', 'Hors devis, annulées et brouillons'),
           ('Panier moyen', '315 €', 'HT par facture'), ('Marge brute', 'Non calculée', '<a href="produits.html">Renseigner les prix d’achat</a>')])
     + f'<div class="cols"><div class="grow">{card(chart)}</div><div class="aside">'
     + card(head('Répartition par catégorie') + empty('box', 'Aucune catégorie à afficher', 'La plupart de vos produits vendus ce mois n’ont pas de catégorie.', btn('Catégoriser les produits', 'soft', href='produits.html')))
     + '</div></div>',
     tabs(['Aperçu', 'Anticipation IA', 'Commerciaux', 'Produits et marques', 'Clients et villes', 'Objectifs', 'Charges', 'Finances']))

# ---------- 3. Messagerie ----------
mails = [('Cabinet dentaire des Lilas', 'Question sur la commande CMD-11681', '14 h 05', True),
         ('Laboratoire Prothésia', 'Demande de devis scanner intra-oral', '11 h 40', False),
         ('Dr Hugo Lambert', 'Changement d’adresse de livraison', 'Hier', False)]
folders = ''.join(f'<a class="mail-item" href="#"{" aria-current=true" if i == 0 else ""}>{f}</a>' for i, f in
                  enumerate(['Réception (3)', 'Envoyés', 'Brouillons', 'Indésirables', 'Corbeille', 'Archives']))
mlist = ''.join(f'<a class="mail-item" href="#"{" aria-current=true" if cur else ""}><b>{s}</b><small class="muted" style="float:right">{t}</small>'
                f'<div>{o}</div></a>' for s, o, t, cur in mails)
reading = ('<div class="card-head"><h2>Question sur la commande CMD-11681</h2><div class="actions">' + btn('Archiver', sm=True) + kebab() + '</div></div>'
           '<p class="muted">Cabinet dentaire des Lilas · aujourd’hui à 14 h 05</p>'
           '<p>Bonjour, pouvez-vous me confirmer la date d’expédition de notre commande passée ce matin ? Merci d’avance.</p>'
           '<a class="item soft" href="ventes.html" style="color:var(--ink)"><span class="item-main"><b>CMD-11681 · 127,58 €</b><small>En préparation · payée</small></span>' + badge('Commande liée', 'info', False) + '</a>'
           f'<div class="reply"><input aria-label="Votre réponse" placeholder="Écrire une réponse…">{btn("Envoyer", "primary", "send", sm=True)}</div>')
page('messagerie.html', 'mail', 'Messagerie', 'Vos e-mails professionnels, reliés aux clients et aux commandes',
     btn('Connecter une boîte', icon='mail') + btn('Nouveau message', 'primary', 'plus'),
     card(f'<div class="mail"><nav aria-label="Dossiers">{folders}</nav><div>{mlist}</div><article>{reading}</article></div>', pad=False),
     tabs([('Courrier', '3'), 'Outils', 'Assistant Elia', 'Réseaux sociaux']))

# ---------- 4. Ventes ----------
vrows = [('CMD-11682', 'Facture provisoire', 'Dr Camille Renaud', 'Direct', '19 nov.', 'Échéance 19 déc.', 'prep', 'no', '105,00 €', 'Expédier'),
         ('CMD-11681', 'FA-2611-0932', 'Cabinet dentaire des Lilas', 'Site internet', '19 nov.', 'Échéance 26 nov.', 'prep', 'ok', '127,58 €', 'Expédier'),
         ('CMD-11680', 'Sans facture', 'Centrale Dentaire Exemple', 'Place de marché', '19 nov.', 'Échéance 19 nov.', 'exp', 'ok', '610,60 €', 'Générer la facture'),
         ('CMD-11679', 'FA-2611-0930', 'SELARL Morel et Associés', 'Site internet', '19 nov.', 'Échéance 26 nov.', 'prep', 'ok', '234,59 €', 'Expédier'),
         ('CMD-11678', 'FA-2610-0871', 'Centre dentaire Voltaire', 'Direct', '28 oct.', '<span class="late">En retard de 12 j</span>', 'ret', 'part', '1 840,00 €', 'Relancer'),
         ('CMD-11677', 'FA-2611-0929', 'Dr Hugo Lambert', 'Site internet', '19 nov.', 'Échéance 26 nov.', 'att', 'ok', '73,80 €', 'Préparer'),
         ('CMD-11676', 'FA-2611-0925', 'Laboratoire Prothésia', 'Direct', '18 nov.', 'Livrée le 19 nov.', 'liv', 'ok', '2 250,00 €', None),
         ('CMD-11675', 'Sans facture', 'Dr Sophie Marchand', 'Direct', '18 nov.', 'À compléter', 'bro', 'no', '318,40 €', 'Reprendre'),
         ('CMD-11674', 'FA-2611-0921', 'SCM Dentaire du Parc', 'Direct', '18 nov.', 'Échéance 18 déc.', 'exp', 'no', '942,10 €', 'Encaisser'),
         ('CMD-11673', 'FA-2611-0919', 'Cabinet Bellecour', 'Site internet', '17 nov.', 'Livrée le 18 nov.', 'liv', 'ok', '86,40 €', None)]
page('ventes.html', 'ventes', 'Ventes', 'Devis, commandes, livraisons et factures au même endroit',
     btn('Exporter', icon='down') + btn('Point de vente', icon='pos') + btn('Nouvelle commande', 'primary', 'plus', 'commande-nouvelle.html'),
     list_card(chips([('Toutes', 450, ''), ('Brouillons', 14, ''), ('En attente', 129, ''), ('En préparation', 148, ''), ('Expédiées', 397, ''), ('Livrées', 310, ''), ('En retard', 237, 'alert')])
               + filters('N° de commande, facture, client ou produit', ['Période : ce mois', 'Canal : tous', 'Paiement : tous']),
               table(['Commande', 'Client', 'Date', 'Statut', 'Paiement', ('Montant TTC', 'r'), ('Prochaine action', 'r')],
                     [[f'<a href="#">{r}</a><small>{f}</small>', c(cl, ca), f'{d}<small>{e}</small>', ST[s], PAY[p], f'<b>{m}</b>', acts(a)]
                      for r, f, cl, ca, d, e, s, p, m, a in vrows], check=True, name='la commande'),
               pager('1 à 10 sur 450 commandes ce mois', 'Page 1 sur 45'))
     + bulkbar('Expédier', ['Imprimer les bons', 'Générer les factures', 'Exporter']),
     tabs([('Devis', '38'), ('Commandes', '450'), ('Bons de livraison', '397'), ('Factures', '426'), ('Avoirs', '12')], 1))

# ---------- 5. Nouvelle commande (formulaire) ----------
lines = table(['Produit', ('Quantité', 'r'), ('Prix unitaire HT', 'r'), ('Remise', 'r'), ('Total HT', 'r'), ''],
              [[c('Résine composite nano-hybride A3,5', 'RC-A35 · 18 en stock'), '<input class="input num" style="width:72px;text-align:right" value="2" aria-label="Quantité">', '37,10 €', '—', '<b>74,20 €</b>', kebab('Retirer ou modifier la ligne')],
               [c('Pointes de gutta-percha 4 %, boîte de 60', 'GP-04 · ' + '<span class="late">2 en stock</span>'), '<input class="input num" style="width:72px;text-align:right" value="4" aria-label="Quantité">', '5,75 €', '10 %', '<b>20,70 €</b>', kebab('Retirer ou modifier la ligne')]])
recap = (head('Récapitulatif') + '<div class="total-line"><span>Total HT</span><b class="num">94,90 €</b></div>'
         '<div class="total-line"><span>TVA 20 %</span><b class="num">18,98 €</b></div><div class="total-line"><span>Livraison</span><b class="num">Offerte</b></div>'
         '<div class="total-line big"><span>Total TTC</span><span class="num">113,88 €</span></div>'
         + item('Encours client : 105,00 €', '1 facture impayée, à jour', tone='warn', icon='alert', soft=True))
page('commande-nouvelle.html', 'ventes', 'Nouvelle commande', 'Brouillon · enregistré automatiquement', btn('Aperçu du bon', icon='print'),
     f'<div class="cols"><div class="grow stack">'
     + card(head('1. Client', btn('Créer un client', sm=True, icon='plus')) + filters('Rechercher un client par nom, code ou téléphone', more=False)
            + item('Dr Camille Renaud', 'Cabinet · Lyon 6e · 04 00 00 00 00', btn('Changer', sm=True), icon='users', soft=True))
     + card('<div class="card-bar">' + head('2. Produits', btn('Commande rapide', sm=True)) + filters('Ajouter un produit par nom, référence ou code-barres', more=False) + '</div>' + lines, pad=False)
     + card(head('3. Livraison et paiement') + '<div class="form-grid">'
            '<label class="field">Mode de livraison<select><option>Transporteur 24 h</option></select></label>'
            '<label class="field">Date souhaitée<input type="date" value="2026-11-20"></label>'
            '<label class="field">Règlement<select><option>Virement à 30 jours</option></select></label>'
            '<label class="field">Commercial<select><option>Sans commercial</option></select></label></div>'
            '<label class="field">Note interne<textarea placeholder="Visible uniquement par votre équipe"></textarea></label>')
     + f'</div><div class="aside sticky-aside">{card(recap)}</div></div>'
     + '<div class="savebar"><span class="muted">Brouillon enregistré à 14 h 32</span>' + btn('Annuler', 'ghost', href='ventes.html')
     + btn('Enregistrer le brouillon') + btn('Valider la commande · 113,88 €', 'primary', 'check') + '</div>',
     back=('Ventes', 'ventes.html'))

# ---------- 6. Clients ----------
risk = {'ok': badge('À jour', 'ok'), 'l': badge('Léger', 'info'), 'm': badge('Modéré', 'warn'), 'e': badge('Élevé', 'danger'), 'c': badge('Critique', 'danger')}
crows = [('Dr Camille Renaud', 'CL-00412 · Cabinet', 'Lyon', '04 00 00 00 01', '19 nov. 2026', '105,00 €', 'l'),
         ('Cabinet dentaire des Lilas', 'CL-00388 · Cabinet', 'Paris', '01 00 00 00 02', '19 nov. 2026', '0,00 €', 'ok'),
         ('Centre dentaire Voltaire', 'CL-00127 · Centre', 'Marseille', '04 00 00 00 03', '28 oct. 2026', '920,00 €', 'm'),
         ('Laboratoire Prothésia', 'CL-00093 · Laboratoire', 'Toulouse', '05 00 00 00 04', '18 nov. 2026', '2 100,00 €', 'e'),
         ('SCM Dentaire du Parc', 'CL-00251 · Cabinet', 'Nantes', '02 00 00 00 05', '18 nov. 2026', '1 315,00 €', 'e'),
         ('SELARL Morel et Associés', 'CL-00470 · Cabinet', 'Bordeaux', '05 00 00 00 06', '19 nov. 2026', '0,00 €', 'ok'),
         ('Cabinet Bellecour', 'CL-00305 · Cabinet', 'Lyon', '04 00 00 00 07', '17 nov. 2026', '4 870,00 €', 'c'),
         ('Dr Hugo Lambert', 'CL-00498 · Cabinet', 'Lille', '03 00 00 00 08', '19 nov. 2026', '0,00 €', 'ok')]
page('clients.html', 'clients', 'Clients', '19 464 clients actifs', btn('Exporter', icon='down') + btn('Importer', icon='upload') + btn('Nouveau client', 'primary', 'plus'),
     kpis([('Clients actifs', '19 464', '3 inactifs'), ('Encours total', '96 300 €', '736 factures ouvertes'), ('Clients à risque', '42', '<span class="late">Encours élevé ou critique</span>'), ('Nouveaux ce mois', '58', '<span class="up">+12 %</span> vs octobre')])
     + list_card(chips([('Tous', '19 464', ''), ('À jour', '18 728', ''), ('Léger', 412, ''), ('Modéré', 282, ''), ('Élevé', 31, ''), ('Critique', 11, 'alert')], 'Filtrer par niveau d’encours')
                 + filters('Nom, code client, ville, téléphone ou e-mail', ['Type : tous', 'Commercial : tous', 'Tag : tous']),
                 table(['Client', 'Ville', 'Téléphone', 'Dernière commande', ('Encours', 'r'), 'Risque', ('Action', 'r')],
                       [[f'<a href="#">{n}</a><small>{k}</small>', v, f'<span class="num">{t}</span>', d, f'<b>{e}</b>', risk[r], acts('Commander')] for n, k, v, t, d, e, r in crows],
                       check=True, name='le client'), pager('1 à 8 sur 19 464 clients', 'Page 1 sur 2 433'))
     + bulkbar('Envoyer une relance', ['Ajouter un tag', 'Exporter']),
     tabs([('Clients', '19 464'), 'Tags']))

# ---------- 7. Prospection ----------
prows = [('19 nov.', 'Clinique dentaire du Port', 'Appel', 'Présentation du scanner intra-oral', 'Florian Bonnet', '<span class="late">En retard de 2 j</span>', 'Relancer'),
         ('18 nov.', 'Dr Inès Colin', 'Visite', 'Démonstration au cabinet', 'Florian Bonnet', 'Aujourd’hui', 'Relancer'),
         ('14 nov.', 'Centre dentaire Garibaldi', 'E-mail', 'Envoi du catalogue implantologie', 'Sans commercial', '26 nov. 2026', 'Planifier'),
         ('12 nov.', 'Dr Marc Olivier', 'Appel', 'Premier contact, à rappeler', 'Florian Bonnet', '2 déc. 2026', 'Planifier')]
page('prospection.html', 'prospection', 'Prospection', 'Suivez vos prospects et vos relances commerciales',
     btn('Importer des prospects', icon='upload') + btn('Nouvelle interaction', 'primary', 'plus'),
     kpis([('Prospects actifs', '12', '4 ajoutés ce mois'), ('Relances à traiter', '3', '<span class="late">1 en retard</span>'), ('Taux de conversion', '18 %', 'Prospects devenus clients sur 90 jours')])
     + list_card(filters('Prospect, sujet ou commercial', ['Type : tous', 'Relance : toutes'], more=False),
                 table(['Date', 'Prospect', 'Type', 'Sujet', 'Commercial', 'Prochaine relance', ('Action', 'r')],
                       [[d, f'<a href="#">{p}</a>', badge(t, dot=False), s, co, r, acts(a)] for d, p, t, s, co, r, a in prows]), pager('4 interactions', 'Page 1 sur 1')),
     tabs(['Mes suivis', 'Mes prospects', 'Toute l’équipe', 'Rapports']))

# ---------- 8. Service client ----------
sev = {'c': badge('Critique', 'danger'), 'm': badge('Moyenne', 'warn'), 'f': badge('Faible')}
tst = {'todo': badge('À faire', 'warn'), 'ass': badge('Assigné', 'info'), 'cours': badge('En cours', 'info'), 'att': badge('En attente'), 'ok': badge('Résolu', 'ok')}
trows = [('TK-2026-0005', 'Dr Hugo Lambert', 'Capteur intra-oral : pas de réponse', 'Technique', 'c', 'todo', 'Non assigné', '19 nov.', 'Prendre en charge'),
         ('TK-2026-0004', 'SELARL Morel et Associés', 'Question sur le scanner intra-oral', 'Technique', 'm', 'todo', 'Non assigné', '18 nov.', 'Prendre en charge'),
         ('TK-2026-0003', 'Cabinet Bellecour', 'Passerelle logiciel d’imagerie', 'Technique', 'm', 'ass', 'D. Yan', '12 nov.', 'Répondre'),
         ('TK-2026-0002', 'Centre dentaire Voltaire', 'Colis reçu incomplet', 'Livraison', 'm', 'cours', 'S. Peretti', '9 nov.', 'Répondre'),
         ('TK-2026-0001', 'Laboratoire Prothésia', 'Installation du capteur', 'Autre', 'f', 'att', 'D. Yan', '2 nov.', 'Relancer le client')]
page('service-client.html', 'sav', 'Service client', '5 tickets ouverts, dont 1 critique', btn('Exporter', icon='down') + btn('Nouveau ticket', 'primary', 'plus'),
     list_card(chips([('Ouverts', 5, ''), ('À faire', 2, 'alert'), ('Assignés', 1, ''), ('En cours', 1, ''), ('En attente', 1, ''), ('Résolus', 3, ''), ('Clôturés', 1, '')])
               + filters('Référence, client ou titre', ['Type : tous', 'Assigné : tous'], more=False),
               table(['Ticket', 'Client', 'Sévérité', 'Statut', 'Assigné à', 'Ouvert le', ('Action', 'r')],
                     [[f'<a href="#">{t}</a><small>{r} · {ty}</small>', f'<b>{cl}</b>', sev[s], tst[stt], a, d, acts(ac)] for r, cl, t, ty, s, stt, a, d, ac in trows]),
               pager('5 tickets ouverts', 'Page 1 sur 1')))

# ---------- 9. Produits ----------
stock = lambda n: badge('Rupture', 'danger') if n == 0 else badge(f'Stock bas · {n}', 'warn') if n < 5 else badge(f'En stock · {n}', 'ok')
prod = [('VIOS', 'Ciment canalaire, seringue de 10 g', 'Endodontie', 'Dental Groupe', 1, '57,60 €'),
        ('ESCOM100-B2', 'Résine composite B2, seringue de 4 g', 'Matériaux dentaires', 'Dental Groupe', 0, '24,00 €'),
        ('IRR-UNIV', 'Lignes d’irrigation tubulure, lot de 10', 'Non catégorisé', 'Dental Groupe', 6, '30,00 €'),
        ('AUGMA-6G', 'Substitut osseux, boîte de 6', 'Biomatériaux', 'Dental Groupe', 0, '590,00 €'),
        ('BRMOB-LARIC', 'Boîtes de rangement pour prothèse, lot de 10', 'Cabinet', 'Dental Groupe', 2, '7,70 €'),
        ('R-CB-10', 'Rouleaux CB 57 × 40 mm, lot de 10', 'Non catégorisé', 'Dental Groupe', 9, '11,70 €'),
        ('ETIQ-EDA', 'Étiquettes compatibles autoclave, lot de 10', 'Hygiène et stérilisation', 'Safe Implant', 18, '79,90 €'),
        ('PPA-F1', 'Pointes papier obturation F1, boîte de 100', 'Endodontie', 'Oofti', 0, '11,63 €')]
page('produits.html', 'produits', 'Produits et stock', '11 229 références · catalogue, tarifs et stocks',
     btn('Exporter', icon='down') + btn('Importer', icon='upload') + btn('Nouveau produit', 'primary', 'plus'),
     kpis([('Références actives', '11 229', 'Sur 3 entités'), ('Stock bas', '36', '<span style="color:var(--warn-fg);font-weight:700">À réapprovisionner</span>'), ('Ruptures', '12', '<span class="late">Vente bloquée</span>'), ('Sans prix d’achat', '99 %', '<a href="#">Compléter pour calculer la marge</a>')])
     + list_card(chips([('Tous', '11 229', ''), ('En stock', '11 181', ''), ('Stock bas', 36, ''), ('Rupture', 12, 'alert'), ('Non catégorisés', 418, '')], 'Filtrer par état du stock')
                 + filters('Nom, référence, code-barres ou marque', ['Entité : toutes', 'Catégorie : toutes', 'Marque : toutes', 'Fournisseur : tous']),
                 table(['Référence', 'Désignation', 'Entité', 'Stock', ('Prix HT', 'r'), ('Action', 'r')],
                       [[f'<code>{s}</code>', f'<a href="#">{d}</a><small>{k}</small>', e, stock(n), f'<b>{p}</b>', acts('Réapprovisionner' if n < 5 else 'Modifier', 'soft' if n < 5 else '')] for s, d, k, e, n, p in prod],
                       check=True, name='le produit'), pager('1 à 8 sur 11 229 références', 'Page 1 sur 1 404'))
     + bulkbar('Modifier les prix', ['Changer de catégorie', 'Désactiver', 'Exporter']),
     tabs([('Catalogue', '11 229'), 'Stock et lots', 'Référentiels']))

# ---------- 10. Comparateur de prix ----------
src = [('Votre boutique en ligne', 'Référence de comparaison', 'ok', 'Actif'), ('Dentaprix', 'dentaprix.example', 'ok', 'Actif'), ('Mégastock Dentaire', 'megastock.example', 'ok', 'Actif'),
       ('Docteur Fournitures', 'docteur-fournitures.example', 'danger', 'Accès refusé'), ('Promo Cabinet', 'promo-cabinet.example', 'danger', 'Accès refusé')]
runs = [('Aujourd’hui, 12 h 20', '25 recherches · 3 alertes'), ('Hier, 12 h 20', '11 recherches · 2 alertes'), ('17 nov., 18 h 20', '44 recherches · 2 alertes'), ('17 nov., 12 h 20', '10 recherches · 2 alertes')]
page('comparateur-prix.html', 'prix', 'Comparateur de prix', 'Dernière veille aujourd’hui à 12 h 20 · prochaine à 18 h 20',
     btn('Importer un fichier', icon='upload') + btn('Relancer la veille', 'primary', 'play'),
     '<div class="banner danger">' + ico('alert') + '<p><b>2 sites concurrents refusent l’accès à la veille.</b> Leurs prix ne sont plus mis à jour depuis 3 jours.</p>' + btn('Voir le détail technique', sm=True) + '</div>'
     + kpis([('Références suivies', '99', 'Sur votre boutique'), ('Correspondances à valider', '8 272', '<a href="#">Valider les correspondances</a>'), ('Plus chers que le marché', '2', '<span class="late">Prix à revoir</span>'), ('Alertes non lues', '50', '<a href="#">Lire les alertes</a>')])
     + '<div class="grid">'
     + card(head('Sites comparés', btn('Ajouter un site', sm=True, icon='plus')) + '<div class="list">'
            + ''.join(item(n, u, badge(l, t) + btn('Modifier', sm=True) + kebab(), soft=True) for n, u, t, l in src) + '</div>')
     + card(head('Dernières veilles', '<a href="#">Historique</a>') + '<div class="list">'
            + ''.join(item(d, r, badge('Terminée', 'ok'), soft=True) for d, r in runs) + '</div>')
     + '</div>',
     tabs(['Vue d’ensemble', 'Comparateur', ('Correspondances', '8 272'), 'Recommandations', ('Alertes', '50'), 'Surveillance', 'Règles']))

# ---------- 11. Catalogues partenaires ----------
part = [('Dentaprix', 'dentaprix.example', 95, '3 325 sur 3 500', 'info', 'En cours'), ('Mégastock Dentaire', 'megastock.example', 100, '12 577 sur 12 577', 'ok', 'À jour'),
        ('Docteur Fournitures', 'docteur-fournitures.example', 61, '4 929 sur 8 100', 'info', 'En cours'), ('Promo Cabinet', 'promo-cabinet.example', 12, '1 010 sur 8 075', 'danger', 'En erreur'),
        ('Centrale Dentaire Exemple', 'centrale.example', 100, '20 107 sur 20 107', 'ok', 'À jour')]
page('catalogues-partenaires.html', 'partenaires', 'Catalogues partenaires', 'Importez les fiches produits de vos fournisseurs et publiez-les sur la place de marché',
     btn('Créer les comptes', icon='users') + btn('Arrêter', 'danger', 'stop') + btn('Peupler les catalogues', 'primary', 'play'),
     '<div class="banner info">' + ico('clock') + '<p><b>Import en cours : 2 catalogues sur 5.</b> Les fiches déjà à jour sont rafraîchies toutes les 12 heures.</p></div>'
     + list_card(head('Fournisseurs'), table(['Fournisseur', 'Avancement', 'État', ('Action', 'r')],
                 [[c(n, u), f'<div style="min-width:220px">{meter(p)}<small class="num">{d} fiches</small></div>', badge(l, t), acts('Réessayer' if t == 'danger' else 'Peupler', 'soft' if t == 'danger' else '')] for n, u, p, d, t, l in part])))

# ---------- 12. 24h Dentaire ----------
kind = lambda h: ('', 'Terminé') if h < 14 else ('live', 'En ligne') if h == 14 else ('todo', 'À valider') if h < 22 else ('ok', 'Validé') if h == 22 else ('free', 'Libre')
slots = ''.join(f'<button type="button" class="slot {kind(h)[0]}" aria-label="Créneau de {h} h, {kind(h)[1]}"><b>{h} h</b>{kind(h)[1]}</button>' for h in range(24))
live = (head('En ligne maintenant · 14 h – 15 h', badge('−24 %', 'info', False)) + '<div><b style="font-size:18px">Résine composite nano-hybride, teinte A3,5</b><p class="muted">100 capsules de 0,25 g</p></div>'
        '<div><span class="price num">28,20 € HT</span> <s class="muted num">37,10 €</s></div><div><p class="small muted">Se termine dans 22 minutes · seuil d’achat 4 sur 10</p>' + meter(63) + '</div>')
nxt = (head('Prochain créneau · 15 h – 16 h', badge('À valider', 'warn')) + '<div><b style="font-size:18px">Pointes de gutta-percha 4 ou 6 %, boîte de 60</b><p class="muted">Endodontie</p></div>'
       '<div><span class="price num">4,50 € HT</span> <s class="muted num">5,75 €</s> <span class="up">−21,7 % · marge 61 %</span></div>'
       '<div class="actions">' + btn('Valider', 'ok', 'check') + btn('Changer de produit') + '</div>')
page('24h-dentaire.html', '24h', '24h Dentaire', 'Un produit en promotion flash chaque heure sur votre boutique en ligne',
     btn('‹ Hier') + btn('Aujourd’hui · jeu. 19 nov.') + btn('Demain ›') + btn('Valider les 7 créneaux', 'primary', 'check'),
     f'<div class="grid">{card(live, cls="hero")}{card(nxt)}</div>'
     + kpis([('Créneaux planifiés', '23 sur 24', '<a href="#">Compléter le créneau de 23 h</a>'), ('À valider', '7', '1 validé · 15 publiés'), ('Marge moyenne après remise', '65,8 %', 'Remise moyenne 25,9 %'), ('Stock engagé', '6 293 € HT', 'Stock × prix promo')])
     + card(head('Les 24 créneaux de la journée') + f'<div class="slots">{slots}</div><p class="small muted">Cliquez sur un créneau pour voir le produit, modifier le prix ou valider la promotion.</p>'),
     tabs(['Résumé', 'Produits', 'Planning', 'Discussion', 'Analyses', 'Flux API']))

# ---------- 13. Achats ----------
ast = {'r': badge('Reçue', 'ok'), 'p': badge('Partiellement reçue', 'warn'), 'e': badge('Envoyée', 'info'), 'b': badge('Brouillon')}
arows = [('PO-2611-0076', 'Dentaprime Fournitures', '12 nov.', '20 nov.', '2 250,00 €', 'e', 'Réceptionner'), ('PO-2610-0074', 'Biomat Santé', '26 oct.', '<span class="late">En retard de 5 j</span>', '14 868,64 €', 'p', 'Réceptionner'),
         ('Brouillon 104', 'Orthoplus Distribution', '21 oct.', '—', '0,00 €', 'b', 'Reprendre'), ('PO-2610-0075', 'Medidental Europe', '8 oct.', 'Reçue le 15 oct.', '3 080,39 €', 'r', None),
         ('PO-2609-0070', 'Biomat Santé', '17 sept.', 'Reçue le 24 sept.', '1 600,25 €', 'r', None)]
page('achats.html', 'achats', 'Achats', 'Commandes fournisseurs, réceptions et factures', btn('Exporter', icon='down') + btn('Nouvelle commande fournisseur', 'primary', 'plus'),
     list_card(chips([('Toutes', 76, ''), ('Brouillons', 1, ''), ('Envoyées', 4, ''), ('Partiellement reçues', 2, ''), ('Reçues', 69, ''), ('En retard', 1, 'alert')])
               + filters('N° de commande ou fournisseur', ['Fournisseur : tous', 'Période : 3 mois'], more=False),
               table(['Commande', 'Fournisseur', 'Date', 'Livraison prévue', ('Montant HT', 'r'), 'Statut', ('Action', 'r')],
                     [[f'<a href="#">{n}</a>', f'<b>{f}</b>', d, l, f'<b>{m}</b>', ast[s], acts(a)] for n, f, d, l, m, s, a in arows]), pager('1 à 5 sur 76 commandes', 'Page 1 sur 16')),
     tabs([('Commandes fournisseurs', '76'), 'Factures', 'Avoirs', 'Fournisseurs']))

# ---------- 14. Expéditions ----------
erows = [('SH-2611-0346', 'CMD-11680', 'Centrale Dentaire Exemple', 'Palavas-les-Flots', 'Transporteur 24 h', '—', badge('À préparer', 'warn'), 'Imprimer l’étiquette'),
         ('SH-2611-0345', 'CMD-11679', 'SELARL Morel et Associés', 'Bordeaux', 'Transporteur 24 h', '8400 1000 5380', badge('Prête', 'info'), 'Marquer expédiée'),
         ('SH-2611-0344', 'CMD-11677', 'Dr Hugo Lambert', 'Lille', 'Coursier', '—', badge('À préparer', 'warn'), 'Imprimer l’étiquette'),
         ('SH-2611-0343', 'CMD-11674', 'SCM Dentaire du Parc', 'Nantes', 'Transporteur 24 h', '8400 1000 5377', badge('En transit', 'info'), 'Suivre le colis'),
         ('SH-2611-0342', 'CMD-11676', 'Laboratoire Prothésia', 'Toulouse', 'Transporteur 24 h', '8400 1000 5371', badge('Livrée', 'ok'), None)]
page('expeditions.html', 'expeditions', 'Expéditions', 'Préparation des colis, reliquats et retours', btn('Liste des commandes', href='ventes.html') + btn('Nouvelle expédition', 'primary', 'plus'),
     list_card(chips([('Toutes', 397, ''), ('À préparer', 148, ''), ('Prêtes', 12, ''), ('En transit', 31, ''), ('Livrées', 206, '')])
               + filters('N° d’expédition, de commande, de suivi ou client', ['Transporteur : tous', 'Période : ce mois'], more=False),
               table(['Expédition', 'Client', 'Transporteur', 'N° de suivi', 'État', ('Action', 'r')],
                     [[f'<a href="#">{e}</a><small>{o}</small>', c(cl, v), t, f'<span class="num">{s}</span>', st, acts(a)] for e, o, cl, v, t, s, st, a in erows], check=True, name='l’expédition'),
               pager('1 à 5 sur 397 expéditions', 'Page 1 sur 80'))
     + bulkbar('Imprimer les étiquettes', ['Imprimer les bons de livraison', 'Marquer expédiées']),
     tabs([('Expéditions', '397'), ('Reliquats', '62'), ('Retours', '4'), ('Retards', '237')]))

# ---------- 15. Ramassage ----------
pick = lambda n, a, z: item(n, a, badge(z, 'info', False) + btn('Ramassé', 'soft', 'check', sm=True) + kebab(), icon='pin', soft=True)
page('ramassage.html', 'ramassage', 'Ramassage', 'Récupération chez le client · matin jusqu’à 11 h 30, après-midi à partir de 14 h 30',
     btn('Zones', icon='pin') + btn('Imprimer la tournée', icon='print') + btn('Nouveau ramassage', 'primary', 'plus'),
     '<div class="filters"><div class="seg" role="group" aria-label="Jour"><button aria-pressed="true">Aujourd’hui</button><button aria-pressed="false">Demain</button><button aria-pressed="false">Cette semaine</button></div>'
     + btn('Zone : toutes', icon='filter') + '</div><div class="grid">'
     + card(head('Matin · 3 ramassages', badge('Jusqu’à 11 h 30', dot=False)) + '<div class="list">' + pick('Cabinet dentaire des Lilas', '12 rue des Lilas, Paris 19e', 'Paris Est')
            + pick('Dr Camille Renaud', '8 cours Vitton, Lyon 6e', 'Lyon') + pick('Centre dentaire Voltaire', '40 boulevard Voltaire, Marseille', 'Marseille') + '</div>')
     + card(head('Après-midi', badge('À partir de 14 h 30', dot=False)) + empty('pin', 'Aucun ramassage cet après-midi', 'Ajoutez un ramassage pour qu’il apparaisse dans la tournée imprimée.', btn('Nouveau ramassage', 'soft', 'plus')))
     + '</div>')

# ---------- 16. Locations ----------
lrows = [('LOC-2026-0002', 'Dr Sophie Marchand', 'Scanner intra-oral', '31 juil. 2026', '150,00 €', badge('Mandat signé', 'ok'), '5 déc. 2026', badge('Actif', 'ok'), 'Voir le contrat'),
         ('LOC-2026-0001', 'Cabinet Bellecour', 'Capteur intra-oral', '21 juin 2026', '19,90 €', badge('Mandat manquant', 'warn'), '—', badge('Brouillon'), 'Finaliser')]
page('locations.html', 'locations', 'Locations', 'Contrats de location de matériel et prélèvements SEPA mensuels', btn('Exporter', icon='down') + btn('Nouveau contrat', 'primary', 'plus'),
     kpis([('Contrats actifs', '1', '1 brouillon à finaliser'), ('Loyers mensuels', '150,00 €', 'Hors brouillons'), ('Prochain prélèvement', '5 déc.', '150,00 € · 1 contrat')])
     + list_card(head('Contrats'), table(['Contrat', 'Client', 'Matériel', 'Début', ('Mensualité', 'r'), 'SEPA', 'Prochain prélèvement', 'Statut', ('Action', 'r')],
                 [[f'<a href="#">{r}</a>', f'<b>{cl}</b>', m, d, f'<b>{p}</b>', s, n, st, acts(a, 'soft' if a == 'Finaliser' else '')] for r, cl, m, d, p, s, n, st, a in lrows]))
     + '<p class="small muted">La facture mensuelle et le prélèvement SEPA sont générés automatiquement après validation du mandat.</p>')

# ---------- 17. Documents ----------
tree = ''.join(f'<a class="mail-item" href="#"{" aria-current=true" if i == 0 else ""} style="padding-left:{12 + lvl * 16}px">{ico("folder")} {n}</a>'
               for i, (n, lvl) in enumerate([('Tous les documents', 0), ('Formations 2026', 1), ('Conventions', 1), ('Attestations', 1), ('Procédures', 0)]))
drows = [('Convention de formation — modèle.pdf', 'Conventions', '12 nov. 2026', '184 Ko'), ('Attestation de présence — modèle.docx', 'Attestations', '12 nov. 2026', '42 Ko'), ('Procédure de retour produit.pdf', 'Procédures', '3 oct. 2026', '96 Ko')]
page('documents.html', 'docs', 'Documents', 'Dossiers, conventions, attestations et procédures', btn('Nouveau dossier', icon='folder') + btn('Ajouter un document', 'primary', 'upload'),
     f'<div class="cols"><div class="aside" style="flex:0 1 260px">{card(head("Dossiers") + f"<nav aria-label=Dossiers>{tree}</nav>")}</div><div class="grow stack">'
     + card('<div class="empty" style="padding:28px;border:2px dashed var(--line-strong);border-radius:14px"><span class="tile">' + ico('upload') + '</span><h2>Glissez vos fichiers ici</h2><p>ou cliquez sur « Ajouter un document ». PDF, Word, images, jusqu’à 20 Mo.</p></div>')
     + list_card(filters('Nom du document', ['Catégorie : toutes'], more=False),
                 table(['Document', 'Dossier', 'Ajouté le', ('Taille', 'r'), ('Action', 'r')], [[f'<a href="#">{n}</a>', f, d, s, acts('Télécharger', '')] for n, f, d, s in drows], check=True, name='le document'))
     + '</div></div>' + bulkbar('Télécharger', ['Déplacer', 'Supprimer']))

# ---------- 18. Ressources humaines ----------
pause = lambda l, v: item(l, v, btn('Démarrer', sm=True), soft=True)
page('rh.html', 'rh', 'Ressources humaines', 'Présence, absences et dossiers de l’équipe', btn('Demander une absence', icon='plus') + btn('Démarrer ma journée', 'primary', 'play'),
     '<div class="banner info">' + ico('clock') + '<p><b>Vous n’avez pas encore pointé aujourd’hui.</b> Il est 14 h 38 · 7 h 00 attendues.</p></div>'
     + kpis([('Temps de travail', '0 h 00', 'Sur 7 h 00 attendues'), ('Pauses', '0 h 00', 'La pause déjeuner est déduite automatiquement'), ('Retard', '0 h 00', 'Aucun retard ce mois'), ('Congés payés', '25 jours', 'RTT : 0 jour')])
     + '<div class="grid">' + card(head('Pauses du jour') + '<div class="list">' + pause('Déjeuner', '0 h 00') + pause('Café du matin', '0 sur 15 min') + pause('Café de l’après-midi', '0 sur 15 min') + pause('Brief ou réunion', '0 h 00') + '</div>')
     + card(head('Mes absences', btn('Demander une absence', 'soft', sm=True)) + empty('team', 'Aucune absence à venir', 'Vos demandes de congés et leur validation apparaîtront ici.')) + '</div>',
     tabs(['Ma journée', 'Mes absences', 'Mon historique', 'Recrutement']))

if __name__ == '__main__':
    for name, html in PAGES.items():
        (ROOT / name).write_text(html, encoding='utf-8')
    print(f'{len(PAGES)} pages générées dans {ROOT}')
