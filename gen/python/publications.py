import json
import os
import re
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd


def remove_old_preprints(data, directory: Path):
    expected = {
        os.path.basename(f"{item['pub_date']}-{item['url_slug']}.md")
        for item in data
    }
    for item in data:
        if item["category"] != "manuscript":
            continue
        filename = os.path.basename(f"{item['pub_date']}-{item['url_slug']}.md")
        if not (directory / filename).is_file():
            continue
        pattern = re.compile(r"\d{4}-\d{2}-\d{2}-" + re.escape(item["url_slug"]) + r"\.md")
        for old in directory.iterdir():
            if old.name in expected or not pattern.fullmatch(old.name) or not old.is_file():
                continue
            # Only remove preprint pages for this slug, preserving unrelated/manual pages.
            sections = old.read_text(encoding="utf-8").split("---", 2)
            if len(sections) != 3 or sections[0].strip():
                continue
            if not re.search(r"^category:\s*preprint\s*$", sections[1], re.MULTILINE):
                continue
            old.unlink()
            print(f"Removed old preprint: {old.name}")


def publications(dirname: str, html_escape: Callable[[str], str]):
    with open(
        os.path.join(dirname, "json/publications.json"),
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    publications = pd.DataFrame(data)

    for row, item in publications.iterrows():
        md_filename = str(item.pub_date) + "-" + item.url_slug + ".md"
        html_filename = str(item.pub_date) + "-" + item.url_slug

        ## YAML variables

        md = '---\ntitle: "' + item.title + '"'

        md += "\nauthors: '" + ", ".join(item.authors) + "'"

        md += "\ncollection: publications"

        assert item.category in ["manuscript", "preprint"], item.category
        md += "\ncategory: " + item.category

        md += """\npermalink: /publication/""" + html_filename

        if len(str(item.excerpt)) > 5:
            md += "\nexcerpt: '" + html_escape(item.excerpt) + "'"

        md += "\ndate: " + str(item.pub_date)

        md += "\nvenue: '" + html_escape(item.venue) + "'"

        if len(str(item.paper_url)) > 5:
            md += "\n" + "paperurl: '" + item.paper_url + "'"

        if item.slides_url is not np.nan:
            md += "\n" + "slidesurl: '" + item.slides_url + "'"

        md += "\n---"

        ## Markdown description for individual page

        if len(str(item.paper_url)) > 5:
            md += "\n\n<a href='" + item.paper_url + "'>Link to the Paper</a>"

            if item.slides_url is not np.nan:
                md += " \\| <a href='" + item.slides_url + "'>Download the Slide</a>"

            md += "\n"

        if len(str(item.excerpt)) > 5:
            md += "\n" + html_escape(item.excerpt) + "\n"

        if item.content is not np.nan:
            md += "\n" + html_escape(item.content) + "\n"

        md_filename = os.path.basename(md_filename)
        print(md_filename)

        with open(
            os.path.join(dirname, "../_publications", md_filename),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(md)

    # Clean up only after every replacement page has been written successfully.
    remove_old_preprints(data, Path(dirname).resolve().parent / "_publications")


def main():
    print("Run from gen_all.py")


if __name__ == "__main__":
    main()
