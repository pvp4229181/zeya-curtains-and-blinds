#!/usr/bin/env python3
"""
Build the deployable static bundle from zeya-website/.

    python tools/build_dist.py

.openai/hosting.json serves `dist/`, so this script produces it. dist/ is a
copy of zeya-website/ carrying only the files the site actually references:
every page, plus each asset reachable from a page's href/src/srcset or from a
url() inside a stylesheet it loads. Nothing is rewritten — the site is already
fully relative, so the copy works at any path, exactly like the source folder.

Anything not reachable is left out and listed at the end, so an asset that
disappears from the bundle is visible rather than silent. Run it after
tools/build_pages.py.
"""
import os
import re
import shutil
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = os.path.join(ROOT, "zeya-website")
DIST = os.path.join(ROOT, "dist")

# Files a browser or crawler fetches by convention, never by a link in the markup.
CONVENTIONAL = ("assets/icons/favicon.ico", "robots.txt", "sitemap.xml")

CSS_URL = re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)""")


def _rel(path):
    return os.path.relpath(path, SITE).replace(os.sep, "/")


def _resolve(base, url):
    """Resolve a document-relative URL to a site-relative path, or None."""
    parts = urlsplit(url.strip())
    if not parts.path or parts.scheme or parts.netloc or url.startswith("#"):
        return None
    target = os.path.normpath(os.path.join(os.path.dirname(base), unquote(parts.path)))
    if target.startswith(".."):
        return None
    return target.replace(os.sep, "/")


class Refs(HTMLParser):
    """Collect every local href/src/srcset/content URL on a page."""

    def __init__(self, page):
        super().__init__()
        self.page = page
        self.found = []

    def _add(self, url):
        target = _resolve(self.page, url)
        if target:
            self.found.append(target)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src", "poster"):
            if a.get(key):
                self._add(a[key])
        for key in ("srcset", "imagesrcset"):
            for candidate in a.get(key, "").split(","):
                candidate = candidate.strip().split(" ")[0]
                if candidate:
                    self._add(candidate)
        if tag == "meta" and a.get("content") and a.get("property", "").endswith("image"):
            self._add(a["content"])


def references(rel_path):
    full = os.path.join(SITE, rel_path)
    if rel_path.endswith(".html"):
        parser = Refs(rel_path)
        parser.feed(open(full, encoding="utf8").read())
        return parser.found
    if rel_path.endswith(".css"):
        text = open(full, encoding="utf8").read()
        return [t for t in (_resolve(rel_path, u) for u in CSS_URL.findall(text)) if t]
    return []


def collect():
    """Walk out from the pages; return (kept, missing)."""
    pages = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    queue = list(pages) + [c for c in CONVENTIONAL if os.path.isfile(os.path.join(SITE, c))]
    kept, missing = set(), []
    while queue:
        item = queue.pop()
        if item in kept:
            continue
        if not os.path.isfile(os.path.join(SITE, item)):
            missing.append(item)
            continue
        kept.add(item)
        queue.extend(references(item))
    return pages, kept, missing


def main():
    if not os.path.isdir(SITE):
        sys.exit("zeya-website/ not found")

    pages, kept, missing = collect()
    if missing:
        for item in sorted(set(missing)):
            print("  missing: %s" % item)
        sys.exit("%d referenced file(s) do not exist — fix the site before building dist/"
                 % len(set(missing)))

    if os.path.isdir(DIST):
        assert os.path.realpath(DIST) != os.path.realpath(ROOT)
        shutil.rmtree(DIST)

    total = 0
    for rel_path in sorted(kept):
        dst = os.path.join(DIST, rel_path.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(SITE, rel_path), dst)
        total += os.path.getsize(dst)

    everything = set()
    for dirpath, _, filenames in os.walk(SITE):
        for name in filenames:
            everything.add(_rel(os.path.join(dirpath, name)))
    skipped = sorted(everything - kept)

    print("dist/  %d file(s), %d page(s), %.1f MB" % (len(kept), len(pages), total / 1e6))
    if skipped:
        print("not referenced, left out (%d):" % len(skipped))
        for rel_path in skipped:
            print("  %s" % rel_path)


if __name__ == "__main__":
    main()
