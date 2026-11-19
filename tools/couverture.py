#!/usr/bin/env python3
"""Vérifie que chaque fonction relevée sur la plateforme a sa place dans la maquette.

Usage : python3 tools/couverture.py   (après python3 tools/build.py)
Pour chaque page, la liste donne les libellés de la maquette qui portent une fonction de la plateforme.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INVENTAIRE = {
    'index.html': ['Guide d’utilisation', 'Personnaliser', 'Partenariats : cabinets', 'Partenariats : laboratoires', 'Produit>', 'Vente>', 'Achat>', 'Client>', 'Point de vente>', 'Aujourd’hui', 'Cette semaine', 'Ce mois', 'Personnalisé',
                   'CA du jour', 'CA HT de la période', 'Encaissements', 'Impayés (encours)', '0–30 j', '31–60 j', '61–90 j', '&gt; 90 j', 'Commandes et panier moyen', 'Répartition par canal', 'Alertes à traiter', 'Pointage', 'Démarrer ma journée', 'Ouvrir le module RH',
                   'Marge brute', 'Couverture des coûts', 'Encaissé / facturé TTC', 'Activité opérationnelle', 'En attente', 'En préparation', 'En retard', 'Expédiées', 'Délai médian', 'Commandes récentes', 'Voir tout', 'Top 5', 'Clients', 'Produits', 'Marques', 'Commerciaux',
                   'Évolution du chiffre d’affaires', 'CA HT 12 mois glissants', 'Voir l’analyse détaillée', 'Échéances à venir'],
    'ventes.html': ['Propositions commerciales', 'Commandes', 'Bons de livraison', 'Factures', 'Avoirs', 'Point de vente', 'Partenariats', 'Nouvelle commande', 'Exporter en Excel', 'Commandes rapides', 'Créer la commande avec ces lignes', 'Brouillon', 'Partiellement expédiée', 'Livrée', 'Annulée',
                    'Saisie du', 'Livraison du', 'Montant TTC min', 'Autre statut', 'Réinitialiser', 'Commercial / envoyée par', 'Entité / canal', 'Voir la facture', 'Historique des paiements', 'Imprimer l’étiquette', 'Imprimer le bon de livraison', 'Imprimer le bon de commande', 'Créer un avoir', 'Bon de prélèvement stock',
                    'En instance', 'Accepté', 'Commandé', 'Rejeté', 'Hors délai', 'Travaux / produits', 'Enregistrer un règlement', 'Imprimer la proposition', 'Résumé des impayés', 'Envoyer les impayés', 'Statistiques factures', 'PDF fusion factures', 'Envoyer la sélection par e-mail', 'Relances', 'Partiellement payée',
                    'Retour rapide', 'Facture d’origine', 'Code-barres', 'Grille', 'Produit sans code-barres', 'Nouveau client', 'Entité commerciale', 'Finaliser la vente', 'Ventes récentes'],
    'commande-nouvelle.html': ['Général', 'Détail de la commande', 'Notes', 'Entité commerciale', 'Patient', 'Type de livraison', 'Date d’échéance souhaitée', 'Date de livraison prévue', 'Niveau de priorité', 'Canal de vente', 'Générer et envoyer la facture', 'proposition commerciale', 'Précédent', 'Suivant', 'Enregistrer en brouillon', 'Valider la commande'],
    'clients.html': ['Exporter', 'Nouveau client', 'Tags', 'Dentiste', 'Ville', 'Téléphone', 'E-mail', 'Commercial', 'Dern. transaction / paiement', 'Statut', 'Encours', 'À jour', 'Léger', 'Modéré', 'Élevé', 'Critique', 'Encours min', 'CA min', 'Produit acheté', 'Commander', 'Modifier le client', 'Ouvrir le dossier',
                     'Identité', 'Coordonnées', 'Facturation et livraison', 'Finances et suivi', 'Informations légales', 'Options avancées', 'Limite de crédit', 'Délai de paiement', 'Remise client', 'Acompte', 'Niveau de prix', 'Nouveau tag'],
    'client-fiche.html': ['Envoyer un e-mail', 'Passer commande', 'Modifier la fiche', 'Packs proposés au client', 'Prix spécifiques', 'Copier les prix d’un autre client', 'Édition multiple'],
    'produits.html': ['Nouveau produit', 'Catalogue', 'Stock', 'Stocks', 'Historique', 'Inventaire', 'Référentiels', 'Catégories', 'Marques', 'Attributs', 'Entrepôts', 'Emplacements', 'Trier par entité', 'Sans entité', 'Stock faible', 'Rupture', 'Fournisseur', 'Lots', 'SKU',
                      'Produits composés', 'Vente additionnelle', 'Produits de substitution', 'Tarification revente', 'Marketplace et visibilité', 'Médias et statut', 'Coefficient de marge', 'Seuil d’alerte', 'Date de péremption'],
    'partenariats.html': ['Cabinets', 'Laboratoires', 'En attente', 'Acceptés', 'Refusés', 'Terminés'],
    'comparateur-prix.html': ['Relancer la veille', 'Ajouter un concurrent', 'Liens confirmés', 'À valider', 'Plus chers que le marché', 'Couverture traitée', 'Indice de prix', 'Alertes non lues', 'Prix à appliquer', 'Sources concurrentes', 'Dernières veilles', 'Comparateur', 'Matching', 'Recommandations', 'Surveillance', 'Règles', 'Import CSV',
                              'Valider', 'Refuser', 'Tout marquer comme lu', 'Mode d’écart', 'Marge minimale', 'Fréquence automatique', 'Arrondi psychologique', 'Appliquer automatiquement', 'Veille automatique', 'Catalogue prérempli', 'Modèle vide', 'Importer'],
    'catalogues-partenaires.html': ['Créer les comptes', 'Peupler les catalogues', 'Arrêter', 'Laboratoires revente', 'Laboratoire', 'Produits', 'File d’import', 'Connexion', 'Peupler'],
    '24h-dentaire.html': ['Jour précédent', 'Jour suivant', 'Aujourd’hui', 'Créneaux planifiés', 'À valider', 'Marge moyenne après remise', 'Valeur engagée', 'Frise des 24 heures', 'Répartition par catégorie', 'Derniers messages', 'Planning 24h', 'Vider le planning', 'Régénérer la proposition', 'Prix et seuil', 'Replanifier', 'Verrouiller',
                          'Valider l’offre', 'Refuser l’offre', 'Ajouter un produit', 'Publier sur la boutique', 'Fil de discussion', 'Analyses', 'Valeur du stock', 'stock dormant', 'Taux de seuil atteint', 'Flux API', 'Copier l’adresse', 'Réponse JSON brute'],
    'achats.html': ['Nouvelle commande fournisseur', 'Factures', 'Avoirs fournisseurs', 'Fournisseurs', 'Nouvelle facture', 'Nouvel avoir', 'Nouveau fournisseur', 'Contient', 'Ne contient pas', 'Supérieur à', 'Est vide', 'Imprimer la commande fournisseur', 'Incoterms', 'Livraison prévue', 'Date de création', 'Payé', 'Statut de qualification', 'Commande minimum'],
    'expeditions.html': ['Liste des commandes', 'Nouvelle expédition', 'Reliquats', 'Retours', 'Retards', 'Contact de livraison', 'Facturation', 'Méthode / préparateur', 'Suivi', 'Commentaires', 'Bon d’expédition', 'Étiquette 70 × 54', 'Documents joints', 'Complète', 'Incomplète', 'Nouveau reliquat', 'Nouveau retour', 'Réception stock', 'Traité par'],
    'ramassage.html': ['Nouveau ramassage', 'Zones', 'Imprimer', 'Aujourd’hui', 'Tout l’historique', 'Entité', 'Zone', 'Créneau', 'Date de début', 'Matin', 'Après-midi', 'Code postal', 'Remarques'],
    'prospection.html': ['Nouvelle interaction', 'Mes prospections', 'Mes suivis', 'Toutes les prospections', 'Tous les suivis', 'Rapports et performance', 'Prospects actifs', 'Relances à traiter', 'Taux de conversion', 'Titre de l’évènement', 'Description', 'Commercial assigné', 'Source du contact', 'Relance', 'Vue laboratoire', 'Mon activité', 'Objectifs commerciaux'],
    'service-client.html': ['Nouveau ticket', 'Tous les statuts', 'À faire', 'Assigné', 'En cours', 'En attente', 'Résolu', 'Clôturé', 'Annulé', 'Sévérité', 'Type de demande', 'Date d’intervention', 'N° de série du produit', 'Facture associée', 'Produit concerné', 'Pièce jointe'],
    'locations.html': ['Nouveau contrat', 'Intitulé', 'Mensuel', 'SEPA', 'Prochain prélèvement', 'Imprimer le contrat', 'N° de série', 'Référence du mandat', 'IBAN', 'Jour de prélèvement', 'Prochaine facturation'],
    'documents.html': ['Nouveau dossier', 'Ajouter un document', 'Racine', 'Tout déplier', 'Convention professionnelle', 'Attestation de formation', 'Feuille d’émargement', 'Évaluation des connaissances', 'Évaluation de satisfaction', 'Procédure / mode opératoire', 'Contrat'],
    'statistiques.html': ['Exporter', 'Aperçu', 'Anticipation IA', 'Commerciaux', 'Produits et marques', 'Clients et villes', 'Objectifs', 'Charges', 'Finances', 'Panier moyen HT par facture', 'Répartition par sous-catégorie', 'Lancer l’analyse', 'Top 10 produits', 'Performance par marque', 'Définir l’objectif global', 'Ajouter une charge', 'Répartition des charges', 'Performance opérationnelle'],
    'rh.html': ['Ma journée', 'Mes absences', 'Mon historique', 'Recrutement', 'Démarrer ma journée', 'Temps de travail', 'Attendu aujourd’hui', 'Pauses', 'Retard', 'Déjeuner', 'Café du matin', 'Café de l’après-midi', 'Brief / réunion', 'Soldes', 'Congés payés', 'RTT', 'Envoyer la demande'],
    'messagerie.html': ['Courrier', 'Outils', 'Elia', 'Réseaux', 'Nouveau message', 'Réception', 'Envoyés', 'Brouillons', 'Indésirables', 'Corbeille', 'Archives', 'Connecter une boîte', 'Actualiser', 'Rechercher un message', 'Parler', 'Discuter', 'Importer la liste', 'Ouvrir la facturation', 'Ajouter le compte', 'Garder en brouillon', 'Mettre en file'],
    'parametres.html': ['Général', 'Utilisateurs', 'E-mails automatiques', 'Entités commerciales', 'Taux de change', 'Expédition et livraison', 'Calendrier et urgences', 'Données et exports', 'Synchronisations', 'Lab Bridge (CFAO)', 'Modèles d’e-mails', 'Sauvegardes', 'Choisir un logo', 'Capital social', 'N° URSSAF', 'IBAN', 'Abonnement', 'Géolocalisation', 'Me localiser automatiquement',
                        'Mode d’activité', 'Ajouter un utilisateur', 'Horaires de connexion', 'Alerte rupture de stock', 'Alerte DLC courte', 'Envoyer le rappel maintenant', 'Informations légales', 'Enregistrer les taux', 'Ajouter une méthode', 'Ajouter un préparateur', 'Fermer le samedi', 'Jours de fermeture', 'majorations automatiques', 'Ajouter une règle',
                        'Synchroniser les produits', 'Importer les commandes GACD', 'Synchronisation complète', 'Identifiant du poste labo', 'Voir / modifier', 'Relance à la date d’échéance'],
}
GLOBAL = ['Rechercher dans Evidentall', 'Démarrer ma journée', 'Elia', 'Aide', 'Notifications', 'Paramètres', 'Réduire le menu']

manque = []
for page, labels in INVENTAIRE.items():
    html = (ROOT / page).read_text(encoding='utf-8')
    for lab in labels + GLOBAL:
        if lab not in html:
            manque.append(f'{page} : {lab}')
total = sum(len(v) + len(GLOBAL) for v in INVENTAIRE.values())
print(f'{total - len(manque)} fonctions présentes sur {total}')
if manque:
    print('Manquantes :\n- ' + '\n- '.join(manque))
    sys.exit(1)
