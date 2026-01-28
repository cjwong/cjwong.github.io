# Cara Wong Academic Site

This repository builds a static website from Markdown content, YAML data, BibTeX bibliography, and Jinja2 templates.

## Local build

### Option 1: uv (recommended)
Install uv (macOS): `brew install uv`
Install uv (macOS/Linux): `curl -LsSf https://astral.sh/uv/install.sh | sh`

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
python build.py
```

### Option 2: venv + pip
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py
```

### Preview locally
Open `index.html` in a browser or start a local server:
```bash
python3 -m http.server
```
Then visit http://localhost:8000/

## Structure
- `content/`: Markdown for the home, projects, teaching, and data/code pages.
- `data/`: Site metadata (`site.yaml`) and bibliography (`wong-vita.bib`).
- `templates/`: HTML templates used by `build.py`.
- `assets/`: CSS and JavaScript for the frontend.

## Publications

The publications page (`published.html`) is generated from `data/wong-vita.bib`. The BibTeX `keywords` field determines which section each entry appears in:

| Keyword | Section |
|---------|---------|
| `book` | Books and Monographs |
| `peer_reviewed` (with `@article`) | Journal Articles |
| `peer_reviewed` (with `@incollection`) | Book Chapters |
| `other_publication` | Other Publications |
| `dataset` | Other Publications |

Author names appear in the order specified in the BibTeX file, and "Cara Wong" is automatically bolded.

To add links (PDFs, publisher pages), use the `doi` field or BibDesk's `bdsk-url-1`, `bdsk-url-2` fields in the BibTeX entry.

## Getting help from Claude Code

When starting a new Claude Code session for this project:

1. Ask Claude to read `HANDOFF.md` first for context on recent changes, decisions, and open questions
2. Claude will automatically read `CLAUDE.md` for build commands and code style guidelines
3. After making significant changes, run `/handoff` to update `HANDOFF.md` for future sessions

Example prompt to start a session:
```
Please read HANDOFF.md to get context on this project, then help me [your task here].
```
