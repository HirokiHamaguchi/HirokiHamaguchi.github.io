"""Check CV awards against researchmap without changing any files."""

import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
PROFILE = "hirokihamaguchi0331"
API = f"https://api.researchmap.jp/{PROFILE}/awards"


def fetch_awards():
    items = []
    while True:
        with urlopen(f"{API}?limit=1000&start={len(items) + 1}", timeout=30) as response:
            page = json.load(response)
        batch = page["items"]
        items.extend(batch)
        if len(items) >= page["total_items"]:
            break
        if not batch:
            raise ValueError("Incomplete researchmap response")
    if not items:
        raise ValueError("No awards returned")
    return sorted(items, key=lambda item: item["award_date"], reverse=True)


def normalize(text):
    return "".join(character for character in unicodedata.normalize("NFKC", text).casefold() if character.isalnum())


def similarity(left, right):
    a, b = normalize(left), normalize(right)
    if not a or not b:
        return 0.0
    if min(len(a), len(b)) >= 4 and (a in b or b in a):
        return 1.0
    score = SequenceMatcher(None, a, b).ratio()
    # English titles may reorder words or add conference details.
    words_a = set(re.findall(r"[a-z]+", left.casefold()))
    words_b = set(re.findall(r"[a-z]+", right.casefold()))
    if words_a and words_b:
        score = max(score, 2 * len(words_a & words_b) / (len(words_a) + len(words_b)))
    return score


def cv_entries(text, heading):
    match = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"Missing CV section: {heading}")
    entries = []
    for line in match[1].splitlines():
        if not line.startswith("* "):
            continue
        fields = line[2:].split(r"\|")
        date = re.match(r"\d{4}(?:-\d{2})?(?:-\d{2})?", fields[0].strip())
        if not date or len(fields) < 3:
            raise ValueError(f"Cannot parse CV award: {line}")
        entries.append((date.group(), fields[2].strip(), line))
    return entries


def check_section(items, entries, language):
    candidates = []
    for i, item in enumerate(items):
        date = item["award_date"]
        title = item["award_name"].get(language) or item["award_name"].get("ja") or item["award_name"].get("en", "")
        for j, (cv_date, cv_title, _) in enumerate(entries):
            # Compare only the precision shared by both dates (usually month).
            precision = min(len(date), len(cv_date))
            if date[:precision] == cv_date[:precision]:
                score = similarity(title, cv_title)
                if score >= 0.6:
                    candidates.append((score, i, j))
    matched_items, matched_entries = set(), set()
    for _, i, j in sorted(candidates, reverse=True):
        if i not in matched_items and j not in matched_entries:
            matched_items.add(i)
            matched_entries.add(j)
    warnings = []
    for i, item in enumerate(items):
        if i not in matched_items:
            warnings.append(f"[{language}] No matching CV award: {item['award_date']} | {item['award_name']} (researchmap ID {item['rm:id']})")
    for j, (_, _, line) in enumerate(entries):
        if j not in matched_entries:
            warnings.append(f"[{language}] No matching researchmap award: {line}")
    return warnings


def awards():
    items = fetch_awards()
    text = (ROOT / "_pages/cv.md").read_text(encoding="utf-8")
    warnings = []
    for heading, language in [("Awards", "en"), ("Awards (日本語)", "ja")]:
        warnings.extend(check_section(items, cv_entries(text, heading), language))
    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}")
    else:
        print(f"CV awards roughly match researchmap ({len(items)} awards, English and Japanese).")
    return warnings


if __name__ == "__main__":
    awards()
