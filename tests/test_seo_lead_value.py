"""Lead events must not carry an invented dollar value.

nav.js sent value: 990 with every generate_lead (GA4) and Lead (Meta) event.
990 is a plan price that is not approved for publication, and a lead is not a
sale, so the figure distorted any value-based bidding and reporting. Revenue
belongs in GHL against the won opportunity, not in the browser.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_lead_events_carry_no_hardcoded_value():
    nav = (ROOT / "nav.js").read_text(encoding="utf-8")
    assert "value: 990" not in nav
    assert "currency:" not in nav
    assert 'gtag("event", "generate_lead", lead)' in nav
    assert 'window.pinkMeta("Lead", { content_name: source }, hashed)' in nav
