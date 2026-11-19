# Evidentall — maquette de la refonte UI/UX

Maquette codée (HTML, CSS, JavaScript, sans framework) des 17 modules de la plateforme, plus le formulaire « Nouvelle commande ». Elle sert de référence pour l'intégration : structure des pages, composants, couleurs et surtout **emplacement des boutons importants**.

Toutes les données affichées sont fictives.

## Voir la maquette

Ouvrez `index.html` dans un navigateur : aucune installation n'est nécessaire. Le dépôt peut aussi être publié tel quel avec GitHub Pages (branche `main`, dossier racine).

## Règles de placement des boutons

| Élément | Emplacement | Collé à l'écran ? |
| --- | --- | --- |
| Action principale de la page (une seule, bleu marine) | En haut à droite de l'en-tête de page | Oui : l'en-tête reste sous la barre supérieure et se compacte au défilement |
| Actions secondaires (Exporter, Importer, Imprimer) | À gauche de l'action principale, en contour | Oui, avec l'en-tête |
| Onglets de la page | Sous le titre, dans l'en-tête | Oui, avec l'en-tête |
| En-tête des tableaux | Juste sous l'en-tête de page | Oui sur ordinateur, non en dessous de 1100 px (défilement horizontal) |
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
| `messagerie.html` | Messagerie (ex-Cockpit) | Nouveau message |
| `ventes.html` | Ventes | Nouvelle commande |
| `commande-nouvelle.html` | Formulaire de commande | Valider la commande (barre du bas) |
| `clients.html` | Clients | Nouveau client |
| `prospection.html` | Prospection | Nouvelle interaction |
| `service-client.html` | Service client | Nouveau ticket |
| `produits.html` | Produits et stock | Nouveau produit |
| `comparateur-prix.html` | Comparateur de prix | Relancer la veille |
| `catalogues-partenaires.html` | Catalogues partenaires | Peupler les catalogues |
| `24h-dentaire.html` | 24h Dentaire | Valider les créneaux en attente |
| `achats.html` | Achats | Nouvelle commande fournisseur |
| `expeditions.html` | Expéditions | Nouvelle expédition |
| `ramassage.html` | Ramassage | Nouveau ramassage |
| `locations.html` | Locations | Nouveau contrat |
| `documents.html` | Documents (ex-GED) | Ajouter un document |
| `rh.html` | Ressources humaines | Démarrer ma journée |

## Organisation du code

- `assets/app.css` : couleurs de la charte, composants et règles de collage (`position: sticky`). Les variables sont en tête du fichier.
- `assets/app.js` : en-tête compact au défilement, barre d'actions groupées, menu réductible, raccourci Ctrl K.
- `tools/build.py` : génère les pages. Le menu, la barre supérieure et l'en-tête sont définis une seule fois ; modifiez ce fichier puis lancez `python3 tools/build.py`.

## Charte

- Logo : `assets/logo-bleus.svg` sur fond clair (utilisé dans le menu), `assets/logo-blanc-bleu.svg` sur fond bleu ou bleu marine. Ce sont vos fichiers d'origine, recadrés au plus près du dessin. `assets/logo-symbole.svg` est un recadrage sur « all » et le sourire, pour le menu réduit et l'icône d'onglet.
- Principale `#0077FD`, secondaire `#032444`, accompagnante `#50C3FF`, police Montserrat.
- Le bouton principal est en bleu marine `#032444` : le texte blanc sur `#0077FD` n'atteint pas le contraste recommandé pour du texte courant. Le bleu `#0077FD` sert aux graphiques, aux onglets actifs et aux accents.
- Vert, orange et rouge sont réservés aux statuts (payé, à valider, en retard) et toujours accompagnés d'un libellé.

## Limites

- Les onglets secondaires de chaque module (par exemple Factures, Avoirs, Stock et lots) ne sont pas maquettés : seul l'onglet principal l'est.
- Les menus déroulants, fenêtres modales et la page Paramètres ne sont pas maquettés.
- Les renommages (Cockpit → Messagerie, GED → Documents, Produits → Produits et stock) sont des propositions.
