# Portfolio — brain

Romain's personal portfolio site. Static site (no `package.json` found —
plain HTML/CSS/JS, not a JS-framework build), deployed via **GitHub Pages +
GitHub Actions**.

## Comment ça marche (2026-11-20)
- Les pages sont **générées** : données dans `tools/build.py` (`PROJECTS`, `SYSTEMS`...), puis `python tools/build.py` régénère tous les `.html` (commit des HTML inclus). Textes FR/EN de l'interface : `assets/js/i18n.js`.
- Ajouter un projet = une entrée dans `PROJECTS` + images dans `assets/img/projects/<id>-N.jpg` (+ mettre à jour les compteurs « 13 projets » dans build.py et i18n.js). Liens gérés : `itch`, `video`, `github`, `playstore`, `demo`.
- Déploiement : push sur `main` → `.github/workflows/deploy.yml` → GitHub Pages (https://romainpitot.github.io).
- Aperçu local : `python -m http.server 8765` depuis la racine.

## Contenu (2026-11-22)
- Données ajoutées par-dessus `PROJECTS` : `tools/content_extra.py` (ENRICH = statuts/notes/défis/rétros de jam, NEW_PROJECTS, SKILL_TIERS, CODE_SAMPLES ; extraits C# dans `tools/samples/`). La page « Systems » (chiffres fictifs) n'existe plus : `code.html` (systems.html redirige).
- Règle : aucun chiffre non vérifiable. Kissoro/Mulu = « Archived ». On Air mentionne l'usage d'IA (règle de la jam).
- Email assemblé en JS (`data-mail`), honeypot `_gotcha`, CSP en `<meta>`, polices locales dans `assets/fonts/`.
- Les « ce que je referais » des jams sont des brouillons à valider par Romain.

## Hero « essaim » + cycle jour/nuit (2026-11-22)
- `assets/js/swarm.js` : port canvas du SwarmSim de Global Invasion (tableaux typés, population seedée, fuient le curseur, évitent le nom/les textes, clic = coup de balai, repop par les bords). Reduced motion = une image fixe. Marqueurs : `data-swarm-hero`, `.h1-line`, `data-swarm-avoid`.
- `assets/js/daynight.js` : palette jour par défaut (CSS `html[data-page="home"]`), fondu RGB vers nuit puis aube selon le scroll ; puce HUD « DAY/NIGHT/DAWN ». Seule la home est concernée (`page(..., home=True)`).
- Police Anton (titre du hero) hébergée dans `assets/fonts/`.
