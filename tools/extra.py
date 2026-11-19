"""Onglets secondaires, fenêtres de création et pages annexes de la maquette.

Appelé par build.py : register(globals()) reçoit les briques (btn, table, card…)
et remplit EXTRA (onglets par page) et MODALS (fenêtres). Données fictives.
"""


def register(h):
    globals().update(h)
    E, M = h['EXTRA'], h['MODALS']

    # ---------- Fenêtres de création ----------
    def field(spec):
        if spec.startswith('#'):
            return f'<h3 class="full sec">{spec[1:].strip()}</h3>'
        if spec.startswith('?'):
            return f'<label class="field full check"><input type="checkbox"> <span>{spec[1:].strip()}</span></label>'
        full = spec.endswith('~') or spec.endswith('=')
        area = spec.endswith('~')
        spec = spec.rstrip('~=')
        kind = 'text'
        if '@' in spec:
            spec, kind = spec.split('@')
        opts = None
        if '|' in spec:
            spec, o = spec.split('|')
            opts = o.split(',')
        req = spec.endswith('*')
        label = spec.rstrip('*')
        r = ' required' if req else ''
        if opts:
            ctl = f'<select{r}>' + ''.join(f'<option>{o}</option>' for o in opts) + '</select>'
        elif area:
            ctl = f'<textarea{r}></textarea>'
        else:
            ctl = f'<input type="{kind}"{r}>'
        star = ' <span class="late" aria-hidden="true">*</span>' if req else ''
        return f'<label class="field{" full" if full else ""}"><span>{label}{star}</span>{ctl}</label>'

    def modal(key, labels, title, fields, submit, done, intro=''):
        body = (f'<p class="muted full" style="grid-column:1/-1">{intro} <b data-context></b></p>' if intro else '') + ''.join(field(f) for f in fields)
        M[key] = (labels, f'<dialog class="modal" data-for="{"|".join(labels)}" data-done="{done}"><form method="dialog">'
                  f'<header><h2>{title}</h2><button class="btn btn-sm btn-ghost" value="cancel" formnovalidate aria-label="Fermer">Fermer</button></header>'
                  f'<div class="modal-body form-grid">{body}</div>'
                  f'<footer><button class="btn btn-ghost" value="cancel" formnovalidate>Annuler</button>'
                  f'<button class="btn btn-primary" value="ok">{submit}</button></footer></form></dialog>')

    modal('client', ['Nouveau client', 'Créer un client'], 'Nouveau client',
          ['Nom du cabinet ou du praticien*=', 'Type|Cabinet,Centre dentaire,Laboratoire,Autre', 'Commercial|Sans commercial,Florian Bonnet', 'Téléphone@tel', 'E-mail@email', 'Adresse=', 'Code postal', 'Ville', 'Tags='],
          'Créer le client', 'Client créé (simulation)')
    modal('tag', ['Nouveau tag'], 'Nouveau tag', ['Nom du tag*=', 'Couleur|Bleu,Vert,Orange,Rouge'], 'Créer le tag', 'Tag créé (simulation)')
    modal('produit', ['Nouveau produit'], 'Nouveau produit',
          ['Désignation*=', 'Référence*', 'Code-barres', 'Entité|Dental Groupe,Oofti,Safe Implant', 'Catégorie|Non catégorisé,Endodontie,Matériaux dentaires,Biomatériaux,Cabinet', 'Prix de vente HT*@number', 'Prix d’achat HT@number', 'TVA|20 %,5,5 %', 'Stock initial@number', 'Description~'],
          'Créer le produit', 'Produit créé (simulation)')
    modal('stock', ['Mouvement de stock', 'Réapprovisionner', 'Ajuster'], 'Mouvement de stock',
          ['Type|Entrée,Sortie,Inventaire', 'Quantité*@number', 'Lot', 'Date de péremption@date', 'Motif~'], 'Enregistrer le mouvement', 'Stock mis à jour (simulation)', 'Produit :')
    modal('ticket', ['Nouveau ticket'], 'Nouveau ticket',
          ['Client*=', 'Titre*=', 'Type|Technique,Livraison,Facturation,Autre', 'Sévérité|Faible,Moyenne,Critique', 'Assigné à|Non assigné,D. Yan,S. Peretti', 'Commande liée', 'Description~'],
          'Créer le ticket', 'Ticket créé (simulation)')
    modal('interaction', ['Nouvelle interaction', 'Ajouter une interaction', 'Planifier'], 'Nouvelle interaction',
          ['Prospect ou client*=', 'Type|Appel,Visite,E-mail,Salon', 'Date@date', 'Sujet*=', 'Source du contact|Recommandation,Site internet,Salon,Autre', 'Prochaine relance@date', 'Compte rendu~'],
          'Enregistrer', 'Interaction enregistrée (simulation)')
    modal('ramassage', ['Nouveau ramassage'], 'Nouveau ramassage',
          ['Client*=', 'Date*@date', 'Créneau|Matin (jusqu’à 11 h 30),Après-midi (à partir de 14 h 30)', 'Adresse=', 'Zone|Paris Est,Lyon,Marseille', 'Remarques~'],
          'Planifier le ramassage', 'Ramassage planifié (simulation)')
    modal('zones', ['Zones'], 'Zones de ramassage', ['Nom de la zone*', 'Codes postaux couverts', 'Jours de passage='], 'Ajouter la zone', 'Zone ajoutée (simulation)')
    modal('expedition', ['Nouvelle expédition'], 'Nouvelle expédition',
          ['Commande à expédier*=', 'Transporteur|Transporteur 24 h,Coursier,Retrait sur place', 'Préparateur|Préparation commandes,Florian Bonnet', 'Nombre de colis@number', 'Poids (kg)@number', 'Commentaire~'],
          'Créer l’expédition', 'Expédition créée (simulation)')
    modal('contrat', ['Nouveau contrat'], 'Nouveau contrat de location',
          ['Client*=', 'Matériel loué*=', 'Date de début*@date', 'Mensualité HT*@number', 'Durée|12 mois,24 mois,36 mois,Sans engagement', 'IBAN du mandat SEPA='],
          'Créer le contrat', 'Contrat créé en brouillon (simulation)')
    modal('po', ['Nouvelle commande fournisseur'], 'Nouvelle commande fournisseur',
          ['Fournisseur*=', 'Date de livraison souhaitée@date', 'Entité|Dental Groupe,Oofti,Safe Implant', 'Produits à commander~', 'Note au fournisseur~'], 'Créer le brouillon', 'Commande fournisseur créée (simulation)')
    modal('facture_f', ['Nouvelle facture'], 'Nouvelle facture fournisseur',
          ['Fournisseur*=', 'N° de facture*', 'Date de facture*@date', 'Échéance@date', 'Montant HT*@number', 'Fichier PDF@file='], 'Enregistrer la facture', 'Facture enregistrée (simulation)')
    modal('avoir', ['Nouvel avoir'], 'Nouvel avoir', ['Facture d’origine*=', 'Montant TTC*@number', 'Motif|Retour produit,Erreur de prix,Geste commercial', 'Commentaire~'], 'Créer l’avoir', 'Avoir créé (simulation)')
    modal('fournisseur', ['Nouveau fournisseur'], 'Nouveau fournisseur', ['Nom*=', 'Contact', 'Téléphone@tel', 'E-mail@email', 'Ville', 'Délai de paiement|30 jours,45 jours,60 jours,Comptant'], 'Créer le fournisseur', 'Fournisseur créé (simulation)')
    modal('document', ['Ajouter un document'], 'Ajouter un document', ['Fichier*@file=', 'Dossier|Tous les documents,Formations 2026,Conventions,Attestations,Procédures', 'Catégorie|Convention,Attestation,Procédure,Autre'], 'Ajouter', 'Document ajouté (simulation)')
    modal('dossier', ['Nouveau dossier'], 'Nouveau dossier', ['Nom du dossier*=', 'Dossier parent|Aucun,Formations 2026,Procédures'], 'Créer le dossier', 'Dossier créé (simulation)')
    modal('message', ['Nouveau message'], 'Nouveau message', ['À*@email=', 'Objet*=', 'Commande ou client lié', 'Modèle|Aucun,Confirmation d’expédition,Relance de paiement', 'Message~'], 'Envoyer', 'Message envoyé (simulation)')
    modal('boite', ['Connecter une boîte'], 'Connecter une boîte e-mail', ['Fournisseur|Gmail,Outlook,Autre (IMAP)', 'Adresse*@email', 'Nom affiché', 'Mot de passe d’application*@password'], 'Connecter la boîte', 'Boîte connectée (simulation)',
          'Gmail et Outlook demandent un mot de passe d’application, à créer dans la sécurité de votre compte.')
    modal('site', ['Ajouter un site'], 'Ajouter un site concurrent', ['Nom du site*', 'Adresse du site*@url', 'Adresse de recherche=', 'Actif|Oui,Non'], 'Ajouter le site', 'Site ajouté à la veille (simulation)')
    modal('absence', ['Demander une absence'], 'Demander une absence', ['Type|Congé payé,RTT,Maladie,Sans solde', 'Durée|Journée,Matin,Après-midi', 'Du*@date', 'Au*@date', 'Motif (facultatif)~'], 'Envoyer la demande', 'Demande envoyée (simulation)')
    modal('utilisateur', ['Inviter un utilisateur'], 'Inviter un utilisateur', ['Prénom et nom*=', 'E-mail*@email', 'Rôle|Administrateur,Commercial,Préparateur,Comptabilité,Lecture seule'], 'Envoyer l’invitation', 'Invitation envoyée (simulation)')
    modal('charge', ['Ajouter une charge'], 'Ajouter une charge', ['Libellé*=', 'Catégorie|Loyer,Salaires,Transport,Logiciels,Autre', 'Montant mensuel HT*@number', 'À partir de@date'], 'Ajouter la charge', 'Charge ajoutée (simulation)')
    modal('objectif', ['Définir l’objectif global', 'Définir'], 'Définir un objectif', ['Mois|Novembre 2026,Décembre 2026,Janvier 2027', 'Objectif de chiffre d’affaires HT*@number', 'Commercial|Toute l’équipe,Florian Bonnet'], 'Enregistrer l’objectif', 'Objectif enregistré (simulation)')
    modal('reglement', ['Enregistrer un règlement', 'Encaisser'], 'Enregistrer un règlement', ['Montant reçu*@number', 'Date*@date', 'Moyen|Virement,Carte bancaire,Chèque,Prélèvement,Espèces', 'Référence du paiement'], 'Enregistrer le règlement', 'Règlement enregistré (simulation)', 'Pour :')
    modal('relance', ['Relancer', 'Relancer les clients', 'Envoyer une relance', 'Relancer le client', 'Prévenir le client', 'Envoyer les impayés'], 'Envoyer une relance',
          ['Canal|E-mail,SMS,Courrier', 'Modèle|Relance amicale,Relance ferme,Mise en demeure', 'Message~'], 'Envoyer la relance', 'Relance envoyée (simulation)', 'Destinataire :')
    modal('import', ['Importer', 'Importer des prospects', 'Importer un fichier'], 'Importer un fichier', ['Fichier CSV ou Excel*@file=', 'Séparateur|Point-virgule,Virgule,Tabulation', 'En cas de doublon|Mettre à jour,Ignorer'], 'Lancer l’import', 'Import lancé (simulation)')
    modal('export', ['Exporter'], 'Exporter', ['Format|Excel (.xlsx),CSV,PDF', 'Contenu|Lignes affichées,Toutes les lignes', 'Période|Ce mois,Mois dernier,Cette année'], 'Télécharger', 'Export prêt (simulation)')
    modal('creneau', ['Changer de produit', 'Compléter le créneau de 23 h', 'Choisir un produit'], 'Choisir le produit du créneau', ['Produit*=', 'Prix promo HT*@number', 'Seuil d’achat (acheteurs)@number'], 'Enregistrer le créneau', 'Créneau mis à jour (simulation)')
    modal('expedier', ['Expédier', 'Marquer expédiée', 'Expédier le reliquat'], 'Expédier la commande', ['Transporteur|Transporteur 24 h,Coursier', 'N° de suivi', 'Prévenir le client par e-mail|Oui,Non'], 'Confirmer l’expédition', 'Commande expédiée (simulation)', 'Commande :')
    modal('reception', ['Réceptionner'], 'Réceptionner la commande', ['Réception|Complète,Partielle', 'Date de réception@date', 'Écarts constatés~'], 'Valider la réception', 'Réception enregistrée, stock mis à jour (simulation)', 'Commande :')

    h.update(modal=modal, field=field)
    # ---------- Petites briques ----------
    def lst(search, cols, rows, sel=(), check=False, foot=None, chip=None):
        bar = (chips(chip) if chip else '') + filters(search, sel, more=False)
        return list_card(bar, table(cols, rows, check=check), pager(foot or f'{len(rows)} lignes', 'Page 1 sur 1'))

    def ref(t, small=''):
        return f'<a href="#">{t}</a>' + (f'<small>{small}</small>' if small else '')

    def meters(title, rows, action=''):
        return card(head(title, action) + '<div class="list" style="gap:14px">' + ''.join(
            f'<div><div class="total-line"><span>{n}</span><b class="num">{v}</b></div>{meter(p)}</div>' for n, v, p in rows) + '</div>')

    h.update(lst=lst, ref=ref, meters=meters)
    C = ['Dr Camille Renaud', 'Cabinet dentaire des Lilas', 'Centre dentaire Voltaire', 'Laboratoire Prothésia', 'SCM Dentaire du Parc', 'SELARL Morel et Associés']

    # ---------- Ventes ----------
    devis = lst('N° de devis, client ou produit', ['Devis', 'Client', 'Contenu', 'Date', 'Statut', ('Montant TTC', 'r'), ('Action', 'r')], [
        [ref('DEV-0412'), c(C[0]), 'Scanner intra-oral + formation', '18 nov.', badge('Envoyé', 'info'), '<b>4 560,00 €</b>', acts('Convertir en commande')],
        [ref('DEV-0411'), c(C[3]), 'Substitut osseux × 12', '15 nov.', badge('Accepté', 'ok'), '<b>7 080,00 €</b>', acts('Convertir en commande')],
        [ref('DEV-0410'), c(C[2]), 'Kit de chirurgie × 3', '9 nov.', badge('Brouillon'), '<b>702,00 €</b>', acts('Reprendre')],
        [ref('DEV-0409'), c(C[4]), 'Résine composite × 20', '2 nov.', badge('Expiré', 'warn'), '<b>480,00 €</b>', acts('Relancer')]],
        ['Période : ce mois'], chip=[('Tous', 38, ''), ('Brouillons', 6, ''), ('Envoyés', 19, ''), ('Acceptés', 9, ''), ('Expirés', 4, '')])
    bl = lst('N° de bon, commande ou client', ['Bon de livraison', 'Client', 'Date', 'Statut', ('Montant TTC', 'r'), ('Action', 'r')], [
        [ref('BL-2611-0397', 'CMD-11680'), c(C[1]), '19 nov.', badge('Expédié', 'ok'), '<b>610,60 €</b>', acts('Imprimer', '')],
        [ref('BL-2611-0396', 'CMD-11676'), c(C[3]), '18 nov.', badge('Livré', 'ok'), '<b>2 250,00 €</b>', acts('Imprimer', '')],
        [ref('BL-2611-0395', 'CMD-11674'), c(C[4]), '18 nov.', badge('Expédié', 'ok'), '<b>942,10 €</b>', acts('Imprimer', '')]], ['Période : ce mois'], check=True)
    fact = ('<div class="banner">' + ico('alert') + '<p><b>517 factures échues pour 81 200 €.</b> Envoyez un récapitulatif à chaque client concerné.</p>'
            + btn('Résumé des impayés', sm=True) + btn('Envoyer les impayés', 'primary', sm=True) + '</div>'
            + lst('N° de facture, client ou commande', ['Facture', 'Client', 'Date', 'Paiement', 'Relances', ('Montant TTC', 'r'), ('Action', 'r')], [
                [ref('FA-2611-0932', 'CMD-11681'), c(C[1]), '19 nov.', PAY['ok'], '—', '<b>127,58 €</b>', acts('Imprimer', '')],
                [ref('FA-2611-0921', 'CMD-11674'), c(C[4]), '18 nov.', PAY['no'], '—', '<b>942,10 €</b>', acts('Enregistrer un règlement')],
                [ref('FA-2610-0871', 'CMD-11678'), c(C[2]), '28 oct.', PAY['part'], '2 relances', '<b>1 840,00 €</b>', acts('Enregistrer un règlement')],
                [ref('FA-2610-0418', 'CMD-11391'), c(C[3]), '15 oct.', PAY['no'], '<span class="late">3 relances</span>', '<b>2 100,00 €</b>', acts('Relancer')]],
                ['Période : ce mois', 'Paiement : tous'], check=True, chip=[('Toutes', 426, ''), ('Payées', 331, ''), ('Impayées', 78, ''), ('Paiement partiel', 17, ''), ('Échues', 517, 'alert')])
            + bulkbar('Envoyer par e-mail', ['Fusionner en PDF', 'Relancer', 'Exporter']))
    avoirs = lst('N° d’avoir, facture ou client', ['Avoir', 'Client', 'Facture d’origine', 'Date', ('Total TTC', 'r'), ('Action', 'r')], [
        [ref('AV-2611-0012'), c(C[5]), 'FA-2611-0902', '17 nov.', '<b>−86,40 €</b>', acts('Imprimer', '')],
        [ref('AV-2611-0011'), c(C[0]), 'FA-2610-0844', '6 nov.', '<b>−24,00 €</b>', acts('Imprimer', '')]], ['Période : ce mois'])
    pos = ('<div class="cols"><div class="grow stack">'
           + card(head('Scanner ou chercher un produit') + filters('Code-barres, référence ou nom du produit', more=False)
                  + empty('cart', 'Le panier est vide', 'Scannez un code-barres ou cherchez un produit pour commencer la vente.'))
           + '</div><div class="aside sticky-aside">' + card(head('Vente en cours') + filters('Client (facultatif)', more=False)
           + '<div class="total-line"><span>Articles</span><b class="num">0</b></div><div class="total-line big"><span>Total TTC</span><span class="num">0,00 €</span></div>'
           + btn('Finaliser la vente', 'primary', 'check') + btn('Historique des ventes (20)', 'ghost')) + '</div></div>')
    E['ventes.html'] = {'panels': {0: devis, 2: bl, 3: fact, 4: avoirs, 5: pos},
                        'primary': {0: 'Nouveau devis', 2: '', 3: '', 4: 'Nouvel avoir', 5: ''}}

    # ---------- Clients ----------
    E['clients.html'] = {'panels': {1: lst('Nom du tag', ['Tag', ('Clients', 'r'), ('Action', 'r')], [
        [badge('Implantologie', 'info', False), '412', acts('Voir les clients', '')], [badge('Grand compte', 'ok', False), '38', acts('Voir les clients', '')]])},
        'primary': {1: 'Nouveau tag'}}

    # ---------- Produits ----------
    stockp = lst('Produit, référence ou numéro de lot', ['Référence', 'Produit', 'Lot', 'Péremption', ('Quantité', 'r'), 'Emplacement', ('Action', 'r')], [
        ['<code>VIOS</code>', ref('Ciment canalaire, seringue de 10 g'), 'V55A00', '31 mai 2027', '<b>1</b>', 'A-12', acts('Ajuster')],
        ['<code>BRMOB-LARIC</code>', ref('Boîtes de rangement pour prothèse'), 'A0-0527', '<span class="late">Périme dans 20 j</span>', '<b>2</b>', 'C-03', acts('Ajuster')],
        ['<code>ETIQ-EDA</code>', ref('Étiquettes compatibles autoclave'), '00-1231', '12 déc. 2028', '<b>18</b>', 'B-07', acts('Ajuster')]],
        ['Entité : toutes'], chip=[('Tous les lots', 214, ''), ('Stock bas', 36, ''), ('Périme bientôt', 9, 'alert')])
    refs = '<div class="grid">' + ''.join(card(head(t, btn('Gérer', sm=True)) + f'<span class="kpi-value num">{n}</span><p class="muted">{d}</p>') for t, n, d in [
        ('Catégories', '42', '418 produits non catégorisés'), ('Marques', '67', '3 marques sans produit'), ('Fournisseurs', '53', 'Liés aux commandes d’achat'), ('Entités', '3', 'Dental Groupe, Oofti, Safe Implant')]) + '</div>'
    E['produits.html'] = {'panels': {1: stockp, 2: refs}, 'primary': {1: 'Mouvement de stock', 2: ''}}

    # ---------- Comparateur de prix ----------
    comp = lst('Référence ou nom du produit', ['Produit', ('Votre prix HT', 'r'), ('Moins cher du marché', 'r'), ('Écart', 'r'), 'Position', ('Action', 'r')], [
        [ref('Résine composite A3,5', 'RC-A35'), '37,10 €', '35,90 €', '<span class="late">+3,3 %</span>', badge('Plus cher', 'danger'), acts('Aligner le prix')],
        [ref('Pointes de gutta-percha 4 %', 'GP-04'), '5,75 €', '6,10 €', '<span class="up">−5,7 %</span>', badge('Moins cher', 'ok'), acts(None)],
        [ref('Gants nitrile, boîte de 100', 'GN-100'), '6,90 €', '6,90 €', '0 %', badge('Aligné'), acts(None)]])
    match = card(head('8 272 correspondances à valider', btn('Tout valider au-dessus de 95 %', sm=True)) + '<div class="list">' + ''.join(
        item(n, f'Proposé : {p} · ressemblance {s} %', btn('Voir', sm=True) + btn('Refuser', 'danger', sm=True) + btn('Valider', 'ok', sm=True), soft=True)
        for n, p, s in [('Résine composite A3,5', 'Composite nano A3.5 — Dentaprix', 97), ('Gants nitrile, boîte de 100', 'Gants nitrile bleus x100 — Mégastock Dentaire', 91), ('Ciment canalaire 10 g', 'Ciment endo seringue — Dentaprix', 78)]) + '</div>')
    reco = lst('Produit', ['Produit', ('Prix actuel', 'r'), ('Prix conseillé', 'r'), 'Raison', ('Action', 'r')], [
        [ref('Résine composite A3,5'), '37,10 €', '<b>35,50 €</b>', '1 % sous le moins cher', acts('Appliquer')],
        [ref('Kit de chirurgie'), '234,00 €', '<b>229,00 €</b>', '1 % sous le moins cher', acts('Appliquer')]])
    alertes = card(head('Alertes', btn('Tout marquer comme lu', sm=True)) + '<div class="list">' + ''.join(item(t, d, badge('Nouveau', 'info', False), tone, 'alert', soft=True) for t, d, tone in [
        ('Vous êtes plus cher que le marché', 'Résine composite A3,5 · +3,3 %', 'danger'), ('Mégastock Dentaire a baissé son prix', 'Gants nitrile · −4 %', 'warn'), ('Lecture impossible sur Promo Cabinet', 'Accès refusé depuis 3 jours', 'warn')]) + '</div>')
    surv = card(head('Ajouter un produit à la veille') + filters('Nom, référence ou code-barres', more=False)
                + '<div class="list">' + item('Résine composite A3,5', 'Suivi sur 3 sites', btn('Retirer', sm=True), soft=True) + item('Gants nitrile, boîte de 100', 'Suivi sur 2 sites', btn('Retirer', sm=True), soft=True) + '</div>')
    regles = (card(head('Règle de prix automatique') + '<div class="form-grid">' + field('Stratégie|Pourcentage sous le moins cher,S’aligner sur le moins cher,Ne rien changer')
                   + field('Écart visé (%)@number') + field('Marge minimale à respecter (%)@number') + field('Appliquer|Après validation manuelle,Automatiquement') + '</div>')
              + '<div class="savebar"><span class="muted">Aucune modification en attente</span>' + btn('Annuler', 'ghost') + btn('Enregistrer la règle', 'primary', 'check') + '</div>')
    E['comparateur-prix.html'] = {'panels': {1: comp, 2: match, 3: reco, 4: alertes, 5: surv, 6: regles},
                                  'primary': {3: 'Appliquer toutes les recommandations', 6: ''}}

    # ---------- 24h Dentaire ----------
    plan = card(head('Planning du jeudi 19 novembre', btn('Vider le planning', 'danger', sm=True) + btn('Régénérer la proposition', sm=True)) + '<div class="list">' + ''.join(
        item(f'{hh} h · {p}', f'{prix} € HT · remise {r} %', badge(s, t) + btn('Changer de produit', sm=True), soft=True) for hh, p, prix, r, s, t in [
            (14, 'Résine composite A3,5', '28,20', 24, 'En ligne', 'info'), (15, 'Pointes de gutta-percha 4 %', '4,50', 22, 'À valider', 'warn'),
            (16, 'Gel de mordançage', '9,90', 18, 'À valider', 'warn'), (17, 'Plaques thermoformables', '21,00', 25, 'À valider', 'warn')]) + '</div>')
    prod24 = lst('Produit éligible', ['Produit', 'Catégorie', ('Stock', 'r'), ('Prix normal HT', 'r'), ('Marge', 'r'), ('Action', 'r')], [
        [ref('Résine composite A3,5'), 'Matériaux dentaires', '18', '37,10 €', '71 %', acts('Planifier')], [ref('Gel de mordançage'), 'Matériaux dentaires', '42', '12,10 €', '64 %', acts('Planifier')]])
    fil = card(head('Fil de discussion du jour') + '<div class="chat"><div class="bubble"><b>Préparation commandes</b><br>Stock vérifié pour les créneaux de l’après-midi.</div>'
               '<div class="bubble me"><b>Vous</b><br>Merci, je valide les 7 créneaux restants.</div>'
               f'<div class="reply"><input aria-label="Votre message" placeholder="Écrire à l’équipe…">{btn("Envoyer", "primary", "send", sm=True)}</div></div>')
    ana = (kpis([('Promos ce mois', '412', '24 par jour'), ('Seuils atteints', '61 %', 'Sur 7 jours'), ('Chiffre d’affaires 24h', '18 400 €', '14 % du total')])
           + lst('Produit', ['Date', 'Heure', 'Produit', ('Remise', 'r'), ('Acheteurs', 'r'), 'Statut'], [
               ['18 nov.', '10 h', ref('Gants nitrile'), '20 %', '14 sur 10', badge('Seuil atteint', 'ok')], ['18 nov.', '11 h', ref('Ciment canalaire'), '15 %', '3 sur 10', badge('Seuil manqué', 'warn')]]))
    api = card(head('Adresse du flux à publier', btn('Copier l’adresse', sm=True)) + '<p><code>https://votre-domaine.example/api/24h/2026-11-19.json</code></p>'
               '<p class="muted">Votre boutique en ligne lit ce flux chaque heure pour afficher la promotion en cours.</p>')
    E['24h-dentaire.html'] = {'panels': {1: prod24, 2: plan, 3: fil, 4: ana, 5: api}}

    # ---------- Achats ----------
    E['achats.html'] = {'panels': {
        1: lst('N° de facture ou fournisseur', ['Facture', 'Fournisseur', 'Date', 'Échéance', ('Montant HT', 'r'), ('Payé', 'r'), 'Statut', ('Action', 'r')], [
            [ref('F-88231'), c('Biomat Santé'), '26 oct.', '<span class="late">Échue depuis 3 j</span>', '<b>14 868,64 €</b>', '0,00 €', badge('À payer', 'danger'), acts('Enregistrer un règlement')],
            [ref('F-10492'), c('Medidental Europe'), '8 oct.', '8 déc.', '<b>3 080,39 €</b>', '3 080,39 €', badge('Payée', 'ok'), acts(None)]]),
        2: card(empty('bag', 'Aucun avoir fournisseur', 'Les avoirs reçus de vos fournisseurs apparaîtront ici.', btn('Nouvel avoir', 'soft', 'plus'))),
        3: lst('Nom, contact ou ville', ['Fournisseur', 'Contact', 'Téléphone', 'Ville', 'Délai de paiement', 'Statut', ('Action', 'r')], [
            [ref('Biomat Santé'), 'Service commandes', '01 00 00 00 10', 'Paris', '30 jours', badge('Actif', 'ok'), acts('Commander', '')],
            [ref('Dentaprime Fournitures'), 'Accueil', '04 00 00 00 11', 'Lyon', '45 jours', badge('Actif', 'ok'), acts('Commander', '')]])},
        'primary': {1: 'Nouvelle facture', 2: 'Nouvel avoir', 3: 'Nouveau fournisseur'}}

    # ---------- Expéditions ----------
    E['expeditions.html'] = {'panels': {
        1: lst('Commande, client ou produit', ['Commande', 'Client', 'Produit manquant', ('Reste à livrer', 'r'), 'En attente depuis', ('Action', 'r')], [
            [ref('CMD-11655'), c(C[2]), 'Substitut osseux, boîte de 6', '2', '<span class="late">9 jours</span>', acts('Expédier le reliquat')],
            [ref('CMD-11661'), c(C[0]), 'Pointes papier F1', '1', '5 jours', acts('Expédier le reliquat')]]),
        2: lst('Retour, commande ou client', ['Retour', 'Commande', 'Client', 'Motif', 'État', ('Action', 'r')], [
            [ref('RET-0004'), 'CMD-11602', c(C[5]), 'Produit endommagé', badge('À traiter', 'warn'), acts('Traiter')],
            [ref('RET-0003'), 'CMD-11570', c(C[1]), 'Erreur de référence', badge('Remboursé', 'ok'), acts(None)]]),
        3: lst('Commande ou client', ['Commande', 'Client', 'Échéance', 'Retard', ('Action', 'r')], [
            [ref('CMD-11678'), c(C[2]), '7 nov.', '<span class="late">12 jours</span>', acts('Prévenir le client')],
            [ref('CMD-11640'), c(C[4]), '12 nov.', '<span class="late">7 jours</span>', acts('Prévenir le client')]])},
        'primary': {1: '', 2: '', 3: ''}}

    # ---------- Prospection ----------
    prosp = lst('Nom du prospect ou ville', ['Prospect', 'Ville', 'Statut', 'Dernier contact', 'Prochaine relance', ('Action', 'r')], [
        [ref('Clinique dentaire du Port'), 'Marseille', badge('En discussion', 'info'), '19 nov.', '<span class="late">En retard de 2 j</span>', acts('Ajouter une interaction')],
        [ref('Dr Inès Colin'), 'Lyon', badge('Démonstration faite', 'ok'), '18 nov.', 'Aujourd’hui', acts('Ajouter une interaction')],
        [ref('Dr Marc Olivier'), 'Lille', badge('Premier contact'), '12 nov.', '2 déc.', acts('Ajouter une interaction')]])
    rapports = (kpis([('Interactions ce mois', '14', '4 visites, 7 appels, 3 e-mails'), ('Prospects convertis', '2', 'Sur 12 actifs'), ('Objectif du mois', '60 %', '9 interactions sur 15')])
                + meters('Activité par commercial', [('Florian Bonnet', '11 interactions', 80), ('Sans commercial', '3 interactions', 20)], btn('Objectifs commerciaux', sm=True)))
    E['prospection.html'] = {'panels': {1: prosp, 2: prosp, 3: rapports}}

    # ---------- Statistiques ----------
    E['statistiques.html'] = {'panels': {
        1: card(head('Anticiper les besoins de vos clients') + '<label class="field">Votre question<textarea placeholder="Exemple : quels clients n’ont pas recommandé de gants depuis 6 mois ?"></textarea></label>'
                + '<div class="actions" style="margin-left:0">' + btn('Lancer l’analyse', 'primary', 'play') + btn('Clients inactifs depuis 6 mois', sm=True) + btn('Produits à réassort', sm=True) + '</div>'),
        2: lst('Commercial', ['Commercial', ('Commandes', 'r'), ('Chiffre d’affaires HT', 'r'), ('Panier moyen', 'r'), ('Objectif', 'r')], [
            [c('Sans commercial'), '426', '<b>128 400 €</b>', '301 €', '—'], [c('Florian Bonnet'), '24', '<b>9 870 €</b>', '411 €', '66 %']]),
        3: '<div class="grid">' + meters('Top produits', [('Substitut osseux — boîte de 6', '66 400 €', 100), ('Scanner intra-oral', '3 800 €', 14), ('Kit de chirurgie', '2 340 €', 10)])
           + meters('Par marque', [('Dental Coop', '104 300 €', 100), ('Safe Implant', '23 500 €', 23), ('Sans marque', '5 300 €', 5)]) + '</div>',
        4: '<div class="grid">' + meters('Top clients', [(C[3], '13 100 €', 100), (C[2], '6 300 €', 48), (C[5], '4 300 €', 33)])
           + meters('Par ville', [('Paris', '31 200 €', 100), ('Lyon', '18 700 €', 60), ('Marseille', '12 400 €', 40)]) + '</div>',
        5: card(head('Objectifs de chiffre d’affaires', btn('Définir l’objectif global', 'soft', sm=True)) + '<div class="list">'
                + item('Novembre 2026', '128 400 € réalisés sur 180 000 €', '<div style="flex:1 1 160px">' + meter(71) + '</div>' + btn('Définir', sm=True), soft=True)
                + item('Décembre 2026', 'Aucun objectif défini', btn('Définir', sm=True), soft=True) + '</div>'),
        6: card(empty('chart', 'Aucune charge renseignée', 'Ajoutez vos charges fixes pour calculer la rentabilité.', btn('Ajouter une charge', 'soft', 'plus'))),
        7: kpis([('Marge brute', 'Non calculée', '<a href="produits.html">Renseigner les prix d’achat</a>'), ('Charges du mois', '0 €', '<a href="#onglet-6">Ajouter les charges</a>'), ('Encaissé sur facturé', '78 %', '112 900 € sur 147 900 €')])
           + meters('Performance opérationnelle', [('Commandes expédiées sous 24 h', '82 %', 82), ('Commandes livrées sans retard', '64 %', 64)])}}

    # ---------- Messagerie ----------
    E['messagerie.html'] = {'panels': {
        1: card(head('Vos outils', btn('Ajouter un outil', sm=True, icon='plus')) + '<div class="list">' + item('Espace transporteur', 'Suivi des colis', btn('Ouvrir', sm=True), icon='truck', soft=True)
                + item('Banque', 'Relevés et virements', btn('Ouvrir', sm=True), icon='pos', soft=True) + '</div>'),
        2: card(head('Assistant Elia') + '<div class="chat"><div class="bubble"><b>Elia</b><br>Bonjour Florian, que voulez-vous faire ?</div>'
                '<div class="actions" style="margin-left:0">' + btn('Retrouver mes dernières factures', sm=True) + btn('Résumer les messages reçus', sm=True) + btn('Préparer une publication', sm=True) + '</div>'
                f'<div class="reply"><input aria-label="Votre demande" placeholder="Dites à Elia ce que vous voulez faire…">{btn("Envoyer", "primary", "send", sm=True)}</div></div>'),
        3: card(head('Nouvelle publication', btn('Ajouter un compte', sm=True, icon='plus')) + '<div class="form-grid">' + field('Réseau|Instagram,Facebook,LinkedIn') + field('Date de publication@date') + field('Texte de la publication~') + '</div>'
                + '<div class="actions">' + btn('Garder en brouillon') + btn('Mettre en file d’attente', 'primary', 'send') + '</div>')},
        'primary': {1: '', 2: '', 3: ''}}

    # ---------- Ressources humaines ----------
    E['rh.html'] = {'panels': {
        1: card(head('Mes absences', btn('Demander une absence', 'soft', sm=True)) + '<div class="list">' + item('Congé payé · 23 au 27 déc. 2026', '5 jours', badge('En attente', 'warn'), soft=True)
                + item('RTT · 2 nov. 2026', '1 jour', badge('Validée', 'ok'), soft=True) + '</div>'),
        2: lst('Date', ['Date', 'Statut', ('Travail', 'r'), ('Attendu', 'r'), ('Pauses', 'r'), ('Retard', 'r')], [
            ['Mer. 18 nov.', badge('Complet', 'ok'), '7 h 05', '7 h 00', '1 h 10', '—'], ['Mar. 17 nov.', badge('Complet', 'ok'), '7 h 00', '7 h 00', '1 h 00', '—'],
            ['Lun. 16 nov.', badge('Incomplet', 'warn'), '6 h 20', '7 h 00', '1 h 15', '<span class="late">0 h 12</span>']]),
        3: card(empty('team', 'Aucune offre en cours', 'Publiez une offre pour recevoir et suivre les candidatures.', btn('Nouvelle offre', 'soft', 'plus')))}}

    # ---------- Fiche client ----------
    hist = table(['Commande', 'Date', 'Statut', 'Paiement', ('Montant TTC', 'r')], [
        [ref('CMD-11682'), '19 nov. 2026', ST['prep'], PAY['no'], '<b>105,00 €</b>'], [ref('CMD-11590'), '2 nov. 2026', ST['liv'], PAY['ok'], '<b>412,30 €</b>'], [ref('CMD-11477'), '14 oct. 2026', ST['liv'], PAY['ok'], '<b>86,00 €</b>']])
    infos = (head('Coordonnées', btn('Modifier', sm=True)) + '<div class="list">' + item('Dr Camille Renaud', 'Cabinet · CL-00412', icon='users', soft=True)
             + item('8 cours Vitton, 69006 Lyon', 'Adresse de livraison et de facturation', icon='pin', soft=True) + item('04 00 00 00 01', 'contact@cabinet-renaud.example', icon='mail', soft=True) + '</div>')
    hist_card = card('<div class="card-bar">' + head('Dernières commandes', btn('Tout voir', sm=True, href='ventes.html')) + '</div>' + hist, pad=False)
    fiche = (kpis([('Chiffre d’affaires 12 mois', '4 870 €', '18 commandes'), ('Encours', '105,00 €', '1 facture impayée, à jour'), ('Dernière commande', '19 nov.', 'En préparation'), ('Panier moyen', '271 €', 'TTC')])
             + '<div class="cols"><div class="grow">' + hist_card + '</div><div class="aside">' + card(infos) + '</div></div>')
    E['client-fiche.html'] = {'panels': {
        1: lst('N° de commande', ['Commande', 'Date', 'Statut', 'Paiement', ('Montant TTC', 'r')], [[ref('CMD-11682'), '19 nov. 2026', ST['prep'], PAY['no'], '<b>105,00 €</b>'], [ref('CMD-11590'), '2 nov. 2026', ST['liv'], PAY['ok'], '<b>412,30 €</b>']]),
        2: lst('N° de facture', ['Facture', 'Date', 'Paiement', ('Montant TTC', 'r'), ('Action', 'r')], [[ref('Facture provisoire'), '19 nov. 2026', PAY['no'], '<b>105,00 €</b>', acts('Enregistrer un règlement')]]),
        3: card(head('Échanges', btn('Nouvelle interaction', 'soft', sm=True)) + '<div class="list">' + item('Appel · 12 nov. 2026', 'Question sur le scanner intra-oral', soft=True, icon='headset') + '</div>'),
        4: card(empty('folder', 'Aucun document', 'Devis signés, mandats et attestations de ce client.', btn('Ajouter un document', 'soft', 'upload')))}}
    page('client-fiche.html', 'clients', 'Dr Camille Renaud', 'Cabinet · Lyon 6e · client depuis mars 2024 · ' + 'encours à jour',
         btn('Envoyer un message', icon='mail', href='messagerie.html') + btn('Modifier') + btn('Nouvelle commande', 'primary', 'plus', 'commande-nouvelle.html'),
         fiche, tabs(['Résumé', ('Commandes', '18'), ('Factures', '18'), 'Échanges', 'Documents']), back=('Clients', 'clients.html'))

    # ---------- Paramètres ----------
    def form(title, specs, extra_html=''):
        return card(head(title) + '<div class="form-grid">' + ''.join(field(s) for s in specs) + '</div>' + extra_html)

    save = '<div class="savebar"><span class="muted">Aucune modification en attente</span>' + btn('Annuler', 'ghost') + btn('Enregistrer', 'primary', 'check') + '</div>'
    general = (form('Informations de l’établissement', ['Nom de l’établissement*', 'Forme juridique', 'Adresse=', 'Code postal', 'Ville', 'Téléphone@tel', 'E-mail@email', 'Nom du gérant', 'SIREN', 'SIRET', 'N° de TVA intracommunautaire', 'Code APE'])
               + card(head('Logo', btn('Choisir un logo', sm=True, icon='upload')) + '<img class="when-light" src="assets/logo-bleus.svg" alt="Logo actuel" width="196" height="57"><img class="when-dark" src="assets/logo-blanc-bleu.svg" alt="Logo actuel" width="196" height="57"><p class="muted">Affiché sur vos devis, factures et bons de livraison.</p>') + save)
    users = lst('Nom ou e-mail', ['Utilisateur', 'Rôle', 'Dernière connexion', 'Statut', ('Action', 'r')], [
        [ref('Florian Bonnet', 'florian@votre-societe.example'), 'Administrateur', 'Aujourd’hui', badge('Actif', 'ok'), acts('Modifier', '')],
        [ref('Préparation commandes', 'preparation@votre-societe.example'), 'Préparateur', 'Hier', badge('Actif', 'ok'), acts('Modifier', '')],
        [ref('Nouvel arrivant', 'invite@votre-societe.example'), 'Commercial', '—', badge('Invitation envoyée', 'warn'), acts('Renvoyer l’invitation')]])
    toggles = lambda title, rows: card(head(title) + '<div class="list">' + ''.join(
        item(n, d, f'<label class="small" style="display:flex;align-items:center;gap:8px"><input type="checkbox"{" checked" if on else ""}> Activé</label>', soft=True) for n, d, on in rows) + '</div>') + save
    E['parametres.html'] = {'panels': {
        1: users,
        2: toggles('E-mails envoyés automatiquement', [('Confirmation de commande', 'À la validation de la commande', True), ('Avis d’expédition', 'Avec le numéro de suivi', True), ('Relance de facture échue', '7 jours après l’échéance', False)]),
        3: lst('Entité', ['Entité', 'Boutique en ligne', 'Préfixe de facture', 'Statut', ('Action', 'r')], [[ref('Dental Groupe'), '—', 'FA', badge('Active', 'ok'), acts('Modifier', '')], [ref('Oofti'), 'oofti.example', 'FT', badge('Active', 'ok'), acts('Modifier', '')], [ref('Safe Implant'), 'safe-implant.example', 'SI', badge('Active', 'ok'), acts('Modifier', '')]]),
        4: form('Taux de change', ['Devise de référence|Euro (EUR)', 'Dollar américain (USD)@number', 'Shekel (ILS)@number', 'Mise à jour|Automatique chaque jour,Manuelle']) + save,
        5: form('Expédition et livraison', ['Transporteur par défaut|Transporteur 24 h,Coursier', 'Franco de port à partir de (€ HT)@number', 'Frais de port standard (€ HT)@number', 'Délai de préparation|Le jour même,24 h,48 h']) + save,
        6: form('Calendrier et urgences', ['Jours ouvrés|Lundi au vendredi,Lundi au samedi', 'Heure limite de commande', 'Supplément urgence (%)@number', 'Jours fériés=']) + save,
        7: card(head('Données et exports') + '<div class="list">' + item('Exporter toutes les données', 'Clients, produits, commandes et factures au format Excel', btn('Exporter', sm=True), icon='down', soft=True)
                + item('Importer des données', 'Depuis un fichier CSV ou Excel', btn('Importer', sm=True), icon='upload', soft=True) + '</div>'),
        8: card(head('Synchronisations') + '<div class="list">' + item('Boutique en ligne', 'Dernière synchronisation il y a 4 minutes', badge('Connectée', 'ok') + btn('Synchroniser', sm=True), soft=True)
                + item('Place de marché', 'Dernière synchronisation il y a 1 heure', badge('Connectée', 'ok') + btn('Synchroniser', sm=True), soft=True)
                + item('Logiciel comptable', 'Non configuré', badge('À connecter', 'warn') + btn('Connecter', 'soft', sm=True), soft=True) + '</div>'),
        9: card(empty('box', 'Passerelle CFAO non configurée', 'Reliez votre logiciel de conception pour recevoir les travaux directement.', btn('Configurer la passerelle', 'soft'))),
        10: lst('Nom du modèle', ['Modèle', 'Objet', 'Modifié le', ('Action', 'r')], [[ref('Confirmation d’expédition'), 'Votre commande est en route', '3 nov. 2026', acts('Modifier', '')], [ref('Relance de paiement'), 'Facture en attente de règlement', '21 oct. 2026', acts('Modifier', '')]]),
        11: card(head('Sauvegardes', btn('Sauvegarder maintenant', 'soft', sm=True)) + '<div class="list">' + item('Aujourd’hui à 3 h 00', 'Sauvegarde automatique complète', badge('Réussie', 'ok') + btn('Télécharger', sm=True), soft=True)
                 + item('Hier à 3 h 00', 'Sauvegarde automatique complète', badge('Réussie', 'ok') + btn('Télécharger', sm=True), soft=True) + '</div>')},
        'primary': {1: 'Inviter un utilisateur'}}
    for i in (0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11):
        E['parametres.html']['primary'][i] = ''
    page('parametres.html', '', 'Paramètres', 'Configuration de votre établissement et de la plateforme', btn('Enregistrer', 'primary', 'check'), general,
         tabs(['Général', 'Utilisateurs', 'E-mails automatiques', 'Entités', 'Taux de change', 'Expédition', 'Calendrier', 'Données', 'Synchronisations', 'Passerelle CFAO', 'Modèles d’e-mails', 'Sauvegardes']))
