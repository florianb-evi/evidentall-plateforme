# Inventaire de la plateforme et correspondance avec la maquette

Relevé fait en lecture seule sur la plateforme le 19 novembre 2026 : chaque page, chaque onglet, les filtres (y compris « Plus de filtres »), les colonnes, les menus de ligne et les formulaires de création. Pendant l'ouverture des formulaires, toute écriture vers le serveur était bloquée : rien n'a été créé ni modifié.

**Règle de la maquette : aucune fonction n'est supprimée.** Ce qui change, c'est l'endroit où elle se trouve.

| Sur la plateforme | Dans la maquette |
| --- | --- |
| Action principale placée différemment selon les pages | Toujours en haut à droite de l'en-tête, qui reste visible |
| Plusieurs boutons de même poids (ex. 6 sur Factures) | Les plus utilisés en évidence, les autres dans « Plus d'actions » ou la barre d'actions groupées |
| 6 à 11 champs de filtre alignés | Recherche et 2 ou 3 filtres clés visibles ; tous les autres dans « Plus de filtres » ; « Réinitialiser » toujours présent |
| Filtre « Contient / Égal à… » dans chaque en-tête de colonne (Achats) | Les mêmes conditions dans « Plus de filtres » : colonne, condition, valeur |
| 9 à 11 colonnes | Toutes conservées, regroupées deux par deux quand elles vont ensemble ; bouton « Colonnes » pour afficher ou masquer |
| 3 à 6 icônes d'action par ligne | Une « prochaine action » visible, toutes les autres dans le menu « … », colonne collée à droite |
| Statut modifiable par liste déroulante dans la ligne | Conservé : le badge de statut est cliquable |
| Formulaires longs en accordéon | Mêmes rubriques et mêmes champs, validation collée en bas |
| Tuiles de création du tableau de bord | Menu « Créer » de l'en-tête |
| Partenariats (bandeau du tableau de bord, bouton de Ventes) | Entrée du menu latéral et page dédiée |
| Guide, visites guidées, 6 langues, Elia flottant, mode compact | Barre supérieure : Aide, langue, Elia, menu du compte |

La liste complète, page par page, est dans `tools/couverture.py` (604 libellés). `python3 tools/couverture.py` vérifie que chacun est présent dans la page correspondante. Ce contrôle porte sur la présence du libellé, pas sur le détail du comportement.

## Ce qui n'a pas pu être relevé

- Paramètres : « Données et exports » et « Sauvegardes » affichent « Accès réservé aux administrateurs » avec le compte utilisé.
- Fiche client : seules les rubriques visibles à l'ouverture ont été relevées (packs, prix spécifiques, actions de l'en-tête).
- Fiche détaillée d'une commande, d'un produit ou d'un ticket : non ouvertes.
- Sous-pages Stock (Stocks, Historique, Inventaire) et Référentiels (Catégories, Marques, Attributs, Entrepôts, Emplacements) : noms relevés, contenu non ouvert.
- Statistiques, Cockpit, Ressources humaines, Prospections : relevé des onglets, titres et boutons, sans les menus déroulants.
- `/billing` ouvert sans paramètre affiche « Impossible d'afficher la page ».
