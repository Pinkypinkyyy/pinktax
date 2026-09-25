import html
import json
import re
import sys
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
    # The site was built from a Service Profit template. One site, one niche
    # is still a firm rule: this site speaks to hospitality, and trades
    # wording belongs on serviceprofit.com.au.
    #
    # HB, 24 Sep 2026: one company, two service lines, one office. The trades
    # line may be named in exactly two identity-owned places, the quiet
    # cross-link line in the footer and the two-doors block on /contact/, plus
    # the schema department that tells Google both lines are one business.
    # Those are stripped before the check; everything else is guarded as before.
    banned = ("Service Profit", "HVAC", "electrical, construction", "tradie")
    allowed = (
        re.compile(r'<p class="sister-line" data-identity="cross-link">.*?</p>', re.S),
        re.compile(r'<section[^>]*data-identity="two-doors".*?</section>', re.S),
        re.compile(r'"department":\[.*?\]'),
    )
    # tools/*.py is included because a stale builder once put the wording
    # back on regeneration. The builders read the trades name from
    # identity.json, so they never need to spell it out.
    targets = PAGES + list(ROOT.glob("*.js")) + list((ROOT / "tools").glob("*.py"))
    for p in targets:
        text = p.read_text(encoding="utf-8")
        for block in allowed:
            text = block.sub("", text)
        for word in banned:
            assert word not in text, f"{p}: {word}"


IDENTITY = json.loads((ROOT / "identity.json").read_text(encoding="utf-8"))
STUBS = [p for p in PAGES if 'http-equiv="refresh"' in p.read_text(encoding="utf-8")]


def org_nodes(text):
    nodes = []
    for raw in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S):
        node = json.loads(raw)
        if node.get("@type") == "AccountingService":
            nodes.append(node)
    return nodes


def test_identity_json_is_published():
    # The Google profile, the trades site and this site all read the same
    # file. It sits at the site root and ships with the Pages artifact (the
    # workflow uploads the whole repo, and .nojekyll keeps nothing hidden).
    ident = json.loads((ROOT / "identity.json").read_text(encoding="utf-8"))
    assert ident["public_name"] == "Pink Accounting"
    assert (ROOT / ".nojekyll").exists()


def test_schema_org_node_matches_identity():
    office = IDENTITY["office"]
    for rel in ("index.html", "contact/index.html"):
        nodes = org_nodes((ROOT / rel).read_text(encoding="utf-8"))
        assert len(nodes) == 1, rel
        n = nodes[0]
        assert n["name"] == IDENTITY["public_name"] == "Pink Accounting", rel
        assert n["@id"] == IDENTITY["schema"]["organization_id"], rel
        assert n["legalName"] == IDENTITY["legal"]["entity"], rel
        assert n["telephone"] == office["phone_e164"], rel
        assert n["email"] == office["email"], rel
        assert n["address"] == {
            "@type": "PostalAddress",
            "streetAddress": office["street"],
            "addressLocality": office["locality"],
            "addressRegion": office["region"],
            "postalCode": office["postcode"],
            "addressCountry": office["country"],
        }, rel
        hours = n["openingHoursSpecification"]
        assert hours["dayOfWeek"] == office["hours"]["days"], rel
        assert (hours["opens"], hours["closes"]) == (office["hours"]["opens"], office["hours"]["closes"]), rel
        assert IDENTITY["google_profile"]["maps_url"] in n["sameAs"], rel
        trades = IDENTITY["service_lines"]["trades"]
        assert {"@type": "AccountingService", "name": trades["service_name"], "url": trades["site"]} in n["department"], rel


def test_public_name_is_pink_accounting():
    # The legal entity belongs in legal and disclosure lines only, and always
    # with "Pty Ltd". Anywhere else the business is "Pink Accounting".
    legal = "Pink Accounting & Tax Solutions"
    for p in PAGES + list(ROOT.glob("*.js")):
        text = html.unescape(p.read_text(encoding="utf-8"))
        for name in IDENTITY["banned_public_names"]:
            assert name.lower() not in text.lower(), f"{p}: {name}"
        assert not re.search(re.escape(legal) + r"(?! Pty Ltd)", text), f"{p}: {legal} without Pty Ltd"
        title = re.search(r"<title>(.*?)</title>", text, re.S)
        if title and "Pink" in title.group(1):
            assert "Tax Solutions" not in title.group(1), p


def test_cross_link_line_once_per_page():
    x = IDENTITY["cross_links"]["on_hospitality_site"]
    line = (
        f'<p class="sister-line" data-identity="cross-link">{html.escape(x["text"])} '
        f'<a href="{x["href"]}">{html.escape(x["link_text"])}</a></p>'
    )
    for p in PAGES:
        if p in STUBS:
            continue  # redirect stubs have no footer
        text = p.read_text(encoding="utf-8")
        assert text.count('data-identity="cross-link"') == 1, p
        assert text.count(line) == 1, f"{p}: cross-link line differs from identity.json"
        foot = text[text.rindex("<footer"):text.rindex("</footer>")]
        assert line in foot, f"{p}: cross-link must sit in the footer"


def test_contact_is_the_office_page():
    # The Google profile's website link points here, so this page is the
    # firm's office page: details from identity.json, hospitality first, and
    # one small block that shows the trades door.
    text = (ROOT / "contact" / "index.html").read_text(encoding="utf-8")
    office = IDENTITY["office"]
    for value in (office["one_line"], office["phone_display"], office["email"], office["hours"]["display"]):
        assert html.escape(value) in text, value
    assert "Saturday" not in text, "office hours are Monday to Friday only"
    start = text.index('data-identity="two-doors"')
    doors = text[start:text.index("</section>", start)]
    trades = IDENTITY["service_lines"]["trades"]
    assert trades["display"] in doors
    assert f'href="{trades["site"]}"' in doors
    assert "Hospitality" in doors
    assert text.index("<h1>") < start, "hospitality must lead the page"
    assert 'data-relay="contact-form"' in text, "contact form removed"


def test_pages_equal_their_identity_rebuild():
    # identity.json is regenerated from the firm's canonical file. If it
    # changes and nobody reruns tools/build_landing_pages.py, this fails.
    sys.path.insert(0, str(ROOT / "tools"))
    import site_identity

    for p in PAGES:
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        assert site_identity.apply(text, rel) == text, f"{rel} is out of step with identity.json"


def test_booking_click_fires_book_click():
    # Intake finishes on Microsoft Bookings, which we cannot observe. The
    # click onto the calendar is the last event we own, so it is the primary
    # conversion until bookings return to this domain. generate_lead is
    # reserved for a real enquiry (name, email, phone), not a calendar click.
    nav = (ROOT / "nav.js").read_text(encoding="utf-8")
    book = (ROOT / "book" / "index.html").read_text(encoding="utf-8")
    assert 'row.e === "book-calendar"' in nav
    assert 'gtag("event", "book_click"' in nav
    assert 'lead_source: "outlook_booking"' in nav
    assert 'gtag("event", "generate_lead", { method: "booking-calendar" })' not in nav
    assert 'method: "hours-check"' not in nav
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
    # Email signatures, the firm email code and every email already sent
    # load the logo from the old WordPress path. Moving it blanks them all.
    assert (ROOT / "wp-content" / "uploads" / "2026" / "06" / "pink_logo_email_360.png").exists()


def test_tab_icon_is_square():
    # Pages used to point the tab icon at the wide wordmark, which the browser
    # squashed into a 16px smear. The icon is now a square tile in favicon.ico.
    import struct

    ico = (ROOT / "favicon.ico").read_bytes()
    count = struct.unpack("<H", ico[4:6])[0]
    sizes = {(ico[6 + 16 * i], ico[7 + 16 * i]) for i in range(count)}
    assert {(16, 16), (32, 32), (48, 48)} <= sizes, sizes
    touch = (ROOT / "apple-touch-icon.png").read_bytes()
    assert struct.unpack(">II", touch[16:24]) == (180, 180)
    for p in PAGES:
        text = p.read_text(encoding="utf-8")
        assert 'href="/assets/logo.png"' not in text, p
        if 'http-equiv="refresh"' not in text:  # redirect stubs fall back to /favicon.ico
            assert 'rel="icon" href="/favicon.ico"' in text, p


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
    # HB, 18 Sep 2026, firm-wide and absolute: never attack another firm or
    # another accountant. It is unprofessional, and an owner who liked their
    # last accountant hears it as an insult to their judgement.
    #
    # The sell is structural and stands on its own: hospitality moves weekly,
    # an annual reporting cycle lands after the year has closed. That point
    # needs no comparison to anyone.
    #
    # "current accountant" and "outgoing accountant" stay allowed: /switching/
    # has to name the other party to explain a handover, and it does so
    # neutrally, including stating that their working papers are their
    # property.
    banned = (
        "autopsy",
        "old accountant",
        "files and forgets",
        "most accountants",
        "other accountants",
        "typical accountant",
        "traditional accounting",
        "traditional accountant",
        "unlike other",
        "unlike most",
        "your accountant never",
        "cheap accountant",
        "bad accountant",
        "wrong accountant",
        # 24 Sep 2026 review: these got through and were live.
        "plenty of",
        "fewer can",
        "most bookkeeping",
        "should be doing",
        "stay somewhere",
    )
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


RELAY = {
    "contact/index.html": "contact-form",
    "index.html": "margin-check",
    "margin-check/index.html": "margin-check",
}


def test_lead_capture_and_tracking():
    # Google Ads spent $255 against zero conversions because the site could
    # neither capture a lead nor report one. This holds the whole chain: the
    # forms exist, the events fire, and every form says what it does with
    # what it collects.
    nav = (ROOT / "nav.js").read_text(encoding="utf-8")
    track = (ROOT / "track.js").read_text(encoding="utf-8")
    assert 'gtag("event", "phone_click"' in nav, "phone clicks are not counted"
    assert "form[data-relay]" in nav, "the shared enquiry relay is gone"
    assert 'gtag("event", "generate_lead", lead)' in nav
    assert "lead_source: source" in nav
    assert "connect.facebook.net" in track, "Meta pixel is not installed"
    assert 'fbq("track", "PageView")' in track
    assert "26989404134047568" in track
    assert "window.pinkHash" in track
    assert "SHA-256" in track
    mc = (ROOT / "margin-check" / "index.html").read_text(encoding="utf-8")
    assert "</html>" in mc
    assert mc.index("/margin-check.js") < mc.index("</body>")
    assert mc.strip().endswith("</html>")

    for rel, method in RELAY.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert f'data-relay="{method}"' in text, rel
        assert 'method="post"' in text, f"{rel} would fall back to GET"
        for field in ('name="name"', 'name="email"', 'name="mobile"'):
            assert field in text, f"{rel} is missing {field}"
        assert 'name="_gotcha"' in text, f"{rel} has no spam trap"
        assert 'href="/privacy/">Privacy Policy</a>' in text, f"{rel} has no consent line"
        # The relay posts to a third party, so the page has to be allowed to
        # reach it. A form that silently fails CSP looks identical to a form
        # nobody used.
        assert "https://formsubmit.co" in text, f"{rel} CSP would block the relay"
        assert 'String(json.success) === "false"' in nav


def test_venue_figures_never_leave_the_browser():
    # A venue's takings, wages and rent are the visitor's financial data. The
    # calculator may hold them; the relay to a third-party form service may
    # not. This is the line the opt-in mailto was built to protect and it has
    # to survive every later edit to these pages.
    for rel in ("index.html", "margin-check/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        start = text.index('id="pmcLead"')
        lead = text[start:text.index("</form>", start)]
        for leak in ("sales", "wages", "cogs", "rent", "other", "revenue"):
            assert f'name="{leak}"' not in lead, f"{rel} would post {leak} to the relay"

        # No name attribute and no action means a failed script cannot fall
        # back to a native GET that puts those figures in the URL.
        start = text.index('id="pmc-calc"')
        calc = text[start:text.index("</form>", start)]
        assert "name=" not in calc, f"{rel} calculator fields would submit"
        assert "action=" not in calc, f"{rel} calculator has a submit target"


def test_margin_check_completion_reaches_both_ad_platforms():
    # Completing the calculator is the strongest signal a visitor gives
    # without handing over contact details, and it is what the Meta warm
    # audience is built from. It fired to Google only, so Meta could neither
    # retarget those people nor learn from them, and paid budget bought the
    # same cold traffic twice.
    js = (ROOT / "margin-check.js").read_text(encoding="utf-8")
    assert "pink_margin_check_complete" in js, "Google event missing"
    assert "pinkMeta(" in js, "Meta event missing - Google-only again"

    # CompleteRegistration, not Lead. nav.js owns Lead for real form submits
    # where an email or phone was given; reusing it here would inflate the
    # lead count both platforms bid against.
    assert "CompleteRegistration" in js, "wrong Meta event for the calculator"
    assert 'pinkMeta("Lead"' not in js, "calculator must not count as a Lead"

    # The event names the tool and nothing else. A venue's figures do not
    # leave the browser through an analytics call either.
    call = js[js.index("pinkMeta("):]
    call = call[:call.index(")")]
    for leak in ("sales", "wages", "cogs", "rent", "value", "revenue"):
        assert leak not in call, f"margin check would send {leak} to Meta"


def test_margin_check_cache_bust_is_uniform():
    # The page builder emitted an older version string than the pages it
    # regenerates, which serves visitors the previous script and silently
    # reverts any fix to it. One version everywhere, or the fix never ships.
    refs = set()
    for p in list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.py")):
        refs.update(re.findall(r"margin-check\.js\?v=([a-z0-9]+)", p.read_text(encoding="utf-8")))
    assert len(refs) == 1, f"margin-check.js served under mixed versions: {sorted(refs)}"


def test_paid_landing_page_feeds_both_platforms():
    # /margin/ is the paid landing page. It ships its own tracking rather than
    # loading track.js, so a placeholder pixel id here is invisible until a
    # month of Meta budget has bought an audience that was never recorded.
    # The kit this page came from had META_PIXEL_ID as XXXXXXXXXXXXXXX.
    lp = (ROOT / "margin" / "index.html").read_text(encoding="utf-8")
    track = (ROOT / "track.js").read_text(encoding="utf-8")

    # "Pink Accounting's Pixel" - the only dataset in the business, and the one
    # the ad account can build audiences from. The site fired at
    # 26989404134047568 until 18 Sep 2026; Events Manager routes that id as an
    # app and returns "content isn't available", so every event went nowhere.
    PIXEL = "1237708438188688"
    assert PIXEL in lp, "paid landing page lost the real Meta pixel"
    assert PIXEL in track, "track.js lost the real Meta pixel"
    assert "META_PIXEL_ID: 'X" not in lp, "placeholder pixel id is back"

    # The dead id must never come back as a value. It is allowed to appear in a
    # comment, because both files explain why it was removed.
    for name, body in (("margin/index.html", lp), ("track.js", track)):
        for form in ('"26989404134047568"', "'26989404134047568'"):
            assert form not in body, f"{name} restored the dead pixel"

    # Paid traffic only. Letting this rank would split organic authority with
    # /margin-check/, which is the page the site already points at.
    assert 'content="noindex' in lp, "paid landing page must not be indexed"

    # The honeypot is the only defence against bot form spam here, since the
    # page deliberately has no third-party form relay.
    assert 'name="company_website"' in lp, "spam honeypot removed"

    # Venue takings are collected on this page. The mailto fallback keeps them
    # in the visitor's own mail client. If a FORM_ENDPOINT is ever wired, that
    # decision needs a human looking at where a venue's sales figure lands.
    assert "mailto:admin@pinktax.com.au" in lp, "lead fallback relay changed"


def test_identity_first_on_every_first_screen():
    # HB 24 Sep 2026: people must know us as accountants, bookkeepers and tax
    # agents first, then hospitality. The ad-matched line sits under the H1.
    trust = "Accountants, bookkeepers and tax agents for hospitality."
    for rel in ("index.html", "margin/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S).group(1)
        assert h1 == "Accountants, bookkeepers and tax agents for hospitality", rel
        # The H1 says who we are, so the line under the buttons carries the offer.
        assert 'class="trust-line">Bookkeeping, payroll, BAS and tax' in text, rel
        assert "$990 + GST a month" in text, rel
    margin = (ROOT / "margin" / "index.html").read_text(encoding="utf-8")
    assert 'class="hook" id="hl"' in margin, "ad message match must target the hook, not the H1"
    for p in PAGES:
        if p in STUBS:
            continue
        text = p.read_text(encoding="utf-8")
        assert "BAS &amp; tax agent" not in text and "BAS & tax agent" not in text, p
        if 'class="phone"' in text:
            assert 'class="call-icon"' in text, f"{p}: no tap-to-call"


def test_guide_pages_carry_the_trust_line():
    for slug in ("cafe-accountant", "restaurant-accountant", "hospitality-bookkeeping", "hospitality-payroll"):
        text = (ROOT / slug / "index.html").read_text(encoding="utf-8")
        assert 'class="trust-line"' in text, slug


def test_hospitality_only_and_food_cost_said_right():
    why = (ROOT / "why-pink" / "index.html").read_text(encoding="utf-8")
    assert "beyond hospitality" not in why
    food = (ROOT / "restaurant-food-cost-percentage" / "index.html").read_text(encoding="utf-8")
    assert "It is purchases divided by sales" not in food


def test_booking_button_on_the_first_screen_of_money_pages():
    book = (ROOT / "book" / "index.html").read_text(encoding="utf-8")
    assert book.index('data-event="book-calendar"') < book.index("What happens on the call")
    margin = (ROOT / "margin" / "index.html").read_text(encoding="utf-8")
    assert margin.index('data-ev="cta_top"') < margin.index('<ul class="ticks">')


def test_ad_page_counts_a_lead_only_when_it_was_sent():
    # 24 Sep 2026: the /margin/ form had no endpoint, opened a mail app and
    # still told the visitor "your details are with us" and fired a Lead.
    m = (ROOT / "margin" / "index.html").read_text(encoding="utf-8")
    assert "FORM_ENDPOINT: 'https://formsubmit.co/ajax/admin@pinktax.com.au'" in m
    assert "setTimeout(done" not in m and "catch(function(){ done(); })" not in m
    assert "String(j.success)==='false'" in m and 'id="sendFail"' in m
    assert "offshore" not in m


def test_no_implied_contrast_lines():
    for rel in ("index.html", "contact/index.html", "switching/index.html", "why-pink/index.html", "margin/index.html", "restaurant-accountant/index.html"):
        text = (ROOT / rel).read_text(encoding="utf-8").lower()
        for phrase in ("ticket queue", "a queue", "easier than staying put", "not a service", "honest tiering"):
            assert phrase not in text, (rel, phrase)



def test_headings_do_not_skip_a_level():
    # Lighthouse 24 Sep 2026: footer h4 after a page h2 skipped a level.
    for p in PAGES:
        if p in STUBS:
            continue
        levels = [int(m) for m in re.findall(r"<h([1-6])[ >]", p.read_text(encoding="utf-8"))]
        for before, after in zip(levels, levels[1:]):
            assert after <= before + 1, f"{p}: h{before} jumps to h{after}"
