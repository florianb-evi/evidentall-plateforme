# Evidentall — maquette de la refonte UI/UX

Maquette codée et cliquable (HTML, CSS, JavaScript, sans framework) des 17 modules de la plateforme et de leurs onglets, plus le formulaire « Nouvelle commande », la fiche client et les paramètres. Elle sert de référence pour l'intégration : structure des pages, composants, couleurs et surtout **emplacement des boutons importants**.

Toutes les données affichées sont fictives.

## Voir la maquette

Ouvrez `index.html` dans un navigateur : aucune installation n'est nécessaire. Le dépôt peut aussi être publié tel quel avec GitHub Pages (branche `main`, dossier racine).

## Règles de placement des boutons

| Élément | Emplacement | Collé à l'écran ? |
| --- | --- | --- |
| Action principale de la page (une seule, bleu marine) | En haut à droite de l'en-tête de page | Oui : l'en-tête reste sous la barre supérieure et se compacte au défilement |
| Actions secondaires (Exporter, Importer, Imprimer) | À gauche de l'action principale, en contour | Oui, avec l'en-tête |
| Onglets de la page | Sous le titre, dans l'en-tête | Oui, avec l'en-tête |
| En-tête des tableaux | En haut du tableau | Oui : le tableau défile dans son cadre, l'en-tête reste visible |
| Colonne d'actions d'un tableau | Dernière colonne | Oui : collée à droite quand le tableau est plus large que l'écran |
| Prochaine action d'une ligne (Expédier, Relancer…) | Dernière colonne, une seule action visible, le reste dans le menu « … » | Non |
| Actions groupées | Barre flottante en bas de l'écran | Oui, mais seulement quand des lignes sont cochées |
| Valider un formulaire | Barre en bas de l'écran, avec le total et « Enregistrer le brouillon » | Oui |
| Récapitulatif d'un formulaire | Colonne de droite | Oui sur ordinateur |
| Répondre à un message | Bas du volet de lecture | Oui |
| Actions destructives (Supprimer, Arrêter) | Menu « … » ou bouton en contour rouge, jamais en action principale | Non |
| Recherche globale, pointage, aide, notifications | Barre supérieure | Oui |
| Menu latéral | À gauche, réductible | Oui, avec son propre défilement |

Sur mobile (moins de 900 px), le menu devient un tiroir et l'action principale de la page passe en bas de l'écran, sur toute la largeur.

## Pages

| Fichier | Module | Action principale |
| --- | --- | --- |
| `index.html` | Tableau de bord | Nouvelle commande |
| `statistiques.html` | Statistiques | Aucune (page de consultation) |
| `messagerie.html` | Cockpit | Nouveau message |
| `partenariats.html` | Partenariats | Inviter un partenaire |
| `ventes.html` | Ventes | Nouvelle commande |
| `commande-nouvelle.html` | Formulaire de commande | Valider la commande (barre du bas) |
| `clients.html` | Clients | Nouveau client |
| `prospection.html` | Prospection | Nouvelle interaction |
| `service-client.html` | Service client | Nouveau ticket |
| `produits.html` | Produits | Nouveau produit |
| `comparateur-prix.html` | Comparateur de prix | Relancer la veille |
| `catalogues-partenaires.html` | Catalogues partenaires | Peupler les catalogues |
| `24h-dentaire.html` | 24h Dentaire | Valider les créneaux en attente |
| `achats.html` | Achats | Nouvelle commande fournisseur |
| `expeditions.html` | Expéditions | Nouvelle expédition |
| `ramassage.html` | Ramassage | Nouveau ramassage |
| `locations.html` | Locations | Nouveau contrat |
| `documents.html` | GED — Documents | Ajouter un document |
| `rh.html` | Ressources humaines | Démarrer ma journée |

## Organisation du code

- `assets/app.css` : couleurs de la charte, composants et règles de collage (`position: sticky`). Les variables sont en tête du fichier.
- `assets/app.js` : en-tête compact au défilement, barre d'actions groupées, menu réductible, raccourci Ctrl K.
- `tools/pages.py`, `tools/pages2.py` : contenu des pages. `tools/extra.py` : fenêtres et onglets secondaires. `tools/couverture.py` : contrôle de l'inventaire.
- `tools/build.py` : génère les pages. Le menu, la barre supérieure et l'en-tête sont définis une seule fois ; modifiez ce fichier puis lancez `python3 tools/build.py`.

## Charte

- Logo : `assets/logo-bleus.svg` sur fond clair (utilisé dans le menu), `assets/logo-blanc-bleu.svg` sur fond bleu ou bleu marine. Ce sont vos fichiers d'origine, recadrés au plus près du dessin. `assets/logo-symbole.svg` est un recadrage sur « all » et le sourire, pour le menu réduit et l'icône d'onglet.
- Principale `#0077FD`, secondaire `#032444`, accompagnante `#50C3FF`, police Montserrat.
- Le bouton principal est en bleu marine `#032444` : le texte blanc sur `#0077FD` n'atteint pas le contraste recommandé pour du texte courant. Le bleu `#0077FD` sert aux graphiques, aux onglets actifs et aux accents.
- Mode nuit : bouton lune de la barre supérieure, choix mémorisé dans le navigateur. Toutes les couleurs sont des variables CSS redéfinies sous `[data-theme="dark"]` dans `assets/app.css` ; le logo passe à la version blanc-bleu.
- Vert, orange et rouge sont réservés aux statuts (payé, à valider, en retard) et toujours accompagnés d'un libellé.

## Ce qui est cliquable

Tout bouton, onglet ou lien de la maquette réagit. Rien n'est enregistré : les actions affichent un message « (simulation) ».

| Élément | Comportement |
| --- | --- |
| Onglets | Changent de contenu ; l'adresse garde l'onglet (`ventes.html#onglet-3`) et l'action principale de l'en-tête suit l'onglet (« Nouvelle facture », « Nouveau fournisseur »…) |
| Boutons de création | Ouvrent une fenêtre avec le formulaire, boutons « Annuler » et de validation collés en bas |
| Référence d'une ligne (CMD-…, FA-…) | Ouvre un panneau de détail à droite, actions collées en bas |
| Bouton « … » d'une ligne | Menu : Voir le détail, Modifier, Dupliquer, Imprimer, Supprimer (avec confirmation) |
| Pastilles de statut, recherche, filtres | Filtrent réellement les lignes du tableau |
| Cases à cocher | Font apparaître la barre d'actions groupées |
| Recherche globale ou Ctrl K | Ouvre un accès rapide aux pages |
| Aide, langue, notifications, compte, société | Menus déroulants |
| Démarrer ma journée | Bascule en « Terminer ma journée » sur toutes les pages |

Pages ajoutées : `parametres.html` (12 onglets) et `client-fiche.html` (fiche client, ouverte depuis la liste des clients).

Test automatique : `python3` + Playwright cliquent chaque élément visible de chaque page et de chaque onglet (1 214 clics) ; aucun n'est resté sans effet, hors éléments déjà actifs.

## Inventaire

Voir `AUDIT.md` : toutes les fonctions relevées sur la plateforme sont présentes dans la maquette, rangées au bon endroit plutôt que supprimées. Les noms d'origine des modules sont conservés (Cockpit, GED, Prospections et suivis…).

## Limites

- Les écrans non relevés sont listés à la fin de `AUDIT.md`.
- Les données sont fictives et les actions simulées.
