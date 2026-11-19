#!/usr/bin/env python3
"""Génère les pages HTML de la maquette Evidentall à la racine du dépôt.

Usage : python3 tools/build.py
Le menu, la barre supérieure et l'en-tête de page sont définis une seule fois ici ;
chaque page ne décrit que son contenu. Toutes les données affichées sont fictives.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
EXTRA = {}   # onglets secondaires par page, remplis par extra.py
MODALS = {}  # fenêtres de création, incluses dans les pages qui en ont besoin

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
    'moon': 'M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z',
    'sun': 'M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M5 19l1.5-1.5M17.5 6.5L19 5',
}

NAV = [
    ('Pilotage', [('dashboard', 'Tableau de bord', 'grid', 'index.html', '', ''),
                  ('stats', 'Statistiques', 'chart', 'statistiques.html', '', ''),
                  ('mail', 'Cockpit', 'mail', 'messagerie.html', '3', '')]),
    ('Commerce', [('ventes', 'Ventes', 'cart', 'ventes.html', '237', 'alert'),
                  ('clients', 'Clients', 'users', 'clients.html', '', ''),
                  ('prospection', 'Prospections et suivis', 'target', 'prospection.html', '3', ''),
                  ('partenariats', 'Partenariats', 'users', 'partenariats.html', '', ''),
                  ('sav', 'Service client', 'headset', 'service-client.html', '5', '')]),
    ('Catalogue', [('produits', 'Produits', 'box', 'produits.html', '', ''),
                   ('prix', 'Comparateur de prix', 'trend', 'comparateur-prix.html', '50', ''),
                   ('partenaires', 'Catalogues partenaires', 'book', 'catalogues-partenaires.html', '', ''),
                   ('24h', '24h Dentaire', 'clock', '24h-dentaire.html', '7', '')]),
    ('Logistique', [('achats', 'Achats', 'bag', 'achats.html', '', ''),
                    ('expeditions', 'Expéditions', 'truck', 'expeditions.html', '', ''),
                    ('ramassage', 'Ramassage', 'pin', 'ramassage.html', '', ''),
                    ('locations', 'Locations', 'key', 'locations.html', '', '')]),
    ('Équipe et documents', [('rh', 'Ressources humaines', 'team', 'rh.html', '', ''),
                             ('docs', 'GED — Documents', 'folder', 'documents.html', '', '')]),
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


def kebab(label='Autres actions', menu=''):
    m = f' data-menu="{menu}"' if menu else ''
    return f'<button type="button" class="btn btn-sm btn-icon" aria-label="{label}"{m}>{ico("more")}</button>'


def acts(label=None, kind='soft', more=True, menu=''):
    a = btn(label, kind, sm=True) if label else ''
    return f'<div class="row-actions">{a}{kebab(menu=menu) if more else ""}</div>'


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
        cur = 'true' if i == active else 'false'
        out += (f'<button type="button" role="tab" data-tab="{i}" aria-selected="{cur}">{label}'
                f'{f"<span class=count>{count}</span>" if count else ""}</button>')
    return f'<div class="tabs" role="tablist" aria-label="Sections de la page">{out}</div>'


def chips(items, label='Filtrer par statut'):
    out = ''
    for i, (l, n, state) in enumerate(items):
        cls = 'chip alert' if state == 'alert' else 'chip'
        out += f'<button type="button" class="{cls}" aria-pressed="{"true" if i == 0 else "false"}">{l}<b class="num">{n}</b></button>'
    return f'<div class="chips" role="group" aria-label="{label}">{out}</div>'


def filters(placeholder, selects=(), more=True):
    out = (f'<label class="search" style="flex:2 1 260px;max-width:none;background:var(--surface)">{ico("search")}'
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
    last = cols[-1][0] if isinstance(cols[-1], tuple) else cols[-1]
    cls = ' class="has-actions"' if last == '' or 'ction' in last else ''
    return f'<div class="table-wrap"><table{cls}><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


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
def shell(slug, title, sub, actions, body, tab_html='', back=None, file=None):
    ex = EXTRA.get(file, {})
    found = re.search(r'data-tab="(\d+)" aria-selected="true"', tab_html)
    act = int(found.group(1)) if found else 0
    prim = lambda i: f' data-primary="{ex["primary"][i]}"' if i in ex.get('primary', {}) else ''
    body = f'<section class="panel stack" data-panel="{act}"{prim(act)}>{body}</section>'
    for i, html in sorted(ex.get('panels', {}).items()):
        body += f'<section class="panel stack" data-panel="{i}"{prim(i)} hidden>{html}</section>'
    body_all = body + actions
    has = lambda l: any(x in body_all for x in (f'>{l}<', f'="{l}"', f'|{l}|', f'"{l}|', f'|{l}"'))
    dialogs = ''.join(html for labels, html in MODALS.values() if any(has(l) for l in labels))
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
<script>try{{if(localStorage.getItem("ev-theme")==="dark")document.documentElement.dataset.theme="dark"}}catch(e){{}}</script>
</head>
<body>
<a class="sr" href="#contenu">Aller au contenu</a>
<div class="app">
<aside class="side">
<a class="logo" href="index.html" aria-label="Evidentall, tableau de bord"><img class="full when-light" src="assets/logo-bleus.svg" alt="Evidentall, le pilotage intelligent" width="196" height="57"><img class="full when-dark" src="assets/logo-blanc-bleu.svg" alt="Evidentall, le pilotage intelligent" width="196" height="57"><img class="mark" src="assets/logo-symbole.svg" alt="" width="40" height="44"></a>
<button type="button" class="org" data-menu="org">{ico("globe")}<span><small>Société active</small><b>Votre société</b></span></button>
<nav class="nav" aria-label="Navigation principale" style="display:flex;flex-direction:column;gap:16px">{nav}</nav>
<div class="side-foot nav">
<a href="parametres.html" title="Paramètres">{ico("gear")}<span>Paramètres</span></a>
<a href="#" data-action="collapse" title="Réduire le menu">{ico("panel")}<span>Réduire le menu</span></a>
</div>
</aside>
<div class="main">
<header class="topbar">
<button type="button" class="btn btn-icon menu-btn" data-action="menu" aria-label="Ouvrir le menu">{ico("menu")}</button>
<label class="search" data-action="palette">{ico("search")}<input type="search" aria-label="Rechercher dans Evidentall" placeholder="Rechercher un client, une commande, un produit…"><span class="kbd hide-sm">Ctrl K</span></label>
<span class="spacer"></span>
<button type="button" class="btn hide-sm" data-action="clock">{ico("play")}<span>Démarrer ma journée</span></button>
<button type="button" class="btn hide-sm" data-action="elia">{ico("send")}<span>Elia</span></button>
<button type="button" class="btn hide-sm" data-menu="aide">{ico("help")}<span>Aide</span></button>
<button type="button" class="btn hide-sm" data-menu="lang" aria-label="Langue : français">{ico("globe")}<span>FR</span></button>
<button type="button" class="btn btn-icon" data-action="theme" aria-label="Activer le mode nuit" title="Mode nuit"><span class="when-light">{ico("moon")}</span><span class="when-dark">{ico("sun")}</span></button>
<button type="button" class="btn btn-icon" data-menu="notifs" aria-label="Notifications : 3 nouvelles">{ico("bell")}</button>
<button type="button" class="btn btn-ghost" data-menu="compte" aria-label="Compte de Florian Bonnet" style="padding:0 6px"><span class="avatar">FB</span></button>
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
{dialogs}
<script src="assets/app.js"></script>
</body>
</html>
'''


PAGES = {}


def page(file, *args, **kw):
    PAGES[file] = shell(*args, file=file, **kw)


ST = {'prep': badge('En préparation', 'info'), 'exp': badge('Expédiée', 'ok'), 'liv': badge('Livrée', 'ok'),
      'att': badge('En attente'), 'ret': badge('En retard', 'danger'), 'bro': badge('Brouillon')}
PAY = {'ok': badge('Payée', 'ok'), 'no': badge('Impayée', 'danger'), 'part': badge('Paiement partiel', 'warn')}

import extra  # noqa: E402
extra.register(globals())

import pages  # noqa: E402
import pages2  # noqa: E402
pages.register(globals())
pages2.register(globals())

if __name__ == '__main__':
    for name, html in PAGES.items():
        (ROOT / name).write_text(html, encoding='utf-8')
    print(f'{len(PAGES)} pages générées dans {ROOT}')
