# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Setup and build (uv recommended)
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt
python build.py

# Alternative with pip
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build.py

# Local preview
python3 -m http.server  # http://localhost:8000/
```

Run `python build.py` after any content or template changes to regenerate HTML.

## Architecture

This is a static academic website built with a custom Python generator. The build process:
1. Reads Markdown from `content/` and YAML from `data/`
2. Renders through Jinja2 templates in `templates/`
3. Outputs HTML files to the repository root

**Key files:**
- `build.py` - Main generator script
- `data/site.yaml` - Site metadata, navigation, hero content
- `data/publications.yaml` - Publication list with citations and links

**Templates:**
- `base.html` - Layout wrapper with nav/footer
- `index.html` - Home page with hero and card grid
- `page.html` - Generic page (used by papers, teaching, datacode)
- `publications.html` - Publications listing

**Content mapping:**
- `content/index.md` → `index.html`
- `content/projects.md` → `papers.html`
- `content/teaching.md` → `teaching.html`
- `content/data-code.md` → `datacode.html`
- `data/publications.yaml` → `published.html`

## Code Style

- 2-space indentation in HTML, YAML, CSS, JavaScript
- Use relative links for assets (e.g., `href="Papers/..."`)
- Keep existing directory case: `Images/`, `Papers/`, `Resources/`
- Short, sentence-case commit messages (e.g., "Update CV")

## CI/CD

Push to `main` triggers GitHub Actions (`.github/workflows/build.yml`) which runs `build.py` and deploys to `gh-pages` branch. Site served at carawong.org via CNAME.
