# romain.pitot — portfolio

Static portfolio site for Romain Pitot (gameplay programmer, Unity/C#).
Plain HTML/CSS/JS, no build tools required to run it — GitHub Actions deploys
this repo straight to GitHub Pages on every push to `main`.

Live at: **https://romainpitot.github.io/**

## Structure

```
index.html            Home
projects.html         Projects listing (filter/sort)
projects/<slug>.html  One page per project
systems.html          Technical systems deep-dives
about.html            About / education / skills
contact.html          Contact form (mailto) + links
assets/css/style.css  Shared styles (design tokens, components)
assets/js/main.js     Nav, filters, scroll reveal, i18n toggle, contact form
assets/js/i18n.js     EN/FR UI copy dictionary
cv.pdf                Placeholder résumé — replace with the real PDF
tools/build.py        Generator that produced the HTML pages (see below)
```

## Editing content

Project/system data, skills, and education lives in `tools/build.py` as plain
Python data (`PROJECTS`, `SYSTEMS`, `SKILLS`, `EDUCATION`). To change copy:

1. Edit the data (or the HTML templates) in `tools/build.py`.
2. Regenerate the static pages:

   ```bash
   python tools/build.py
   ```

3. Commit the regenerated `.html` files along with your `build.py` change.

If you only need to tweak one page's wording, editing the generated `.html`
file directly also works — just know it'll be overwritten next time someone
runs the generator.

## Known placeholders to replace

This content was reconstructed from an earlier Base44 draft that still had
template placeholders in it. Before treating the site as final, replace:

- Per-project GitHub / itch.io / demo links in `tools/build.py` (`PROJECTS[*]["links"]`)
  — currently point at bare `github.com` / `itch.io` / `demo.io`. Blocked on the
  real itch.io page being published.
- The `PROJECTS` list itself is still the fictional Base44 sample content
  (Echoes of the Rift, Nexus Tower Defense, ...) — swap in the real shipped
  projects (Kissoro, La légende de Mulu, MiniCup, ...) once screenshots/links
  are ready.
- Project cover art is CSS-only placeholders — swap in real screenshots/GIFs
  when available.

`cv.pdf` is now the real résumé (replace the same path whenever it's updated —
no code changes needed). Education in `tools/build.py` (`EDUCATION`) reflects
the real degrees.

GitHub and LinkedIn links in the footer/contact page already point at the
real profiles (`github.com/romainpitot`, `linkedin.com/in/romain-pitot`).

## Deployment (GitHub Actions → GitHub Pages)

One-time setup on GitHub: **Settings → Pages → Build and deployment → Source
→ GitHub Actions**. After that, every push to `main` runs
`.github/workflows/deploy.yml`, which uploads the repo as a Pages artifact
and deploys it — no build step needed since the site is already static HTML.
