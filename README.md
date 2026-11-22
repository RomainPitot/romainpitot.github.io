# romain.pitot — portfolio

Static portfolio site for Romain Pitot (Unity / C# developer, Toulouse).
Plain HTML/CSS/JS, no framework: GitHub Actions deploys this repo straight to
GitHub Pages on every push to `main`.

Live at: **https://romainpitot.github.io/**

## Structure

```
index.html            Home
projects.html         Projects listing (filter/sort)
projects/<slug>.html  One page per project (challenge, jam retrospective, links)
code.html             Real C# extracts with the reasoning behind them
about.html            About, how I work, education, skills by level of use
contact.html          Contact form (Formspree) + availability
systems.html          Redirect to code.html (old URL)
assets/css/style.css  Design tokens and components
assets/js/main.js     Nav, filters, reveal, i18n toggle, form, email assembly
assets/js/i18n.js     EN/FR UI copy
assets/fonts/         Self-hosted Inter and JetBrains Mono (latin subset)
cv.pdf                Résumé
tools/build.py        Generator for every .html page
tools/content_extra.py  Corrections, challenges, retrospectives, skills, code samples
tools/samples/        The C# extracts shown on code.html
```

## Editing content

Pages are generated. Base project data is in `tools/build.py` (`PROJECTS`),
everything added on top is in `tools/content_extra.py`:

- `ENRICH` — per-project overrides (status, note, challenges, jam retrospective, facts).
- `NEW_PROJECTS` — projects added after the base list.
- `SKILL_TIERS` — skills grouped by how they are used.
- `CODE_SAMPLES` — the extracts of `code.html` (source files in `tools/samples/`).

Then:

```bash
python tools/make_project_covers.py   # only if a project has no real screenshot
python tools/build.py                 # regenerates every .html, sitemap, robots
```

Commit the regenerated `.html` files with the data change.

Preview locally: `python -m http.server 8765` from the root.

## Content rules

- Nothing on the site is a number I cannot defend. Store figures are public
  (Google Play), test counts come from the repo, measurements are labelled.
- Projects removed from stores are marked **Archived** with the reason.
- Where a project relied on AI tools (On Air), its page says so.

## Security and privacy

- Content-Security-Policy and referrer policy are set with `<meta>` (GitHub
  Pages cannot send headers). Third parties: only Formspree (contact form).
- The e-mail address is assembled by JavaScript from two data attributes, and
  the form has a honeypot field, to limit scraping and spam.
- Fonts are self-hosted: no request to Google at load time.

## Deployment

One-time setup on GitHub: **Settings → Pages → Build and deployment → Source
→ GitHub Actions**. After that every push to `main` runs
`.github/workflows/deploy.yml`.
