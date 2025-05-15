import http.client
import json
import os
from typing import Callable


def qiita(dirname: str, html_escape: Callable[[str], str]):
    USER_ID = "hari64"

    # Assume that the number of items is less than 100
    PAGE = "1"
    PAR_PAGE = "100"

    conn = http.client.HTTPSConnection("qiita.com", 443)
    conn.request(
        "GET",
        "/api/v2/users/" + USER_ID + "/items?page=" + PAGE + "&per_page=" + PAR_PAGE,
    )
    res = conn.getresponse()
    if res.reason != "OK":
        print(res.status, res.reason)
        conn.close()
        raise Exception("Failed to get data from Qiita")

    data = res.read().decode("utf-8")
    jsonStr = json.loads(data)
    for num in range(len(jsonStr)):
        created_at = jsonStr[num]["created_at"]
        title = html_escape(jsonStr[num]["title"])
        date = created_at[:10]

        body = jsonStr[num]["rendered_body"]
        thumbnail = ""
        target = 'data-canonical-src="'
        if body.find(target) != -1:
            s = body.find(target) + len(target)
            e = body.find('"', s)
            thumbnail = body[s:e]

        md = '---\ntitle: "' + title + '"'

        md += """\npermalink: /blog-posts/""" + date

        md += "\ndate: " + str(date)

        md += "\nthumbnail: " + thumbnail

        md += "\n---"

        md += "\n\n" + "[Link to Qiita](" + jsonStr[num]["url"] + ")" + "\n"

        md_filename = str(date) + "-" + date + ".md"

        with open(
            os.path.join(dirname, "../_posts/" + md_filename), "w", encoding="utf-8"
        ) as f:
            f.write(md)

    conn.close()


def main():
    print("Run from gen.py")


if __name__ == "__main__":
    main()
