"""The 404 page must never be indexed or canonicalised.

GitHub Pages serves 404.html with a 404 status for unknown URLs, but the file
itself also answers 200 at /404.html. Without noindex that URL can be indexed
as a thin duplicate, and a canonical to itself tells Google it is a real page.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_404_page_is_noindex_and_has_no_canonical():
    text = (ROOT / "404.html").read_text(encoding="utf-8")
    assert re.search(r'<meta name="robots" content="noindex,follow">', text)
    assert 'rel="canonical"' not in text


def test_404_page_is_not_in_the_sitemap():
    assert "404" not in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
