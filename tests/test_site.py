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


def test_home_carries_the_margin_check():
    # The calculator was the only genuinely interactive thing on the site and
    # it sat on a page almost nobody reached. Same ids and same script as
    # /margin-check/, so there is one implementation, not two.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'id="pmc-calc"' in home
    assert "margin-check.js" in home
    for f in ("pmc-sales", "pmc-wages", "pmc-cogs", "pmc-rent", "pmc-other"):
        assert f'id="{f}"' in home, f
    js = (ROOT / "margin-check.js").read_text(encoding="utf-8")
    assert "is-' + state" in js, "benchmark state class missing"


def test_legacy_urls_are_recovered():
    # These paths were live on the WordPress site until 12 Sep 2026 and
    # returned hard 404s after the move. GitHub Pages cannot serve a 301, so
    # each one is a stub that canonicalises to its replacement, carries
    # noindex, and moves the visitor there.
    legacy = {
        "service": "/system/",
        "services": "/system/",
        "about": "/why-pink/",
        "blog": "/",
        "tax-returns": "/",
        "bookkeeping": "/hospitality-bookkeeping/",
        "the-60-second-margin-self-check": "/margin-check/",
    }
    for slug, dest in legacy.items():
        f = ROOT / slug / "index.html"
        assert f.exists(), slug
        t = f.read_text(encoding="utf-8")
        assert f'href="https://pinktax.com.au{dest}"' in t, slug
        assert "noindex" in t, f"{slug} must not compete in the index"
        assert f'url={dest}' in t, slug
    # Stubs are for humans arriving on dead links, not for the sitemap.
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for slug in legacy:
        assert f"/{slug}/" not in sitemap, slug


def test_margin_check_privacy_claim_is_exact():
    # The calculator now has an opt-in "email these results" button, so an
    # absolute "nothing is sent anywhere" would no longer be true. A firm
    # that audits other people's claims cannot be loose with its own.
    for p in PAGES:
        t = p.read_text(encoding="utf-8")
        assert "nothing sent anywhere." not in t.lower(), p
        assert "nothing is sent anywhere;" not in t.lower(), p
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'id="pmc-send"' in home
    assert "unless you choose" in home
    js = (ROOT / "margin-check.js").read_text(encoding="utf-8")
    # Opt-in send must stay a mailto: venue takings and wages should not be
    # posted through a third-party form relay.
    assert "mailto:admin@pinktax.com.au" in js
    assert "formsubmit" not in js


def test_switching_page_exists_and_is_linked():
    # Changing accountants is the biggest objection in this market and no
    # page addressed it.
    f = ROOT / "switching" / "index.html"
    assert f.exists()
    t = f.read_text(encoding="utf-8")
    assert 'canonical" href="https://pinktax.com.au/switching/"' in t
    assert "30 June" in t, "mid-year switching must be addressed"
    assert "/switching/" in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert "/switching/" in (ROOT / "index.html").read_text(encoding="utf-8")


def test_assets():
    assert (ROOT / "assets" / "logo.png").exists()
    assert (ROOT / "assets" / "logo-white.png").exists()
    assert (ROOT / "assets" / "pink-portrait.jpg").exists()


LANDING = (
    "restaurant-accountant",
    "cafe-accountant",
    "hospitality-bookkeeping",
    "restaurant-bookkeeping",
    "hospitality-payroll",
    "restaurant-food-cost-percentage",
    "hospitality-wage-percentage",
    "restaurant-profit-margin",
    "hospitality-accountant-brisbane",
)


def test_no_competitor_attack_copy():
    # The sell is the structural one: hospitality moves weekly, traditional
    # accounting reports yearly. Attacking the previous accountant is not
    # needed to make it and reads badly to an owner who liked theirs.
    banned = ("autopsy", "old accountant", "files and forgets")
    for p in PAGES:
        text = p.read_text(encoding="utf-8").lower()
        for word in banned:
            assert word not in text, f"{p}: {word}"


def test_one_trust_statement_only():
    # "No pitch", "no upsell" and "we'll tell you honestly" were repeated
    # across the site. Piling up reassurance introduces the doubt it is
    # trying to remove, so the cheaper-tier promise is made once, on the
    # booking page, where the decision actually happens.
    hits = [p for p in PAGES if "cheaper tier" in p.read_text(encoding="utf-8")]
    assert len(hits) == 1, [str(p) for p in hits]
    assert hits[0] == ROOT / "book" / "index.html"
    for p in PAGES:
        text = p.read_text(encoding="utf-8").lower()
        assert "no pitch" not in text, p
        assert "no upsell" not in text, p


def test_offer_leads_with_the_four_questions():
    # $990 Margin Protection is the product. It has to read as a management
    # system rather than a list of accounting tasks, and it has to dominate
    # the other three tiers instead of being compared with them.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    feat = home.index('<div class="feat">')
    tiers = home.index('<div class="tiers">')
    assert feat < tiers, "the $990 block must come before the other tiers"
    assert "$990" in home[feat:tiers]
    for q in (
        "Are you actually making money?",
        "What changed?",
        "Where is margin leaking?",
        "What should you do next?",
    ):
        assert q in home[feat:tiers], q
    # bookkeeping, payroll and BAS are the infrastructure, not the headline
    lead_in = home[feat:home.index("</div>", home.index('class="fdesc"'))]
    assert "Bookkeeping" not in lead_in.split('class="fnote"')[0]


def test_landing_pages_build_and_match_sitemap():
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>https://pinktax\.com\.au(/[^<]*)</loc>", sitemap)
    assert len(locs) == len(set(locs)), "duplicate sitemap entries"
    for slug in LANDING:
        page = ROOT / slug / "index.html"
        assert page.exists(), slug
        text = page.read_text(encoding="utf-8")
        assert f'<link rel="canonical" href="https://pinktax.com.au/{slug}/">' in text
        assert f"/{slug}/" in locs, f"{slug} missing from sitemap"
    for loc in locs:
        target = ROOT / loc.strip("/") / "index.html" if loc != "/" else ROOT / "index.html"
        assert target.exists(), f"sitemap points at a page that does not exist: {loc}"


def test_landing_pages_are_distinct_and_convert():
    titles, descs = set(), set()
    for slug in LANDING:
        text = (ROOT / slug / "index.html").read_text(encoding="utf-8")
        title = re.search(r"<title>(.*?)</title>", text).group(1)
        desc = re.search(r'<meta name="description" content="(.*?)">', text).group(1)
        assert title not in titles, f"duplicate title: {title}"
        assert desc not in descs, f"duplicate description on {slug}"
        titles.add(title)
        descs.add(desc)
        assert len(title) <= 65, f"{slug} title too long for the SERP: {len(title)}"
        assert 'href="/book/"' in text, slug
        assert 'href="/margin-check/"' in text, slug
        assert len(text.split()) > 600, f"{slug} is too thin to rank"


def test_footer_links_the_landing_pages():
    # Orphan pages do not rank. Every landing page is reachable from the
    # footer of every page, which is where the builder lifts it from.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    foot = home[home.index('<footer class="foot">'):]
    for slug in LANDING:
        assert f'href="/{slug}/"' in foot, slug
