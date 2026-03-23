import http.client
import json
import urllib.request
from io import BytesIO
from pathlib import Path
from typing import Callable

from PIL import Image


def _extract_thumbnail_url(rendered_body: str) -> str:
    target = 'data-canonical-src="'
    start = rendered_body.find(target)
    if start == -1:
        return ""
    start += len(target)
    end = rendered_body.find('"', start)
    if end == -1:
        return ""
    return rendered_body[start:end]


def _download_image(url: str):
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            image_data = response.read()
        return Image.open(BytesIO(image_data))
    except Exception as e:
        print(f"[WARN] Failed to download thumbnail: {url} ({e})")
        return None


def _ensure_webp_thumbnail(thumbnail_url: str, webp_path: Path) -> bool:
    if webp_path.exists():
        return True

    image = _download_image(thumbnail_url)
    if image is None:
        return False

    try:
        image.save(webp_path, "WEBP", quality=85)
        return True
    except Exception as e:
        print(f"[WARN] Failed to save webp: {webp_path} ({e})")
        return False


def qiita(dirname: str, html_escape: Callable[[str], str]):
    USER_ID = "hari64"
    project_root = Path(dirname).parent
    posts_dir = project_root / "_posts"
    thumbnails_dir = project_root / "images" / "thumbnails"
    thumbnails_dir.mkdir(parents=True, exist_ok=True)

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
        thumbnail_url = _extract_thumbnail_url(body)

        webp_filename = str(date) + "-thumbnail.webp"
        webp_path = thumbnails_dir / webp_filename
        webp_rel_path = "/images/thumbnails/" + webp_filename

        thumbnail = ""
        if thumbnail_url:
            # ここで、thumbnailが実際に存在するか判定、存在済みならcontinue
            _ensure_webp_thumbnail(thumbnail_url, webp_path)
            thumbnail = webp_rel_path

        md = '---\ntitle: "' + title + '"'

        md += """\npermalink: /blog/""" + date

        md += "\ndate: " + str(date)

        md += "\nthumbnail: " + thumbnail

        md += "\n---"

        # Check if Qiita.md exists in the external QiitaArticles folder
        # Folder name may be like "20250827_ColorTile", matching "20250827*" pattern
        qiita_articles_dir = Path("c:\\Users\\hirok\\Documents\\QiitaArticles")
        date_without_dash = date.replace("-", "")
        qiita_md_path = None

        assert qiita_articles_dir.exists()
        matching_folders = list(qiita_articles_dir.glob(f"{date_without_dash}*"))
        if len(matching_folders) == 1:
            qiita_md_path = matching_folders[0] / "Qiita.md"
            with open(qiita_md_path, "r", encoding="utf-8") as f:
                md += "\n" + f.read()
        elif len(matching_folders) == 0:
            md += "\n\n" + "[Link to Qiita](" + jsonStr[num]["url"] + ")" + "\n"
        else:
            raise Exception(
                f"Multiple matching folders found for date {date_without_dash} in {qiita_articles_dir}"
            )

        md_filename = (
            str(date)
            + "-"
            + title.replace(" ", "-").replace("/", "-").replace(":", "-")
            + ".md"
        )

        with open(posts_dir / md_filename, "w", encoding="utf-8") as f:
            f.write(md)

    conn.close()


def main():
    print("Run from gen.py")


if __name__ == "__main__":
    main()
