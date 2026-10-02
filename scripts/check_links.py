#!/usr/bin/env python3
"""Check local links and fragment targets in the static site."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        for attr in ("href", "src"):
            if values.get(attr):
                self.links.append(values[attr])


def parse_page(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main():
    pages = sorted(ROOT.rglob("*.html"))
    parsed = {page.resolve(): parse_page(page) for page in pages}
    errors = []

    for page, parser in parsed.items():
        for raw_link in parser.links:
            link = urlsplit(raw_link)
            if link.scheme in SKIP_SCHEMES or raw_link.startswith("//"):
                continue
            target = (page.parent / unquote(link.path)).resolve() if link.path else page
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: missing {raw_link}")
                continue
            if link.fragment and target.suffix.lower() == ".html":
                target_parser = parsed.get(target) or parse_page(target)
                if unquote(link.fragment) not in target_parser.ids:
                    errors.append(
                        f"{page.relative_to(ROOT)}: missing fragment #{link.fragment} in "
                        f"{target.relative_to(ROOT)}"
                    )

    if errors:
        print("Internal-link check failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"Internal-link check passed: {len(pages)} HTML files checked.")


if __name__ == "__main__":
    main()
