# Vidéos Higgsfield pour la boutique GAF STUDIO

Le site est prêt à recevoir deux types de vidéos :

| Emplacement | Réglage dans `index.html` | Effet sur le site |
|---|---|---|
| Hero de l'accueil | `const HERO_VIDEO = "images/hero.mp4";` | La vidéo remplace la photo animée (muette, en boucle, la photo s'affiche si la vidéo ne se lance pas) |
| Page produit, par couleur | dans `PRODUCTS`, sur une couleur : `video:"images/video-coeur-rose.mp4"` | Une vignette avec une icône de lecture apparaît dans la galerie ; la vidéo se lit à la place de la photo |

Ces vidéos se génèrent avec **votre** compte Higgsfield : il faut vous connecter (`higgsfield auth login`) et avoir des crédits. Je ne peux pas le faire à votre place.

---

## 1. Étapes

1. Connectez-vous sur higgsfield.ai (ou avec l'outil en ligne de commande : `higgsfield auth login`).
2. Choisissez un modèle **image → vidéo** (par exemple Kling ou Seedance), en durée de 5 à 8 secondes.
3. Comme **image de départ**, utilisez une photo du dossier `images/` du site (liste ci-dessous).
4. Copiez le prompt correspondant (en anglais, les modèles le comprennent mieux).
5. **Vérifiez chaque vidéo avant de la publier** (voir la partie 4).
6. Exportez en MP4, puis mettez le fichier dans `images/` et réglez `HERO_VIDEO` ou `video:` (voir le tableau plus haut).

**Format conseillé :** MP4 (H.264), sans son, 1080 px de large maximum, 8 Mo maximum par vidéo, 5 à 8 secondes, idéalement en boucle sans coupure visible.

---

## 2. Vidéo du hero (accueil)

**Image de départ :** `images/hero-campagne.jpg` (les trois filles en pyjama).
**Format :** 16:9 pour l'ordinateur. Une version 9:16 est possible pour les stories.

```
Three young women in pink pyjamas laughing together naturally, leaning on each other,
gentle body sway and soft shoulder movement while they laugh, hair moving slightly,
soft snowflakes falling in front of a pale blue studio wall, warm soft lighting,
static camera with a very slow push-in, photorealistic, fashion campaign, 6 seconds, seamless loop
```

**À éviter (champ « negative prompt ») :**
```
distorted faces, extra fingers, warped hands, changing outfits, changing pyjama print,
text, logo, watermark, camera shake, fast motion
```

---

## 3. Vidéos produit (« 3D / 360° »)

**Image de départ :** la photo détourée de face, `images/<produit>-<couleur>-face.webp`. Elle est déjà sur fond neutre, ce qui donne les meilleurs résultats.
**Format :** 4:5 (portrait), 6 à 8 secondes.

### Prompt de base (rotation sur podium)

Remplacez `[DESCRIPTION]` par la ligne du produit dans le tableau ci-dessous :

```
E-commerce fashion turntable video. A woman wearing [DESCRIPTION] slowly turns 360 degrees
in place on a round beige studio podium, showing the front, the right side, the back and the left side,
natural relaxed pose, plain warm ivory background, even soft studio lighting,
static camera, full body visible, garment colours, print and details exactly unchanged,
photorealistic, 8 seconds
```

**À éviter :**
```
changing the garment, new patterns, different colours, extra pockets, logo, text,
distorted body, extra limbs, background change, camera movement
```

### Description de chaque produit

| Produit | Fichier image (une par couleur) | `[DESCRIPTION]` |
|---|---|---|
| Pyjama coton à pois | `pyjama-pois-<beige, sauge, bleu, mauve>-face.webp` | an ivory cotton pyjama set with small polka dots, Peter Pan collar with lace trim, buttoned top, two embroidered flower pockets |
| Pyjama doux zippé | `pyjama-zip-<sauge, gris, taupe, rose>-face.webp` | a soft textured fleece pyjama set, half-zip high-neck top with kangaroo pocket, joggers gathered at the ankles |
| Peignoir caniche | `peignoir-caniche-<beige, rose, taupe, bleu>-face.webp` | a long curly fleece bathrobe with a contrasting curly shawl collar, tie belt and two patch pockets |
| Ensemble peignoir mariée | `peignoir-matelasse-1-face.webp` | a white quilted short robe with lace-trimmed shawl collar, tie belt and two large pockets, with matching straight trousers |
| Pyjama à nœuds | `pyjama-noeuds-<lilas, vert, beige, rose, gris>-face.webp` | a tone-on-tone checked pyjama set with embossed texture, buttoned V-neck top with plain trim, two decorative bows on the front, straight trousers |
| Pyjama ourson à capuche | `pyjama-ourson-<rose, bleu, vert, beige>-face.webp` | a soft embossed fleece pyjama set, hoodie with two small bear ears, kangaroo pocket, joggers gathered at the ankles |
| Pyjama vichy cœurs | `pyjama-coeur-<rose, beige, mauve, vert, bleu>-face.webp` | a gingham check pyjama set, ruffled collar and cuffs, wooden-look buttons, two heart-shaped ruffled pockets with a small embroidered bear, straight trousers |
| Pyjama équestre | `pyjama-equestre-<blanc, noir, orange>-face.webp` | a long-sleeve pyjama set, plain shirt with notch collar, buttons and a horse motif on the front, ruffled cuffs, printed trousers with ruffled ankles |

Nommez chaque vidéo `video-<produit>-<couleur>.mp4` (par exemple `video-coeur-rose.mp4`), puis ajoutez-la sur la bonne couleur :

```js
{name:"Rose", hex:"#EBB3BC", img:PHOTOS["pyjama-coeur-rose"], video:"images/video-coeur-rose.mp4", views:{...}}
```

---

## 4. Vérification obligatoire avant publication

Higgsfield **invente** ce qu'il ne voit pas sur la photo de départ : le dos, les côtés, parfois les motifs. Avant de mettre une vidéo en ligne, vérifiez qu'elle correspond au vrai vêtement :

- les couleurs et l'imprimé (pois, carreaux, nœuds, broderies) ;
- le dos : présence ou non de capuche, d'étiquette, de couture, de motif ;
- les poches, les boutons, les volants ;
- le corps et les mains (pas de doigts déformés).

Si le dos inventé ne correspond pas au vrai produit, **ne publiez pas la vidéo** : une cliente qui reçoit autre chose que ce qu'elle a vu se sent trompée, et vous risquez des retours. Pour la vue de dos, une vraie photo reste plus sûre. Le site l'affiche déjà dans la Fit Room dès que vous l'ajoutez (`views:{dos:"…"}`).

**Ne générez jamais** de logo ni de nom de marque (Hermès ou autre) dans les vidéos.
