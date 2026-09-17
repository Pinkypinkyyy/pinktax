from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = list(ROOT.rglob("*.html"))
HOSP = "PinkAccountingTaxSolutionsClientBookings"
SP = "ServiceProfit@pinktax.com.au"


def test_hospitality_calendar_only():
    for p in PAGES:
        text = p.read_text(encoding="utf-8")
        assert SP not in text, p
        if p.name != "404.html" and "contact" not in str(p):
            pass


def test_book_has_filter_questions():
    text = (ROOT / "book" / "index.html").read_text(encoding="utf-8")
    assert HOSP in text
    assert SP not in text
    for name in ("revenue", "staff", "hurt", "position", "vision"):
        assert f'name="{name}"' in text
    assert text.find("enquiryForm") < text.find("pick-time")


def test_no_service_profit_offer():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    book = (ROOT / "book" / "index.html").read_text(encoding="utf-8")
    assert "HVAC" not in home
    assert "Job Profit" not in home
    assert SP not in book
    assert HOSP in book


def test_urls_exist():
    for rel in (
        "index.html",
        "system/index.html",
        "why-pink/index.html",
        "book/index.html",
        "contact/index.html",
        "margin-check/index.html",
        "working-with-us/index.html",
        "privacy/index.html",
        "terms/index.html",
        "feedback/index.html",
        "hospitality-accountant-brisbane/index.html",
        "restaurant-cafe-bookkeeping-brendale/index.html",
        "accountant-brendale/index.html",
        "404.html",
        "sitemap.xml",
        "robots.txt",
    ):
        assert (ROOT / rel).exists(), rel


def test_no_cross_brand_wording_anywhere():
    # The site was built from a Service Profit template. Hospitality-only is a
    # firm rule on every public Pink surface, so guard every page and script.
    banned = ("Service Profit", "HVAC", "electrical, construction", "tradie")
    for p in PAGES + list(ROOT.glob("*.js")):
        text = p.read_text(encoding="utf-8")
        for word in banned:
            assert word not in text, f"{p}: {word}"


def test_enquiry_form_fires_generate_lead():
    # Google Ads' primary conversion is the GA4 generate_lead event. If the
    # success path stops firing it, paid spend has no conversion signal.
    nav = (ROOT / "nav.js").read_text(encoding="utf-8")
    assert 'gtag("event", "generate_lead", { method: "enquiry-form" })' in nav
    assert "spLead" not in nav


def test_assets():
    assert (ROOT / "assets" / "logo.png").exists()
    assert (ROOT / "assets" / "logo-white.png").exists()
    assert (ROOT / "assets" / "pink-portrait.jpg").exists()
