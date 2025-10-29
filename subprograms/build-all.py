import json
import subprocess
from pathlib import Path
from typing import NamedTuple


class Assets(NamedTuple):
    js_path: str
    css_path: str
    root_id: str


def extract_root_id(html_content: str, project_name: str) -> str:
    body_start = html_content.find("<body>")
    body_end = html_content.find("</body>")
    if body_start == -1 or body_end == -1:
        raise ValueError("HTML must contain <body> tags")

    body_content = html_content[body_start + 6 : body_end].strip()

    if body_content.count("<div") != 1 or body_content.count("</div>") != 1:
        raise ValueError(f"Expected exactly one <div> in body, found: {body_content}")

    div_start = body_content.index("<div")
    div_end = body_content.index(">", div_start)
    div_tag = body_content[div_start : div_end + 1]

    if 'id="' not in div_tag:
        raise ValueError("Root div must have an id attribute")

    root_id = div_tag.split('id="')[1].split('"')[0]
    expected_id = f"{project_name.replace('_', '-')}-root"

    if root_id != expected_id:
        raise ValueError(f"Expected root id '{expected_id}', found '{root_id}'")

    return root_id


def extract_assets(dist_dir: Path, project_name: str) -> Assets:
    if not dist_dir.exists():
        raise FileNotFoundError(f"Distribution directory {dist_dir} not found")

    # Find the HTML file for this project (in subdirectory)
    html_file = dist_dir / project_name / "index.html"
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file {html_file} not found")

    html_content = html_file.read_text(encoding="utf-8")
    root_id = extract_root_id(html_content, project_name)

    # Find JS and CSS files in assets directory
    assets_dir = dist_dir / "assets"
    if not assets_dir.exists():
        raise FileNotFoundError(f"Assets directory {assets_dir} not found")

    # Look for JS file matching the project name
    js_files = list(assets_dir.glob(f"{project_name}.js"))
    css_files = list(assets_dir.glob(f"{project_name}.css"))

    js_path = f"/programs/dist/assets/{js_files[0].name}" if js_files else ""
    css_path = f"/programs/dist/assets/{css_files[0].name}" if css_files else ""

    return Assets(js_path=js_path, css_path=css_path, root_id=root_id)


def process_project(
    project_name: str, programs_dir: Path, dist_dir: Path, output_dir: Path
) -> None:
    meta_path = programs_dir / project_name / "meta.json"
    assert meta_path.exists()
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    assets = extract_assets(dist_dir, project_name)

    required_keys = {
        "title",
        "authors",
        "collection",
        "permalink",
        "excerpt",
        "thumbnail",
        "date",
    }
    if set(metadata.keys()) != required_keys:
        raise ValueError(
            f"Metadata keys mismatch for {project_name}: {metadata.keys()}"
        )

    frontmatter = f"""---
title: "{metadata["title"]}"
authors: '{metadata["authors"]}'
collection: {metadata["collection"]}
permalink: {metadata["permalink"]}
excerpt: '{metadata["excerpt"]}'
thumbnail: "{metadata["thumbnail"]}"
date: {metadata["date"]}
---

"""

    html_parts = [frontmatter]

    # Add CSS link if exists
    if assets.css_path:
        html_parts.append(f'<link rel="stylesheet" href="{assets.css_path}">\n')

    # Add root div
    html_parts.append(
        f'<div id="{assets.root_id}" style="all: unset; display: revert;"></div>\n'
    )

    # Add JS script tag
    if assets.js_path:
        html_parts.append(f'<script type="module" src="{assets.js_path}"></script>\n')

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{project_name}.html"
    output_path.write_text("".join(html_parts), encoding="utf-8")
    print(f"  ✅ Generated Jekyll file: {output_path}")


def main() -> None:
    subprograms_dir = Path(__file__).parent

    assert (subprograms_dir / "node_modules").exists()

    # Build all projects at once
    output_dir = subprograms_dir.parent / "_programs"
    subprocess.run(
        ["npm", "run", "build"],
        cwd=subprograms_dir,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        shell=True,
        encoding="utf-8",
    )
    print("✅ Build completed!")

    # Process each project
    dist_dir = output_dir / "dist"
    for item in subprograms_dir.iterdir():
        if not item.is_dir() or not (item / "meta.json").exists():
            continue
        process_project(item.name, subprograms_dir, dist_dir, output_dir)

    print("🎉 All projects processed!")


if __name__ == "__main__":
    main()
