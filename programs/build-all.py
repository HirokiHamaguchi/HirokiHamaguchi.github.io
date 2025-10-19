import json
import subprocess
from pathlib import Path
from typing import Dict, List, NamedTuple


class Assets(NamedTuple):
    js: str
    css: str
    root_id: str


def read_file(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return ""


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


def extract_assets(dist_dir: Path) -> Assets:
    if not dist_dir.exists():
        raise FileNotFoundError(f"Distribution directory {dist_dir} not found")

    assets_dir = dist_dir / "assets"
    if not assets_dir.exists():
        raise FileNotFoundError(f"Assets directory {assets_dir} not found")

    html_files = list(dist_dir.glob("*.html"))
    if len(html_files) != 1:
        raise ValueError(
            f"Expected exactly one .html file in {dist_dir}, found {len(html_files)}"
        )

    html_content = read_file(html_files[0])
    root_id = extract_root_id(html_content, dist_dir.parent.name)

    js_files = list(assets_dir.glob("*.js"))
    if len(js_files) > 1:
        raise ValueError(
            f"Expected at most one .js file in {assets_dir}, found {len(js_files)}"
        )
    js_content = read_file(js_files[0]) if js_files else ""

    css_files = list(assets_dir.glob("*.css"))
    if len(css_files) > 1:
        raise ValueError(
            f"Expected at most one .css file in {assets_dir}, found {len(css_files)}"
        )
    css_content = read_file(css_files[0]) if css_files else ""

    return Assets(js=js_content, css=css_content, root_id=root_id)


def validate_metadata(metadata: Dict, project_name: str) -> None:
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


def generate_jekyll_html(
    project_name: str,
    metadata: Dict,
    assets: Assets,
    output_dir: Path,
) -> None:
    validate_metadata(metadata, project_name)

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

    if assets.css:
        html_parts.append(f"<style>\n{assets.css}\n</style>\n")

    html_parts.append(f'<div id="{assets.root_id}"></div>\n')

    if assets.js:
        html_parts.append(f"<script>\n{assets.js}\n</script>\n")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{project_name}.html"
    output_path.write_text("".join(html_parts), encoding="utf-8")
    print(f"  ✅ Generated Jekyll file: {output_path}")


def run_command(command: List[str], cwd: Path) -> None:
    if not cwd.exists():
        raise FileNotFoundError(f"Working directory {cwd} does not exist")

    try:
        subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{e.stdout}")


def build_project(project_name: str, project_path: Path, output_dir: Path) -> None:
    print(f"📦 Building {project_name}...")

    meta_path = project_path / "meta.json"
    dist_dir = project_path / "dist"

    try:
        if not meta_path.exists():
            raise FileNotFoundError(f"meta.json not found in {project_path}")

        metadata = json.loads(meta_path.read_text(encoding="utf-8"))

        if not (project_path / "node_modules").exists():
            raise FileNotFoundError(f"node_modules not found in {project_path}")

        print("  🏗️  Building project...")
        run_command(["npm", "run", "build"], project_path)

        print("  📝 Extracting assets...")
        assets = extract_assets(dist_dir)

        print("  📄 Generating Jekyll file...")
        generate_jekyll_html(project_name, metadata, assets, output_dir)

        print(f"  ✅ {project_name} completed!\n")

    except Exception as e:
        print(f"  ❌ Error building {project_name}: {e}\n")


def get_project_directories(programs_dir: Path) -> List[str]:
    project_dirs = []
    for item in programs_dir.iterdir():
        if not item.is_dir():
            continue

        meta_json = item / "meta.json"
        package_json = item / "package.json"

        if not meta_json.exists():
            print(f"  ⚠️  Skipping {item.name}: meta.json not found")
            continue

        if not package_json.exists():
            print(f"  ⚠️  Skipping {item.name}: package.json not found")
            continue

        project_dirs.append(item.name)

    return project_dirs


def main() -> None:
    programs_dir = Path(__file__).parent
    output_dir = programs_dir.parent / "_programs"

    print("🔨 Building all React/TypeScript programs for Jekyll...\n")

    project_dirs = get_project_directories(programs_dir)
    if not project_dirs:
        print("No valid projects found.")
        return

    for project_name in project_dirs:
        project_path = programs_dir / project_name
        build_project(project_name, project_path, output_dir)

    print("🎉 All projects processed!")


if __name__ == "__main__":
    main()
