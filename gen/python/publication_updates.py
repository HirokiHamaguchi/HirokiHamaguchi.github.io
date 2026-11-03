"""Promote unambiguously matched ORCID works using Crossref publication metadata."""

import json
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ORCID = "0009-0005-7348-1356"
SOURCE = Path(__file__).resolve().parents[1] / "json/publications.json"


def normalize(value):
    return "".join(
        c for c in unicodedata.normalize("NFKC", value).casefold() if c.isalnum()
    )


def fetch(url):
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "HirokiHamaguchi-homepage/1.0 (https://hirokihamaguchi.github.io/)"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def identifiers(work, kind):
    return {
        entry["external-id-value"].strip()
        for entry in (work.get("external-ids") or {}).get("external-id", [])
        if entry.get("external-id-type") == kind
        and entry.get("external-id-relationship") in ("self", "version-of")
    }


def publication_date(work):
    # Do not invent a day for records containing only a publication year/month.
    dates = []
    for key in ("published-online", "published-print", "published"):
        for parts in work.get(key, {}).get("date-parts", []):
            if len(parts) == 3:
                dates.append(date(*parts).isoformat())
    return min(dates) if dates else None


def find_update(item, groups, cache):
    candidates = set()
    arxiv = item["paper_url"].removeprefix("https://arxiv.org/abs/")
    for group in groups:
        summaries = group.get("work-summary", [])
        same_title = any(
            normalize(work["title"]["title"]["value"]) == normalize(item["title"])
            for work in summaries
        )
        same_arxiv = any(arxiv in identifiers(work, "arxiv") for work in summaries)
        if same_title or same_arxiv:
            for work in summaries:
                if work.get("type") == "journal-article":
                    candidates.update(identifiers(work, "doi"))

    matches = []
    for doi in sorted(candidates):
        doi = doi.removeprefix("https://doi.org/").removeprefix("http://dx.doi.org/").lower()
        if doi not in cache:
            # Official APIs: https://info.orcid.org/documentation/api-tutorials/api-tutorial-read-data-on-a-record/
            # https://www.crossref.org/documentation/retrieve-metadata/rest-api/
            cache[doi] = fetch(f"https://api.crossref.org/works/{quote(doi, safe='')}")["message"]
        work = cache[doi]
        authors = {normalize(author) for author in item["authors"]}
        names = {
            normalize(f"{author.get('given', '')} {author.get('family', '')}")
            for author in work.get("author", [])
        }
        title_matches = any(
            normalize(title) == normalize(item["title"]) for title in work.get("title", [])
        )
        if (work.get("type") != "journal-article" or not title_matches or names != authors
                or not work.get("container-title") or not publication_date(work)):
            print(f"Review required: {item['title']} -> https://doi.org/{doi}")
            continue
        matches.append((doi, work))

    # Multiple editions/DOIs require a manual choice, never an arbitrary winner.
    matches = {doi: work for doi, work in matches}
    if len(matches) != 1:
        if matches:
            print(f"Ambiguous publication: {item['title']}: {', '.join(matches)}")
        return None
    doi, work = next(iter(matches.items()))
    return {
        "category": "manuscript",
        "venue": work["container-title"][0],
        "paper_url": f"https://doi.org/{doi}",
        "pub_date": publication_date(work),
    }


def update_publications():
    items = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not any(item["category"] == "preprint" for item in items):
        return
    groups = fetch(f"https://pub.orcid.org/v3.0/{ORCID}/works")["group"]
    cache = {}
    changed = False
    for item in items:
        if item["category"] != "preprint":
            continue
        update = find_update(item, groups, cache)
        if update is None:
            print(f"Unchanged: {item['title']}")
            continue
        item.update(update)
        changed = True
        print(f"Published: {item['title']} -> {item['venue']} ({item['paper_url']})")
    # Complete all remote checks before writing, so API failures leave sources intact.
    if changed:
        temporary = SOURCE.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(SOURCE)
