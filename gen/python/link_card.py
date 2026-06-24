import re
from html import escape
from urllib.parse import quote

_STANDALONE_MARKDOWN_URL_RE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<url>https?://[^\s<>'\"]+)[ \t]*(?P<newline>\r?\n)?$"
)
_CODE_FENCE_RE = re.compile(r"^[ \t]*(```|~~~)")
_PLAIN_HTML_URL_PARAGRAPH_RE = re.compile(
    r"<p>\s*(?P<url>https?://[^<\s]+)\s*</p>"
)
_LINK_HTML_URL_PARAGRAPH_RE = re.compile(
    r"<p>\s*<a\s+[^>]*\bhref=(?P<quote>[\"'])(?P<href>https?://[^\"']+)(?P=quote)[^>]*>\s*(?P<text>https?://[^<\s]+)\s*</a>\s*</p>",
    re.IGNORECASE,
)


def make_link_card_embed(url: str) -> str:
    escaped_url = escape(url, quote=True)
    embed_url = "https://hatenablog-parts.com/embed?url=" + quote(url, safe="")
    return (
        '<iframe class="link-card" '
        f'src="{embed_url}" '
        f'title="link card: {escaped_url}" '
        'style="width:100%;height:155px;border:0;display:block;margin:1em 0;" '
        'loading="lazy"></iframe>'
    )


def replace_standalone_markdown_urls_with_link_cards(content: str) -> str:
    in_code_fence = False
    converted_lines: list[str] = []

    for line in content.splitlines(keepends=True):
        if _CODE_FENCE_RE.match(line):
            in_code_fence = not in_code_fence
            converted_lines.append(line)
            continue

        match = _STANDALONE_MARKDOWN_URL_RE.match(line)
        if in_code_fence or match is None:
            converted_lines.append(line)
            continue

        converted_lines.append(
            match.group("indent")
            + make_link_card_embed(match.group("url"))
            + (match.group("newline") or "")
        )

    return "".join(converted_lines)


def replace_standalone_html_urls_with_link_cards(content: str) -> str:
    def replace_link(match: re.Match[str]) -> str:
        href = match.group("href")
        text = match.group("text")
        if href != text:
            return match.group(0)
        return make_link_card_embed(href)

    content = _LINK_HTML_URL_PARAGRAPH_RE.sub(replace_link, content)
    return _PLAIN_HTML_URL_PARAGRAPH_RE.sub(
        lambda match: make_link_card_embed(match.group("url")),
        content,
    )
