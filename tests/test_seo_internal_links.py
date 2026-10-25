"""No indexable page may be an orphan.

Crawl of the live site on 25 Oct 2026 found /accountant-brendale/ and
/restaurant-cafe-bookkeeping-brendale/ in the sitemap with zero internal
links pointing at them. Every sitemap URL must be linked from at least one other page.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sitemap_paths():
    xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>https://pinktax\.com\.au(/[^<]*)</loc>", xml)


def test_no_sitemap_page_is_an_orphan():
    pages = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
             for p in ROOT.rglob("*.html") if ".git" not in p.parts}
    orphans = []
    for path in sitemap_paths():
        if path == "/":
            continue
        own = path.strip("/") + "/index.html"
        if not any(f'href="{path}"' in t for rel, t in pages.items() if rel != own):
            orphans.append(path)
    assert not orphans, f"sitemap pages no other page links to: {orphans}"


def test_every_footer_guides_list_links_the_local_pages():
    # Only the home page and the nine generated guides carry a Guides column.
    n = 0
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        t = p.read_text(encoding="utf-8")
        if "<h2>Guides</h2>" not in t:
            continue
        n += 1
        for href in ("/accountant-brendale/", "/restaurant-cafe-bookkeeping-brendale/"):
            assert f'href="{href}"' in t, f"{p.relative_to(ROOT)} lacks {href}"
    assert n >= 10
