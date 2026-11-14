# Prompt WordPress : site de lingerie GAF STUDIO

> À donner tel quel à votre développeur WordPress ou à un outil IA pour WordPress.
> Les éléments entre `[crochets]` sont à remplacer par vos vraies informations.

---

## PROMPT

Crée sur **WordPress + WooCommerce** un site e-commerce **simple, élégant et rapide** pour **GAF STUDIO**, une boutique marocaine de **lingerie pour femme**.

L'expérience doit ressembler à celle des grandes enseignes de lingerie comme Etam : navigation claire par rayons, choix de taille facile, guide des tailles, ensembles assortis et service client rassurant. Le site doit cependant garder sa propre identité : **ne copie ni texte, ni logo, ni photo, ni nom de produit d'une autre marque.**

Priorité absolue : **la simplicité.** Peu de pages, peu de clics, rien d'inutile. La cliente doit trouver sa taille, ajouter au panier et commander en moins de 2 minutes, sur son téléphone.

### 1. Informations de la boutique

- **Nom :** GAF STUDIO, signature « Lingerie · Nuit · Lounge »
- **Pays :** Maroc · **Langue :** français (arabe en option plus tard) · **Devise :** DH (MAD), prix TTC
- **WhatsApp :** +212 6 98 87 49 40, lien `https://wa.me/212698874940`
- **Livraison :** partout au Maroc, en 24 à 72 h selon la ville
- **Livraison offerte :** dès 2 articles ou dès 500 DH, sinon `[X DH]`
- **Paiement :** à la livraison (espèces) **ou** en ligne par carte
- **Emballage :** discret, avec emballage cadeau offert
- **Échanges et retours :** `[votre politique]`. Ajouter la mention : « Pour des raisons d'hygiène, les culottes, strings et bodys portés ou sans leur protection ne sont ni repris ni échangés. »
- **Réseaux :** `[Instagram]` · `[TikTok]` · `[Facebook]`
- **E-mail :** `[contact@…]`

### 2. Thème et réglages techniques

- **Thème** léger et compatible WooCommerce, par exemple **Kadence** ou **Blocksy**, monté avec l'éditeur de blocs WordPress. Éviter les constructeurs lourds si possible, pour la rapidité sur mobile.
- **Extensions** (une seule par besoin) :
  - WooCommerce ;
  - pastilles de couleur et de taille sur les variations (ex. *Variation Swatches for WooCommerce*) ;
  - filtres de produits par taille, bonnet, couleur et prix (ex. *WooCommerce Product Filters*) ;
  - guide des tailles affiché sur la fiche produit (ex. *Product Size Chart for WooCommerce*) ;
  - **commande par WhatsApp** (ex. *OneClick Chat to Order* ou un code équivalent, voir section 7) ;
  - **paiement en ligne** par une passerelle marocaine : `[CMI, YouCan Pay ou Payzone, selon votre contrat]` ;
  - paiement à la livraison : « Paiement à la livraison » natif de WooCommerce ;
  - cache et optimisation des images (ex. *LiteSpeed Cache* ou *WP Rocket*, conversion en WebP) ;
  - SEO (ex. *Rank Math* ou *Yoast*) ;
  - bandeau de consentement aux cookies.
- Commande **sans création de compte** (compte facultatif).
- HTTPS obligatoire.

### 3. Style (UI)

- **Couleurs :**
  - fond ivoire `#FBF8F4` ;
  - texte et boutons principaux en encre `#1F1A17` ;
  - sections claires `#F8F2EB` ;
  - nude `#E9D6C7` ;
  - accent bronze `#86613F` (prix promo, badges) ;
  - gris `#6B625B` (textes secondaires).
- **Polices :** *Cormorant Garamond* pour les titres et noms de produits, *Jost* pour les textes et les boutons.
- **Boutons :** fond encre, texte ivoire, en majuscules espacées, hauteur 48 px, coins presque droits (2 px).
- **Photos :** grandes, lumineuses, fond neutre. Mannequins de différentes morphologies et tailles de bonnet. Rendu élégant et non explicite. Format portrait 4:5 partout, pour une grille régulière.
- **Icônes :** au trait fin et toutes du même style, pas d'émojis.
- Beaucoup d'espace blanc, une seule action principale par écran.

### 4. Menu (simple)

En-tête : logo au centre ; recherche, favoris et panier à droite ; menu burger sur mobile.

Menu principal :
1. **Nouveautés**
2. **Soutiens-gorge** : avec armatures, sans armatures, push-up, balconnet, triangle
3. **Culottes** : slip, shorty, string, culotte haute, lots
4. **Ensembles**
5. **Nuisettes et bodys**
6. **Pyjamas et peignoirs**
7. **Promos**

Au-dessus de l'en-tête, un bandeau fin : « Livraison offerte dès 2 articles · Paiement à la livraison ou en ligne ».

### 5. Pages

**Accueil (court) :**
1. Grande photo de campagne + un bouton « Découvrir la lingerie ».
2. Bandeau de 4 garanties avec icônes : paiement à la livraison ou en ligne · livraison 24 à 72 h partout au Maroc · emballage discret · conseil taille sur WhatsApp.
3. 4 grandes cases de rayons (Soutiens-gorge, Culottes, Ensembles, Nuisettes).
4. Nouveautés (8 produits, défilement horizontal sur mobile).
5. Bloc « Trouvez votre taille », avec un bouton vers le guide.
6. Avis clientes : **uniquement de vrais avis**, sinon la section est masquée.
7. Pied de page : contact WhatsApp, livraison, échanges, guide des tailles, FAQ, pages légales, réseaux.

**Page rayon :**
- Titre et nombre d'articles.
- Filtres : **tour de dos** (70 à 105), **bonnet** (A à F), taille (S à XXL), couleur, prix. Sur mobile, un bouton « Filtrer » ouvre un panneau depuis le bas.
- Tri : nouveautés, prix croissant, prix décroissant.
- Grille de 2 produits par ligne sur mobile, 4 sur ordinateur.
- **Carte produit** : 2e photo au survol, pastilles de couleur, nom, prix (prix barré si promo), badge « Nouveau » ou « -20 % ».

**Fiche produit :**
- Galerie de photos (zoom au toucher), photo portée, photo de dos et détail de la matière.
- Nom, prix, avis (s'il y en a).
- **Couleur** en pastilles avec le nom affiché.
- **Taille** en boutons :
  - soutien-gorge : d'abord le **tour de dos**, puis le **bonnet** ;
  - autres articles : S à XXL ;
  - combinaisons épuisées grisées et barrées.
- Lien **« Guide des tailles »** qui s'ouvre dans une fenêtre, sans quitter la page.
- Stock : « En stock » ou « Plus que 2 ».
- Bouton **« Ajouter au panier »** bien visible, collé en bas de l'écran sur mobile.
- Bouton **« Une question ? WhatsApp »** (message prérempli avec le produit, la couleur et la taille).
- **« Complétez l'ensemble »** : la pièce assortie, avec son propre choix de taille et un ajout en un clic.
- Accordéons :
  - description ;
  - composition et entretien `[selon l'étiquette]` ;
  - livraison et paiement ;
  - échanges.
- « Vous aimerez aussi » (4 produits).

**Guide des tailles** (page + fenêtre sur la fiche produit) :
- Tableau soutiens-gorge : tour sous la poitrine → tour de dos ; différence avec le tour de poitrine → bonnet.
- Tableau culottes : tour de taille et tour de hanches → S à XXL.
- Petit schéma qui montre où mesurer.
- **Calculateur :** la cliente entre 2 mesures et obtient sa taille (ex. 85C), avec un bouton « Voir les modèles dans ma taille ».
- Bouton « Besoin d'aide ? Écrivez-nous sur WhatsApp ».

**Autres pages :** FAQ courte, Livraison, Échanges et retours, Contact, Mentions légales, CGV, Confidentialité (loi 09-08 / CNDP).

### 6. Panier

- Mini-panier qui s'ouvre sur le côté après chaque ajout.
- Pour chaque article : photo, nom, couleur, taille, quantité (+ / −), prix, « Retirer ».
- Barre de progression : « Encore 1 article pour la livraison offerte ».
- Sous-total, livraison, total.
- **Deux boutons de même taille :**
  - **« Commander sur WhatsApp »** (vert) ;
  - **« Payer en ligne »** (encre).
- Panier vide : « Votre panier est vide » + bouton « Voir les nouveautés ».

### 7. Commande : 2 choix simples

**Formulaire commun, sur une seule page :**
- nom et prénom ;
- téléphone marocain (vérifié : 10 chiffres commençant par 05, 06 ou 07) ;
- ville (liste des villes du Maroc) ;
- adresse ;
- e-mail : facultatif pour WhatsApp, obligatoire pour le paiement en ligne ;
- remarque (facultative) ;
- case « C'est un cadeau ».

Supprimer tous les autres champs WooCommerce (société, code postal, pays, adresse 2). Le pays est fixé sur le Maroc.

**Choix 1 : Commander sur WhatsApp (paiement à la livraison)**
- La commande est enregistrée dans WooCommerce avec le statut « En attente ».
- WhatsApp s'ouvre vers le +212 6 98 87 49 40 avec un message déjà écrit : numéro de commande, articles (nom, couleur, taille, quantité, prix), total, nom, téléphone, ville, adresse, cadeau oui ou non, « Paiement à la livraison ».
- Page de confirmation : « Appuyez sur Envoyer dans WhatsApp pour confirmer votre commande », avec un bouton « Réessayer » si WhatsApp ne s'est pas ouvert.

**Choix 2 : Payer en ligne**
- Paiement par carte (CB marocaines, Visa, Mastercard) via `[CMI / YouCan Pay / Payzone]`, avec 3-D Secure et une page de paiement sécurisée de la passerelle.
- Bouton « Paiement en cours… » non cliquable deux fois.
- En cas d'échec : « Paiement refusé. Essayez une autre carte ou commandez sur WhatsApp. »
- En cas de succès : page de confirmation, e-mail de confirmation et lien WhatsApp pour le suivi.

**Après la commande :** l'équipe confirme par WhatsApp, puis informe la cliente à l'expédition.

### 8. WhatsApp sur tout le site

- Bouton WhatsApp flottant en bas à gauche, sur toutes les pages (il ne doit pas cacher le bouton « Ajouter au panier »).
- Messages préremplis selon la page : question produit, aide taille, suivi de commande.

### 9. Expérience client (UX)

- **Mobile d'abord :** la plupart des clientes viennent d'Instagram et de WhatsApp.
- **3 clics maximum** entre l'accueil et le panier.
- **Pas de pop-up** à l'arrivée sur le site.
- **Messages clairs et rassurants :** « Ajouté au panier : Soutien-gorge Rose, 85C », et sous chaque champ, une erreur qui dit comment corriger.
- **Animations discrètes** (200 à 300 ms), désactivées si le téléphone le demande.
- **Lien direct partageable** pour chaque produit.
- **Accessibilité :** contraste suffisant, boutons de 44 px minimum, textes alternatifs sur les photos, navigation au clavier.
- **Rapidité :** images WebP, chargement différé, objectif moins de 2,5 s sur mobile.

### 10. À ne pas faire

- Pas de faux avis, pas de faux compteurs (« 12 personnes regardent ce produit »), pas de faux comptes à rebours.
- Aucun contenu, logo, nom ou photo copié d'une autre marque.
- Les informations manquantes restent visibles `[à compléter]`, sans être inventées.

### 11. Livrables

- Le site WordPress complet, testé sur iPhone et Android.
- 6 produits d'exemple **marqués « exemple »**, à remplacer par les vrais produits.
- Un court guide : ajouter un produit avec ses tailles et couleurs, gérer le stock, traiter une commande WhatsApp, voir un paiement en ligne.

---

## À compléter avant de commencer

| Information | Votre réponse |
|---|---|
| Passerelle de paiement en ligne (CMI, YouCan Pay, Payzone…) | |
| Frais de livraison quand elle n'est pas offerte | |
| Politique d'échange et de retour | |
| E-mail de contact | |
| Liens Instagram, TikTok, Facebook | |
| Tailles disponibles (tours de dos, bonnets, tailles) | |
| Produits : noms, prix, couleurs, matières, entretien | |
