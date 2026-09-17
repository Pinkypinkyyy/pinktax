import re
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


def test_book_page_has_one_intake_only():
    # Microsoft Bookings asks revenue, staff, what is hurting, where the
    # business is now and where it is going, several of them mandatory. The
    # site used to ask all of it again first, so a visitor wrote the same
    # three paragraphs twice before they could pick a time.
    text = (ROOT / "book" / "index.html").read_text(encoding="utf-8")
    assert HOSP in text, "Bookings link missing"
    assert SP not in text
    assert "enquiryForm" not in text, "duplicate intake form is back"
    for name in ("revenue", "staff", "hurt", "position", "vision"):
        assert f'name="{name}"' not in text, f"{name} asked twice"


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
    # tools/*.py is included because build_pages.py generated this site and
    # still carried the wording; regenerating would have restored it.
    targets = PAGES + list(ROOT.glob("*.js")) + list((ROOT / "tools").glob("*.py"))
    for p in targets:
        text = p.read_text(encoding="utf-8")
        # The build guard has to name the rule in order to enforce it.
        if p.suffix == ".py" and "PINK_ALLOW_STALE_REGEN" in text:
            continue
        for word in banned:
            assert word not in text, f"{p}: {word}"


def test_booking_click_fires_generate_lead():
    # Google Ads' primary conversion is the GA4 generate_lead event. Intake
    # now happens on bookings.cloud.microsoft, an origin we cannot observe,
    # so the click onto the calendar is the last event we own. If it stops
    # firing, paid spend has no conversion signal at all.
    nav = (ROOT / "nav.js").read_text(encoding="utf-8")
    book = (ROOT / "book" / "index.html").read_text(encoding="utf-8")
    assert 'row.e === "book-calendar"' in nav
    assert 'gtag("event", "generate_lead", { method: "booking-calendar" })' in nav
    assert 'data-event="book-calendar"' in book
    assert "spLead" not in nav


def test_counter_fallback_matches_target():
    # The proof-bar numbers are printed in the HTML so they are right with JS
    # off and on reduced motion. If a printed value drifts from its data-to,
    # visitors without the animation see a different number to everyone else.
    import re

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    ticks = re.findall(r'<span class="tick"([^>]*)>([^<]*)</span>', html)
    assert ticks, "proof bar counters missing"
    for attrs, shown in ticks:
        to = float(re.search(r'data-to="([\d.]+)"', attrs).group(1))
        dp = int((re.search(r'data-dp="(\d+)"', attrs) or [0, "0"])[1])
        prefix = (re.search(r'data-prefix="([^"]*)"', attrs) or [0, ""])[1]
        body = f"{to:.{dp}f}"
        if 'data-sep="1"' in attrs:
            whole, _, frac = body.partition(".")
            body = f"{int(whole):,}" + (f".{frac}" if frac else "")
        assert shown == prefix + body, f"{shown!r} != {prefix + body!r}"


def test_stars_are_svg_not_glyphs():
    # Neither Montserrat nor Manrope contains U+2605, so the character would
    # render in a system fallback face.
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "★" not in html
    assert html.count('<svg class="stars"') == 3


def test_no_synthesised_font_weights():
    # Only weights actually fetched from Google may be used, or the browser
    # fakes the face and the text reads as a different font.
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    loaded = {"400", "500", "600", "700", "800"}
    used = set(re.findall(r"font-weight:(\d+)", css))
    assert used <= loaded, f"weights with no loaded face: {sorted(used - loaded)}"


def test_assets():
    assert (ROOT / "assets" / "logo.png").exists()
    assert (ROOT / "assets" / "logo-white.png").exists()
    assert (ROOT / "assets" / "pink-portrait.jpg").exists()
