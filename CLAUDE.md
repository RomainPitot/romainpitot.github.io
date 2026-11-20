# Portfolio — brain

Romain's personal portfolio site. Static site (no `package.json` found —
plain HTML/CSS/JS, not a JS-framework build), deployed via **GitHub Pages +
GitHub Actions**.

## Comment ça marche (2026-11-20)
- Les pages sont **générées** : données dans `tools/build.py` (`PROJECTS`, `SYSTEMS`...), puis `python tools/build.py` régénère tous les `.html` (commit des HTML inclus). Textes FR/EN de l'interface : `assets/js/i18n.js`.
- Ajouter un projet = une entrée dans `PROJECTS` + images dans `assets/img/projects/<id>-N.jpg` (+ mettre à jour les compteurs « 13 projets » dans build.py et i18n.js). Liens gérés : `itch`, `video`, `github`, `playstore`, `demo`.
- Déploiement : push sur `main` → `.github/workflows/deploy.yml` → GitHub Pages (https://romainpitot.github.io).
- Aperçu local : `python -m http.server 8765` depuis la racine.
