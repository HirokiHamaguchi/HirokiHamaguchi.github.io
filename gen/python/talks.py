import json
import os

import numpy as np
import pandas as pd


def talks(dirname: str, html_escape: callable):
    with open(os.path.join(dirname, "json/talks.json"), "r", encoding="utf-8") as file:
        data = json.load(file)

    talks = pd.DataFrame(data)

    for row, item in talks.iterrows():

        md_filename = str(item.date) + "-" + item.url_slug + ".md"
        html_filename = str(item.date) + "-" + item.url_slug

        md = '---\ntitle: "' + item.title + '"'

        md += "\nauthors: '" + ", ".join(item.authors) + "'"

        md += "\ncollection: talks" + "\n"

        if len(str(item.type)) > 3:
            md += 'type: "' + item.type + '"\n'
        else:
            md += 'type: "Talk"\n'

        md += "permalink: /talks/" + html_filename + "\n"

        if len(str(item.venue)) > 3:
            md += 'venue: "' + item.venue + '"\n'

        if len(str(item.location)) > 3:
            md += "date: " + str(item.date) + "\n"

        if len(str(item.location)) > 3:
            md += 'location: "' + str(item.location) + '"\n'

        md += "---\n"

        if len(str(item.talk_url)) > 3:
            md += "\n[Link to the Page](" + item.talk_url + ")"

            if item.poster_url is not np.nan:
                md += " \\| [Download the Poster](" + item.poster_url + ")"

            if item.slide_url is not np.nan:
                md += " \\| [Download the Slide](" + item.slide_url + ")"

            md += "\n"

        if "description" in item:
            md += html_escape(item.description) + "\n"

        md_filename = os.path.basename(md_filename)
        print(md_filename)
        with open(os.path.join(dirname, "../_talks/" + md_filename), "w") as f:
            f.write(md)


def main():
    print("Run from gen.py")


if __name__ == "__main__":
    main()
