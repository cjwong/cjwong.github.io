# Repository Guidelines

## Project Structure & Module Organization
- `content/` holds Markdown sources for the home, projects, teaching, and data/code pages.
- `data/` contains `site.yaml` metadata and `publications.yaml` for citation lists.
- `templates/` contains Jinja2 HTML templates; `build.py` generates HTML in the repo root.
- `assets/` stores the site CSS and JavaScript.
- `Images/`, `Papers/`, and `Resources/` store site assets and documents (case-sensitive paths).
- `WongCV.pdf` is the primary CV link; `CNAME` configures the custom domain for GitHub Pages.

## Build, Test, and Development Commands
Generate the site and preview it locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py
python3 -m http.server
```

Then open `http://localhost:8000/` to verify navigation, styling, and asset links.

## Coding Style & Naming Conventions
- Use 2-space indentation in HTML templates, YAML, CSS, and JavaScript.
- Keep Markdown content concise and structured with headings and lists.
- Prefer relative links (e.g., `href="Papers/..."`) and keep filenames lowercase unless matching existing directory names (`Images/`, `Papers/`, `Resources/`).
- Run `build.py` after content edits to regenerate the HTML files in the root.

## Testing Guidelines
- No automated tests are configured.
- Manually check each page in a browser, confirming:
  - Navigation highlights and the mobile menu toggle work.
  - Images and PDFs load without 404s.
  - External links and mailto links work as intended.

## Commit & Pull Request Guidelines
- Recent commits use short, sentence-case summaries like “Update CV” or “Fix typo in CV.” Follow that concise style.
- PRs should describe the pages/assets changed and include screenshots for any visible layout or styling updates.
