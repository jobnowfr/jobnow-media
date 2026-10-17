# JobNow : routine quotidienne des réseaux sociaux

Chaque soir, Claude prépare et programme dans Metricool les posts du **lendemain** : 2 thèmes (A le matin et le midi, B l'après-midi et le soir), 22 posts sur 9 réseaux. Sur Instagram, uniquement des Reels (plus de posts carrousel). Les posts texte (X, Threads, Bluesky, LinkedIn, post Facebook) partent la plupart du temps avec un visuel : le Reel, la miniature ou l'infographie de l'épingle, en rotation (environ un post sur cinq reste en texte seul).

| Réseau | Thème A | Thème B |
|---|---|---|
| Facebook | post texte 10h, Reel 12h30 | post texte 18h, Reel 19h |
| Instagram | Reel 12h30 | Reel 19h |
| YouTube | vidéo longue 10h, Short 14h | vidéo longue 16h, Short 18h30 |
| TikTok | vidéo 12h | vidéo 18h |
| LinkedIn (profil perso de Jassim) | 11h | 17h |
| X | 12h30 | 19h |
| Bluesky | 12h | 19h30 |
| Threads | 13h | 20h |
| Pinterest (tableau « Modèles de CV ») | 13h | 20h30 |

## Accès

- **Metricool** : connecteur Metricool, marque JobNow, `blogId` 7430673, fuseau Europe/Paris.
- **GitHub** : repo public `jobnowfr/jobnow-media`. Il sert à héberger les visuels le temps que Metricool les copie (il les copie au moment de la programmation).

## Étapes

1. **Date cible** D = demain, heure de Paris. Lire `getScheduledPosts` pour D : si des posts existent déjà (relance après un échec), ne programmer que ce qui manque.
2. **Repo** : `add_repo(owner="jobnowfr", repo="jobnow-media", access="push")`, puis `git clone --depth 1 https://github.com/jobnowfr/jobnow-media /home/claude/jobnow-media`, puis `git config user.name Claude && git config user.email noreply@anthropic.com`.
3. **Choisir les 2 sujets** à partir de `content/history.json` et `content/backlog.md` :
   - jamais un `topic` déjà traité dans les 45 derniers jours ;
   - A et B dans deux catégories différentes, et pas la même catégorie que la veille pour le même créneau ;
   - environ un thème sur trois en catégorie `produit` ;
   - entre 3 et 7 items selon le sujet, pas toujours 5 ;
   - varier les accroches : question, chiffre concret, idée reçue, scène vécue, avant/après.
4. **Choisir les 2 styles visuels** : `python3 tools/pick_styles.py D` affiche les deux styles les moins utilisés récemment (jamais ceux de la veille). Les mettre dans le champ `style` de A puis de B. On peut échanger A et B si un style colle mieux à un sujet (voir « Styles visuels »), mais pas reprendre un style de la veille ni mettre le même style aux deux thèmes.
5. **Écrire `content/D.json`** avec exactement la structure de `content/exemple.json` (schéma plus bas). Avant les légendes, `python3 tools/plan_posts.py --medias D` indique quel post texte part avec une vidéo, une image ou rien : la légende peut y faire allusion (« en 30 secondes 👇 » pour une vidéo, « à enregistrer » pour l'infographie), mais doit rester compréhensible sans le visuel.
6. `python3 tools/check_content.py content/D.json` doit afficher `OK`. Sinon, corriger le contenu et relancer.
7. `python3 tools/build_day.py content/D.json` (environ 10 minutes). Les fichiers vont dans `media/D/`, les planches de contrôle dans `.preview/D/`. Si la sortie liste des textes dans `shrunk`, ils ont dû être réduits pour tenir : les raccourcir dans `content/D.json` et refaire les étapes 6 et 7.
8. **Contrôle visuel** : ouvrir (Read) chaque planche de `.preview/D/` : `_sheet_reel_*`, `_sheet_yt_*` et `_sheet_pin_thumb_*`. Si un texte déborde, est coupé ou en chevauche un autre, raccourcir ce texte dans `content/D.json` et refaire les étapes 6 et 7.
9. **Historique** : ajouter les 2 sujets à `content/history.json` (date, key, category, topic, title, style).
10. **Publier sur GitHub** en gardant une seule révision, pour que le repo reste léger. Supprimer les dossiers `media/` des autres dates, puis :
    ```
    git checkout --orphan publish
    git add -A
    git commit -m "Médias du D" -m "Co-Authored-By: Claude <noreply@anthropic.com>"
    git push -f origin publish:main
    ```
    Puis vérifier que `curl -s -o /dev/null -w "%{http_code}" <base_url>/pin_A.jpg` répond 200 (`base_url` est dans `media/D/manifest.json`).
11. **Programmer** : `python3 tools/plan_posts.py content/D.json > /tmp/plan.json`. Pour chaque entrée, appeler `createScheduledPost(blogId="7430673", date=<date>, info=<info>)` en copiant `info` tel quel (le champ `media` contient déjà le visuel). Si un appel échoue, lire l'erreur, corriger la légende concernée (longueur, champ manquant) et réessayer une fois. Si c'est le visuel qui est refusé (format, taille), retirer `media` et `mediaAltText` de ce post, le programmer en texte seul et le signaler dans le résumé.
12. **Vérifier** avec `getScheduledPosts` pour D : il doit y avoir 22 posts.
13. **Résumé final**, court et en français : les deux sujets et leurs styles, le nombre de posts programmés et les éventuels échecs.

## Styles visuels

Chaque thème a son propre look, pour que le fil ne ressemble pas tous les jours à la même chose. La couleur de chaque style change aussi d'un passage à l'autre (palette choisie selon la date ; on peut forcer `palette` avec un entier, inutile en général).

| style | le look | va bien avec |
|---|---|---|
| `bleu` | le look d'origine : fond bleu quadrillé, surlignage vert citron | tout, surtout `produit` |
| `cahier` | page de cahier à grands carreaux, date écrite en haut, corrections au stylo rouge, surligneur, post-it | `methode`, `erreurs`, `checklist`, `avant_apres` |
| `affiche` | affiche de rue aux couleurs vives, énormes titres en capitales, languettes « jobnow.fr » à détacher | `mythes`, `erreurs`, accroches choc |
| `dossier` | chemise cartonnée, feuilles tapées à la machine, tampons MYTHE / RÉALITÉ, trombones | `mythes`, `candidature`, `situation`, `checklist` |
| `bureau` | fenêtres d'ordinateur rétro, police pixel, boîtes de dialogue, barre de progression | `erreurs`, `produit`, `candidature` |
| `riso` | impression deux encres : grain, trames de points, couleurs légèrement décalées | `exemples`, `situation`, `methode` |

Les styles sont dans `tools/styles/` (un fichier par style). `tools/pick_styles.py` fait tourner les six.

## Règles de contenu

- Français, tutoiement, ton direct et utile. Aucun tiret long ni « - » comme ponctuation (ça fait IA). Les mots composés comme « mots-clés » sont permis.
- **Ce qu'on peut dire de JobNow, et rien d'autre** : créateur de CV en français ; 14 modèles ; aperçu A4 en direct ; export PDF et Word ; comparaison du CV avec une annonce ; suivi des candidatures ; c'est l'utilisateur qui écrit, JobNow ne rédige pas à sa place ; accès de 30 jours à 9,99 € en paiement unique, sans abonnement ; site jobnow.fr ; slogan « Un CV propre, sans y passer la soirée. »
- **Interdit** : le mot « gratuit » ; chiffres, statistiques ou études inventés ; faux témoignages ; promesses de résultat (« garanti », « 100 % », « décroche le job ») ; critiquer un concurrent nommé.
- Les conseils doivent être justes et applicables pour un CV en France et dans la francophonie. En cas de doute, formuler prudemment.
- Pas deux posts identiques le même jour : chaque réseau a sa propre légende, adaptée à son format.
- Hashtags : X 1 ou 2 ; LinkedIn 3 ; Instagram 5 ou 6 ; TikTok 4 ou 5 ; Facebook 0 à 2 ; Bluesky et Threads aucun.
- Dans les textes affichés sur les visuels, `[[...]]` met un passage en valeur (surligneur, bande noire, étiquette, sélection... selon le style).

## Schéma d'un thème (`themes[0]` = A, `themes[1]` = B)

| Champ | Rôle | Longueur |
|---|---|---|
| key | "A" ou "B" | |
| category | erreurs, methode, avant_apres, mythes, checklist, exemples, situation, candidature, produit | |
| topic | identifiant court, unique (slug) | |
| kick | libellé des sections dans les vidéos : ERREUR, ÉTAPE, POINT, MYTHE, EXEMPLE, ASTUCE | |
| style | bleu, cahier, affiche, dossier, bureau ou riso (étape 4) | |
| eyebrow | petite ligne au-dessus du titre (ex. « Idées reçues · infos perso ») | 32 |
| sub | sous-titre de l'écran titre de la vidéo longue | 90 |
| v_hook, v_hook_sub | accroche et sous-titre de la vidéo verticale | 60 / 60 |
| w_title | titre de la vidéo longue (écran titre) | 60 |
| thumb_text | texte de la miniature YouTube, 3 lignes max avec `\n` | 40 |
| pin_headline, pin_foot | titre et pied de l'épingle Pinterest | 55 / 45 |
| cta_headline | écran de fin des vidéos (garder `\n` avant le passage surligné) | 60 |
| chips | 3 pastilles de fonctions JobNow (parmi les vraies fonctions) | |
| items | 3 à 7 éléments (voir ci-dessous) | |
| captions | légendes par réseau (voir ci-dessous) | |

Chaque item : `n` ("01", "02"…), `title` (44 max), `short` (42), `body` (120), `body_short` (80), `fix` (95), `fix_short` (55), `why` (190, explication pour la vidéo longue), et en option `fixlab` (étiquette de l'encadré de conseil, par défaut « À FAIRE » ; ex. « POURQUOI », « EN VRAI », « À VÉRIFIER »), **soit** `example` {bad, good, badtag, goodtag} (ex. AVANT/APRÈS, MYTHE/RÉALITÉ, NON/OUI), **soit** `card` (texte d'un champ « Titre de poste »).

`captions` : `x` (270 en comptage X), `bluesky` (300), `threads` (500), `linkedin`, `linkedin_comment` (lien jobnow.fr en premier commentaire), `facebook_post`, `facebook_reel`, `facebook_reel_title`, `instagram_reel`, `tiktok`, `tiktok_title`, `youtube_long_title` (100), `youtube_long_intro`, `youtube_long_outro` (les chapitres sont ajoutés automatiquement entre les deux), `youtube_tags` (liste), `youtube_short_title` (100, avec #shorts), `youtube_short_text`, `pinterest_title` (100), `pinterest_text` (480).

Les champs `headline`, `cta_note` et `instagram_post` des anciens fichiers ne servent plus.
