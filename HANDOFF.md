# Handoff Summary

## Overview

This is Cara Wong's academic website (carawong.org), a static site built with a custom Python generator. Previous sessions converted the publications page from manual YAML to BibTeX-based generation. **This session focused on launching the site at carawong.org via GitHub Pages.**

---

## Key Decisions Made

### From Previous Sessions (Publications)

1. **BibTeX as source of truth**: Publications are generated from `data/wong-vita.bib` instead of `data/publications.yaml`. This allows maintaining a single bibliography file (managed in BibDesk) for both the website and academic documents.

2. **Author order preservation**: The BibTeX author order is preserved exactly as written, reflecting actual authorship order on papers.

3. **Bold author highlighting**: "Cara Wong" and "Cara J. Wong" are automatically wrapped in `<strong>` tags.

4. **Section categorization via keywords**: Publications are grouped based on the BibTeX `keywords` field:
   - `book` keyword OR `@book` entry type → "Books and Monographs"
   - `peer_reviewed` + `@article` → "Journal Articles"
   - `peer_reviewed` + `@incollection` → "Book Chapters"
   - `other_publication` OR `dataset` → "Other Publications"

5. **PDF linking via mapping**: PDFs in `Papers/` are linked via `PDF_MAPPING` dictionary in `build.py`.

6. **DOI handling**: DOIs are automatically extracted and linked (handles both bare DOIs and full URLs).

### This Session (Deployment)

7. **GitHub Pages serves from `main` branch directly**: GitHub Pages is configured to serve from `main`. The GitHub Actions workflow regenerates HTML when source files change and commits back to `main`.

8. **DNS already configured on Dreamhost**: The domain carawong.org already points to GitHub Pages IPs. No DNS changes needed.

9. **Keep `master` branch as backup**: The old site remains on `master` for reference; can be deleted later.

10. **Workflow only triggers on source changes**: The GitHub Action only runs when files in `content/`, `data/`, `templates/`, `build.py`, or `requirements.txt` change—not on every push.

---

## Files Changed and Why

### Previous Sessions

| File | Changes |
|------|---------|
| `build.py` | Added BibTeX parsing, `PDF_MAPPING` dictionary, author formatting functions |
| `templates/publications.html` | Added `\|safe` filter to render `<strong>` tags |
| `assets/site.css` | Added `.publications { padding-top: 16px; }` |
| `requirements.txt` | Added `bibtexparser==1.4.3` |
| `README.md` | Updated with build instructions |

### This Session

| File | Changes |
|------|---------|
| `.github/workflows/build.yml` | Updated to commit regenerated HTML back to `main` instead of deploying to `gh-pages`. Added `paths` filter so workflow only triggers on source file changes. |
| `HANDOFF.md` | Updated with deployment status and new architecture |

---

## Current Blockers / Open Questions

### ✅ RESOLVED: Site is Live

The site is now live at https://carawong.org. GitHub Pages is configured to serve from the `main` branch.

### Open Questions

1. **Unmapped PDFs**: Several PDFs in `Papers/` don't have matches to publications:
   - `MapsMPSA.pdf`, `MeasurementCanada.pdf`, `MultiracialIdentities.pdf`
   - `NatlIdentity.pdf`, `Objective.pdf`, `Pictures.pdf`
   - These may be conference papers or working papers not currently displayed.

2. **Conference papers not displayed**: The BibTeX contains `@misc` entries with `keywords = {conference}` or `keywords = {invited}` that are not shown. New sections could be added if desired.

3. **`data/publications.yaml` is unused**: The old YAML file still exists but is no longer read. Could be deleted.

---

## Important Context to Preserve

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  Edit source files in content/, data/, templates/, or build.py     │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Push to main branch                                                │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GitHub Action triggers (only for content/data/template changes)   │
│  → Runs build.py                                                    │
│  → Commits regenerated HTML back to main                            │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│  GitHub Pages serves from main branch → carawong.org               │
└─────────────────────────────────────────────────────────────────────┘
```

### Branch Structure

| Branch | Purpose |
|--------|---------|
| `main` | Active development; source AND generated HTML; served by GitHub Pages |
| `gh-pages` | Legacy (no longer used); can be deleted |
| `master` | Old website (backup); can be deleted after launch verified |
| `oldwebsite` | Another backup of old site |

### DNS Configuration (Already Done on Dreamhost)

- `carawong.org` → A records pointing to GitHub Pages IPs (185.199.x.x)
- `www.carawong.org` → CNAME to `cjwong.github.io`

### GitHub Repository

- **Repo**: https://github.com/cjwong/cjwong.github.io
- **Owner**: `cjwong` (Cara Wong)
- **HTTPS Certificate**: Valid until March 2026
- **Domain verification**: Already verified

### BibTeX Keywords

The `keywords` field in each BibTeX entry determines section placement:
- `book` → Books section
- `peer_reviewed` → Journal Articles or Book Chapters (depends on entry type)
- `other_publication` or `dataset` → Other Publications

### PDF Mapping

The `PDF_MAPPING` in `build.py` currently includes 22 entries mapping BibTeX entry IDs to PDF file paths in `Papers/` or `Resources/`.

---

## What's Done

- [x] Publications page generates from BibTeX file
- [x] Author order matches BibTeX exactly
- [x] "Cara Wong" / "Cara J. Wong" displayed in bold
- [x] DOI links automatically extracted
- [x] PDF links mapped for 22 publications
- [x] Edited books show "Editors" label
- [x] GitHub Actions workflow configured to build and commit to `main`
- [x] CNAME file set to `carawong.org`
- [x] DNS configured on Dreamhost (verified working)
- [x] HTTPS certificate approved
- [x] **Site is live at https://carawong.org**
- [x] GitHub Pages configured to serve from `main` branch

---

## What Remains

### Future Improvements

- [ ] Consider auto-detecting PDFs by matching filename to BibTeX key
- [ ] Add sections for invited talks or conference presentations if desired
- [ ] Delete or archive the unused `data/publications.yaml`
- [ ] Map remaining PDFs if their corresponding publications are identified
- [ ] Consider adding more link types (e.g., "Publisher" links for books)
- [ ] Clean up unused branches (`master`, `oldwebsite`, `gh-pages`)

---

## How to Add New Publications

1. Add the entry to `data/wong-vita.bib` with appropriate `keywords` field
2. If there's a PDF, add it to `Papers/` and add a mapping to `PDF_MAPPING` in `build.py`
3. Push to `main` branch; GitHub Actions will rebuild and deploy automatically

---

## Build Commands

```bash
# Setup (first time)
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Build
python build.py

# Preview locally
python3 -m http.server
# Visit http://localhost:8000/
```

---

## Site Verification (Completed)

The site is live and verified:
- ✅ https://carawong.org - serving new site
- ✅ https://www.carawong.org - works
- ✅ HTTPS certificate valid
- ✅ All pages accessible
