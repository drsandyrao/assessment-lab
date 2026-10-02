# Assessment Lab

Assessment Lab is a dependency-free, mobile-first educational website for SK651: Advanced Social Work Practice with Individuals.

## Preview locally

From the repository root, run:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000/>. The site is also usable by opening `index.html` directly.

## Validate links

```sh
python3 scripts/check_links.py
```

The checker scans every HTML file and reports missing local page, asset, and fragment targets. It requires only Python 3.

## Publish with GitHub Pages

No build step or deployment workflow is required. In the GitHub repository:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select the `main` branch and `/ (root)` folder, then save.

GitHub will publish the site at `https://USERNAME.github.io/assessment-lab/`. All links are relative, so repository-path hosting works without configuration.

## Structure

- `index.html` — student homepage
- `lab/` — orientation, round selection, and role views
- `library/` — library landing page and reusable resource-page template
- `reveal/` — discreet whole-class reveal page
- `instructor/` — discreet facilitation guide
- `assets/styles.css` — shared responsive, accessible, and print styles
- `scripts/check_links.py` — dependency-free internal-link validation

Substantive client cases and assessment approaches are intentionally left as clearly labelled placeholders.
