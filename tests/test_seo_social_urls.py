"""og:url must equal the page's own canonical URL.

/switching/ once shared /working-with-us/ as its og:url, so every share and
every crawler that trusts og:url credited the wrong page.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]


def test_og_url_matches_canonical_everywhere():
    checked = 0
    for p in PAGES:
        text = p.read_text(encoding="utf-8")
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', text)
        og = re.search(r'<meta property="og:url" content="([^"]+)"', text)
        if not (canon and og):
            continue  # redirect stubs, the 404 page and the paid page carry no social tags
        checked += 1
        assert og.group(1) == canon.group(1), f"{p.relative_to(ROOT)}: og:url {og.group(1)} != canonical {canon.group(1)}"
    assert checked >= 20, "og/canonical check ran on too few pages"
