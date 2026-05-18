"""
Fetch recent energy storage papers from arXiv API.
Outputs to src/data/papers-feed.json and individual paper .md files.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    ensure_dirs, today_str, cached_fetch, read_json, write_json,
    write_markdown, SRC_DATA_DIR, SRC_CONTENT_DIR, logger,
)

PAPERS_DIR = SRC_CONTENT_DIR / "papers"

# arXiv API query for energy storage topics
ARXIV_QUERIES = [
    "energy+storage+battery",
    "solid+state+electrolyte",
    "sodium+ion+battery",
    "flow+battery+energy+storage",
    "compressed+air+energy+storage",
]

def fetch_arxiv(query: str, max_results: int = 5) -> list:
    """Fetch papers from arXiv API for a given query."""
    url = (
        f"http://export.arxiv.org/api/query"
        f"?search_query=all:{query}"
        f"&start=0"
        f"&max_results={max_results}"
        f"&sortBy=submittedDate"
        f"&sortOrder=descending"
    )
    body = cached_fetch(url, ttl_hours=12)
    if not body:
        return []
    return _parse_arxiv_response(body)


def _parse_arxiv_response(xml_body: str) -> list:
    """Parse arXiv Atom XML response. Simple approach using string splitting."""
    import re

    papers = []
    # Split by <entry> tags
    entries = re.split(r'<entry>|</entry>', xml_body)

    for entry in entries:
        if '<title>' not in entry:
            continue

        def extract(tag: str, text: str) -> str:
            m = re.search(f'<{tag}.*?>(.*?)</{tag}>', text, re.DOTALL)
            return m.group(1).strip() if m else ""

        def extract_name(tag: str, text: str) -> str:
            m = re.search(f'<{tag}>.*?<name>(.*?)</name>', text, re.DOTALL)
            return m.group(1).strip() if m else ""

        title = extract('title', entry)
        arxiv_id_full = extract('id', entry)
        arxiv_id = arxiv_id_full.split('/abs/')[-1] if '/abs/' in arxiv_id_full else arxiv_id_full
        abstract = extract('summary', entry)
        published = extract('published', entry)

        # Get all authors
        authors = []
        for m in re.finditer(r'<author>.*?<name>(.*?)</name>.*?</author>', entry, re.DOTALL):
            authors.append(m.group(1).strip())

        if title and abstract:
            papers.append({
                "title": title,
                "authors": authors[:8],
                "journal": "arXiv",
                "publishDate": published[:10] if published else "",
                "abstract": abstract[:500],
                "keywords": _extract_keywords(title + " " + abstract),
                "arxivId": arxiv_id,
                "doi": "",
                "relevance": "medium",
            })

    return papers


def _extract_keywords(text: str) -> list:
    """Extract simple keywords from text based on energy storage vocabulary."""
    keywords = [
        "solid-state battery", "sodium-ion", "lithium metal", "electrolyte",
        "cathode", "anode", "cycling stability", "energy density",
        "flow battery", "compressed air", "thermal runaway", "BMS",
        "machine learning", "screening", "interface", "interphase",
        "dendrite", "LCOE", "liquid metal", "all-solid-state",
    ]
    found = []
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            found.append(kw)
    return found[:6]


def main():
    ensure_dirs()
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)

    all_papers = []

    for query in ARXIV_QUERIES[:2]:  # Limit to 2 queries to be respectful
        logger.info(f"Fetching arXiv: {query}")
        papers = fetch_arxiv(query, max_results=3)
        all_papers.extend(papers)

    # Deduplicate by title
    seen = set()
    unique_papers = []
    for p in all_papers:
        if p["title"] not in seen:
            seen.add(p["title"])
            unique_papers.append(p)

    # Sort by date
    unique_papers.sort(key=lambda p: p["publishDate"], reverse=True)
    unique_papers = unique_papers[:8]

    # Write feed JSON
    feed = {
        "lastUpdated": today_str(),
        "papers": unique_papers,
        "totalCount": len(unique_papers),
    }
    write_json(SRC_DATA_DIR / "papers-feed.json", feed)

    # Write individual paper MD files
    for i, paper in enumerate(unique_papers):
        date_str = paper["publishDate"] or today_str()
        authors_yaml = "\n  - ".join(paper["authors"])
        keywords_yaml = "\n  - ".join(paper.get("keywords", []))

        md_content = f"""---
title: "{paper['title']}"
authors:
  - {authors_yaml}
journal: "{paper['journal']}"
publishDate: {date_str}
abstract: "{paper['abstract'][:300]}"
keywords:
  - {keywords_yaml or 'energy storage'}
doi: "{paper.get('doi', '')}"
arxivId: "{paper.get('arxivId', '')}"
relevance: "{paper.get('relevance', 'medium')}"
---

## Abstract

{paper['abstract']}

## Keywords

{', '.join(paper.get('keywords', ['energy storage']))}

---
*Source: {paper['journal']} · Fetched {today_str()}*
"""
        slug = f"paper-{date_str}-{i+1:03d}"
        write_markdown(PAPERS_DIR / f"{slug}.md", md_content)

    logger.info(f"Fetched {len(unique_papers)} unique papers")


if __name__ == "__main__":
    main()
