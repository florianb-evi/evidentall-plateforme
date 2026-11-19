"""Pages principales (2/2) : pilotage, catalogue, logistique, équipe, paramètres.

Même règle que pages.py : toutes les fonctions relevées sur la plateforme sont présentes.
"""


def register(h):
    globals().update(h)
    E = h['EXTRA']
    save = '<div class="savebar"><span class="muted">Aucune modification en attente</span>' + btn('Annuler', 'ghost') + btn('Enregistrer', 'primary', 'check') + '</div>'

    def form(title, specs, extra_html='', action=''):
        return card(head(title, action) + '<div class="form-grid">' + ''.join(field(s) for s in specs) + '</div>' + extra_html)

    def toggles(title, rows, intro=''):
        return card(head(title) + (f'<p class="muted">{intro}</p>' if intro else '') + '<div class="list">' + ''.join(
            item(n, d, f'<label class="small" style="display:flex;align-items:center;gap:8px"><input type="checkbox"{" checked" if on else ""}> Activé</label>', soft=True) for n, d, on in rows) + '</div>')

    h['MODALS'].pop('avoir', None)

    # ================= STATISTIQUES =================
    E['statistiques.html']['panels'][2] = '<div class="grid">' + ''.join(card(head(n) + kpis([('CA HT', ca, ''), ('Commandes', nb, ''), ('Panier moyen', pm, '')])) for n, ca, nb, pm in [
        ('Sans commercial', '128 400 €', '426', '301 €'), ('Florian Bonnet', '9 870 €', '24', '411 €'), ('Préparation commandes', '0 €', '0', '—')]) + '</div>'
    E['statistiques.html']['panels'][3] = ('<div class="grid">' + meters('Top 10 produits (CA)', [('Substitut osseux — boîte de 6 · 107 u.', '66 400 €', 100), ('Scanner intra-oral · 1 u.', '3 800 €', 14), ('Kit de chirurgie · 18 u.', '2 340 €', 10)])
                                           + meters('Performance par marque', [('Dental Coop', '104 300 €', 100), ('Safe Implant', '23 500 €', 23), ('Oofti', '1 400 €', 2), ('Sans marque', '5 300 €', 5)]) + '</div>'
                                           + lst('Désignation', ['Marque', 'Désignation', ('Quantité', 'r'), ('Total CA', 'r')], [['Dental Coop', 'Substitut osseux — boîte de 6', '107', '<b>66 400 €</b>'], ['Safe Implant', 'Kit de chirurgie', '18', '<b>2 340 €</b>']]))
    E['statistiques.html']['panels'][5] = (card(head('Objectifs commerciaux', btn('Définir l’objectif global', 'soft', sm=True))
                                               + chips([(m, '', '') for m in ['Janv.', 'Févr.', 'Mars', 'Avr.', 'Mai', 'Juin', 'Juil.', 'Août', 'Sept.', 'Oct.', 'Nov.', 'Déc.']], 'Mois')
                                               + '<div class="list">' + item('Objectif global · novembre', '128 400 € réalisés sur 180 000 €', '<div style="flex:1 1 160px">' + meter(71) + '</div>' + btn('Définir', sm=True), soft=True)
                                               + item('Florian Bonnet', '9 870 € réalisés sur 15 000 €', '<div style="flex:1 1 160px">' + meter(66) + '</div>' + btn('Définir', sm=True), soft=True) + '</div>'))
    E['statistiques.html']['panels'][7] = (kpis([('Marge brute', 'Non calculée', '<a href="produits.html">Renseigner les prix d’achat</a>'), ('Charges du mois', '0 €', '<a href="#onglet-6">Ajouter les charges</a>'), ('Résultat estimé', '—', 'Analyse de la rentabilité')])
                                           + '<div class="grid">' + card(head('Répartition des charges') + empty('chart', 'Aucune charge', 'Ajoutez vos charges pour voir leur répartition.'))
                                           + meters('Performance opérationnelle', [('Commandes expédiées sous 24 h', '82 %', 82), ('Commandes livrées sans retard', '64 %', 64)]) + '</div>')
    page('statistiques.html', 'stats', 'Statistiques', 'Analyse détaillée de l’activité', sel('Période', ['Ce mois', 'Aujourd’hui', 'Cette semaine', 'Ce trimestre', 'Cette année', 'Dates libres…']) + btn('Exporter', icon='down'),
         '<p class="small muted">Le chiffre d’affaires est le total des factures hors taxes, avoirs déduits. Le nombre de commandes compte toutes les commandes hors devis, annulées et brouillons.</p>'
         + kpis([('Chiffre d’affaires HT', '128 400 €', 'Avoirs déduits'), ('Nombre de commandes', '450', 'Hors devis, annulées, brouillons'), ('Panier moyen HT par facture', '315 €', '426 factures'), ('Marge brute', 'Non calculée', '<a href="produits.html">Renseigner les prix d’achat</a>')])
         + f'<div class="cols"><div class="grow">{card(chart + "<p class=small><span class=badge>Réalisé</span> <span class=badge>Objectif</span></p>")}</div><div class="aside">'
         + card(head('Répartition par sous-catégorie') + empty('box', 'Aucune donnée disponible', 'Catégorisez vos produits pour voir la répartition.', btn('Catégoriser les produits', 'soft', href='produits.html'))) + '</div></div>',
         tabs(['Aperçu', 'Anticipation IA', 'Commerciaux', 'Produits et marques', 'Clients et villes', 'Objectifs', 'Charges', 'Finances']))

    # ================= COCKPIT =================
    mails = [('Cabinet dentaire des Lilas', 'Question sur la commande CMD-11681', '14 h 05', True), ('Laboratoire Prothésia', 'Demande de devis scanner intra-oral', '11 h 40', False)]
    folders = ''.join(f'<a class="mail-item" href="#"{" aria-current=true" if i == 0 else ""}>{f}</a>' for i, f in enumerate(['Réception (3)', 'Envoyés', 'Brouillons', 'Indésirables', 'Corbeille', 'Archives']))
    mlist = ('<label class="search" style="max-width:none;margin-bottom:8px">' + ico('search') + '<input type="search" aria-label="Rechercher un message" placeholder="Rechercher un message"></label>'
             + ''.join(f'<a class="mail-item" href="#"{" aria-current=true" if cur else ""}><b>{s}</b><small class="muted" style="float:right">{t}</small><div>{o}</div></a>' for s, o, t, cur in mails))
    reading = ('<div class="card-head"><h2>Question sur la commande CMD-11681</h2><div class="actions">' + btn('Archiver', sm=True) + kebab(menu='Répondre|Transférer|Marquer comme non lu|Déplacer vers…|Indésirable|!Supprimer') + '</div></div>'
               '<p class="muted">Cabinet dentaire des Lilas · aujourd’hui à 14 h 05</p><p>Bonjour, pouvez-vous me confirmer la date d’expédition de notre commande passée ce matin ?</p>'
               f'<div class="reply"><input aria-label="Votre réponse" placeholder="Écrire une réponse…">{btn("Envoyer", "primary", "send", sm=True)}</div>')
    eliabar = ('<div class="banner info">' + ico('send') + '<p><b>Elia</b> · Florian, écrivez à Elia ou lancez la discussion.</p>' + btn('Parler', sm=True) + btn('Discuter', 'soft', sm=True) + '</div>')
    E['messagerie.html']['panels'][1] = form('Vos outils', ['Catégorie|Autre,Transporteur,Banque,Fournisseur', 'Nom de l’outil', 'Adresse (https://)@url'], '<div class="actions">' + btn('Ajouter', 'soft', 'plus') + '</div>'
                                             '<div class="list">' + item('Espace transporteur', 'Suivi des colis', btn('Ouvrir', sm=True) + kebab(menu='Modifier|!Retirer'), icon='truck', soft=True) + '</div>')
    E['messagerie.html']['panels'][2] = card(head('Elia', btn('Importer la liste', sm=True) + btn('Ouvrir la facturation', sm=True, href='ventes.html#onglet-3')) + '<div class="chat"><div class="bubble"><b>Elia</b><br>Bonjour Florian, que voulez-vous faire ?</div>'
                                             '<div class="actions" style="margin-left:0">' + ''.join(btn(t, sm=True) for t in ['Retrouve mes dernières factures', 'Résume les messages classés', 'Prépare un post pour présenter le cabinet', 'Ouvre le courrier', 'Comment Elia peut m’aider ?']) + '</div>'
                                             f'<div class="reply"><input aria-label="Votre demande" placeholder="Florian, dites à Elia ce que vous voulez faire">{btn("Parler", sm=True)}{btn("Discuter", sm=True)}{btn("Envoyer", "primary", "send", sm=True)}</div></div>')
    E['messagerie.html']['panels'][3] = (form('Comptes connectés', ['Réseau|Instagram,Facebook,LinkedIn', 'Identifiant (@cabinet)', 'Adresse du profil (https://)@url'], '<div class="actions">' + btn('Ajouter le compte', 'soft', 'plus') + '</div>')
                                         + card(head('Rédigez une publication, ou demandez une idée à Elia') + '<div class="actions" style="margin-left:0">' + ''.join(btn(t, sm=True) for t in ['Découvrez notre cabinet', 'Nouveau : prise de rendez-vous en ligne', 'Merci à nos patients pour leur confiance']) + '</div>'
                                                + field('Texte~') + '<div class="actions">' + btn('Garder en brouillon') + btn('Mettre en file', 'primary', 'send') + '</div>'))
    page('messagerie.html', 'mail', 'Cockpit', 'Courrier, outils, assistant Elia et réseaux sociaux', btn('Actualiser') + btn('Connecter une boîte', icon='mail') + btn('Nouveau message', 'primary', 'plus'),
         '<div class="banner">' + ico('mail') + '<p><b>Aucune boîte connectée.</b> Connectez Gmail, Outlook ou une messagerie professionnelle pour lire et envoyer vos messages depuis Evidentall. (Exemple d’affichage ci-dessous.)</p>' + btn('Connecter une boîte', 'soft', sm=True) + '</div>'
         + card(f'<div class="mail"><nav aria-label="Dossiers">{folders}</nav><div>{mlist}</div><article>{reading}</article></div>', pad=False) + eliabar,
         tabs([('Courrier', '3'), 'Outils', 'Elia', 'Réseaux']))

    # ================= PROSPECTIONS ET SUIVIS =================
    TS = ['Date', 'Client', 'Type', 'Titre de l’évènement', 'Description', 'Commercial assigné', 'Source du contact', 'Relance', ('Action', 'r')]
    suivis = lambda n: [['19 nov. 10 h 00', '<a href="#">Clinique dentaire du Port</a>', badge('Appel', dot=False), 'Présentation du scanner', 'Intéressée, rappeler après devis', 'F. Bonnet', 'Salon', '<span class="late">En retard de 2 j</span>', A('Relancer', 'Modifier|Marquer comme fait|Passer commande|!Supprimer')],
                        ['18 nov. 15 h 30', '<a href="#">Dr Inès Colin</a>', badge('Visite', dot=False), 'Démonstration au cabinet', 'Démo faite, attend un tarif', 'F. Bonnet', 'Recommandation', 'Aujourd’hui', A('Relancer', 'Modifier|Marquer comme fait|!Supprimer')]][:n]
    prospects = lambda: lst('Rechercher un prospect…', ['Prospect', 'Ville', 'Statut', 'Dernier contact', 'Prochaine relance', ('Action', 'r')], [
        ['<a href="#">Clinique dentaire du Port</a>', 'Marseille', badge('En discussion', 'info'), '19 nov.', '<span class="late">En retard de 2 j</span>', A('Ajouter une interaction', 'Convertir en client|Modifier|!Supprimer')],
        ['<a href="#">Dr Inès Colin</a>', 'Lyon', badge('Démonstration faite', 'ok'), '18 nov.', 'Aujourd’hui', A('Ajouter une interaction', 'Convertir en client|Modifier|!Supprimer')]])
    modal('interaction', ['Nouvelle interaction', 'Ajouter une interaction', 'Planifier'], 'Nouvelle interaction', ['Client*=', 'Type|Appel,Visite,E-mail,Salon,Autre', 'Titre de l’évènement=', 'Commercial assigné|Florian Bonnet,Sans commercial', 'Date@date', 'Heure@time', 'Description*~', 'Source du contact (facultatif)|—,Recommandation,Site internet,Salon,Autre', 'Relance (facultatif)@date'], 'Enregistrer', 'Interaction enregistrée (simulation)')
    E['prospection.html'] = {'panels': {0: prospects(), 2: prospects(), 3: list_card(bar('Client, titre, commercial…', sel('Type', ['tous', 'Appel', 'Visite', 'E-mail'])), table(TS, suivis(2)), pager('4 suivis', 'Page 1 sur 1')),
                                        4: views('rap', [('Vue laboratoire', kpis([('Interactions', '14', 'Ce mois'), ('Prospects convertis', '2', 'Sur 12'), ('Taux de conversion', '18 %', '')]) + meters('Par commercial', [('Florian Bonnet', '11', 80), ('Sans commercial', '3', 20)])),
                                                         ('Mon activité', kpis([('Mes interactions', '11', 'Ce mois'), ('Mes relances à traiter', '3', ''), ('Mon objectif', '60 %', '9 sur 15')]))])
                                        + '<div class="actions">' + btn('Objectifs commerciaux', href='statistiques.html#onglet-5') + '</div>'}}
    page('prospection.html', 'prospection', 'Prospections et suivis', 'Suivez vos prospects et vos relances commerciales', btn('Importer des prospects', icon='upload') + btn('Nouvelle interaction', 'primary', 'plus'),
         kpis([('Prospects actifs', '12', '4 ajoutés ce mois'), ('Relances à traiter', '3', '<span class="late">1 en retard</span>'), ('Taux de conversion', '18 %', 'Sur 90 jours')])
         + list_card(bar('Client, titre, commercial…', sel('Type', ['tous', 'Appel', 'Visite', 'E-mail']) + sel('Relance', ['toutes', 'En retard', 'Aujourd’hui'])), table(TS, suivis(2)), pager('2 suivis', 'Page 1 sur 1')),
         tabs(['Mes prospections', 'Mes suivis', 'Toutes les prospections', 'Tous les suivis', 'Rapports et performance'], 1))

    # ================= SERVICE CLIENT =================
    TK = ['À faire', 'Assigné', 'En cours', 'En attente', 'Résolu', 'Clôturé', 'Annulé']
    sev = {'c': badge('Critique', 'danger'), 'm': badge('Moyenne', 'warn'), 'f': badge('Faible')}
    trows = [('TK-2026-0005', 'Dr Hugo Lambert', 'Capteur intra-oral : pas de réponse', 'Technique', 'c', ('À faire', 'warn'), 'Non assigné', '19 nov. 09 h 12', 'Prendre en charge'),
             ('TK-2026-0003', 'Cabinet Bellecour', 'Passerelle logiciel d’imagerie', 'Technique', 'm', ('Assigné', 'info'), 'D. Yan', '12 nov. 10 h 22', 'Répondre'),
             ('TK-2026-0002', 'Centre dentaire Voltaire', 'Colis reçu incomplet', 'Autre', 'm', ('En cours', 'info'), 'S. Peretti', '9 nov. 15 h 11', 'Répondre'),
             ('TK-2026-0001', 'Laboratoire Prothésia', 'Installation du capteur', 'Formation', 'f', ('Résolu', 'ok'), 'D. Yan', '2 nov. 01 h 56', None)]
    modal('ticket', ['Nouveau ticket'], 'Nouvelle intervention', ['Client*=', 'Type de demande|Technique,Formation,Autre', 'Sévérité|Faible,Moyenne,Critique', 'Titre*=', 'Description*~', 'Date d’intervention@datetime-local', 'Assigné à|Florian Bonnet,D. Yan,S. Peretti', 'N° de série du produit', 'Facture associée', 'Produit concerné', 'Pièce jointe (facultatif)@file'], 'Créer', 'Ticket créé (simulation)')
    page('service-client.html', 'sav', 'Service client', 'Gestion des tickets d’intervention SAV · 5 ouverts', btn('Exporter', icon='down') + btn('Nouveau ticket', 'primary', 'plus'),
         list_card(bar('Référence, client ou titre', sel('Type', ['tous', 'Technique', 'Formation', 'Autre']) + sel('Assigné', ['tous', 'Non assigné', 'D. Yan', 'S. Peretti']), None,
                       chips([('Tous les statuts', 9, '')] + [(s, n, 'alert' if s == 'À faire' else '') for s, n in zip(TK, [2, 1, 1, 1, 2, 1, 1])])),
                   table(['Réf.', 'Client', 'Titre', 'Type', 'Sévérité', 'Statut', 'Assigné', 'Date', ('Action', 'r')],
                         [[f'<a href="#">{r}</a>', f'<b>{cl}</b>', t, ty, sev[s], stat(st[0], st[1], TK), a, d, A(ac, 'Modifier|Assigner|Ajouter une pièce jointe|Voir la facture associée|!Supprimer')] for r, cl, t, ty, s, st, a, d, ac in trows]),
                   pager('9 tickets', 'Page 1 sur 1')))

    # ================= COMPARATEUR DE PRIX =================
    src = [('Votre boutique en ligne', 'https://oofti.example', 'ok', 'Actif'), ('Dentaprix', 'https://dentaprix.example', 'ok', 'Actif'), ('Mégastock Dentaire', 'https://megastock.example', 'ok', 'Actif'),
           ('Docteur Fournitures', 'https://docteur-fournitures.example · accès refusé (HTTP 403)', 'danger', 'Erreur'), ('Promo Cabinet', 'https://promo-cabinet.example · accès refusé (HTTP 403)', 'danger', 'Erreur')]
    runs = [('19/11/2026 12 h 20 · automatique', 'Terminée · 25 recherches · 3 alertes'), ('18/11/2026 12 h 20 · automatique', 'Terminée · 11 recherches · 2 alertes'), ('17/11/2026 18 h 20 · automatique', 'Terminée · 44 recherches · 2 alertes')]
    modal('site', ['Ajouter un concurrent', 'Ajouter un site', 'Modifier le site'], 'Site concurrent', ['Nom du site*', 'Adresse du site*@url', 'Adresse de recherche (utilisez {q} pour le mot-clé)=', 'Actif|Oui,Non'], 'Enregistrer', 'Site enregistré (simulation)')
    reg = (form('Moteur de tarification', ['Mode d’écart|Pourcentage sous le moins cher,Montant fixe sous le moins cher', 'Écart %@number', 'Écart €@number', 'Marge minimale % (sur le coût d’achat)@number', 'TVA %@number', 'Fréquence automatique (heures)@number',
                                           '?Arrondi psychologique (,99)', '?Appliquer automatiquement les prix recommandés', '?Veille automatique', '?Afficher tout le catalogue revente dans le comparateur'],
                '<p class="small muted">Le prix recommandé est calculé en TTC, puis ramené au type de prix du produit (HT ou TTC).</p>') + save)
    imp = card(head('Import des liens concurrents', btn('Catalogue prérempli', sm=True, icon='down') + btn('Modèle vide', sm=True, icon='down'))
               + '<p class="muted">Le catalogue prérempli liste les produits revente vendus sur la période choisie.</p>' + field('Lignes à importer (slug;référence;prix;url;nom)~') + '<div class="actions">' + btn('Importer', 'primary', 'upload') + '</div>')
    E['comparateur-prix.html']['panels'][6] = reg
    E['comparateur-prix.html']['panels'][7] = imp
    E['comparateur-prix.html']['primary'] = {3: 'Appliquer toutes les recommandations valides', 6: '', 7: ''}
    page('comparateur-prix.html', 'prix', 'Comparateur de prix', 'La veille parcourt les produits de votre boutique par lots de 300 recherches · dernière veille aujourd’hui à 12 h 20',
         btn('Ajouter un concurrent', icon='plus') + btn('Relancer la veille', 'primary', 'play'),
         '<div class="banner danger">' + ico('alert') + '<p><b>2 sites concurrents refusent l’accès à la veille (HTTP 403).</b> 0 proposition lors de la dernière veille pour ces sites.</p>' + btn('Voir le détail technique', sm=True) + '</div>'
         + kpis([('Références suivies', '99', 'Sur votre boutique'), ('Liens confirmés', '1', 'Couples produit × site'), ('À valider', '8 272', '<a href="#onglet-2">Valider les correspondances</a>'), ('Plus chers que le marché', '2', '<span class="late">Prix à revoir</span>')])
         + kpis([('Couverture traitée', '0,1 %', 'Couples confirmés'), ('Indice de prix', '191,5', '100 = aligné sur le moins cher'), ('Alertes non lues', '50', '<a href="#onglet-4">Lire les alertes</a>'), ('Prix à appliquer', '2', '<a href="#onglet-3">Voir les recommandations</a>')])
         + '<div class="grid">' + card(head('Sources concurrentes', btn('Ajouter un concurrent', sm=True, icon='plus')) + '<p class="small muted">Créez, modifiez ou supprimez les sites à comparer.</p><div class="list">'
                                        + ''.join(item(n, u, badge(l, t) + btn('Modifier le site', sm=True) + kebab(menu='Tester la connexion|Désactiver|!Supprimer'), soft=True) for n, u, t, l in src) + '</div>')
         + card(head('Dernières veilles', '<a href="#">Historique</a>') + '<div class="list">' + ''.join(item(d, r, badge('Terminée', 'ok'), soft=True) for d, r in runs) + '</div>') + '</div>',
         tabs(['Tableau de bord', 'Comparateur', ('Matching', '8 272'), 'Recommandations', ('Alertes', '50'), 'Surveillance', 'Règles', 'Import CSV']))

    # ================= CATALOGUES PARTENAIRES =================
    part = [('Dentaprix', 'https://dentaprix.example', '#32 · en cours', '3 325 en catalogue', '3 325 sur la place de marché', '0 en attente · 3 325 à jour · 500 écartées · 0 en erreur', 'catalogue.dentaprix@votre-domaine.example', 95, 'info', 'En cours'),
            ('Mégastock Dentaire', 'https://megastock.example', '#30 · en cours', '12 577 en catalogue', '12 564 sur la place de marché', '0 en attente · 12 577 à jour · 107 écartées · 1 en erreur', 'catalogue.megastock@votre-domaine.example', 100, 'ok', 'À jour'),
            ('Promo Cabinet', 'https://promo-cabinet.example', '#36 · en cours', '8 075 en catalogue', '7 843 sur la place de marché', '12 en attente · 8 075 à jour · 1 écartée · 3 en erreur', 'catalogue.promo@votre-domaine.example', 88, 'danger', 'Erreurs')]
    page('catalogues-partenaires.html', 'partenaires', 'Catalogues partenaires', 'Chaque fournisseur a son propre laboratoire revente : les fiches sont récupérées puis publiées sur la place de marché',
         btn('Créer les comptes', icon='users') + btn('Arrêter', 'danger', 'stop') + btn('Peupler les catalogues', 'primary', 'play'),
         '<div class="banner info">' + ico('clock') + '<p><b>Le comparateur de prix reste inchangé.</b> Une tâche horaire reprend la file et rafraîchit les produits importés depuis plus de 12 heures. Les passages suivants mettent à jour les fiches déjà liées.</p></div>'
         + list_card(head('Laboratoires revente') + bar('Fournisseur', cols=True), table(['Fournisseur', 'Laboratoire', 'Produits', 'File d’import', 'Connexion', 'État', ('Action', 'r')],
                     [[c(n, u), lab, c(p1, p2), f'<div style="min-width:200px">{meter(pc)}<small style="white-space:normal">{f}</small></div>', f'<small>{cx}</small>', badge(l, t), A('Peupler', 'Voir les fiches en erreur|Réinitialiser la file|Créer le compte|!Arrêter', '')] for n, u, lab, p1, p2, f, cx, pc, t, l in part])))

    # ================= 24h DENTAIRE =================
    kind = lambda hh: ('', 'Terminé') if hh < 14 else ('live', 'En ligne') if hh == 14 else ('todo', 'À valider') if hh < 22 else ('ok', 'Validé') if hh == 22 else ('free', 'Libre')
    slots = ''.join(f'<button type="button" class="slot {kind(x)[0]}" aria-label="Créneau de {x} h, {kind(x)[1]}"><b>{x} h</b>{kind(x)[1]}</button>' for x in range(24))
    live = (head('En cours · 14 h – 15 h', badge('−24,8 %', 'info', False)) + '<div><b style="font-size:18px">Résine composite nano-hybride, teinte A3,5</b><p class="muted">20 capsules de 0,25 g · en ligne</p></div>'
            '<div><span class="price num">28,20 € HT</span> <s class="muted num">37,10 €</s></div><div><p class="small muted">Se termine dans 22 minutes · seuil 15 u. · stock 25</p>' + meter(63) + '</div>')
    nxt = (head('Prochain · 15 h – 16 h', badge('À valider', 'warn')) + '<div><b style="font-size:18px">Pointes de gutta-percha 4 ou 6 %, boîtes de 60</b><p class="muted">Endodontie · stock 53 · seuil 30 u.</p></div>'
           '<div><span class="price num">4,50 € HT</span> <s class="muted num">5,75 €</s> <span class="up">−21,7 % · marge 65,8 %</span></div><div class="actions">' + btn('Valider l’offre', 'ok', 'check') + btn('Prix et seuil') + btn('Changer de produit') + '</div>')
    MS = 'Prix et seuil|Replanifier|Verrouiller|Voir sur la boutique|Consulter le produit|Refuser l’offre|!Retirer du planning'
    plan = card(head('Planning 24 h du jeudi 19 novembre', btn('Vider le planning', 'danger', sm=True) + btn('Régénérer la proposition', sm=True) + btn('Publier sur la boutique', 'soft', sm=True)) + '<div class="list">' + ''.join(
        item(f'{a} h – {a + 1} h · {p}', f'Remise {r} · marge {mg} · stock {stk} · seuil {seu} u. · résultat : {res}', badge(s, t) + (btn('Valider l’offre', 'ok', sm=True) if s == 'À valider' else '') + kebab(menu=MS), soft=True)
        for a, p, r, mg, stk, seu, res, s, t in [(13, 'Colle composite', '−27,6 %', '—', 16, 9, '— u. · — acheteurs', 'Terminé', ''), (14, 'Résine composite A3,5', '−24,8 %', '65,8 %', 25, 15, 'en cours', 'En ligne', 'info'),
                                                  (15, 'Pointes de gutta-percha', '−21,7 %', '65,8 %', 53, 30, '—', 'À valider', 'warn'), (22, 'Ciment de scellement', '−25,0 %', '61 %', 12, 7, '—', 'Validé', 'ok')])
        + item('23 h – 0 h · créneau libre', 'Aucun produit planifié', btn('Ajouter un produit', 'soft', sm=True, icon='plus'), soft=True) + '</div>')
    modal('creneau', ['Changer de produit', 'Compléter le créneau de 23 h', 'Choisir un produit', 'Ajouter un produit', 'Prix et seuil'], 'Produit, prix et seuil du créneau', ['Produit*=', 'Prix promo HT*@number', 'Seuil d’achat (unités)@number', '?Verrouiller ce créneau'], 'Enregistrer le créneau', 'Créneau mis à jour (simulation)')
    fil = card(head('Fil de discussion — équipe et assistant') + '<div class="filters">' + sel('Créneau', ['Toute la journée', '14 h – 15 h — Résine composite', '15 h – 16 h — Pointes de gutta-percha']) + sel('Sujet', ['Message général (journée)', 'À propos d’un produit']) + '</div>'
               '<div class="chat"><div class="bubble"><b>Préparation commandes</b><br>Stock vérifié pour les créneaux de l’après-midi.</div><div class="bubble me"><b>Vous</b><br>Merci, je valide les 7 créneaux restants.</div>'
               f'<div class="reply"><input aria-label="Votre message" placeholder="Votre message… (Ctrl + Entrée pour envoyer)">{btn("Envoyer", "primary", "send", sm=True)}</div></div>')
    ana = (kpis([('Valeur du stock (prix de revient)', '412 800 €', ''), ('Dont stock dormant', '38 200 €', ''), ('Dont péremption < 6 mois', '6 900 €', '')])
           + kpis([('Créneaux publiés', '412', 'Ce mois'), ('Taux de seuil atteint', '61 %', ''), ('Unités vendues', '1 840', ''), ('CA HT promo', '18 400 €', '')])
           + '<div class="grid">' + meters('Couverture de stock (valeur par tranche)', [('Moins de 30 jours', '96 000 €', 40), ('30 à 90 jours', '182 000 €', 76), ('Plus de 90 jours', '134 800 €', 56)])
           + meters('Chiffre d’affaires mensuel : total et sites internet', [('Total HT', '128 400 €', 100), ('Sites internet HT', '50 600 €', 39)]) + '</div>'
           + lst('Catégorie', ['Catégorie', ('Produits', 'r'), ('Unités', 'r'), ('CA HT', 'r')], [['Matériaux dentaires', '214', '1 120', '<b>24 300 €</b>'], ['Endodontie', '96', '480', '<b>8 900 €</b>']])
           + lst('Produit', ['Date', 'Heure', 'Produit', ('Remise', 'r'), ('Seuil', 'r'), ('Acheteurs', 'r'), 'Statut'], [['18 nov.', '10 h', 'Gants nitrile', '20 %', '10', '14', badge('Seuil atteint', 'ok')], ['18 nov.', '11 h', 'Ciment canalaire', '15 %', '10', '3', badge('Seuil manqué', 'warn')]])
           + '<p class="small muted">Les ventes proviennent des commandes du canal « sites internet ». Aucune donnée de visites ou de conversion de la boutique n’est disponible.</p>')
    api = (card(head('Adresse du flux JSON', btn('Copier l’adresse', sm=True)) + '<p><code>https://votre-domaine.example/api/24h/2026-11-19.json</code></p><p class="muted">Ce qu’il faut publier, à quelle heure et à quel prix.</p>')
           + lst('Produit ou SKU', ['Heure', 'Produit', 'SKU', ('Prix normal HT', 'r'), ('Prix promo HT', 'r'), ('Remise', 'r'), ('Seuil', 'r'), 'Statut', 'Action attendue'],
                 [['14 h', 'Résine composite A3,5', '<code>RC-A35</code>', '37,10 €', '28,20 €', '24,8 %', '15', badge('En ligne', 'info'), 'Publier'], ['15 h', 'Pointes de gutta-percha', '<code>GP-04</code>', '5,75 €', '4,50 €', '21,7 %', '30', badge('À valider', 'warn'), 'Attendre la validation']])
           + card(head('Réponse JSON brute', btn('Copier', sm=True)) + '<pre class="small" style="overflow:auto;margin:0">{ "date": "2026-11-19", "slots": [ { "hour": 14, "sku": "RC-A35", "promo_ht": 28.20 } ] }</pre>'))
    E['24h-dentaire.html']['panels'].update({2: plan, 3: fil, 4: ana, 5: api})
    page('24h-dentaire.html', '24h', '24h Dentaire', 'Un produit en promotion flash chaque heure sur votre boutique. À l’issue de l’heure, le prix promo n’est conservé que si le seuil d’achat est atteint.',
         btn('‹ Jour précédent') + '<label class="field" style="flex:0 0 170px"><span class="sr">Choisir la date du planning</span><input type="date" value="2026-11-19"></label>' + btn('Jour suivant ›') + btn('Aujourd’hui') + btn('Valider les 7 créneaux', 'primary', 'check'),
         f'<div class="grid">{card(live, cls="hero")}{card(nxt)}</div>'
         + kpis([('Créneaux planifiés', '23 sur 24', '<a href="#">Compléter le créneau de 23 h</a>'), ('À valider', '7', '1 validé · 15 publiés'), ('Marge moyenne après remise', '65,8 %', 'Remise moyenne 25,9 %'), ('Valeur engagée', '6 293 € HT', 'Stock × prix promo, par créneau')])
         + card(head('Frise des 24 heures', '<span class="small muted">Terminé : 14 · En ligne : 1 · À valider : 7 · Validé : 1 · Libre : 1</span>') + f'<div class="slots">{slots}</div>'
                '<p class="small muted">7 derniers jours : 0 seuil atteint · 0 manqué. Cliquez sur un créneau pour voir le produit, modifier le prix ou valider.</p>')
         + '<div class="grid">' + meters('Répartition par catégorie', [('Sans catégorie', '7', 100), ('Matériaux dentaires', '4', 57), ('Instruments dentaires', '4', 57), ('Endodontie', '4', 57), ('Laboratoire', '2', 29), ('Hygiène et stérilisation', '2', 29)])
         + card(head('Derniers messages', '<a href="#onglet-3">Ouvrir le fil</a>') + empty('mail', 'Aucun message', 'Les échanges de l’équipe sur le planning du jour apparaîtront ici.')) + '</div>',
         tabs(['Résumé', 'Produits', 'Planning 24h', 'Fil de discussion', 'Analyses', 'Flux API']))

    # ================= ACHATS =================
    OPS = 'Contient,Ne contient pas,Commence par,Se termine par,Est,N’est pas,Est vide,N’est pas vide,Égal à,Différent de,Supérieur à,Supérieur ou égal à,Inférieur à,Inférieur ou égal à'
    adv = lambda cols_: ['Colonne|' + ','.join(cols_), 'Condition|' + OPS, 'Valeur']
    PS = ['Brouillon', 'Envoyée', 'Confirmée', 'Partiellement reçue', 'Reçue', 'Annulée']
    FS = ['Brouillon', 'Enregistrée', 'Partiellement payée', 'Payée', 'Annulée']
    arows = [('PO-2611-0076', 'Dentaprime Fournitures', '12 nov.', '20 nov.', '2 250,00 €', ('Envoyée', 'info'), 'Réceptionner'), ('PO-2610-0074', 'Biomat Santé', '26 oct.', '<span class="late">Retard 5 j</span>', '14 868,64 €', ('Partiellement reçue', 'warn'), 'Réceptionner'),
             ('Brouillon 104', 'Orthoplus Distribution', '21 oct.', '—', '0,00 €', ('Brouillon', ''), 'Reprendre'), ('PO-2610-0075', 'Medidental Europe', '8 oct.', '15 oct.', '3 080,39 €', ('Reçue', 'ok'), None)]
    modal('po', ['Nouvelle commande fournisseur'], 'Nouvelle commande fournisseur', ['Fournisseur*=', 'Statut|' + ','.join(PS), 'Date de commande*@date', 'Livraison prévue@date', 'Incoterms|Non renseigné,CFR,CIF,CIP,CPT,DAP,DAT,DDP', '#Lignes commandées (produit ou matière première)', 'Produit ou matière première', 'Quantité@number', 'Prix unitaire HT@number', 'Notes ou instructions spéciales~'], 'Créer la commande', 'Commande fournisseur créée (simulation)')
    modal('facture_f', ['Nouvelle facture'], 'Nouvelle facture fournisseur', ['Fournisseur*=', 'Commande liée (facultatif)', 'Numéro de facture fournisseur', 'Statut|' + ','.join(FS), 'Date de facture*@date', 'Date d’échéance@date', '#Lignes facturées (produit ou matière première, scan possible)', 'Produit ou matière première', 'Quantité@number', 'Notes~'], 'Créer la facture', 'Facture créée (simulation)')
    modal('avoir_f', ['Nouvel avoir'], 'Créer un avoir fournisseur', ['Facture fournisseur*|Facture 6 — Dentaprime Fournitures,Facture 3 — Biomat Santé'], 'Créer l’avoir', 'Avoir créé (simulation)')
    modal('fournisseur', ['Nouveau fournisseur'], 'Ajouter un fournisseur', ['#Identité', 'Nom du fournisseur*=', 'Alias', 'Code fournisseur', 'Code client (si aussi client)', 'Personne de contact', 'Téléphone*@tel', 'E-mail@email', 'Code postal', 'Ville',
                                                                         '#Informations légales', 'SIREN', 'SIRET', 'N° de TVA intracommunautaire', 'Code APE', '#Conditions', 'Échéance fournisseur|Comptant,15 jours,30 jours,45 jours,60 jours', 'Mode de règlement|Non défini,Espèces,Chèque,Virement,Carte bancaire,Prélèvement SEPA,Effet / LCR', 'Remise fournisseur (%)@number', 'Commande minimum (€)@number', 'Compte comptable de vente', 'Compte comptable d’achat',
                                                                         '#Adresses', 'Adresse~', 'Adresse de facturation~', 'Adresse de livraison~', '#Notes et qualification', 'Note privée~', 'Note publique~', 'Notes internes~', 'Statut de qualification|—,Qualifié,En cours,Refusé', 'Dernière évaluation@date', 'Note de qualification', '?Fournisseur actif'], 'Créer le fournisseur', 'Fournisseur créé (simulation)')
    E['achats.html'] = {'panels': {
        1: list_card(bar('Rechercher une facture…', '', adv(['N° facture', 'Fournisseur', 'Date facture', 'Date de création', 'Échéance', 'Montant', 'Payé', 'Statut'])),
                     table(['N° facture', 'Fournisseur', 'Date facture', 'Date de création', 'Échéance', ('Montant', 'r'), ('Payé', 'r'), 'Statut', ('Action', 'r')], [
                         ['<a href="#">F-88231</a>', c('Biomat Santé'), '26 oct.', '27 oct.', '<span class="late">Échue depuis 3 j</span>', '<b>14 868,64 €</b>', '0,00 €', stat('Enregistrée', 'warn', FS), A('Enregistrer un règlement', 'Voir|Imprimer|Créer un avoir|!Supprimer')],
                         ['<a href="#">F-10492</a>', c('Medidental Europe'), '8 oct.', '8 oct.', '8 déc.', '<b>3 080,39 €</b>', '3 080,39 €', stat('Payée', 'ok', FS), A(None, 'Voir|Imprimer|Créer un avoir')]]), pager('5 factures', 'Page 1 sur 1')),
        2: list_card(bar('Rechercher un avoir…', cols=False), '', empty('bag', 'Aucun avoir fournisseur', 'Aucun avoir fournisseur n’a été créé pour le moment.', btn('Nouvel avoir', 'soft', 'plus'))),
        3: list_card(bar('Rechercher un fournisseur…', '', adv(['Nom', 'Contact', 'Téléphone', 'E-mail', 'Ville', 'Délai de paiement', 'Statut'])),
                     table(['Nom', 'Contact', 'Téléphone', 'E-mail', 'Ville', 'Délai de paiement', 'Statut', ('Action', 'r')], [
                         ['<a href="#">Biomat Santé</a>', 'Service commandes', '01 00 00 00 10', 'commandes@biomat.example', 'Paris', '30 jours', badge('Actif', 'ok'), A('Commander', 'Modifier|Voir les commandes|Voir les factures|Désactiver|!Supprimer', '')],
                         ['<a href="#">Dentaprime Fournitures</a>', 'Accueil', '04 00 00 00 11', 'contact@dentaprime.example', 'Lyon', '45 jours', badge('Actif', 'ok'), A('Commander', 'Modifier|Voir les commandes|Voir les factures|Désactiver|!Supprimer', '')]]), pager('1 à 50 sur 53 fournisseurs', 'Page 1 sur 2'))},
        'primary': {1: 'Nouvelle facture', 2: 'Nouvel avoir', 3: 'Nouveau fournisseur'}}
    page('achats.html', 'achats', 'Achats', 'Gérez vos fournisseurs, commandes et facturation', btn('Exporter', icon='down') + btn('Nouvelle commande fournisseur', 'primary', 'plus'),
         list_card(bar('N° de commande ou fournisseur', sel('Période', PERIODE), adv(['N° commande', 'Fournisseur', 'Date', 'Livraison prévue', 'Montant', 'Statut']),
                       chips([('Toutes', 99, '')] + [(s, n, '') for s, n in zip(PS, [1, 4, 2, 2, 89, 1])])),
                   table(['N° commande', 'Fournisseur', 'Date', 'Livraison prévue', ('Montant', 'r'), 'Statut', ('Action', 'r')],
                         [[f'<a href="#">{n}</a>', f'<b>{f}</b>', d, l, f'<b>{m}</b>', stat(s[0], s[1], PS), A(a, 'Voir|Imprimer la commande fournisseur|Créer la facture|Dupliquer|!Annuler')] for n, f, d, l, m, s, a in arows]), pager('1 à 50 sur 99 commandes', 'Page 1 sur 2'))
         + '<p class="small muted">Préparez et suivez vos bons de commande fournisseurs. « Plus de filtres » permet de filtrer chaque colonne avec une condition (contient, égal à, supérieur à…).</p>',
         tabs([('Commandes fournisseurs', '99'), ('Factures', '5'), 'Avoirs fournisseurs', ('Fournisseurs', '53')]))

    # ================= EXPÉDITIONS =================
    ME = 'Modifier|Bon d’expédition|Étiquette 70 × 54 mm (référence + lot)|Documents joints|Suivre le colis|!Supprimer'
    erows = [('SH-2611-0346', 'CMD-11680 · 19/11', 'Centrale Dentaire Exemple', 'Sud Médic · 11 rue Blanche, 34250 Palavas · 04 00 00 00 20', '—', 'Ciblex', 'Préparation commandes', '—', ('Incomplète', 'warn'), 'Import automatique', 'Compléter'),
             ('SH-2611-0345', 'CMD-11679 · 19/11', C[5], 'Cabinet Morel · 2 rue de Gaulle, 33000 Bordeaux · 05 00 00 00 06', 'SELARL Morel', 'Ciblex', 'Préparation commandes', '8400 1000 5380', ('Complète', 'ok'), '—', 'Suivre le colis'),
             ('SH-2611-0344', 'CMD-11677 · 19/11', 'Dr Hugo Lambert', 'Dr Lambert · 112 rue Nationale, 59000 Lille · 03 00 00 00 08', 'Dr Lambert', 'Coursier', 'Dominique', '—', ('Reliquat', 'info'), '1 produit manquant', 'Expédier le reliquat')]
    modal('expedition', ['Nouvelle expédition', 'Compléter'], 'Nouvelle expédition', ['Référence commande*=', 'Méthode d’expédition|Choisir…,Chronopost,Ciblex,Coursier,TNT,UPS,Sur place', 'Préparateur de commande|Choisir…,Préparation commandes,Dominique', '#Lignes produit', 'Produit', 'Lot', 'Quantité@number', 'N° de suivi', 'État de l’expédition|Incomplète,Complète,Reliquat', 'Commentaires~', 'Documents joints@file'], 'Enregistrer', 'Expédition enregistrée (simulation)')
    modal('reliquat', ['Nouveau reliquat'], 'Nouveau reliquat', ['Référence commande*=', '#Lignes produit', 'Produit', 'Lot', 'Quantité@number', 'Motif~', 'Traité par|Préparateur,Dominique', 'Commentaires~'], 'Enregistrer', 'Reliquat enregistré (simulation)')
    modal('retourc', ['Nouveau retour'], 'Nouveau retour client', ['Commande=', 'Client*', 'Référence commande*', '#Lignes produit', 'Produit', 'Lot', 'Quantité@number', 'Motif~', 'Traité par|Préparateur,Dominique', 'Commentaires~'], 'Enregistrer et générer le bon', 'Retour enregistré (simulation)')
    E['expeditions.html'] = {'panels': {
        1: lst('Commande, client ou produit', ['Client', 'Commande', 'Date cmd', 'Produits', 'Traitement', 'Motif', 'Traité par', 'État', 'Commentaires', ('Action', 'r')], [
            [c(C[2]), '<a href="#">CMD-11655</a>', '10 nov.', 'Substitut osseux × 2', 'À expédier', 'Rupture fournisseur', 'Dominique', badge('En attente', 'warn'), '—', A('Expédier le reliquat', 'Modifier|Prévenir le client|!Supprimer')]]),
        2: lst('Retour, commande ou client', ['Client', 'Commande', 'Produits retournés', 'Réception stock', 'Motif', 'Traité par', 'Commentaires', ('Action', 'r')], [
            [c(C[5]), '<a href="#">CMD-11602</a>', 'Pointes papier F1 × 1', badge('Reçu', 'ok'), 'Produit endommagé', 'Dominique', '—', A('Imprimer le bon', 'Modifier|Créer un avoir|!Supprimer', '')]]),
        3: lst('Commande ou client', ['Commande', 'Client', 'Échéance', 'Retard', ('Action', 'r')], [['<a href="#">CMD-11678</a>', c(C[2]), '7 nov.', '<span class="late">12 jours</span>', A('Prévenir le client', 'Ouvrir la commande|Expédier')]])},
        'primary': {1: 'Nouveau reliquat', 2: 'Nouveau retour', 3: ''}}
    page('expeditions.html', 'expeditions', 'Expéditions', 'Gérez les expéditions, reliquats et retours', btn('Liste des commandes', href='ventes.html') + btn('Nouvelle expédition', 'primary', 'plus'),
         list_card(bar('Expédition, commande, client, suivi…', sel('État', ['tous les états', 'Complète', 'Incomplète', 'Reliquat']), ['Client', 'N° de suivi', 'Date de création@date', 'Date prévue de livraison@date']),
                   table(['Expédition', 'Commande', 'Client', 'Contact de livraison', 'Facturation', 'Méthode / préparateur', 'Suivi', 'État', 'Commentaires', ('Action', 'r')],
                         [[f'<a href="#">{e}</a>', o, f'<b>{cl}</b>', f'<small style="white-space:normal">{ct}</small>', fa, c(me, pr), f'<span class="num">{s}</span>', badge(st[0], st[1]), f'<small style="white-space:normal">{cm}</small>', A(a, ME)] for e, o, cl, ct, fa, me, pr, s, st, cm, a in erows], check=True, name='l’expédition'),
                   pager('1 à 50 sur 27 541 expéditions', 'Page 1 sur 551'))
         + bulkbar('Imprimer les étiquettes', ['Imprimer les bons d’expédition', 'Marquer complètes']), tabs([('Expéditions', '27 541'), ('Reliquats', '62'), ('Retours', '4'), ('Retards', '237')]))

    # ================= RAMASSAGE =================
    modal('ramassage', ['Nouveau ramassage'], 'Nouveau ramassage', ['Entité|Choisir une entité,Dental Groupe,Oofti,Safe Implant', 'Client*', 'Date*@date', 'Matin (jusqu’à 11 h 30)@time', 'Après-midi (à partir de 14 h 30)@time', 'Adresse=', 'Code postal', 'Ville', 'Zone|Sans zone,Paris Est,Lyon,Marseille', 'Remarques~'], 'Enregistrer', 'Ramassage enregistré (simulation)')
    modal('zones', ['Zones'], 'Zones de ramassage', ['Nouvelle zone='], 'Ajouter', 'Zone ajoutée (simulation)')
    rrows = [(C[1], 'Oofti', '19 nov.', '10 h 00', '—', '12 rue des Lilas', '75019', 'Paris', 'Paris Est', 'Sonner à l’interphone'), (C[0], 'Dental Groupe', '19 nov.', '—', '15 h 00', '8 cours Vitton', '69006', 'Lyon', 'Lyon', '—')]
    page('ramassage.html', 'ramassage', 'Ramassage', 'Récupération chez le client · matin jusqu’à 11 h 30, après-midi à partir de 14 h 30', btn('Zones', icon='pin') + btn('Imprimer', icon='print') + btn('Nouveau ramassage', 'primary', 'plus'),
         list_card(bar('Client, adresse, ville, code postal, remarque…', sel('Entité', ENT[:4]) + sel('Zone', ['toutes', 'Paris Est', 'Lyon', 'Marseille']) + sel('Créneau', ['Matin et après-midi', 'Matin', 'Après-midi']), ['Date de début@date', 'Date de fin@date'],
                       '<div class="filters"><div class="seg" role="group" aria-label="Période"><button aria-pressed="true">Aujourd’hui</button><button aria-pressed="false">Tout l’historique</button></div><span class="muted">2 ramassages</span></div>'),
                   table(['Client', 'Entité', 'Date', 'Matin', 'Après-midi', 'Adresse', 'Code postal', 'Ville', 'Zone', 'Remarques', ('Action', 'r')],
                         [[f'<b>{a}</b>', b, d, m, ap, ad, cp, v, badge(z, 'info', False), r, A('Ramassé', 'Modifier|Reporter|!Supprimer')] for a, b, d, m, ap, ad, cp, v, z, r in rrows], check=True, name='le ramassage'), pager('2 ramassages', 'Page 1 sur 1'))
         + bulkbar('Imprimer la tournée', ['Marquer ramassés', 'Exporter']))

    # ================= LOCATIONS =================
    modal('contrat', ['Nouveau contrat', 'Finaliser'], 'Nouveau contrat de location', ['Client*=', 'Intitulé du contrat*=', 'Date de début*@date', 'Date de fin@date', '#Produits loués', 'Désignation*', 'N° de série', 'Quantité@number', 'Mensuel / unité@number', 'Montant mensuel TTC (€)*@number',
                                                                         '#Prélèvement SEPA', 'Référence du mandat', 'IBAN', 'BIC', 'Jour de prélèvement@number', 'Prochaine facturation@date', 'Notes~'], 'Créer le contrat', 'Contrat créé (simulation)')
    lrows = [('LOC-2026-0002', 'Dr Sophie Marchand', 'Location scanner intra-oral', ('Actif', 'ok'), '31 juil. 2026', '150,00 €', badge('Mandat signé', 'ok'), '5 déc. 2026', 'Voir le contrat'), ('LOC-2026-0001', 'Cabinet Bellecour', 'Location capteur', ('Brouillon', ''), '21 juin 2026', '19,90 €', badge('Mandat manquant', 'warn'), '—', 'Finaliser')]
    page('locations.html', 'locations', 'Locations produits', 'Contrats, prélèvement SEPA mensuel et suivi du matériel loué', btn('Exporter', icon='down') + btn('Nouveau contrat', 'primary', 'plus'),
         kpis([('Contrats en cours', '1', '1 brouillon à finaliser'), ('Loyers mensuels', '150,00 €', 'Hors brouillons'), ('Prochain prélèvement', '5 déc.', '150,00 € · 1 contrat')])
         + list_card(head('Contrats en cours') + bar('Référence, client ou intitulé', sel('Statut', ['tous', 'Actif', 'Brouillon', 'Terminé'])), table(['Réf.', 'Client', 'Intitulé', 'Statut', 'Début', ('Mensuel', 'r'), 'SEPA', 'Prochain prélèvement', ('Action', 'r')],
                     [[f'<a href="#">{r}</a>', f'<b>{cl}</b>', i, badge(s[0], s[1]), d, f'<b>{m}</b>', se, n, A(a, 'Imprimer le contrat|Modifier|Voir les prélèvements|Résilier|!Supprimer', 'soft' if a == 'Finaliser' else '')] for r, cl, i, s, d, m, se, n, a in lrows]))
         + '<p class="small muted">La facturation mensuelle automatique par prélèvement SEPA est déclenchée par un job planifié, après validation du mandat bancaire.</p>')

    # ================= GED =================
    DC = ['Toutes les catégories', 'Convention professionnelle', 'Attestation de formation', 'Feuille d’émargement', 'Évaluation des connaissances', 'Évaluation de satisfaction', 'Procédure / mode opératoire', 'Contrat', 'Autre']
    modal('dossier', ['Nouveau dossier'], 'Nouveau dossier', ['Nom*=', 'Description~'], 'Enregistrer', 'Dossier créé (simulation)')
    modal('document', ['Ajouter un document'], 'Nouveau document', ['Catégorie|' + ','.join(DC[1:]), 'Titre*=', 'Description~', 'Fichier*@file='], 'Enregistrer', 'Document ajouté (simulation)')
    tree = ''.join(f'<a class="mail-item" href="#"{" aria-current=true" if i == 0 else ""} style="padding-left:{12 + lvl * 16}px">{ico("folder")} {n}</a>' for i, (n, lvl) in enumerate([('Racine', 0), ('Journée de formation 2026', 1), ('Formations 2026', 1), ('Documents formations', 2)]))
    folders_ = '<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px">' + ''.join(item(n, d, kebab(menu='Ouvrir|Renommer|Déplacer|!Supprimer'), icon='folder') for n, d in [('Journée de formation 2026', '4 documents'), ('Formations 2026', 'Documents formations')]) + '</div>'
    page('documents.html', 'docs', 'GED — Documents', 'Arborescence de dossiers, conventions, attestations et procédures', btn('Nouveau dossier', icon='folder') + btn('Ajouter un document', 'primary', 'upload'),
         f'<div class="cols"><div class="aside" style="flex:0 1 260px">{card(head("Dossiers", btn("Tout déplier", sm=True)) + f"<nav aria-label=Dossiers>{tree}</nav>")}</div><div class="grow stack">'
         + card(head('Racine') + folders_ + '<div class="empty" style="padding:24px;border:2px dashed var(--line-strong);border-radius:14px"><span class="tile">' + ico('upload') + '</span><h2>Glissez vos fichiers ici</h2><p>ou cliquez sur « Ajouter un document ».</p></div>')
         + list_card(head('Documents à la racine') + bar('Titre du document', sel('Catégorie', DC)),
                     table(['Document', 'Catégorie', 'Ajouté le', ('Taille', 'r'), ('Action', 'r')], [['<a href="#">Convention de formation — modèle.pdf</a>', 'Convention professionnelle', '12 nov. 2026', '184 Ko', A('Télécharger', 'Aperçu|Renommer|Déplacer|Changer de catégorie|!Supprimer', '')]], check=True, name='le document'))
         + '</div></div>' + bulkbar('Télécharger', ['Déplacer', 'Changer de catégorie', 'Supprimer']))

    # ================= RESSOURCES HUMAINES =================
    tile = lambda l, v, b='': item(l, v, btn(b, sm=True) if b else '', soft=True)
    modal('absence', ['Demander une absence', 'Envoyer la demande'], 'Demander une absence', ['Type|Congé payé,RTT,Maladie,Sans solde', 'Durée|Journée,Matin,Après-midi', 'Du*@date', 'Au*@date', 'Motif (facultatif)~'], 'Envoyer la demande', 'Demande envoyée (simulation)')
    E['rh.html']['panels'][1] = (form('Demander une absence', ['Type|Congé payé,RTT,Maladie,Sans solde', 'Durée|Journée,Matin,Après-midi', 'Du@date', 'Au@date', 'Motif (facultatif)~'], '<div class="actions">' + btn('Envoyer la demande', 'primary', 'send') + '</div>')
                                 + card(head('Mes absences') + '<div class="list">' + item('Congé payé · 23 au 27 déc. 2026', '5 jours', badge('En attente', 'warn') + kebab(menu='Modifier|!Annuler la demande'), soft=True) + item('RTT · 2 nov. 2026', '1 jour', badge('Validée', 'ok'), soft=True) + '</div>'))
    E['rh.html']['panels'][3] = card(head('Recrutement', btn('Nouvelle offre', 'soft', sm=True, icon='plus')) + empty('team', 'Aucune offre en cours', 'Publiez une offre pour recevoir et suivre les candidatures.'))
    page('rh.html', 'rh', 'Ressources humaines', 'Présence, absences et dossiers de l’équipe', btn('Recrutement', href='#onglet-3') + btn('Demander une absence', icon='plus') + btn('Démarrer ma journée', 'primary', 'play', attrs='data-action="clock"'),
         card(head('Pointage · 14 h 38', badge('Pas encore pointé', 'warn')) + '<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">'
              + tile('Temps de travail', '0 h 00') + tile('Attendu aujourd’hui', '7 h 00') + tile('Pauses', '0 h 00') + tile('Retard', '0 h 00')
              + tile('Déjeuner', '0 h 00', 'Démarrer') + tile('Café du matin', '0 sur 15 min', 'Démarrer') + tile('Café de l’après-midi', '0 sur 15 min', 'Démarrer') + tile('Brief / réunion', '0 h 00', 'Démarrer') + '</div>'
              + btn('Démarrer ma journée', 'ok', 'play', attrs='data-action="clock"') + '<p class="small muted">La pause déjeuner de votre horaire type est appliquée automatiquement si vous ne la déclarez pas.</p>')
         + card(head('Soldes') + '<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">' + tile('Congés payés', '25 jours · pris 0 · en attente 5') + tile('RTT', '0 jour · pris 1 · en attente 0') + '</div>'),
         tabs(['Ma journée', 'Mes absences', 'Mon historique', 'Recrutement']))

    # ================= PARAMÈTRES =================
    general = (form('Informations de l’établissement', ['Nom de l’établissement*', 'Adresse=', 'Ville', 'Code postal', 'Téléphone@tel', 'E-mail@email', 'Nom du gérant', 'Téléphone du gérant@tel', 'Forme juridique', 'SIREN (9 chiffres)', 'SIRET (14 chiffres)', 'N° de TVA intracommunautaire', 'Code APE', 'Ville du greffe (RCS)', 'Capital social (€)@number', 'N° URSSAF', 'Nom de la banque', 'IBAN', 'BIC', 'Abonnement|Annuel'])
               + card(head('Logo de l’établissement', btn('Choisir un logo', sm=True, icon='upload') + btn('Supprimer', 'danger', sm=True)) + '<img class="when-light" src="assets/logo-bleus.svg" alt="Logo actuel" width="196" height="57"><img class="when-dark" src="assets/logo-blanc-bleu.svg" alt="Logo actuel" width="196" height="57"><p class="muted">Format carré recommandé. Affiché sur vos devis, factures et documents.</p>')
               + form('Géolocalisation de l’établissement', ['Latitude', 'Longitude'], '<div class="empty" style="padding:28px;border:1px dashed var(--line-strong);border-radius:14px"><p>Carte : cliquez pour sélectionner l’emplacement exact de l’établissement.</p></div>', btn('Me localiser automatiquement', sm=True, icon='pin'))
               + card(head('Mode d’activité') + '<p class="muted">Différencie un laboratoire de prothèses, un fournisseur dentaire ou les deux.</p><div class="list">' + ''.join(
                   f'<label class="item soft"><input type="radio" name="mode"{" checked" if i == 2 else ""}><span class="item-main"><b>{t}</b><small>{d}</small></span></label>' for i, (t, d) in enumerate([
                       ('Travaux / prothèses uniquement', 'Catalogue et commandes centrés sur la fabrication, avec schéma dentaire.'), ('Produits en vente uniquement', 'Catalogue et commandes centrés sur la revente, sans schéma dentaire.'), ('Travaux et produits en vente', 'Accès complet : travaux et produits revendables.')])) + '</div>') + save)
    modal('utilisateur', ['Ajouter un utilisateur', 'Inviter un utilisateur'], 'Ajouter un utilisateur', ['Nom d’utilisateur*', 'Nom complet*', 'E-mail*@email', 'Rôle|Administrateur,Commercial,Préparateur,Comptabilité,Lecture seule', 'Horaires de connexion autorisés'], 'Ajouter', 'Utilisateur ajouté (simulation)')
    alertes = [('Alerte rupture de stock (service achats)', '9 249 produits en rupture seront listés dans l’e-mail', True, True), ('Alerte DLC courte (moins d’un an)', 'Liste mensuelle · 139 lots concernés', True, True), ('Commandes en attente d’expédition (entrée en stock)', 'À chaque entrée en stock d’un produit', False, False),
               ('Paiement en ligne échoué (service financier)', 'Alerte immédiate pour relancer le client', False, False), ('Expédition incomplète (service logistique)', 'Alerte interne à chaque expédition incomplète', False, False), ('Alerte de prix concurrentiel', 'Résumé après chaque veille · aucun destinataire', False, False)]
    emails = card(head('Destinataires des e-mails automatiques') + '<p class="muted">Configurez qui reçoit chaque type de notification.</p><div class="list">' + ''.join(
        item(n, d, '<label class="field" style="flex:1 1 200px"><span class="sr">Ajouter un destinataire</span><input type="email" placeholder="email@exemple.fr"></label>' + btn('Ajouter', sm=True) + btn('Retirer', sm=True) + (btn('Envoyer le rappel maintenant', 'soft', sm=True) if now else ''), soft=True) for n, d, on, now in alertes) + '</div>') + save
    entites = (form('Nouvelle entité', ['Libellé de la nouvelle entité', 'Nom court (liste des commandes)'], '<div class="actions">' + btn('Ajouter', 'soft', 'plus') + '</div>')
               + card(head('Entités commerciales') + '<p class="muted">Chaque commande peut être rattachée à une entité. Renseignez les informations légales de l’entreprise émettrice.</p><div class="list">' + ''.join(
                   item(n, 'Active', '<label class="small" style="display:flex;gap:8px;align-items:center"><input type="checkbox" checked> Active</label>' + btn('Informations légales', sm=True) + btn('Supprimer', 'danger', sm=True), soft=True) for n in ['Dental Groupe', 'Oofti', 'Safe Implant', 'Safe Coaching']) + '</div>'))
    taux = card(head('Taux de change', badge('Référence : EUR (€)', dot=False)) + '<div class="list">' + ''.join(
        item(f'{d}', f'1 {d[:3]} = … EUR', f'<label class="small" style="display:flex;gap:8px;align-items:center"><input type="checkbox"{" checked" if i == 0 else ""}> Activée</label><input class="input num" style="width:110px" type="number" step="0.01" value="{v}" aria-label="Taux {d}">', soft=True)
        for i, (d, v) in enumerate([('USD $', '0.92'), ('GBP £', '1.17'), ('CHF', '1.04'), ('MAD DH', '0.09'), ('ILS ₪', '0.25'), ('CNY ¥', '0.13'), ('JPY ¥', '0.006'), ('CAD CA$', '0.68')])) + '</div><div class="actions">' + btn('Enregistrer les taux', 'primary', 'check') + '</div>')
    exped = (card(head('Méthodes d’expédition', btn('Ajouter une méthode', sm=True, icon='plus')) + '<p class="muted">Chronopost, Ciblex, Coursier, TNT, UPS, Sur place — personnalisables. L’adresse de suivi utilise {TRACKING_ID}.</p><div class="list">' + ''.join(
        item(n, u, '<label class="small" style="display:flex;gap:8px;align-items:center"><input type="checkbox" checked> Active</label>' + btn('Modifier', sm=True), soft=True) for n, u in [('Chronopost', 'https://suivi.example/{TRACKING_ID}'), ('Ciblex', 'https://suivi.example/{TRACKING_ID}'), ('Coursier', 'Sans suivi')]) + '</div>')
             + card(head('Préparateurs de commande', btn('Ajouter un préparateur', sm=True, icon='plus')) + '<p class="muted">Noms proposés lors de la saisie des expéditions.</p><div class="list">' + item('Dominique', 'Préparateur', btn('Retirer', sm=True), soft=True) + '</div>') + save)
    cal = (toggles('Jours travaillés', [('Fermer le vendredi', '', False), ('Fermer le samedi (Shabbat)', '', True), ('Fermer le dimanche', '', True), ('Fêtes et jours fériés israéliens', '', False)], 'Les délais de livraison sont calculés uniquement sur les jours réellement travaillés.')
           + form('Jours de fermeture', ['Date@date', 'Libellé (facultatif)'], '<div class="actions">' + btn('Ajouter', 'soft', 'plus') + '</div>')
           + form('Majorations d’urgence', ['?Activer les majorations automatiques', 'Libellé', 'Heures max@number', 'Majoration %@number'], '<p class="small muted">Supplément calculé selon le délai ouvré demandé (exemple : 24 h → +50 %).</p><div class="actions">' + btn('Ajouter une règle', 'soft', 'plus') + '</div>') + save)
    sync = (card(head('Boutiques en ligne') + '<p class="muted">Poussez les produits vers une ou plusieurs boutiques. Sans sélection : toutes les boutiques actives. 500 liens produit · 20 liens commande.</p><div class="actions" style="margin-left:0">'
                 '<label class="small"><input type="checkbox" checked> Oofti</label><label class="small"><input type="checkbox" checked> Safe Implant</label>' + btn('Synchroniser les produits', 'soft', sm=True) + btn('Synchroniser les commandes', 'soft', sm=True) + '</div>')
            + form('Place de marché GACD', ['Adresse de l’API', 'Clé API vendeur@password'], '<p class="small muted">Seules les commandes acceptées sont importées. Dernière synchronisation : 19/11/2026 15 h 17.</p><div class="actions">' + btn('Importer les commandes GACD', 'soft', sm=True) + '</div>', badge('Configuré', 'ok'))
            + card(head('Autres connecteurs') + '<div class="list">' + item('Synchronisation complète', 'Clients, produits et commandes', btn('Synchronisation complète', sm=True), soft=True) + item('Formations', 'Connecteur Safe Coaching — à configurer', btn('Synchroniser les formations', sm=True), soft=True)
                   + item('Ancien logiciel de gestion', 'File d’attente dans les deux sens', btn('Planifier la synchronisation complète', sm=True), soft=True) + '</div>')
            + lst('Intégration ou message', ['Date', 'Intégration', 'Sens', 'Statut', 'Message'], [['19/11 15 h 17', 'GACD', 'Import', badge('Réussi', 'ok'), '3 commandes importées'], ['19/11 15 h 00', 'Boutique Oofti', 'Export', badge('Réussi', 'ok'), '12 produits mis à jour']]))
    modeles = ''.join(card(head(g) + '<div class="list">' + ''.join(item(n, o, badge('Par défaut', dot=False) + btn('Voir / modifier', sm=True), soft=True) for n, o in rows) + '</div>') for g, rows in [
        ('Commandes et paiements', [('Confirmation de commande', 'Objet : Confirmation de votre commande {{order_reference}}'), ('Commande en préparation (expédition)', 'Objet : Votre commande est en cours d’expédition'), ('Commande en préparation (coursier)', 'Objet : Votre commande est en cours de livraison'),
                                    ('Expédition incomplète', 'Objet : Expédition partielle de votre commande'), ('Remerciement de paiement', 'Objet : Merci pour votre règlement — Facture {{invoice_number}}')]),
        ('Relances de factures', [('Relance à la date d’échéance', 'Délai standard 30 jours · lien de paiement joint'), ('1re relance (+15 jours)', 'Objet : Factures impayées — 1re relance'), ('2e relance (+30 jours)', 'Objet : Factures impayées — 2e relance'), ('3e relance (+45 jours, service juridique)', 'Objet : Transfert au service juridique')]),
        ('E-mails génériques', [('Modèle libre', 'Variables disponibles : {{client_name}}, {{order_reference}}')])])
    admin = lambda t: card(empty('gear', 'Accès réservé aux administrateurs', f'{t} : demandez à un administrateur de vous donner l’accès.'))
    E['parametres.html'] = {'panels': {
        1: lst('Nom ou e-mail', ['Nom d’utilisateur', 'Nom complet', 'E-mail', 'Rôle', ('Actions', 'r')], [['<a href="#">florian</a>', 'Florian Bonnet', 'florian@votre-societe.example', 'Administrateur', A('Modifier', 'Horaires de connexion|Réinitialiser le mot de passe|Désactiver|!Supprimer', '')],
                                                                                                         ['<a href="#">preparation</a>', 'Préparation commandes', 'preparation@votre-societe.example', 'Préparateur', A('Modifier', 'Horaires de connexion|Réinitialiser le mot de passe|Désactiver|!Supprimer', '')]]),
        2: emails, 3: entites, 4: taux, 5: exped, 6: cal, 7: admin('Données et exports'), 8: sync,
        9: form('Lab Bridge (CFAO)', ['Identifiant du poste labo (ex. CFAO-01, FRAISAGE-02)'], '<p class="small muted">Même valeur que labStationId dans le fichier de configuration de l’agent Lab Bridge sur ce poste.</p><div class="actions">' + btn('Effacer', 'danger') + btn('Enregistrer', 'primary', 'check') + '</div>'),
        10: '<p class="muted">Personnalisez les e-mails transactionnels et les relances de facturation.</p>' + modeles, 11: admin('Sauvegardes')},
        'primary': {i: ('Ajouter un utilisateur' if i == 1 else '') for i in range(12)}}
    page('parametres.html', '', 'Paramètres', 'Configuration et gestion de votre établissement', btn('Enregistrer', 'primary', 'check'), general,
         tabs(['Général', 'Utilisateurs', 'E-mails automatiques', 'Entités commerciales', 'Taux de change', 'Expédition et livraison', 'Calendrier et urgences', 'Données et exports', 'Synchronisations', 'Lab Bridge (CFAO)', 'Modèles d’e-mails', 'Sauvegardes']))
