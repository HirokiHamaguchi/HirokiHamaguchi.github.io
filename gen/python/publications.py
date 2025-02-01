import json
import os

import numpy as np
import pandas as pd


def publications(dirname: str, html_escape: callable):
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
            md += "\npaperurl: '" + item.paper_url + "'"

        if item.slides_url is not np.nan:
            md += "\nslidesurl: '" + item.slides_url + "'"

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
        ) as f:
            f.write(md)


def main():
    print("Run from gen.py")


if __name__ == "__main__":
    main()
