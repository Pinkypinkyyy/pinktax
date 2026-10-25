"""Sitemap lastmod and the AccountingService schema.

lastmod is the date of the last commit that touched each page, written by
tools/build_landing_pages.py. Schema no longer carries a priceRange (a "$$"
guess, no approved price list) or a generic Country areaServed.
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_every_sitemap_url_has_a_real_lastmod():
    xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    entries = re.findall(r"<url><loc>([^<]+)</loc>(<lastmod>([^<]+)</lastmod>)?</url>", xml)
    assert len(entries) >= 20
    for loc, _, mod in entries:
        assert mod, f"{loc} has no lastmod"
        assert date.fromisoformat(mod) <= date(2099, 1, 1)
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", mod), f"{loc}: lastmod must be a plain date, got {mod}"


def jsonld(path):
    t = (ROOT / path).read_text(encoding="utf-8")
    return [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)]


def test_accounting_service_schema_has_no_price_range_or_generic_area():
    seen = 0
    for rel in ("index.html", "contact/index.html"):
        for node in jsonld(rel):
            if node.get("@type") == "AccountingService":
                seen += 1
                assert "priceRange" not in node
                assert "areaServed" not in node
    assert seen == 2
