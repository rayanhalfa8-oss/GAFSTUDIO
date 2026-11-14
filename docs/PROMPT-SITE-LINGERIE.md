# Prompt : site e-commerce de lingerie GAF STUDIO

> À copier tel quel dans un outil de création de site (Claude, Lovable, Bolt, v0, Cursor…).
> Les éléments entre `[crochets]` sont à remplacer par vos vraies informations. N'inventez rien à leur place.

---

## PROMPT

Crée un site e-commerce complet, moderne, premium et minimaliste pour **GAF STUDIO Lingerie**, une marque marocaine de lingerie pour femme. Le site s'inspire de l'organisation et du niveau de service des grands sites de lingerie européens : rayons clairs, guide des tailles précis, filtres par taille de bonnet, ensembles coordonnés et service client rassurant. Il doit avoir sa propre identité : **ne copie aucun texte, logo, photo, nom de produit ni slogan d'une autre marque** (Etam ou autre).

### 1. Identité de la marque

- **Nom :** GAF STUDIO, signature « Lingerie · Nuit · Lounge ».
- **Positionnement :** lingerie élégante, confortable et accessible, pensée pour toutes les morphologies, vendue partout au Maroc.
- **Ton :** chaleureux, rassurant, féminin sans être vulgaire. On vouvoie la cliente. Phrases courtes et claires.
- **Langues :** français par défaut, avec un sélecteur vers l'arabe (affichage de droite à gauche) et la darija pour les messages WhatsApp.
- **Devise :** dirham marocain (DH), prix TTC.
- **Palette :**
  - encre `#1F1A17` (textes, boutons principaux) ;
  - fond ivoire `#FBF8F4` ;
  - blush `#F8F2EB` (sections claires) ;
  - nude champagne `#E9D6C7` ;
  - bronze `#86613F` (prix promo, accents) ;
  - or doux `#B8955A` (ornements uniquement, jamais pour du texte) ;
  - gris `#6B625B` (textes secondaires).
- **Typographies :** Cormorant Garamond (titres, logo, noms de produits) et Jost (textes, boutons, formulaires), via Google Fonts avec `font-display: swap`.
- **Style :** beaucoup d'espace, grandes photos, coins peu arrondis (2 à 4 px), ombres légères teintées de brun, icônes SVG au trait fin (jamais d'émojis comme icônes).
- **Photos :** mannequins de différentes morphologies et tailles de bonnet. Rendu sensuel mais élégant et non explicite, adapté au public marocain. Fond neutre et lumière douce. Une photo portée et une photo « à plat » ou studio pour chaque produit.

### 2. Arborescence et navigation

Menu principal (méga-menu sur ordinateur, menu latéral sur mobile) :

- **Nouveautés**
- **Soutiens-gorge :** emboîtant, balconnet, corbeille, triangle, push-up, sans armatures, minimiseur, grandes tailles de bonnet, allaitement, sport.
- **Culottes :** slip, shorty, tanga, string, culotte haute, gainante, packs de 3.
- **Ensembles coordonnés :** soutien-gorge et bas assortis, achetés séparément pour que chaque cliente choisisse ses deux tailles.
- **Bodys et nuisettes**
- **Nuit et lounge :** pyjamas, chemises de nuit, peignoirs (reprend la collection actuelle de pyjamas GAF STUDIO).
- **Mariée et trousseau :** ensembles et coffrets pour le trousseau.
- **Coffrets cadeaux**
- **Promotions**

En haut de chaque page : barre de recherche avec suggestions instantanées, compte (optionnel), favoris et panier avec compteur.

Un bandeau fin au-dessus de l'en-tête affiche une seule promesse à la fois, en rotation : « Livraison offerte dès 2 articles ou 500 DH », « Paiement à la livraison ou en ligne », « Emballage discret ».

### 3. Page d'accueil

1. **Hero** plein écran : photo ou vidéo de campagne (muette, en boucle), un titre court, un bouton « Découvrir la collection ».
2. **Bandeau de réassurance :** paiement à la livraison ou en ligne · livraison partout au Maroc en 24 à 72 h · emballage discret · conseil taille sur WhatsApp.
3. **Univers :** 4 grandes cases (Soutiens-gorge, Culottes, Ensembles, Nuit et lounge).
4. **Nouveautés :** carrousel de produits.
5. **« Trouvez votre taille » :** bloc qui mène à l'outil de calcul de taille (section 6).
6. **Best-sellers :** grille de 4 à 8 produits (`[à définir avec vos vraies ventes]`).
7. **Le look du moment :** une photo d'ensemble avec des points cliquables sur chaque pièce, qui ouvrent la fiche ou l'ajout au panier.
8. **La marque :** court texte sur GAF STUDIO et ses engagements.
9. **Avis clientes :** uniquement de vrais avis, avec l'accord des clientes. Section masquée s'il n'y en a pas. **N'invente aucun avis.**
10. **FAQ courte et inscription aux nouveautés par WhatsApp.**

### 4. Page catégorie (liste de produits)

- Titre, courte introduction et nombre d'articles.
- **Filtres** dans une barre collante sur ordinateur et dans un panneau qui glisse depuis le bas sur mobile, avec le nombre de résultats mis à jour en direct :
  - **taille de bonnet** (A à G) et **tour de dos** (70 à 110), uniquement pour les soutiens-gorge ;
  - **taille** (XS à 3XL) pour les culottes, bodys et nuit ;
  - forme ou modèle, maintien (avec ou sans armatures, rembourré, non rembourré), matière (dentelle, microfibre, coton, satin, tulle), couleur (pastilles), prix ;
  - « Disponible dans ma taille » : ne montre que les articles en stock dans la taille choisie.
- **Tri :** nouveautés, prix croissant, prix décroissant, meilleures ventes.
- **Carte produit :** photo portée qui devient la photo à plat au survol ; pastilles de couleur ; nom ; prix (et prix barré si promo) ; badge « Nouveau », « -20 % » ou « Plus que 2 » ; bouton favori ; bouton rapide « Choisir ma taille ».
- Chargement progressif (« Voir plus de produits ») et squelettes gris pendant le chargement, jamais de page blanche.

### 5. Page produit

- **Galerie** haute définition : photo portée, photo de dos, détail de la matière, photo à plat ; zoom au survol (ordinateur) et au pincement (mobile) ; vidéo courte si disponible ; vue 360° si les photos existent.
- Nom, prix, prix barré et économie en dirhams si promotion.
- **Choix de la couleur** (pastilles + nom affiché).
- **Choix de la taille :**
  - soutien-gorge : sélection en deux temps, **tour de dos** puis **bonnet** (ex. 85 puis C), avec les combinaisons épuisées grisées ;
  - autres articles : tailles XS à 3XL ;
  - lien « Guide des tailles » et lien « Trouver ma taille ».
- **Disponibilité :** « En stock », « Plus que N », ou « Épuisé dans cette taille » avec un bouton « Prévenez-moi sur WhatsApp ».
- Bouton **« Ajouter au panier »** très visible, collé en bas de l'écran sur mobile.
- Bouton **« Une question sur ce modèle ? WhatsApp »** qui ouvre WhatsApp avec le nom du produit, la couleur et la taille déjà écrits.
- **Complétez l'ensemble :** les pièces assorties (culotte, string, porte-jarretelles) avec leur propre choix de taille et un ajout en un clic.
- Onglets ou accordéons :
  - description (accroche, points forts, conseils de port) ;
  - **composition et entretien** : matières en % et consignes de lavage (`[selon l'étiquette]`) ;
  - **forme et maintien** : niveau de maintien, type d'armature, bretelles amovibles ou non, type d'agrafes ;
  - livraison et paiement ;
  - échanges et retours, avec la mention d'hygiène : « Pour des raisons d'hygiène, les culottes, strings et bodys ne sont ni repris ni échangés s'ils ont été portés ou si l'emballage hygiénique a été retiré » (`[à adapter à votre politique]`).
- Avis sur ce produit (s'il y en a), avec la taille commandée et le ressenti (« taille petit », « taille normalement », « taille grand »).
- « Vous aimerez aussi » et « Déjà vus ».
- Lien direct partageable pour chaque produit (pour Instagram et WhatsApp).

### 6. Guide et calcul des tailles

- **Page guide des tailles** avec des tableaux clairs :
  - **soutiens-gorge :** tour de dessous de poitrine (cm) → tour de dos (70, 75, 80… 110) ; écart entre tour de poitrine et tour de dessous de poitrine → bonnet (A à G) ;
  - **culottes et bas :** tour de taille et tour de hanches (cm) → taille XS à 3XL ;
  - schéma SVG simple qui montre où mesurer ;
  - équivalences des tailles françaises et européennes.
- **Outil « Trouver ma taille »** : la cliente saisit deux mesures (dessous de poitrine et poitrine), et l'outil calcule sa taille (ex. 85C) avec une phrase d'explication et un bouton « Voir les modèles dans ma taille ». La taille est mémorisée pour pré-remplir les filtres.
- Conseils : « Entre deux bonnets ? », « Comment savoir si un soutien-gorge vous va bien ».
- Bouton « Besoin d'aide ? Une conseillère vous répond sur WhatsApp ».

### 7. Panier

- Panier latéral qui s'ouvre après chaque ajout, et une page panier complète.
- Pour chaque article : photo, nom, couleur, **taille modifiable** (menu déroulant), quantité (+ / −), prix, « Retirer ».
- Barre de progression : « Plus qu'un article pour la livraison offerte ».
- Suggestions pour compléter l'ensemble.
- Champ code promo (`[si vous en proposez]`).
- Récapitulatif : sous-total, livraison (offerte ou montant), total.
- Deux boutons de commande côte à côte, de même taille :
  - **« Commander sur WhatsApp »** (vert WhatsApp) ;
  - **« Payer en ligne »** (couleur encre).
- Panier vide : message, rappel de la livraison offerte et bouton « Découvrir la collection ».

### 8. Commande : deux parcours au choix

Le formulaire de livraison est commun aux deux parcours, sur une seule page, avec le moins de champs possible :

- nom et prénom ;
- téléphone (format marocain 06 / 07 / 05, vérifié) ;
- ville (liste des villes du Maroc + « Autre ville ») ;
- adresse complète ;
- e-mail : facultatif pour WhatsApp, obligatoire pour le paiement en ligne (pour le reçu) ;
- remarque (facultative) ;
- case « C'est un cadeau » (emballage cadeau offert, prix masqué sur le bon de livraison) ;
- les informations sont mémorisées pour la prochaine commande.

Les erreurs s'affichent sous chaque champ, en français clair, avec la façon de corriger.

**A. Commander sur WhatsApp (paiement à la livraison)**

1. La cliente remplit le formulaire et clique « Envoyer ma commande sur WhatsApp ».
2. WhatsApp s'ouvre vers le **+212 6 98 87 49 40** (lien `https://wa.me/212698874940?text=…`) avec un message déjà rédigé : référence de commande, articles (nom, couleur, taille, quantité, prix), sous-total, livraison, total, nom, téléphone, ville, adresse, cadeau oui/non, remarque, et « Paiement à la livraison ».
3. Un écran de confirmation dit « Appuyez sur Envoyer dans WhatsApp pour valider votre commande », avec un bouton « Réessayer » si WhatsApp ne s'est pas ouvert.
4. La commande est aussi enregistrée côté boutique avec le statut « En attente de confirmation WhatsApp ».

**B. Payer en ligne**

1. Étape 2 sur la même page : récapitulatif + choix de la livraison.
2. Paiement par carte bancaire (CB marocaines, Visa, Mastercard) via une passerelle marocaine : **`[CMI, Payzone ou YouCan Pay, selon votre contrat]`**. Paiement 3-D Secure, page de paiement hébergée par la passerelle, aucun numéro de carte stocké sur le site.
3. Pendant le paiement, le bouton passe en « Paiement en cours… » et ne peut pas être cliqué deux fois.
4. En cas d'échec, message clair (« Paiement refusé par votre banque. Essayez une autre carte ou commandez sur WhatsApp ») et bascule possible vers WhatsApp sans retaper les informations.
5. En cas de succès, page de confirmation (numéro de commande, récapitulatif, délai de livraison), e-mail de confirmation, et lien « Suivre ma commande sur WhatsApp ».

**Après la commande (les deux parcours) :** page « Suivi de commande » (numéro + téléphone) et message WhatsApp à chaque étape (confirmée, expédiée, livrée).

### 9. WhatsApp partout

- Bouton WhatsApp flottant sur toutes les pages (icône seule sur mobile, « Besoin d'aide ? » sur ordinateur), placé pour ne pas cacher le bouton d'ajout au panier.
- Messages préremplis selon la page : question sur un produit, aide pour la taille, suivi de commande, échange.
- Inscription aux nouveautés par WhatsApp au lieu d'une newsletter par e-mail.

### 10. Réassurance et informations de la boutique

À reprendre dans le pied de page, la FAQ et les pages produit :

- **Livraison :** partout au Maroc, en 24 à 72 h selon la ville. Offerte dès 2 articles ou dès 500 DH, sinon `[frais : X DH]`.
- **Paiement :** à la livraison en espèces, ou en ligne par carte (passerelle sécurisée).
- **Emballage :** discret (aucune mention du contenu sur le colis) et emballage cadeau offert.
- **Échanges et retours :** `[votre politique : délai, conditions, frais, articles exclus pour l'hygiène]`.
- **Contact :** WhatsApp +212 6 98 87 49 40 · `[e-mail]` · `[horaires de réponse]`.
- **Réseaux :** `[Instagram]`, `[TikTok]`, `[Facebook]`.
- **Pages légales :** mentions légales, conditions générales de vente, politique de confidentialité (loi marocaine 09-08 sur les données personnelles, déclaration à la CNDP), politique de cookies avec un bandeau de consentement simple.

### 11. Compte client (facultatif, jamais obligatoire pour commander)

- Connexion par téléphone (code reçu par SMS ou WhatsApp) ou par e-mail.
- Historique des commandes, adresses enregistrées, favoris, « Ma taille » mémorisée.
- Achat sans compte toujours possible.

### 12. Expérience, animations et mobile

- Pensé d'abord pour le mobile : la plupart des clientes arrivent d'Instagram et de WhatsApp.
- Animations douces et courtes (150 à 400 ms) : apparition des sections, ouverture du panier, changement de photo. Toutes désactivées si l'appareil demande moins d'animations (`prefers-reduced-motion`).
- Pas d'écrans bloquants, pas de pop-up à l'arrivée ; au maximum une offre discrète après 30 secondes, facile à fermer.
- Liens directs partageables pour chaque produit et chaque catégorie, retour arrière du navigateur qui fonctionne partout.

### 13. Accessibilité

- Contraste du texte de 4,5:1 minimum ; anneau de focus visible ; navigation complète au clavier.
- Zones tactiles de 44 × 44 px minimum ; libellés sur tous les boutons à icône.
- Textes alternatifs descriptifs sur les photos produits.
- Fenêtres (panier, filtres, guide des tailles) : focus gardé à l'intérieur, fermeture avec Échap.
- Messages d'ajout au panier annoncés aux lecteurs d'écran.
- Un seul titre `h1` par page, puis des `h2` et des `h3` dans l'ordre.

### 14. Performance et référencement

- Images en WebP ou AVIF, plusieurs tailles (`srcset`), chargement différé sous la ligne de flottaison, dimensions réservées pour éviter les sauts de mise en page.
- Objectifs : LCP < 2,5 s sur mobile 4G, CLS < 0,1.
- SEO : titres et descriptions uniques par page, données structurées `Product` (prix, disponibilité, avis réels), `BreadcrumbList` et `Organization`, plan du site XML, balises Open Graph pour le partage WhatsApp et Instagram.
- Suivi : Meta Pixel et Google Analytics 4, uniquement après consentement aux cookies.

### 15. Administration

- Gestion des produits : variantes couleur × tour de dos × bonnet (ou × taille), stock par variante, photos par couleur, prix et prix barré, badges.
- Gestion des commandes WhatsApp et en ligne dans une seule liste, avec statuts (en attente, confirmée, expédiée, livrée, annulée) et export pour le livreur.
- Alertes de stock faible.
- Codes promo, promotions par catégorie, bandeau d'annonce modifiable.
- Avis clientes : ajout et modération manuels (uniquement de vrais avis).

### 16. Livrables attendus

- Le site complet, responsive (375, 768, 1024 et 1440 px), testé sur iPhone et Android.
- Un catalogue d'exemple **clairement marqué comme exemple**, à remplacer par les vrais produits.
- Un fichier de réglages en tête de projet : numéro WhatsApp, seuils de livraison offerte, frais de livraison, clés de la passerelle de paiement (en variables d'environnement, jamais dans le code), liens des réseaux.
- Une courte documentation : ajouter un produit, gérer le stock, traiter une commande WhatsApp, traiter un paiement en ligne.

### Règles à respecter

- Ne jamais inventer d'avis, de chiffres de vente, de certifications ou de « fabriqué au Maroc » sans preuve.
- Ne copier aucun contenu, logo, nom de produit ni photo d'une autre marque.
- Laisser visibles les emplacements `[à compléter]` plutôt que de les remplir avec de fausses informations.

---

## À compléter avant de lancer la création

| Information | Votre réponse |
|---|---|
| Passerelle de paiement en ligne (CMI, Payzone, YouCan Pay…) | |
| Frais de livraison quand elle n'est pas offerte | |
| Politique d'échange et de retour (délai, conditions) | |
| E-mail de contact et horaires de réponse | |
| Liens Instagram, TikTok, Facebook | |
| Gamme de tailles réelle (tours de dos, bonnets, tailles) | |
| Liste des produits, prix, matières et entretien | |
| Best-sellers | |
