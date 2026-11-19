"""Pages principales (1/2) : tableau de bord, ventes, clients, produits, partenariats.

Chaque écran reprend TOUTES les fonctions relevées sur la plateforme (voir AUDIT.md) :
rien n'est supprimé, les éléments secondaires sont rangés dans « Plus de filtres »,
le menu « … » de chaque ligne ou un menu « Plus d'actions ». Données fictives.
"""


def register(h):
    globals().update(h)
    E = h['EXTRA']

    # ---------- Briques communes ----------
    def sel(label, opts, cur=None):
        return (f'<button type="button" class="btn" style="flex:1 1 150px;justify-content:space-between" data-options="{"|".join(opts)}">'
                f'{label} : {cur or opts[0]}{ico("filter")}</button>')

    def bar(search, sels='', more=None, chips_html='', cols=True):
        row = (f'<label class="search" style="flex:2 1 240px;max-width:none;background:var(--surface)">{ico("search")}'
               f'<input type="search" aria-label="Rechercher" placeholder="{search}"></label>{sels}')
        if more:
            row += btn('Plus de filtres', 'ghost', 'filter', attrs='data-action="more"')
        if cols:
            row += btn('Colonnes', 'ghost', attrs='data-action="columns"')
        row += btn('Réinitialiser', 'ghost', attrs='data-action="reset"')
        extra = ('<div class="more-filters form-grid" hidden>' + ''.join(field(f) for f in more) + '</div>') if more else ''
        return chips_html + f'<div class="filters">{row}</div>' + extra

    def A(label=None, menu='', kind='soft'):
        return acts(label, kind, menu=menu)

    def stat(label, tone, opts):
        return (f'<button type="button" class="badge {tone} dot status-pick" data-menu="{"|".join(opts)}" '
                f'aria-label="Statut : {label}. Cliquer pour changer">{label}</button>')

    def more_btn(items, label="Plus d’actions"):
        return f'<button type="button" class="btn" data-menu="{"|".join(items)}">{ico("more")}<span>{label}</span></button>'

    def views(name, tabs_):
        """Petits onglets internes à une carte : [(libellé, html)]."""
        b = ''.join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-show="{name}-{i}">{t}</button>' for i, (t, _) in enumerate(tabs_))
        v = ''.join(f'<div data-view="{name}-{i}"{"" if i == 0 else " hidden"}>{html}</div>' for i, (_, html) in enumerate(tabs_))
        return f'<div class="seg" role="group">{b}</div>{v}'

    def rank(rows):
        return '<div class="list" style="gap:14px">' + ''.join(
            f'<div><div class="total-line"><span>{n}</span><b class="num">{v}</b></div>{meter(p)}</div>' for n, v, p in rows) + '</div>'

    h.update(sel=sel, bar=bar, A=A, stat=stat, more_btn=more_btn, views=views, rank=rank)
    PERIODE = ['Mois en cours', 'Aujourd’hui', '7 derniers jours', '30 derniers jours', '90 derniers jours', 'Tout l’historique', 'Dates libres…']
    ENT = ['toutes', 'Dental Groupe', 'Oofti', 'Safe Implant', 'Sans entité']
    C = ['Dr Camille Renaud', 'Cabinet dentaire des Lilas', 'Centre dentaire Voltaire', 'Laboratoire Prothésia', 'SCM Dentaire du Parc', 'SELARL Morel et Associés']
    h.update(PERIODE=PERIODE, ENT=ENT, C=C)

    # ================= 1. TABLEAU DE BORD =================
    months = [('Déc', 188), ('Jan', 172), ('Fév', 196), ('Mar', 224), ('Avr', 205), ('Mai', 214), ('Juin', 238), ('Juil', 190), ('Août', 141), ('Sep', 229), ('Oct', 221), ('Nov', 128)]
    bars = ''.join(f'<div class="bar{" now" if i == 11 else ""}"><b class="num">{v}</b><div class="track"><i style="height:{round(v * .8)}px"></i></div><span>{m}</span></div>' for i, (m, v) in enumerate(months))
    chart = (head('Évolution du chiffre d’affaires', '<a href="statistiques.html">Voir l’analyse détaillée</a>')
             + f'<div class="bars" role="img" aria-label="CA HT mensuel sur 12 mois, en milliers d’euros">{bars}</div>'
             + '<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px">'
             + ''.join(f'<div class="item soft"><div class="item-main"><small>{l}</small><b class="num">{v}</b></div></div>' for l, v in
                       [('CA HT de la période', '128 400 €'), ('Encaissements', '112 900 €'), ('CA HT 12 mois glissants', '2 445 900 €')]) + '</div>')
    h['chart'] = chart
    todo = head('Alertes à traiter', badge('4', 'danger', False)) + '<div class="list">' + ''.join([
        item('517 factures échues non réglées', '81 200 € · dont 36 600 € à plus de 90 j', btn('Relancer', 'soft', sm=True), 'danger', 'alert'),
        item('237 commandes en retard', 'Échéance dépassée, non soldées', btn('Voir', 'soft', href='expeditions.html#onglet-3', sm=True), 'warn', 'clock'),
        item('148 commandes en préparation', 'Dont 62 partiellement expédiées', btn('Préparer', 'soft', href='expeditions.html', sm=True), '', 'box'),
        item('5 tickets service client', '1 ticket critique', btn('Ouvrir', 'soft', href='service-client.html', sm=True), '', 'headset')]) + '</div>'
    pointage = (head('Pointage', badge('Pas encore pointé', 'warn'))
                + '<div class="grid" style="grid-template-columns:1fr 1fr;gap:12px"><div class="item soft"><div class="item-main"><small>Temps de travail</small><b class="num">0 h 00</b></div></div>'
                  '<div class="item soft"><div class="item-main"><small>Attendu aujourd’hui</small><b class="num">7 h 00</b></div></div></div>'
                + btn('Démarrer ma journée', 'ok', 'play', attrs='data-action="clock"') + '<a href="rh.html">Ouvrir le module RH</a>')
    orders = [('CMD-11682', 'Direct', C[0], 'prep', 'no', '105,00 €'), ('CMD-11681', 'Sites internet', C[1], 'prep', 'ok', '127,58 €'),
              ('CMD-11680', 'GACD', 'Centrale Dentaire Exemple', 'exp', 'ok', '610,60 €'), ('CMD-11679', 'Sites internet', C[5], 'prep', 'ok', '234,59 €'),
              ('CMD-11678', 'Général', C[2], 'ret', 'part', '1 840,00 €')]
    last = card('<div class="card-bar">' + head('Commandes récentes', btn('Voir tout', href='ventes.html', sm=True)) + '</div>'
                + table(['Commande', 'Client', 'Entité / canal', 'Statut', 'Paiement', ('Montant', 'r')],
                        [[f'<a href="#">{r}</a><small>Échéance souhaitée 19 déc.</small>', f'<b>{cl}</b>', c('Safe Implant', ca), ST[s], PAY[p], f'<b>{m}</b>'] for r, ca, cl, s, p, m in orders]), pad=False)
    flow = (head('Activité opérationnelle')
            + '<div class="split" role="img" aria-label="129 en attente, 148 en préparation, 397 expédiées, 237 en retard"><i style="flex:129;background:#B8C4D3"></i>'
              '<i style="flex:148;background:#0077FD"></i><i style="flex:397;background:#12925A"></i><i style="flex:237;background:#B3261E"></i></div><div class="list">'
            + ''.join(f'<a class="item soft" href="ventes.html" style="color:var(--ink)"><span class="item-main"><b>{l}</b><small>{d}</small></span><b class="num {k}">{n}</b></a>' for l, d, n, k in
                      [('En attente', 'Commandes des 90 derniers jours', 129, ''), ('En préparation', 'Dont partiellement expédiées : 62', 148, ''),
                       ('En retard', 'Échéance dépassée, non soldées', 237, 'late'), ('Expédiées', 'Sur la période', 397, ''), ('Délai médian', 'Commande → 1re expédition', '0,6 j', '')]) + '</div>')
    dues = head('Échéances à venir', '<a href="ventes.html#onglet-3">Toutes les factures</a>') + '<p class="small muted">Factures non réglées : 7 jours à venir et échues</p><div class="list">' + ''.join(
        item(n, f'{f} · <span class="{k}">{d}</span>', f'<b class="num">{m}</b>' + btn('Relancer', 'soft', sm=True), soft=True)
        for n, f, d, k, m in [(C[3], 'FA-2610-0418', 'Échue depuis 4 j', 'late', '2 100,00 €'), (C[4], 'FA-2610-0411', 'Échue depuis 4 j', 'late', '1 315,00 €'),
                              ('Dr Sophie Marchand', 'FA-2610-0452', 'Échéance aujourd’hui', '', '2 079,00 €'), ('Cabinet Bellecour', 'FA-2610-0449', 'Échéance aujourd’hui', '', '891,41 €')]) + '</div>'
    top = head('Top 5 de la période') + views('top', [
        ('Clients', rank([(C[3], '13 100 €', 100), (C[2], '6 340 €', 48), ('Clinique Exemple', '6 170 €', 47), (C[5], '4 330 €', 33), (C[4], '4 230 €', 32)])),
        ('Produits', rank([('Substitut osseux — boîte de 6 (× 107)', '66 400 €', 100), ('Journée de formation (× 13)', '6 870 €', 22), ('Scanner intra-oral (× 1)', '3 800 €', 14), ('Kit de chirurgie (× 18)', '2 340 €', 10), ('Résine composite A3,5', '1 960 €', 8)])),
        ('Marques', rank([('Dental Coop', '104 300 €', 100), ('Safe Implant', '23 500 €', 23), ('Sans marque', '5 300 €', 5), ('Oofti', '1 400 €', 2)])),
        ('Commerciaux', rank([('Sans commercial (426)', '128 400 €', 100), ('Florian Bonnet (24)', '9 870 €', 8)]))])
    marge = (head('Marge brute', badge('Coûts non renseignés', 'warn', False))
             + '<p>Renseignez les prix d’achat des produits pour calculer la marge.</p>'
             + '<div class="total-line"><span>Couverture des coûts</span><b class="num">1 %</b></div>' + meter(2, '#E08A00')
             + '<p class="small muted">630 € sur 128 400 € de chiffre d’affaires avec coût connu</p>'
             + '<div class="total-line"><span>Encaissé / facturé TTC</span><b class="num">78 %</b></div>' + meter(78)
             + btn('Renseigner les prix d’achat', 'soft', href='produits.html'))
    canal = (head('Répartition par canal') + rank([('Direct / autres · 149 commandes', '80 400 € · 60 %', 60), ('Boutiques en ligne · 212', '50 600 € · 38 %', 38), ('GACD · 65', '3 400 € · 3 %', 3)])
             + '<p class="small muted">CA facturé HT : factures validées, hors brouillons, abandons et tests.</p>')
    modal('perso', ['Personnaliser'], 'Personnaliser le tableau de bord', ['?Alertes à traiter', '?Indicateurs clés', '?Pointage', '?Marge brute', '?Activité opérationnelle', '?Commandes récentes', '?Top 5', '?Évolution du chiffre d’affaires', '?Échéances à venir'],
          'Enregistrer la disposition', 'Tableau de bord mis à jour (simulation)', 'Cochez les blocs à afficher ; glissez-les pour les réordonner.')
    modal('dates', ['Personnalisé'], 'Choisir une période', ['Du@date', 'Au@date'], 'Appliquer', 'Période appliquée (simulation)')
    modal('guide', ['Guide d’utilisation'], 'Guide d’utilisation', ['Rechercher dans le guide=', '#Démarrage', '#Modes d’activité : prothèses, fourniture / revente', '#Tous les modules', '?Ne plus afficher ce guide à l’ouverture du tableau de bord'], 'J’ai compris', 'Guide fermé')
    page('index.html', 'dashboard', 'Bonjour Florian', 'Supervision de l’activité · jeudi 19 novembre 2026',
         '<div class="seg" role="group" aria-label="Période"><button aria-pressed="false">Aujourd’hui</button><button aria-pressed="false">Cette semaine</button><button aria-pressed="true">Ce mois</button><button aria-pressed="false">Personnalisé</button></div>'
         + more_btn(['Guide d’utilisation', 'Personnaliser', 'Partenariats : cabinets>partenariats.html', 'Partenariats : laboratoires>partenariats.html#onglet-1'])
         + f'<button type="button" class="btn" data-menu="Produit>produits.html|Vente>commande-nouvelle.html|Achat>achats.html|Client>clients.html|Point de vente>ventes.html#onglet-5">{ico("plus")}<span>Créer</span></button>'
         + btn('Nouvelle commande', 'primary', 'plus', 'commande-nouvelle.html'),
         kpis([('CA du jour', '2 919 €', 'TTC 3 228 € · 15 commandes'), ('CA HT de la période', '128 400 €', '<span class="up">+8,3 %</span> vs période préc. · TTC 141 200 €'),
               ('Encaissements', '112 900 €', '<span class="up">+3,0 %</span> · 359 règlements, 1 260 € remboursés'),
               ('Impayés (encours)', '96 300 €', '736 factures · 0–30 j 39 400 € · 31–60 j 16 500 € · 61–90 j 3 300 € · <span class="late">&gt; 90 j 37 100 €</span>'),
               ('Commandes et panier moyen', '450', '<span class="down">−5,6 %</span> · panier moyen HT 315 € · 426 factures')])
         + f'<div class="cols"><div class="grow stack">{card(chart)}{last}</div><div class="aside stack">{card(todo)}{card(pointage)}{card(flow)}</div></div>'
         + f'<div class="grid">{card(dues)}{card(top)}{card(marge)}{card(canal)}</div>')

    # ================= 2. VENTES =================
    MV = 'Ouvrir la commande|Voir la facture|Historique des paiements|Imprimer l’étiquette|Imprimer le bon de livraison|Imprimer le bon de commande|Passer en brouillon|Passer en préparation|Créer un avoir|Bon de prélèvement stock|!Annuler la commande'
    vrows = [('CMD-11682', 'Facture provisoire', C[0], '—', 'Préparation', 'Safe Implant', 'Général', '19 nov.', '19 déc.', 'prep', 'no', '105,00 €', 'Expédier'),
             ('CMD-11681', 'FA-2611-0932', C[1], '—', '—', 'Oofti', 'Sites internet', '19 nov.', '26 nov.', 'prep', 'ok', '127,58 €', 'Expédier'),
             ('CMD-11680', 'Sans facture', 'Centrale Dentaire Exemple', '—', '—', 'Safe Implant', 'GACD', '19 nov.', '19 nov.', 'exp', 'ok', '610,60 €', 'Générer la facture'),
             ('CMD-11678', 'FA-2610-0871', C[2], 'F. Bonnet', 'F. Bonnet', 'Dental Groupe', 'Commerciaux', '28 oct.', '<span class="late">Retard 12 j</span>', 'ret', 'part', '1 840,00 €', 'Relancer'),
             ('CMD-11677', 'FA-2611-0929', 'Dr Hugo Lambert', '—', '—', 'Oofti', 'Téléphone', '19 nov.', '26 nov.', 'att', 'ok', '73,80 €', 'Préparer'),
             ('CMD-11675', 'Sans facture', 'Dr Sophie Marchand', 'F. Bonnet', '—', 'Dental Groupe', 'Général', '18 nov.', 'À compléter', 'bro', 'no', '318,40 €', 'Reprendre')]
    rapides = ('<details class="card card-pad"><summary><b>Commandes rapides</b> <span class="muted">— choisissez plusieurs produits et quantités, puis ouvrez la fiche de création</span></summary>'
               '<div class="form-grid" style="margin-top:16px">' + field('Client (facultatif)') + field('Produit') + field('Quantité@number') + '</div><div class="actions" style="margin:12px 0 0">'
               + btn('Ajouter une ligne', icon='plus') + btn('Créer la commande avec ces lignes', 'soft', href='commande-nouvelle.html') + '</div></details>')
    cmd = (rapides + list_card(bar('Référence, facture, produit, commercial…', sel('Période', PERIODE) + sel('Canal', ['tous', 'Général', 'Sites internet', 'Téléphone', 'GACD', 'Commerciaux']) + sel('Entité', ENT),
                                   ['Client', 'Saisie du@date', 'Saisie au@date', 'Livraison du@date', 'Livraison au@date', 'Montant TTC min@number', 'Montant TTC max@number', 'Autre statut|Tous les statuts,Avoir,Bon de prélèvement stock'],
                                   chips([('Toutes', '82 206', ''), ('Brouillon', 14, ''), ('En attente', 129, ''), ('En préparation', 148, ''), ('Partiellement expédiée', 62, ''), ('Expédiée', 397, ''), ('Livrée', 310, ''), ('Annulée', 9, ''), ('En retard', 237, 'alert')])),
                               table(['Commande', 'Client', 'Commercial / envoyée par', 'Entité / canal', 'Saisie / échéance', 'Statut', 'Paiement', ('Montant TTC', 'r'), ('Prochaine action', 'r')],
                                     [[f'<a href="#">{r}</a><small>{f}</small>', f'<a href="client-fiche.html">{cl}</a>', c(co, en), c(et, ca), f'{d}<small>{e}</small>', ST[s] + '<small>Priorité normale</small>', PAY[p], f'<b>{m}</b>', A(a, MV)]
                                      for r, f, cl, co, en, et, ca, d, e, s, p, m, a in vrows], check=True, name='la commande'),
                               pager('1 à 30 sur 82 206 commandes', 'Page 1 sur 2 741'))
           + bulkbar('Expédier', ['Imprimer les étiquettes', 'Imprimer les bons', 'Générer les factures', 'Exporter en Excel']))
    DS = ['En instance', 'Accepté', 'Commandé', 'Rejeté', 'Hors délai']
    devis = list_card(bar('Référence, client, produit, commercial…', sel('Période', PERIODE), ['Client', 'Saisie du@date', 'Saisie au@date', 'Montant TTC min@number', 'Montant TTC max@number'],
                          chips([('Toutes', 526, ''), ('En instance', 41, ''), ('Accepté', 62, ''), ('Commandé', 388, ''), ('Rejeté', 21, ''), ('Hors délai', 14, 'alert')])),
                      table(['Proposition', 'Client', 'Commercial / envoyée par', 'Travaux / produits', 'Date', 'Statut', ('Montant TTC', 'r'), ('Action', 'r')], [
                          ['<a href="#">PC-0412</a>', c(C[0]), c('F. Bonnet', 'F. Bonnet'), 'Scanner intra-oral + formation', '18 nov.', stat('En instance', 'info', DS), '<b>4 560,00 €</b>', A('Convertir en commande', 'Modifier|Enregistrer un règlement|Imprimer la proposition|Ouvrir la commande|!Supprimer')],
                          ['<a href="#">PC-0411</a>', c(C[3]), c('—', 'F. Bonnet'), 'Substitut osseux × 12', '15 nov.', stat('Accepté', 'ok', DS), '<b>7 080,00 €</b>', A('Convertir en commande', 'Modifier|Enregistrer un règlement|Imprimer la proposition|!Supprimer')],
                          ['<a href="#">PC-0409</a>', c(C[4]), c('—', '—'), 'Résine composite × 20', '2 nov.', stat('Hors délai', 'warn', DS), '<b>480,00 €</b>', A('Relancer', 'Modifier|Imprimer la proposition|!Supprimer')]]),
                      pager('1 à 30 sur 526 propositions', 'Page 1 sur 18'))
    bl = list_card(bar('Référence, client, commande…', sel('Période', PERIODE), ['Client', 'Livraison du@date', 'Livraison au@date']),
                   table(['Bon de livraison', 'Client', 'Commercial', 'Date', 'Statut', ('Montant TTC', 'r'), ('Action', 'r')], [
                       ['<a href="#">BL-2611-0397</a><small>CMD-11680</small>', c(C[1]), '—', '19 nov.', badge('Expédié', 'ok'), '<b>610,60 €</b>', A('Imprimer le BL', 'Ouvrir le bon d’expédition|Imprimer le bon de commande|Historique des paiements', '')],
                       ['<a href="#">BL-2611-0396</a><small>CMD-11676</small>', c(C[3]), 'F. Bonnet', '18 nov.', badge('Livré', 'ok'), '<b>2 250,00 €</b>', A('Imprimer le BL', 'Ouvrir le bon d’expédition|Imprimer le bon de commande|Historique des paiements', '')]], check=True),
                   pager('2 bons de livraison', 'Page 1 sur 1'))
    fact = ('<div class="banner">' + ico('alert') + '<p><b>517 factures échues pour 81 200 €.</b> Relances actives : 3 niveaux (échéance, +15 j, +30 j, +45 j service juridique).</p>'
            + btn('Résumé des impayés', sm=True) + btn('Envoyer les impayés', 'primary', sm=True) + '</div>'
            + list_card(bar('N° de facture, client, commande…', sel('Période', PERIODE) + sel('Paiement', ['tous', 'Payée', 'Partiellement payée', 'Impayée']), ['Client', 'Date du@date', 'Date au@date'],
                            chips([('Toutes', 426, ''), ('Payée', 331, ''), ('Partiellement payée', 17, ''), ('Impayée', 78, ''), ('Échues', 517, 'alert')])),
                        table(['Facture', 'Client', 'Commercial', 'Date', 'Paiement', 'Relances', ('Montant TTC', 'r'), ('Action', 'r')], [
                            ['<a href="#">FA-2611-0932</a><small>CMD-11681</small>', c(C[1]), '—', '19 nov.', PAY['ok'], '—', '<b>127,58 €</b>', A('Imprimer', 'Ouvrir la commande|Historique des paiements|Créer un avoir|Envoyer par e-mail', '')],
                            ['<a href="#">FA-2611-0921</a><small>CMD-11674</small>', c(C[4]), '—', '18 nov.', PAY['no'], '—', '<b>942,10 €</b>', A('Enregistrer un règlement', 'Ouvrir la commande|Historique des paiements|Créer un avoir|Envoyer par e-mail|Relancer')],
                            ['<a href="#">FA-2610-0418</a><small>CMD-11391</small>', c(C[3]), 'F. Bonnet', '15 oct.', PAY['no'], '<span class="late">3 relances</span>', '<b>2 100,00 €</b>', A('Relancer', 'Ouvrir la commande|Historique des paiements|Enregistrer un règlement|Créer un avoir')]], check=True, name='la facture'),
                        pager('1 à 30 sur 426 factures', 'Page 1 sur 15'))
            + bulkbar('Envoyer la sélection par e-mail', ['Fusionner en PDF', 'Relancer', 'Exporter en Excel']))
    avoirs = list_card(bar('N° d’avoir, facture, client…', sel('Période', PERIODE), ['Client', 'Date du@date', 'Date au@date']),
                       table(['Avoir', 'Client', 'Commercial', 'Facture d’origine', 'Date', ('Total TTC', 'r'), ('Action', 'r')], [
                           ['<a href="#">AV-2611-0012</a>', c(C[5]), '—', 'FA-2611-0902', '17 nov.', '<b>−86,40 €</b>', A('Imprimer', 'Ouvrir la commande|Ouvrir le dossier client', '')],
                           ['<a href="#">AV-2611-0011</a>', c(C[0]), 'F. Bonnet', 'FA-2610-0844', '6 nov.', '<b>−24,00 €</b>', A('Imprimer', 'Ouvrir la commande|Ouvrir le dossier client', '')]]), pager('2 avoirs', 'Page 1 sur 1'))
    pos = ('<div class="cols"><div class="grow stack">' + card(head('Ajouter des produits', '<div class="seg" role="group" aria-label="Mode de saisie"><button aria-pressed="true">Code-barres</button><button aria-pressed="false">Grille</button></div>')
           + '<div class="filters"><label class="search" style="flex:2 1 240px;max-width:none;background:var(--surface)">' + ico('search') + '<input aria-label="Code-barres" placeholder="Scannez ou saisissez un code-barres…"></label>'
           + field('Quantité@number') + btn('Ajouter', 'soft', 'plus') + btn('Produit sans code-barres') + '</div>'
           + empty('cart', 'Le panier est vide', 'Scannez un code-barres ou choisissez un produit dans la grille.'))
           + card(head('Ventes récentes', badge('20 dernières', dot=False)) + empty('clock', 'Aucune vente enregistrée', 'L’historique des ventes au point de vente apparaîtra ici.'))
           + '</div><div class="aside sticky-aside">' + card(head('Vente en cours') + field('Entité commerciale*|Choisir une entité…,Dental Groupe,Oofti,Safe Implant') + field('Client')
           + btn('Nouveau client', sm=True, icon='plus') + '<div class="total-line"><span>Lignes</span><b class="num">0</b></div><div class="total-line big"><span>Total</span><span class="num">0,00 €</span></div>'
           + btn('Finaliser la vente', 'primary', 'check')) + '</div></div>')
    E['ventes.html'] = {'panels': {0: devis, 2: bl, 3: fact, 4: avoirs, 5: pos}, 'primary': {0: 'Nouvelle proposition commerciale', 2: '', 3: '', 4: 'Retour rapide', 5: ''}}
    modal('retour', ['Retour rapide'], 'Retour rapide (plusieurs lignes)', ['Client*=', 'Scanner un produit (code GS1) ou le chercher=', '#Lignes : produit, prix de vente initial, remise € et %, prix unitaire, quantité', 'Motif~', 'Notes internes~'],
          'Valider le retour', 'Retour validé, avoir créé (simulation)', 'Le brouillon est enregistré automatiquement.')
    modal('statsfact', ['Statistiques factures'], 'Statistiques factures', ['Année|2026,2025,2024', 'Période|Toute l’année,Trimestre 1,Trimestre 2,Trimestre 3,Trimestre 4', 'Jusqu’au@date',
                                                                             'Export|Factures de l’année (ZIP Excel par mois),Factures par client (CSV),Lignes par mois (ZIP Excel),TVA collectée par mois (CSV)'], 'Calculer', 'Statistiques calculées (simulation)')
    modal('pdf', ['Fusionner en PDF', 'PDF fusion factures'], 'Fusionner des factures en un PDF', ['Client=', 'Du@date', 'Au@date'], 'Générer le PDF', 'PDF généré (simulation)')
    page('ventes.html', 'ventes', 'Ventes', 'Propositions commerciales, commandes, livraisons, factures et avoirs',
         more_btn(['Exporter en Excel', 'Statistiques factures', 'PDF fusion factures', 'Partenariats>partenariats.html']) + btn('Point de vente', icon='pos', href='ventes.html#onglet-5')
         + btn('Nouvelle commande', 'primary', 'plus', 'commande-nouvelle.html'), cmd,
         tabs([('Propositions commerciales', '526'), ('Commandes', '82 206'), ('Bons de livraison', '397'), ('Factures', '426'), ('Avoirs', '12'), 'Point de vente'], 1))

    # ================= 3. NOUVELLE COMMANDE =================
    lines = table(['Produit', ('Quantité', 'r'), ('Prix unitaire HT', 'r'), ('Remise', 'r'), ('Total HT', 'r'), ''], [
        [c('Résine composite nano-hybride A3,5', 'RC-A35 · 18 en stock'), '<input class="input num" style="width:72px;text-align:right" value="2" aria-label="Quantité">', '37,10 €', '—', '<b>74,20 €</b>', kebab('Actions sur la ligne', 'Modifier la remise|Changer de lot|!Retirer la ligne')],
        [c('Pointes de gutta-percha 4 %, boîte de 60', 'GP-04 · <span class="late">2 en stock</span>'), '<input class="input num" style="width:72px;text-align:right" value="4" aria-label="Quantité">', '5,75 €', '10 %', '<b>20,70 €</b>', kebab('Actions sur la ligne', 'Modifier la remise|Changer de lot|!Retirer la ligne')]])
    recap = (head('Récapitulatif') + '<div class="total-line"><span>Total HT</span><b class="num">94,90 €</b></div><div class="total-line"><span>Remise globale</span><b class="num">0 %</b></div>'
             '<div class="total-line"><span>TVA 20 %</span><b class="num">18,98 €</b></div><div class="total-line big"><span>Total TTC</span><span class="num">113,88 €</span></div>'
             + item('Encours client : 105,00 €', 'Limite de crédit 2 000 € · à jour', tone='warn', icon='alert', soft=True))
    general = (card(head('Client et entité', btn('Nouveau client', sm=True, icon='plus')) + '<div class="form-grid">' + field('Entité commerciale*|Choisir une entité…,Dental Groupe,Oofti,Safe Implant') + field('Client*') + field('Patient') + '</div>')
               + card(head('Livraison et suivi') + '<div class="form-grid">' + field('Type de livraison|Choisir…,Chronopost,DHL,DPD,Fedex,Coursier,Sur place,Ciblex') + field('Date d’échéance souhaitée*@date') + field('Date de livraison prévue@date')
                      + field('Niveau de priorité|Normale,Urgente') + field('Canal de vente|Général,Sites internet,Téléphone,GACD,Commerciaux') + field('Remise globale@number') + field('Type de remise|%,€')
                      + field('?Générer et envoyer la facture à la validation') + field('?Enregistrer comme proposition commerciale') + '</div>'))
    detail = card('<div class="card-bar">' + head('Produits de la commande', btn('Commande rapide', sm=True)) + bar('Ajouter un produit par nom, référence ou code-barres', cols=False) + '</div>' + lines, pad=False)
    notes = card(head('Notes') + field('Note interne~') + field('Note visible sur la facture~'))
    E['commande-nouvelle.html'] = {'panels': {1: detail, 2: notes}}
    page('commande-nouvelle.html', 'ventes', 'Nouvelle commande', 'Brouillon · enregistré automatiquement', btn('Aperçu du bon', icon='print'),
         f'<div class="cols"><div class="grow stack">{general}</div><div class="aside sticky-aside">{card(recap)}</div></div>'
         + '<div class="savebar"><span class="muted">Brouillon enregistré à 14 h 32</span>' + btn('Annuler', 'ghost', href='ventes.html') + btn('Précédent') + btn('Suivant')
         + btn('Enregistrer en brouillon') + btn('Valider la commande · 113,88 €', 'primary', 'check') + '</div>',
         tabs(['Général', 'Détail de la commande', 'Notes']), back=('Ventes', 'ventes.html'))

    # ================= 4. CLIENTS =================
    risk = {'ok': badge('À jour', 'ok'), 'l': badge('Léger', 'info'), 'm': badge('Modéré', 'warn'), 'e': badge('Élevé', 'danger'), 'c': badge('Critique', 'danger')}
    crows = [(C[0], 'CL-00412 · Cabinet', 'Dr C. Renaud', 'Lyon', '04 00 00 00 01', 'contact@renaud.example', 'F. Bonnet', '19 nov.', '2 nov.', '105,00 €', 'l'),
             (C[1], 'CL-00388 · Cabinet', 'Dr A. Martin', 'Paris', '01 00 00 00 02', 'accueil@lilas.example', '—', '19 nov.', '19 nov.', '0,00 €', 'ok'),
             (C[2], 'CL-00127 · Centre', 'Dr P. Durand', 'Marseille', '04 00 00 00 03', 'direction@voltaire.example', 'F. Bonnet', '28 oct.', '30 sept.', '920,00 €', 'm'),
             (C[3], 'CL-00093 · Laboratoire', '—', 'Toulouse', '05 00 00 00 04', 'labo@prothesia.example', '—', '18 nov.', '2 sept.', '2 100,00 €', 'e'),
             ('Cabinet Bellecour', 'CL-00305 · Cabinet', 'Dr L. Petit', 'Lyon', '04 00 00 00 07', 'cabinet@bellecour.example', '—', '17 nov.', '11 juil.', '4 870,00 €', 'c')]
    MC = 'Ouvrir le dossier>client-fiche.html|Modifier le client|Passer commande>commande-nouvelle.html|Envoyer un e-mail|Relancer|!Désactiver le client'
    modal('client', ['Nouveau client', 'Créer un client', 'Modifier le client', 'Modifier la fiche'], 'Ajouter un client', [
        '#Identité', 'Nom du client*=', 'Type de client*|Cabinet,Clinique,Centre,Hôpital,Université,Société,Centre de formation,Laboratoire', 'Catégorie|Client,Prospect', 'Dentiste responsable', 'Assistant(e)', 'Statut du compte|Actif,Inactif', 'Commercial affecté|Aucun commercial,Florian Bonnet',
        '#Coordonnées', 'Adresse=', 'Code postal', 'Ville', 'Pays|France,Belgique,Suisse,Luxembourg', 'Téléphone du client@tel', 'E-mail du client@email', 'Téléphone du dentiste@tel', 'E-mail du dentiste@email',
        '#Facturation et livraison', 'Adresse de facturation (si différente)~', 'Adresse de livraison (si différente)~', 'Contact de facturation', 'Contact de livraison',
        '#Finances et suivi', 'Limite de crédit (€)*@number', 'Délai de paiement|Non renseigné,Paiement immédiat,15 jours,30 jours,45 jours,60 jours', 'Mode de règlement par défaut|Non défini,Espèces,Chèque,Virement,Carte bancaire,Prélèvement SEPA,Effet / LCR', 'Remise client (%)@number', 'Acompte (%)@number', 'Niveau de prix@number',
        '#Informations légales', 'SIREN', 'SIRET', 'N° de TVA intracommunautaire', '#Options avancées', '?Afficher les prix sur le portail client', '#Tags', 'Tags|Aucun,ADF,VIP', '#Notes', 'Notes~'],
          'Enregistrer le client', 'Client enregistré (simulation)')
    modal('tag', ['Nouveau tag'], 'Nouveau tag', ['Nom*=', 'Couleur|Vert sapin,Bleu,Violet,Rose,Orange,Olive,Ardoise'], 'Enregistrer', 'Tag créé (simulation)')
    E['clients.html'] = {'panels': {1: lst('Nom du tag', ['Tag', ('Clients', 'r'), ('Action', 'r')], [[badge('ADF', 'info', False), '412', A('Voir les clients', 'Renommer|Changer la couleur|!Supprimer', '')], [badge('VIP', 'ok', False), '38', A('Voir les clients', 'Renommer|Changer la couleur|!Supprimer', '')]])
                                    .replace('</div><div class="table-wrap">', '<p class="small muted">Créez ici les tags de segmentation, puis assignez-les dans la fiche client.</p></div><div class="table-wrap">', 1)},
                         'primary': {1: 'Nouveau tag'}}
    page('clients.html', 'clients', 'Clients', '19 464 actifs sur 19 467 au total', btn('Exporter', icon='down') + btn('Nouveau client', 'primary', 'plus'),
         kpis([('Clients actifs', '19 464', '3 inactifs'), ('Encours total', '96 300 €', '736 factures ouvertes'), ('Clients à risque', '42', '<span class="late">Encours élevé ou critique</span>'), ('Nouveaux ce mois', '58', '<span class="up">+12 %</span> vs octobre')])
         + list_card(bar('Nom ou code client…', sel('Statut', ['Actif', 'Inactif', 'Tous']) + sel('Tag', ['tous', 'ADF', 'VIP']),
                         ['Dentiste', 'Ville', 'Téléphone', 'E-mail', 'Encours min (€)@number', 'Encours max (€)@number', 'CA min (€)@number', 'Produit acheté'],
                         chips([('Tous', '19 464', ''), ('À jour', '18 728', ''), ('Léger', 412, ''), ('Modéré', 282, ''), ('Élevé', 31, ''), ('Critique', 11, 'alert')], 'Encours et retard de paiement')),
                     table(['Client', 'Dentiste', 'Ville', 'Téléphone / e-mail', 'Commercial', 'Dern. transaction / paiement', 'Statut', ('Encours', 'r'), ('Action', 'r')],
                           [[f'<a href="client-fiche.html">{n}</a><small>{k}</small>', d, v, f'<span class="num">{t}</span><small>{m}</small>', co, c(dt, 'Payé le ' + dp), badge('Actif', 'ok'), f'<b>{e}</b>' + risk[r], A('Commander', MC)]
                            for n, k, d, v, t, m, co, dt, dp, e, r in crows], check=True, name='le client'), pager('1 à 50 sur 19 464 clients', 'Page 1 sur 390'))
         + bulkbar('Envoyer une relance', ['Envoyer un e-mail', 'Ajouter un tag', 'Exporter']), tabs([('Clients', '19 464'), ('Tags', '2')]))

    # ---------- Fiche client ----------
    hist = table(['Commande', 'Date', 'Statut', 'Paiement', ('Montant TTC', 'r')], [['<a href="#">CMD-11682</a>', '19 nov. 2026', ST['prep'], PAY['no'], '<b>105,00 €</b>'], ['<a href="#">CMD-11590</a>', '2 nov. 2026', ST['liv'], PAY['ok'], '<b>412,30 €</b>']])
    infos = (head('Coordonnées', btn('Modifier la fiche', sm=True)) + '<div class="list">' + item('Dr Camille Renaud', 'Cabinet · CL-00412 · tags : ADF', icon='users', soft=True)
             + item('8 cours Vitton, 69006 Lyon', 'Livraison et facturation', icon='pin', soft=True) + item('04 00 00 00 01', 'contact@renaud.example', icon='mail', soft=True)
             + item('Paiement à 30 jours · virement', 'Limite de crédit 2 000 € · remise 0 %', icon='pos', soft=True) + '</div>')
    packs = card(head('Packs proposés au client', btn('Ajouter', sm=True, icon='plus')) + empty('box', 'Aucun pack proposé', 'Ajoutez un pack de produits à tarif négocié pour ce client.'))
    prix = card('<div class="card-bar">' + head('Prix spécifiques', btn('Copier les prix d’un autre client', sm=True) + btn('Édition multiple', sm=True) + btn('Ajouter', 'soft', sm=True, icon='plus')) + '</div>'
                + table(['Produit', ('Prix public HT', 'r'), ('Prix client HT', 'r'), ('Remise', 'r'), ('Action', 'r')], [[c('Résine composite A3,5', 'RC-A35'), '37,10 €', '<b>33,40 €</b>', '10 %', A('Modifier', '!Supprimer le prix', '')]]), pad=False)
    E['client-fiche.html'] = {'panels': {
        1: lst('N° de commande', ['Commande', 'Date', 'Statut', 'Paiement', ('Montant TTC', 'r')], [['<a href="#">CMD-11682</a>', '19 nov. 2026', ST['prep'], PAY['no'], '<b>105,00 €</b>']]),
        2: lst('N° de facture', ['Facture', 'Date', 'Paiement', ('Montant TTC', 'r'), ('Action', 'r')], [['<a href="#">Facture provisoire</a>', '19 nov. 2026', PAY['no'], '<b>105,00 €</b>', A('Enregistrer un règlement', 'Imprimer|Créer un avoir')]]),
        3: packs + prix,
        4: card(head('Échanges', btn('Nouvelle interaction', 'soft', sm=True)) + '<div class="list">' + item('Appel · 12 nov. 2026', 'Question sur le scanner intra-oral', soft=True, icon='headset') + '</div>'),
        5: card(empty('folder', 'Aucun document', 'Devis signés, mandats et attestations de ce client.', btn('Ajouter un document', 'soft', 'upload')))}}
    page('client-fiche.html', 'clients', 'Dr Camille Renaud', 'Cabinet · Lyon 6e · encours 105,00 € (à jour)',
         btn('Envoyer un e-mail', icon='mail') + btn('Modifier la fiche') + btn('Passer commande', 'primary', 'plus', 'commande-nouvelle.html'),
         kpis([('Chiffre d’affaires 12 mois', '4 870 €', '18 commandes'), ('Encours', '105,00 €', '1 facture impayée'), ('Dernière transaction', '19 nov.', 'Dernier paiement le 2 nov.'), ('Panier moyen', '271 €', 'TTC')])
         + '<div class="cols"><div class="grow">' + card('<div class="card-bar">' + head('Dernières commandes') + '</div>' + hist, pad=False) + '</div><div class="aside">' + card(infos) + '</div></div>',
         tabs(['Résumé', ('Commandes', '18'), ('Factures', '18'), 'Packs et prix spécifiques', 'Échanges', 'Documents']), back=('Clients', 'clients.html'))

    # ================= 5. PRODUITS =================
    stock = lambda n: badge('Rupture', 'danger') if n == 0 else badge(f'Stock faible · {n}', 'warn') if n < 5 else badge(f'En stock · {n}', 'ok')
    prod = [('VIOS', 'Ciment canalaire, seringue de 10 g', 'Endodontie', 'Dental Groupe', 1, 'V55A00 · 05/27', '57,60 €', '48,00 €'),
            ('ESCOM100-B2', 'Résine composite B2, seringue de 4 g', 'Matériaux dentaires', 'Dental Groupe', 0, '—', '24,00 €', '20,00 €'),
            ('IRR-UNIV', 'Lignes d’irrigation tubulure, lot de 10', 'Non catégorisé', 'Oofti', 6, '001 · sans date', '30,00 €', '25,00 €'),
            ('ETIQ-EDA', 'Étiquettes compatibles autoclave', 'Hygiène et stérilisation', 'Safe Implant', 18, '3 lots', '79,90 €', '66,58 €')]
    MP = 'Modifier le produit|Dupliquer|Voir les mouvements de stock|Ajuster le stock|Imprimer l’étiquette|Désactiver|!Supprimer'
    CATS = ['toutes', 'CFAO', 'Endodontie', 'Fils de suture', 'Formations', 'Hygiène et stérilisation', 'Implants', 'Instruments dentaires', 'Laboratoire', 'Le cabinet', 'Livraison', 'Matériaux dentaires', 'Prophylaxie']
    modal('produit', ['Nouveau produit', 'Modifier le produit'], 'Nouveau produit', [
        '#Informations produit', 'Type|Produit,Travail / prothèse,Formation', 'Nom du produit*=', 'SKU*', 'Code-barres', 'Description~', 'Classification', 'Catégorie principale|' + ','.join(CATS[1:]), 'Marque', 'Couleur',
        '#Stock initial', 'Entrepôt', 'Quantité@number', 'Seuil d’alerte@number', 'Seuil max@number', 'N° de lot', 'Date de péremption@date', 'Emplacement physique',
        '#Produits composés', 'Composant à ajouter', '#Vente additionnelle', 'Produit suggéré', '#Produits de substitution', 'Produit de remplacement',
        '#Tarification revente', 'Devise d’achat|EUR,USD,GBP,CHF', 'Prix d’achat HT (€)@number', 'Type de prix d’achat|HT,TTC', 'Coefficient de marge@number', 'Prix de vente TTC@number', 'Type de prix|TTC,HT', 'TVA par défaut|20 %,5,5 %,0 %',
        '#Marketplace et visibilité', '?Visible sur la place de marché', '?Visible sur le portail patient', '?Afficher le prix', 'Quantité minimale de commande@number',
        '#Médias et statut', 'Statut du produit|Actif,Inactif', 'Image principale@file', 'Galerie photos (5 max)@file'], 'Créer le produit', 'Produit créé (simulation)')
    modal('stock', ['Mouvement de stock', 'Réapprovisionner', 'Ajuster', 'Ajuster le stock'], 'Mouvement de stock', ['Type|Entrée,Sortie,Inventaire,Transfert', 'Entrepôt', 'Quantité*@number', 'Lot', 'Date de péremption@date', 'Emplacement', 'Motif~'], 'Enregistrer le mouvement', 'Stock mis à jour (simulation)', 'Produit :')
    stocks = views('stk', [
        ('Stocks', lst('Produit, référence ou lot', ['Référence', 'Produit', 'Entrepôt / emplacement', 'Lot', 'Péremption', ('Quantité', 'r'), ('Action', 'r')], [
            ['<code>VIOS</code>', '<a href="#">Ciment canalaire</a>', c('Dépôt principal', 'A-12'), 'V55A00', '31 mai 2027', '<b>1</b>', A('Ajuster', 'Voir l’historique|Transférer')],
            ['<code>ETIQ-EDA</code>', '<a href="#">Étiquettes autoclave</a>', c('Dépôt principal', 'B-07'), '00-1231', '12 déc. 2028', '<b>18</b>', A('Ajuster', 'Voir l’historique|Transférer')]])),
        ('Historique', lst('Produit ou utilisateur', ['Date', 'Produit', 'Mouvement', ('Quantité', 'r'), 'Par', 'Motif'], [['19 nov. 10 h 12', 'Résine composite A3,5', badge('Sortie', 'info'), '−2', 'Préparation', 'CMD-11682'], ['18 nov. 16 h 40', 'Étiquettes autoclave', badge('Entrée', 'ok'), '+20', 'F. Bonnet', 'Réception PO-2611-0076']])),
        ('Inventaire', card(empty('box', 'Aucun inventaire en cours', 'Lancez un inventaire pour compter le stock d’un entrepôt et corriger les écarts.', btn('Démarrer un inventaire', 'soft', 'plus'))))])
    refs = views('ref', [(t, lst(f'Rechercher dans {t.lower()}', ['Nom', ('Produits', 'r'), ('Action', 'r')], rows)) for t, rows in [
        ('Catégories', [[n, k, A('Modifier', '!Supprimer', '')] for n, k in [('Endodontie', '1 204'), ('Matériaux dentaires', '2 310'), ('Hygiène et stérilisation', '987')]]),
        ('Marques', [[n, k, A('Modifier', '!Supprimer', '')] for n, k in [('Dental Coop', '8 420'), ('Safe Implant', '1 902'), ('Oofti', '907')]]),
        ('Attributs', [[n, k, A('Modifier', '!Supprimer', '')] for n, k in [('Teinte', '412'), ('Taille', '1 077')]]),
        ('Entrepôts', [[n, k, A('Modifier', '!Supprimer', '')] for n, k in [('Dépôt principal', '11 229')]]),
        ('Emplacements', [[n, k, A('Modifier', '!Supprimer', '')] for n, k in [('A-12', '14'), ('B-07', '9')]])]])
    E['produits.html'] = {'panels': {1: stocks, 2: refs}, 'primary': {1: 'Mouvement de stock', 2: 'Ajouter un élément'}}
    page('produits.html', 'produits', 'Produits', 'Gestion du catalogue, de la tarification et des stocks · 11 229 références', btn('Exporter', icon='down') + btn('Importer', icon='upload') + btn('Nouveau produit', 'primary', 'plus'),
         kpis([('Références actives', '11 229', 'Sur 3 entités'), ('Stock faible', '36', '<span style="color:var(--warn-fg);font-weight:700">À réapprovisionner</span>'), ('Ruptures', '9 249', '<span class="late">Dont produits revendables</span>'), ('Lots à DLC courte', '139', 'Péremption dans moins d’un an')])
         + list_card(bar('Nom, référence, SKU, code-barres…', sel('Entité', ENT) + sel('Catégorie', CATS) + sel('Niveau', ['tous', 'En stock', 'Stock faible', 'Rupture']),
                         ['Statut|Actif,Inactif,Tous', 'Prix|Tous prix,0 à 50 €,50 à 100 €,100 à 500 €,500 € et plus', 'Marque|Toutes marques,Dental Coop,Oofti,Safe Implant', 'Fournisseur|Tous fournisseurs,Biomat Santé,Dentaprime Fournitures', '?Trier par entité'],
                         chips([('Toutes', '11 229', ''), ('Dental Groupe', '8 420', ''), ('Oofti', 907, ''), ('Safe Implant', '1 902', ''), ('Sans entité', 0, '')], 'Filtrer par entité')),
                     table(['SKU', 'Désignation', 'Catégorie', 'Entité', 'Stock', 'Lots', ('Prix TTC / HT', 'r'), 'Statut', ('Action', 'r')],
                           [[f'<code>{s}</code>', f'<a href="#">{d}</a><small>Dental Coop</small>', k, e, stock(n), f'<small>{lo}</small>', f'<b>{p}</b><small>HT {ht} · TVA 20 %</small>', badge('Actif', 'ok'), A('Réapprovisionner' if n < 5 else 'Modifier le produit', MP, 'soft' if n < 5 else '')]
                            for s, d, k, e, n, lo, p, ht in prod], check=True, name='le produit'), pager('1 à 50 sur 11 229 références', 'Page 1 sur 225'))
         + bulkbar('Modifier les prix', ['Changer de catégorie', 'Changer d’entité', 'Désactiver', 'Exporter']), tabs([('Catalogue', '11 229'), 'Stock', 'Référentiels']))

    # ================= 6. PARTENARIATS =================
    part_tbl = lambda who: list_card(bar(f'Nom du {who}', cols=False, chips_html=chips([('Tous', 0, ''), ('En attente', 0, ''), ('Acceptés', 0, ''), ('Refusés', 0, ''), ('Terminés', 0, '')])),
                                     '', empty('users', 'Aucune demande de partenariat', f'Les demandes de sous-traitance avec un {who} partenaire apparaîtront ici.', btn('Inviter un partenaire', 'soft', 'plus')))
    modal('partenaire', ['Inviter un partenaire'], 'Inviter un partenaire', ['Type|Cabinet dentaire,Laboratoire', 'Nom*=', 'E-mail*@email', 'Message~'], 'Envoyer l’invitation', 'Invitation envoyée (simulation)')
    E['partenariats.html'] = {'panels': {1: part_tbl('laboratoire')}}
    page('partenariats.html', 'partenariats', 'Partenariats', 'Cabinets dentaires ou laboratoires partenaires (sous-traitance)', btn('Inviter un partenaire', 'primary', 'plus'), part_tbl('cabinet'), tabs(['Cabinets', 'Laboratoires']))
