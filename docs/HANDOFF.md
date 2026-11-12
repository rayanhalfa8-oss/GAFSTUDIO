# Handoff Spec : boutique GAF STUDIO

## Overview

Boutique en ligne de pyjamas, peignoirs et tenues de nuit pour femme, au Maroc.
Une seule page (`index.html`), sans framework ni build : HTML, CSS et JavaScript natifs.
Les photos sont dans `images/` dans la version zip ; dans le dépôt, elles sont intégrées au fichier (data URI).

**Parcours principal :** accueil → page produit → panier → formulaire de livraison → commande envoyée sur WhatsApp → confirmation.
Il n'y a ni paiement en ligne ni compte client : la cliente paie à la livraison, et la commande est confirmée par WhatsApp.

**Utilisatrices :** surtout sur mobile, venant d'Instagram ou de WhatsApp. Elles veulent vérifier le prix, la taille et la livraison avant de commander, et se rassurer.

---

## Layout

| Élément | Règle |
|---|---|
| Conteneur `.wrap` | `width: min(1440px, 100% - 48px)` centré ; `calc(100% - 32px)` sous 820 px |
| Sections | `padding: 80px 0` ; `60px 0` sous 820 px |
| Grille produits `.grid` | 4 colonnes, `gap: 40px 18px` → 3 colonnes ≤ 1100 px → 2 colonnes ≤ 820 px (`gap: 28px 12px`) |
| En-tête | `height: 96px` (grille `1fr auto 1fr` : langue · logo · recherche/favoris/panier) → `70px` ≤ 820 px, menu burger |
| Page produit | 2 colonnes `1.1fr / .9fr`, `gap: 56px`, galerie collante (`top: 84px`) → 1 colonne ≤ 900 px |
| Commande | 2 colonnes `1.25fr / .9fr` (formulaire / récapitulatif collant) → 1 colonne ≤ 820 px, récapitulatif en haut |

**Ordre des sections de l'accueil :** bandeau info → en-tête → hero animé → bandeau de confiance → La marque → Collections (4 cases) → Nouveautés / Best-sellers → Collection (filtres + grille) → Fit Room → bandeau promo → offre « 2e article » → Commander en 3 étapes → Avis (si renseignés) → FAQ → Nouveautés WhatsApp → pied de page.

---

## Design Tokens Used

### Couleurs (`:root`, thème « luxe »)

| Token | Valeur | Usage |
|---|---|---|
| `--ink` | `#1F1A17` | Texte principal, boutons foncés, chiffres du panier |
| `--grey` | `#7D736C` | Texte secondaire, sous-titres, légendes |
| `--line` | `#E9E0D5` | Séparateurs, bordures de cartes et de champs |
| `--soft` | `#F4EEE6` | Fond des images en chargement, champs de recherche |
| `--pink` | `#E9D6C7` | Boutons doux (`.btn-pink`), sélection de texte |
| `--blush` | `#F8F2EB` | Fonds de sections claires, blocs de réassurance |
| `--pink-hot` | `#9A7350` | Accent bronze : prix promo, « Nouveauté », icônes de réassurance |
| `--gold` | `#B8955A` | Ornements, anneau de focus, repère du podium Fit Room |
| `--white` | `#FFFDFA` | Fond des fenêtres et de la page produit |
| fond de page | `#FBF8F4` | `body` |
| WhatsApp | `#25D366` | Bouton flottant et bouton d'envoi de commande uniquement |
| Stock | `#3E8E5A` ok · `#C48A1C` faible · `#A8423A` épuisé | Pastille de disponibilité (page produit) |

### Ombres

| Token | Valeur | Usage |
|---|---|---|
| `--sh-1` | `0 1px 2px rgba(60,40,25,.06), 0 6px 14px rgba(60,40,25,.06)` | Cartes au repos |
| `--sh-3d` | `0 2px 4px …, 0 14px 28px …, 0 40px 70px -24px rgba(60,40,25,.32)` | Cartes au survol, image de la marque |

Les ombres sont teintées en brun chaud (`rgba(60,40,25,…)`), jamais en noir pur.

### Typographie (Google Fonts)

| Token | Valeur | Usage |
|---|---|---|
| `--serif` | Cormorant Garamond 400/500/600 + italique, repli Didot, Georgia | Logo, titres de sections, noms de produits, accroches |
| `--sans` | Jost 300/400/500/600, repli Helvetica Neue, Arial | Texte courant, boutons, formulaires |
| `--track` | `.16em` | Espacement des libellés en majuscules (boutons, menu) |
| Titre de section | `clamp(2rem, 3.4vw, 3rem)` serif 400 | `.sec-head h3` |
| Nom produit (page produit) | `clamp(2rem, 3.4vw, 2.9rem)` serif 400 | `#pdpName` |
| Hero | `clamp(2.6rem, 5vw, 5.2rem)` serif 400 | `h1` du hero |
| Bouton | `.78rem`, 500, majuscules, `letter-spacing: var(--track)` | `.btn` |

### Rayons et hauteurs
- Rayon : `2px` pour les boutons et les tailles, `3–4px` pour les cartes et les fenêtres, `50%` pour les pastilles de couleur.
- Bouton : `height: 46px`, `padding: 0 28px` ; `50px` dans la page produit ; `54–56px` pour l'envoi de commande.
- Zone tactile minimale : 40 × 40 px (icônes, tailles 52 × 44 px).

---

## Components

| Composant | Variantes | Données / props | Notes |
|---|---|---|---|
| `.btn` | `btn-dark` (action principale), `btn-pink` (douce), `btn-line` (secondaire), `btn-wa` (contour WhatsApp), `btn-wa-solid` (envoi) | libellé, icône optionnelle | Un seul `btn-dark` par zone de décision |
| Carte produit `.card` | badge `-X %` / `Nouveau` / `Best-seller`, cœur favori, bouton rapide | un objet de `PRODUCTS` | Clic sur l'image, le nom ou le bouton → page produit |
| Pastilles couleur | `.swatches button` (carte), `.colors button` (page produit) | `colors[i].hex`, `name` | Bouton accessible, `aria-label` = nom de la couleur |
| Sélecteur de taille `.size-row` | normal, sélectionné `.on`, épuisé `:disabled` (barré) | `sizes`, `soldout`, `STOCK` | Secousse `.shake` si on ajoute sans taille |
| Page produit `#pdp` | — | `id`, couleur initiale | Lien partageable `#produit-<slug>` |
| Panier `.drawer` | vide / rempli | `cart` (localStorage) | Quantité ±, changement de taille (`<select>`), retrait |
| Formulaire de commande `#coForm` | normal, champ en erreur `.f.err` | nom, téléphone, ville (+ autre ville), adresse, remarque, cadeau, paiement | Validation à l'envoi, message sous le champ |
| Fit Room `#mixStage` | photo détourée sur podium, 4 angles | `colors[i].views` | Angle sans photo : bouton grisé « bientôt disponible » |
| Toast `#toast` | — | texte | Bas d'écran, 2,4 s, 2 lignes max sur mobile |
| Bouton WhatsApp flottant `.wa-float` | libellé (desktop) / icône seule (mobile) | `WHATSAPP` | Présent sur toutes les vues |

### Modèle de données produit (`PRODUCTS`)

```js
{ id, collection: "pyjamas" | "peignoirs", name, matiere, price, old /* null si pas de promo */,
  tags: ["new" | "best"], sizes: ["M","L","XL","XXL"], soldout: [],
  colors: [{ name, hex, img /* photo boutique */,
             views: { face, droit, dos, gauche } /* photos détourées 760×1100 */ }],
  images: [], desc, hook, points: [], tip, care /* entretien, optionnel */ }
```

### Réglages (en haut du script, repérés par ✏️)

| Constante | Rôle | Par défaut |
|---|---|---|
| `WHATSAPP` | Numéro des commandes (format `212…`, sans `+` ni `0`) | `212698874940` |
| `FREE_SHIP_ITEMS` / `FREE_SHIP` | Livraison offerte dès N articles / dès X DH | 2 / 500 |
| `SHIPPING_FEE` | Frais si non offerte (`null` = « à confirmer ») | `null` |
| `OFFER_END` | Fin réelle de l'offre ; vide = compte à rebours masqué | `""` |
| `REVIEWS` | Vrais avis clientes ; vide = section masquée | `[]` |
| `RETURNS_POLICY` | Politique d'échange ; vide = invitation WhatsApp | `""` |
| `STOCK` | Quantités par produit › couleur › taille | `{}` |
| `PAYMENT_METHODS` | Modes de paiement proposés | paiement à la livraison |
| `SOCIAL` | Liens Instagram / Facebook / TikTok ; vide = icône masquée | vides |

---

## States and Interactions

| Élément | État | Comportement |
|---|---|---|
| `btn-dark` | Survol | Dégradé plus clair, `translateY(-2px)`, ombre plus large |
| Tous les `.btn` | Appui | `translateY(1px) scale(.99)` |
| Tous les éléments interactifs | Focus clavier | `outline: 2px solid var(--gold)`, `offset: 3px` |
| Carte produit | Survol (souris uniquement) | Inclinaison 3D (±6°) + reflet qui suit le curseur ; bouton rapide qui monte |
| Carte produit | Tactile | Pas d'inclinaison ; bouton rapide toujours visible |
| Taille | Épuisée | `disabled`, texte barré, `title="Épuisé"` |
| Bouton « Ajouter au panier » | Sans taille | Secousse de la rangée de tailles + toast « Choisissez votre taille… » |
| Bouton « Ajouter au panier » | Taille choisie | Libellé « Ajouter au panier · 199 DH » (prix × quantité) |
| Après ajout | — | Toast « Ajouté au panier : nom, taille · couleur », badge du panier qui pulse, panier ouvert après 250 ms |
| Disponibilité | Aucune taille choisie | « Disponible en M, L, XL, XXL. » |
| Disponibilité | Stock 1 à 3 | Pastille ambre « Plus que N en stock en taille L. » |
| Disponibilité | Épuisé | Pastille rouge + proposition WhatsApp |
| Image principale (page produit) | Survol souris | Zoom ×1,8 centré sur le curseur |
| Champ du formulaire | Erreur | Bordure `#C0392B` + message sous le champ ; focus sur le premier champ en erreur ; l'erreur s'efface dès qu'on retape |
| Envoi de commande | Valide | Ouvre WhatsApp (message rédigé), affiche l'écran « Merci », vide le panier |
| Bandeau du haut | « J'ai compris » | Masqué et mémorisé (`gaf_notice`) |
| Favoris (cœur) | Bascule | Toast « Ajouté à vos favoris » / « Retiré… » ; l'icône de l'en-tête filtre la grille |

---

## Responsive Behavior

| Breakpoint | Changements |
|---|---|
| > 1240 px | Bandeau de confiance fixe et centré |
| ≤ 1240 px | Bandeau de confiance en défilement continu (pause au survol) |
| ≤ 1100 px | Grilles produits et collections en 3 colonnes ; menu aligné à gauche, défilable |
| ≤ 900 px | Page produit en 1 colonne, galerie non collante ; barre « Quantité + Ajouter au panier » collée en bas de l'écran ; Fit Room en 1 colonne ; marque en 1 colonne |
| ≤ 820 px | En-tête 70 px + burger (menu latéral 320 px) ; hero : image puis texte ; grilles en 2 colonnes ; filtres défilables ; fenêtres en feuille depuis le bas ; commande en 1 colonne, récapitulatif en haut ; bouton WhatsApp réduit à l'icône |
| ≤ 520 px | Pied de page en 1 colonne ; formulaire WhatsApp empilé |

Les gestes principaux sont placés en bas de l'écran sur mobile (barre d'ajout au panier, bouton WhatsApp), car la cliente tient le téléphone d'une main.

---

## Edge Cases

- **Panier vide** : « Votre panier est vide. » + livraison offerte dès 2 articles + bouton « Découvrir la collection ».
- **Recherche sans résultat** : « Aucun article ne correspond à « mot ». Essayez un autre mot… » + « Voir toute la collection ».
- **Filtres sans résultat** : « …Essayez une autre taille ou une autre couleur. »
- **Favoris vides** : toast « Aucun favori pour l'instant… » ; aucune page vide.
- **Produit sans photo** : emplacement à motif + icône « Votre image ici » (pas de lien d'image cassé).
- **Angle Fit Room sans photo** : bouton grisé ; au clic, toast « La vue « Dos » de cet article arrive bientôt. »
- **Avis absents** : section « Elles en parlent » masquée ; ne jamais remplir avec de faux avis.
- **Lien produit inconnu** (`#produit-xxx`) : retour silencieux à l'accueil.
- **Nom de produit long** : retour à la ligne équilibré (`text-wrap: balance`), jamais tronqué ; prévoir +30 % de longueur pour l'arabe.
- **Connexion lente** : images en `loading="lazy"` (sauf le hero) ; animation du hero lancée seulement quand ses images sont chargées, la photo fixe s'affiche en attendant.
- **Sans WebGL, ou avec « réduire les animations »** : hero en photo fixe ; toutes les animations sont coupées (`prefers-reduced-motion`).
- **Ouverture du fichier sans serveur** (`file://`) : le navigateur bloque WebGL, la photo fixe reste ; tout le reste fonctionne.
- **Stockage local bloqué** (navigation privée) : toutes les lectures et écritures de `localStorage` sont protégées par `try/catch` ; le panier fonctionne pour la visite en cours.
- **WhatsApp ne s'ouvre pas** : l'écran « Merci » propose « Cliquez ici pour réessayer ».

---

## Animation / Motion

| Élément | Déclencheur | Animation | Durée | Easing |
|---|---|---|---|---|
| Hero (photo) | Chargement | Zoom 1,18 → 1,04 + flou → net | 2200 ms | `cubic-bezier(.16,.8,.24,1)` |
| Hero (photo) | En continu | Dérive lente 1,04 → 1,11 | 22 s aller-retour | `ease-in-out` |
| Hero (filles) | En continu | Corps et têtes animés en WebGL (rires décalés) | cycles de 6,2 à 7 s | sinusoïdal |
| Titre du hero | Chargement | Lignes qui montent hors d'un masque, en cascade | 1100 ms, décalage 150 ms | `cubic-bezier(.16,.8,.24,1)` |
| Sections `.reveal` | Entrée à l'écran (seuil 10 %) | Montée 46 px + `rotateX(9deg)` → à plat | 900 ms | `cubic-bezier(.2,.7,.2,1)` |
| Panier | Ouverture | Glisse depuis la droite | 450 ms | `cubic-bezier(.2,.7,.2,1)` |
| Page produit / commande | Ouverture | Fondu + montée de 24 px | 350–400 ms | `cubic-bezier(.2,.7,.2,1)` |
| Toast | Apparition | Monte depuis le bas | 400 ms | `cubic-bezier(.2,.7,.2,1)` |
| Badge du panier | Ajout | Pulsation ×1,4 | 400 ms | `ease` |
| Fit Room | Changement d'angle | Fondu enchaîné sur place, sans mouvement | 360 ms | `cubic-bezier(.4,0,.2,1)` |
| Fit Room | Repère du podium | Glisse le long de l'ellipse | 520 ms | ease-out cubique |
| Bandeau de confiance | En continu (≤ 1240 px) | Défilement horizontal | 34 s | `linear` |

Les animations n'utilisent que `transform`, `opacity` et `filter`. Elles se coupent toutes avec `prefers-reduced-motion: reduce`.

---

## Accessibility Notes

- **Lien d'évitement** « Aller aux produits », premier élément focusable, visible au focus.
- **Ordre du focus** : bandeau → en-tête (burger, logo, recherche, favoris, panier) → menu → contenu → bouton WhatsApp → retour en haut.
- **Fenêtres** (`#pdp`, `#qv`, `#sg`, `#co`) : `role="dialog"`, `aria-modal="true"`, `aria-labelledby` sur leur titre. `Échap` ferme la fenêtre du dessus (guide des tailles → commande → page produit → panier).
- **Fit Room** : zone focusable (`tabindex="0"`) ; flèches ← → pour changer d'angle ; onglets d'angle avec `aria-pressed` ; angles indisponibles en `aria-disabled`.
- **Boutons à icône** : tous ont un `aria-label` (panier, favoris, fermer, zoom, couleurs).
- **Images** : `alt` descriptif pour les photos produits et le hero ; `alt=""` pour les doublons décoratifs (miniatures, colonnes du bandeau promo).
- **Formulaire** : chaque champ a un libellé visible ; les erreurs sont écrites en texte sous le champ, pas seulement en couleur ; focus automatique sur le premier champ en erreur.
- **Contraste** : texte principal `#1F1A17` sur `#FBF8F4`. Vérifier au cas par cas le bronze `#9A7350` sur les fonds clairs (prix promo, petits libellés en majuscules).
- **À améliorer** : annoncer les toasts aux lecteurs d'écran (`aria-live="polite"` sur `#toast`) et piéger le focus dans les fenêtres ouvertes.
