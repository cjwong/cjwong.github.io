#!/usr/bin/env python3
"""Build the static site from markdown, YAML data, and HTML templates."""

from __future__ import annotations

import datetime
import re
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape


BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"

# Mapping of BibTeX entry IDs to PDF filenames in Papers/ or Resources/
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


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def parse_bibtex_name(name: str) -> str:
    """Convert a BibTeX name to display format, preserving the form."""
    name = name.strip()
    if "," in name:
        # "Last, First" or "Last, First Middle" format
        parts = [p.strip() for p in name.split(",", 1)]
        if len(parts) == 2:
            return f"{parts[1]} {parts[0]}"
    return name


def format_authors(author_string: str) -> str:
    """Format BibTeX author string, preserving order and bolding Cara Wong."""
    if not author_string:
        return ""
    # Split on " and " (BibTeX convention)
    authors = [a.strip() for a in author_string.split(" and ")]
    formatted = []
    for author in authors:
        name = parse_bibtex_name(author)
        # Bold Cara Wong variations
        if re.match(r"^Cara\s+(J\.\s+)?Wong$", name, re.IGNORECASE):
            name = f"<strong>{name}</strong>"
        formatted.append(name)
    return ", ".join(formatted)


def format_editors(editor_string: str) -> str:
    """Format BibTeX editor string, preserving order and bolding Cara Wong."""
    if not editor_string:
        return ""
    editors = [e.strip() for e in editor_string.split(" and ")]
    formatted = []
    for editor in editors:
        name = parse_bibtex_name(editor)
        if re.match(r"^Cara\s+(J\.\s+)?Wong$", name, re.IGNORECASE):
            name = f"<strong>{name}</strong>"
        formatted.append(name)
    return ", ".join(formatted)


def clean_bibtex_text(text: str) -> str:
    """Clean up BibTeX formatting artifacts."""
    if not text:
        return ""
    # Remove LaTeX braces used for capitalization preservation
    text = re.sub(r"\{([^}]+)\}", r"\1", text)
    # Convert LaTeX quotes
    text = text.replace("``", '"').replace("''", '"')
    text = text.replace("`", "'")
    # Handle common LaTeX special chars
    text = text.replace("\\&", "&")
    text = text.replace("~", " ")
    text = text.replace("\\textsuperscript", "")
    text = text.replace("\\emph", "")
    return text.strip()


def format_venue(entry: dict) -> str:
    """Format the publication venue from BibTeX entry."""
    entry_type = entry.get("ENTRYTYPE", "")

    if entry_type == "article":
        journal = clean_bibtex_text(entry.get("journal", ""))
        volume = entry.get("volume", "")
        number = entry.get("number", "")
        pages = entry.get("pages", "").replace("--", "-")

        venue = journal
        if volume:
            venue += f" {volume}"
            if number:
                venue += f"({number})"
        if pages:
            venue += f": {pages}"
        return venue

    elif entry_type == "book":
        publisher = entry.get("publisher", "")
        address = entry.get("address", "")
        if address and publisher:
            return f"{publisher}"
        return publisher

    elif entry_type == "incollection":
        booktitle = clean_bibtex_text(entry.get("booktitle", ""))
        editor = entry.get("editor", "")
        publisher = entry.get("publisher", "")
        pages = entry.get("pages", "").replace("--", "-")

        venue = f"In {booktitle}"
        if editor:
            editors_formatted = format_editors(editor)
            venue += f". Edited by {editors_formatted}"
        if publisher:
            venue += f". {publisher}"
        if pages:
            venue += f", pp. {pages}"
        return venue

    elif entry_type == "techreport":
        institution = entry.get("institution", "")
        return institution

    return ""


def get_links(entry: dict) -> list[dict]:
    """Extract links from BibTeX entry."""
    links = []

    # Check for PDF in our mapping
    entry_id = entry.get("ID", "")
    if entry_id in PDF_MAPPING:
        links.append({
            "label": "PDF",
            "url": PDF_MAPPING[entry_id]
        })

    if entry.get("doi"):
        doi = entry["doi"]
        # Handle DOIs that already include the URL prefix
        if doi.startswith("https://doi.org/"):
            doi_url = doi
        elif doi.startswith("http://doi.org/"):
            doi_url = doi.replace("http://", "https://")
        else:
            doi_url = f"https://doi.org/{doi}"
        links.append({
            "label": "DOI",
            "url": doi_url
        })

    # Check for bdsk-url fields (BibDesk URLs)
    for i in range(1, 5):
        url_key = f"bdsk-url-{i}"
        if entry.get(url_key):
            url = entry[url_key]
            if "doi.org" not in url:  # Don't duplicate DOI
                links.append({
                    "label": "Link",
                    "url": url
                })

    if entry.get("url"):
        url = entry["url"]
        if not any(link["url"] == url for link in links):
            links.append({
                "label": "Link",
                "url": url
            })

    return links


def categorize_entry(entry: dict) -> str | None:
    """Determine which section a BibTeX entry belongs to."""
    entry_type = entry.get("ENTRYTYPE", "")
    keywords = entry.get("keywords", "").lower()

    # Books (authored or edited)
    if entry_type == "book":
        return "Books and Monographs"

    # Journal articles
    if entry_type == "article" and "peer_reviewed" in keywords:
        return "Journal Articles"

    # Book chapters
    if entry_type == "incollection" and "peer_reviewed" in keywords:
        return "Book Chapters"

    # Other publications
    if "other_publication" in keywords:
        return "Other Publications"

    # Tech reports that are other publications
    if entry_type == "techreport" and "other_publication" in keywords:
        return "Other Publications"

    # Articles marked as other publication
    if entry_type == "article" and "other_publication" in keywords:
        return "Other Publications"

    # Datasets
    if "dataset" in keywords:
        return "Other Publications"

    return None


def load_publications_from_bibtex(path: Path) -> dict:
    """Load and parse BibTeX file into publications structure."""
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode

    with open(path, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    # Initialize sections
    sections_order = [
        "Books and Monographs",
        "Journal Articles",
        "Book Chapters",
        "Other Publications",
    ]
    sections_dict = {name: [] for name in sections_order}

    for entry in bib_database.entries:
        section = categorize_entry(entry)
        if section is None:
            continue

        # Handle author vs editor for edited books
        if entry.get("editor") and not entry.get("author"):
            editors = format_editors(entry.get("editor", ""))
            editor_label = "Editor" if " and " not in entry.get("editor", "") else "Editors"
            authors = f"{editors}, {editor_label},"
            note = entry.get("note", "")
        else:
            authors = format_authors(entry.get("author", ""))
            note = entry.get("note", "")

        title = clean_bibtex_text(entry.get("title", ""))
        year = entry.get("year", "")
        venue = format_venue(entry)
        links = get_links(entry)

        item = {
            "authors": authors,
            "year": year,
            "title": title,
            "venue": venue,
            "links": links,
        }
        if note:
            item["note"] = note

        sections_dict[section].append(item)

    # Sort each section by year descending
    for section in sections_dict.values():
        section.sort(key=lambda x: int(x.get("year", 0) or 0), reverse=True)

    # Build final structure
    sections = []
    for name in sections_order:
        if sections_dict[name]:
            sections.append({
                "title": name,
                "items": sections_dict[name]
            })

    return {"sections": sections}


def render_markdown(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    md = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists"])
    return md.convert(text)


def render_template(env: Environment, name: str, context: dict) -> str:
    return env.get_template(name).render(**context)


def wrap_with_base(env: Environment, context: dict, content: str) -> str:
    base = env.get_template("base.html")
    return base.render(**context, content=content)


def write_page(output: str, html: str) -> None:
    (BASE_DIR / output).write_text(html, encoding="utf-8")


def build_site() -> None:
    site = load_yaml(DATA_DIR / "site.yaml")
    publications = load_publications_from_bibtex(DATA_DIR / "wong-vita.bib")
    build_year = datetime.datetime.now().year

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )

    common_context = {
        "site": site,
        "build_year": build_year,
    }

    index_body = render_template(
        env,
        "index.html",
        {
            **common_context,
            "page_body": render_markdown(CONTENT_DIR / "index.md"),
        },
    )
    index_page = wrap_with_base(
        env,
        {
            **common_context,
            "page_title": site.get("site_title", ""),
            "page_description": site.get("description", ""),
            "body_class": "home",
            "current_url": "index.html",
        },
        index_body,
    )
    write_page("index.html", index_page)

    page_definitions = [
        {
            "source": "projects.md",
            "output": "papers.html",
            "title": "Current Projects",
            "kicker": "Current work",
            "intro": "Book projects, works in progress, and related work.",
        },
        {
            "source": "teaching.md",
            "output": "teaching.html",
            "title": "Teaching",
            "kicker": "Courses",
            "intro": "",
        },
        {
            "source": "data-code.md",
            "output": "datacode.html",
            "title": "Data & Code",
            "kicker": "Materials",
            "intro": "Replication materials, project repositories, and data resources.",
        },
    ]

    for page in page_definitions:
        body = render_template(
            env,
            "page.html",
            {
                **common_context,
                "page_title": page["title"],
                "page_kicker": page["kicker"],
                "page_intro": page["intro"],
                "page_body": render_markdown(CONTENT_DIR / page["source"]),
            },
        )
        page_html = wrap_with_base(
            env,
            {
                **common_context,
                "page_title": page["title"],
                "page_description": site.get("description", ""),
                "body_class": "page",
                "current_url": page["output"],
            },
            body,
        )
        write_page(page["output"], page_html)

    publications_body = render_template(
        env,
        "publications.html",
        {
            **common_context,
            "page_title": "Publications",
            "publications": publications,
        },
    )
    publications_page = wrap_with_base(
        env,
        {
            **common_context,
            "page_title": "Publications",
            "page_description": site.get("description", ""),
            "body_class": "page",
            "current_url": "published.html",
        },
        publications_body,
    )
    write_page("published.html", publications_page)


if __name__ == "__main__":
    build_site()
