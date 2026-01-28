# Handoff Summary

## Overview

This session focused on improving the publications page (`published.html`) of Cara Wong's academic website. The main achievement was switching from a manually-curated YAML file to automatically generating publications from a BibTeX file (`data/wong-vita.bib`).

## Key Decisions Made

1. **BibTeX as source of truth**: Publications are now generated from `data/wong-vita.bib` instead of `data/publications.yaml`. This allows the user to maintain a single bibliography file (likely managed in BibDesk) that serves both the website and academic documents.

2. **Author order preservation**: The BibTeX author order is preserved exactly as written, rather than always listing Cara Wong first. This reflects actual authorship order on papers.

3. **Bold author highlighting**: "Cara Wong" and "Cara J. Wong" are automatically wrapped in `<strong>` tags for visual emphasis.

4. **Section categorization via keywords**: Publications are grouped into sections based on the BibTeX `keywords` field:
   - `book` keyword OR `@book` entry type → "Books and Monographs"
   - `peer_reviewed` + `@article` → "Journal Articles"
   - `peer_reviewed` + `@incollection` → "Book Chapters"
   - `other_publication` OR `dataset` → "Other Publications"

5. **Edited books display**: For books with editors instead of authors (like the Handbook), the display shows "Name, Name, Name, Editors," before the year.

6. **PDF linking via mapping**: PDFs in `Papers/` are linked to publications via a `PDF_MAPPING` dictionary in `build.py`. This requires manual mapping but allows flexible file naming.

7. **DOI handling**: DOIs are automatically extracted and linked. The code handles both bare DOIs (`10.1234/...`) and full URLs (`https://doi.org/10.1234/...`).

## Files Changed and Why

### `build.py`
- Added `bibtexparser` import and BibTeX parsing functions
- Added `PDF_MAPPING` dictionary mapping BibTeX entry IDs to PDF file paths
- Added functions: `parse_bibtex_name()`, `format_authors()`, `format_editors()`, `clean_bibtex_text()`, `format_venue()`, `get_links()`, `categorize_entry()`, `load_publications_from_bibtex()`
- Changed `build_site()` to call `load_publications_from_bibtex()` instead of loading YAML
- User also modified the teaching page intro to be empty (`"intro": ""`)

### `templates/publications.html`
- Changed `{{ item.authors }}` to `{{ item.authors|safe }}` to render the `<strong>` HTML tags for bolding Cara Wong's name

### `assets/site.css`
- Added `.publications { padding-top: 16px; }` to reduce vertical space between the page header and the first section

### `requirements.txt`
- Added `bibtexparser==1.4.3` dependency

### `README.md`
- Updated to include build instructions and documentation about how the publications page works, including the keyword-to-section mapping

## Current PDF Mapping

The `PDF_MAPPING` in `build.py` currently includes 22 entries:

```python
PDF_MAPPING = {
    # Books
    "wong2010boundaries": "Resources/Boundaries-Appendix.pdf",
    "cain2000ethnic": "Papers/ppic.pdf",
    # Journal Articles
    "wong2025twopath": "Papers/wong2025maps.pdf",
    "wong2025quirks": "Papers/guay-et-al-2025-quirks-of-cognition-explain-why-we-dramatically-overestimate-the-size-of-minority-groups.pdf",
    "hayes2023officials": "Papers/hayes2023officials.pdf",
    "wongetal2020": "Papers/PSRMWongEtAl.pdf",
    "wong2020citizenship": "Papers/wong2020citizenship.pdf",
    "citrin2017bilingual": "Papers/BilingualEd2017.pdf",
    "hutchings2014racism": "Papers/HutchingsWong2014Page1.pdf",
    "wong2014integration": "Papers/Wong2014AndersonComments.pdf",
    "wong2012jop": "Papers/wong2012jop.pdf",
    "wong2007little": "Papers/WongPOQ.pdf",
    "wong2007fights": "Papers/WongDuBoisReview.pdf",
    "campbell2006racial": "Papers/PolBehavior.pdf",
    "wong2005two": "Papers/PolPsych.pdf",
    "citrin2001multiculturalism": "Papers/bjps.pdf",
    "citrin1997public": "Papers/jop.pdf",
    # Book Chapters
    "hutchings2011explaining": "Papers/Explaining2011.pdf",
    "wong2009belongs": "Papers/NationsOfImmigrants2009.pdf",
    "wong2006jus": "Papers/JusMeritum.pdf",
    "citrin2001meaning": "Papers/citrin2001meaning.pdf",
    # Other Publications
    "wong1998pilot": "Papers/nes008587.pdf",
}
```

## Current Blockers / Open Questions

1. **Unmapped PDFs**: Several PDFs in `Papers/` don't have clear matches to publications:
   - `MapsMPSA.pdf`
   - `MeasurementCanada.pdf`
   - `MultiracialIdentities.pdf`
   - `NatlIdentity.pdf`
   - `Objective.pdf`
   - `Pictures.pdf`

   These may be conference papers or working papers not currently displayed on the publications page.

2. **Conference papers not displayed**: The BibTeX contains many `@misc` entries with `keywords = {conference}` or `keywords = {invited}` that are not shown on the publications page. If desired, new sections could be added for these.

3. **`data/publications.yaml` is now unused**: The old YAML file still exists but is no longer read by `build.py`. It could be deleted or kept for reference.

## Important Context to Preserve

1. **BibTeX keywords are critical**: The `keywords` field in each BibTeX entry determines whether and where it appears. Valid keywords for publication display:
   - `book` - Books section
   - `peer_reviewed` - Journal Articles or Book Chapters (depends on entry type)
   - `other_publication` - Other Publications
   - `dataset` - Other Publications

2. **Author name formats**: BibTeX supports both "First Last" and "Last, First" formats. The code handles both and converts to "First Last" for display.

3. **DOI field flexibility**: The `doi` field can contain just the DOI (`10.1234/xyz`) or the full URL (`https://doi.org/10.1234/xyz`). Both work.

4. **Jinja2 autoescape**: The template uses `|safe` filter for authors because we inject `<strong>` tags. Be careful if adding user-controlled content.

## What's Done

- [x] Publications page generates from BibTeX file
- [x] Author order matches BibTeX exactly
- [x] "Cara Wong" / "Cara J. Wong" displayed in bold
- [x] DOI links automatically extracted
- [x] PDF links mapped for 22 publications
- [x] Edited books show "Editors" label
- [x] Reduced vertical spacing on publications page
- [x] README updated with build instructions and publications documentation
- [x] DOI handling works with both bare DOIs and full URLs

## What Remains / Future Improvements

- [ ] Consider auto-detecting PDFs by matching filename to BibTeX key (e.g., `Papers/{entry_id}.pdf`)
- [ ] Add sections for invited talks or conference presentations if desired
- [ ] Delete or archive the unused `data/publications.yaml`
- [ ] Map remaining PDFs if their corresponding publications are identified
- [ ] Consider adding more link types (e.g., "Publisher" links for books)

## How to Add New Publications

1. Add the entry to `data/wong-vita.bib` with appropriate `keywords` field
2. If there's a PDF, add it to `Papers/` and add a mapping to `PDF_MAPPING` in `build.py`
3. Run `python build.py` to regenerate the site

## Build Commands

```bash
# With uv (recommended)
source .venv/bin/activate
python build.py

# Preview locally
python3 -m http.server
# Visit http://localhost:8000/
```
