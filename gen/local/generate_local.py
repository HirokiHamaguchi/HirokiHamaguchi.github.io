import email.utils
import html
import os
import re
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from gen.python.link_card import replace_standalone_html_urls_with_link_cards

os.chdir(Path(__file__).parent)
assert os.getcwd().endswith("local")

zip_files = [file for file in os.listdir(".") if file.endswith(".zip")]
xml_files = [file for file in os.listdir(".") if file.endswith(".xml")]

if len(xml_files) == 0:
    for file in zip_files:
        print(f"Extracting {file}...")
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(".")
    xml_files = [file for file in os.listdir(".") if file.endswith(".xml")]
else:
    print("XML files already exist, skipping extraction.")

assert len(xml_files) > 0, "No XML files found after extraction."
print(f"Found {len(xml_files)} XML files.")


dist_folder = Path("../../_diary")

if Path("./assets").exists():
    # move to dist_folder/assets
    dist_assets = dist_folder / "assets"
    if not dist_assets.exists():
        dist_assets.mkdir(parents=True, exist_ok=True)
    for item in Path("./assets").iterdir():
        assert item.is_file()
        dest = dist_assets / item.name
        os.replace(item, dest)
    os.rmdir("./assets")

summary = Counter()
for xml_path in xml_files:  # xml_files は既存の変数を使用
    p = Path(xml_path)
    tree = ET.parse(p)
    root = tree.getroot()
    print(f"Processing {p.name} with {len(root)} elements.")
    channel = root.find("channel")
    assert channel is not None, f"No channel found in {p.name}"
    for item in channel.findall("item"):
        for elem in item:
            if elem.tag.endswith("/status"):
                # todo? publishedのみ処理
                assert elem.text == "publish", f"Item not published: {elem.text}"

        title_elem = item.find("title")
        title: str = str(title_elem.text) if title_elem is not None else "No Title"

        link_elem = item.find("link")
        link: str = str(link_elem.text) if link_elem is not None else "No Link"

        pubdate_elem = item.find("pubDate")
        pubdate: str = (
            str(pubdate_elem.text) if pubdate_elem is not None else "1970-01-01"
        )
        dt = email.utils.parsedate_to_datetime(pubdate)
        pubdate = dt.date().isoformat()

        safe_title = title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        out_path = dist_folder / f"{safe_title}.html"
        print(f"Title: {title} Link: {link} Date: {pubdate} Output: {out_path}")

        # content:encodedを取得（より詳細な内容）
        content_elem = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")
        content: str = str(content_elem.text if content_elem is not None else "")

        content = re.sub(r'\s+(name|id)="[^"]*"', "", content)

        first_fig: str = content.split('<img src="')[1].split('"')[0]

        # <img src="/assets/ を <img src="assets/ に置換
        content = content.replace('<img src="/assets/', '<img src="/diary/assets/')
        content = replace_standalone_html_urls_with_link_cards(content)

        html_content = f"""---
title: '{html.escape(title)}'
authors: 'Hiroki Hamaguchi'
collection: diary
permalink: /diary/{urllib.parse.urlencode({"key": safe_title})[4:]}/
excerpt: '{html.escape(title)}'
thumbnail: /diary/{html.escape(first_fig)}
date: {html.escape(pubdate)}
---

<div class="content">
    {content}
</div>
"""

        if not out_path.parent.exists():
            out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)

