"""One-time scaffold that generated this site on 12 September 2026.

DO NOT RUN. The HTML is hand-maintained now and this script was never kept in
step with it. Running it would revert, among other things:

  * the hero rebuild (.hero-lede / .hero-shot)
  * the "Is profit lying to you?" video block
  * the Google reviews section
  * the scope-of-work section
  * the removal of Service Profit wording from /contact/

That last one is a firm rule, not a preference: Pink is hospitality-only on
every public surface. Re-running this would silently put the breach back on
the live site.

Either retire this file or bring it back in step with the HTML deliberately.
The guard below stops an accident; it is not a substitute for that decision.
"""

import os
import sys
from pathlib import Path
from shared import (
    MSBOOK,
    ORIGIN,
    REVIEW,
    business_node,
    enquiry_form,
    faq_node,
    footer,
    head,
    jsonld,
    nav,
)

ROOT = Path(__file__).resolve().parents[1]


def write(rel, html):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", rel, path.stat().st_size)


def home():
    h = head(
        "Hospitality Accounting Australia | Pink Accounting",
        "Your margins are leaking. We find where. Bookkeeping, payroll and monthly margin protection for hospitality businesses across Australia.",
        "/",
        extra=jsonld(business_node()),
    )
    body = f"""{nav("home")}
  <main id="main">
    <section class="hero">
      <div class="wrap">
        <span class="eyebrow">Hospitality Margin Protection</span>
        <h1>Your margins are leaking. We find where.</h1>
        <p class="lead">We've found up to $70,000 a year leaking from a $1M venue — the wrong shift design, food waste, even the wrong opening hours. Pink finds it before the BAS does, and keeps finding it every month.</p>
        <div class="cta">
          <a class="btn btn-primary" href="/book/" data-event="home-book">Book a 15-minute call</a>
          <a class="btn btn-outline" href="/margin-check/">Free 60-second Margin Check</a>
        </div>
        <p class="creds">5.0 rated on Google · Registered Tax Agent 26284368 · Hospitality businesses across Australia</p>
      </div>
    </section>
    <section class="page">
      <div class="wrap">
        <span class="eyebrow">The problem</span>
        <h2>You find out in July. Your costs move every week.</h2>
        <p class="lead">A tax return is an autopsy — it tells you what happened a year after you could do anything about it. Hospitality margins don't work on that timeline.</p>
        <div class="grid3">
          <article class="card"><h3>The P&amp;L lands too late</h3><p>Twelve months after the decisions that shaped it. By the time you see the number, it's already spent.</p></article>
          <article class="card"><h3>Costs drift constantly</h3><p>Wages creep, suppliers nudge prices, waste becomes a habit. An annual check can't catch a weekly problem.</p></article>
          <article class="card"><h3>Nobody flags it</h3><p>Your old accountant files and forgets. We watch the margin every month and tell you the moment a line moves.</p></article>
        </div>
      </div>
    </section>
    <section class="page" id="pink-pricing">
      <div class="wrap">
        <span class="eyebrow">The plans</span>
        <h2>A system that protects your margin.</h2>
        <p class="lead">Monthly, ex GST. Start where your venue needs to — dial it up when you're ready.</p>
        <div class="grid3">
          <article class="card"><span class="eyebrow">Most venues</span><h3>Hospitality Margin Protection</h3><p class="price">$990 + GST / month</p><p>Every month we run a margin protection review — wages %, COGS drift and overhead pressure. Bookkeeping, payroll (up to 5 staff) and BAS sit underneath it.</p></article>
          <article class="card"><h3>Compliance Foundations</h3><p class="price">$550 + GST / month</p><p>Structure and certainty while you keep your own books.</p></article>
          <article class="card"><h3>Weekly Visibility</h3><p class="price">$1,950 + GST / month</p><p>Weekly snapshots and early-warning signals, not month-old reports.</p></article>
        </div>
        <p>Ready to Scale is $3,500+ + GST a month, application only. We'll tell you honestly if a cheaper tier fits.</p>
        <div class="cta"><a class="btn btn-primary" href="/book/">Book a 15-minute call</a></div>
      </div>
    </section>
    <section class="meet">
      <div class="wrap split">
        <div>
          <span class="eyebrow">Meet Pink</span>
          <h2>Hello, I'm Pink.</h2>
          <p>I'm Huong Bui. I founded Pink Accounting in 2020. Today we work with hospitality businesses across Australia. When I look at a venue, I watch the numbers that decide whether this month works — and tell you while there's still time.</p>
          <p>Registered Tax Agent 26284368 · MIPA / AFA · Master of Professional Accounting (Griffith)</p>
          <a class="btn btn-primary" href="/why-pink/">Why Pink</a>
        </div>
        <div>
          <img src="/assets/pink-portrait.jpg" alt="Pink, founder of Pink Accounting" width="838" height="1059">
        </div>
      </div>
    </section>
    <section class="page">
      <div class="wrap">
        <h2>Stop finding out in July.</h2>
        <p class="lead">See where your margin is going — and keep seeing it, every month. A direct 15-minute call with Pink. No pitch deck.</p>
        <div class="cta">
          <a class="btn btn-primary" href="/book/">Book a 15-minute call</a>
          <a class="btn btn-outline" href="{REVIEW}" rel="noopener">See Google reviews</a>
        </div>
      </div>
    </section>
  </main>
{footer()}"""
    return h + body


def system():
    h = head(
        "The Pink System | Monthly Margin Protection for Venues",
        "Clean bookkeeping, disciplined payroll and monthly margin visibility in one practical system for hospitality.",
        "/system/",
    )
    body = f"""{nav("system")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">The Pink System</span>
      <h1>Hospitality numbers, read in time to act.</h1>
      <p class="lead">Clean bookkeeping, disciplined payroll and monthly margin visibility in one practical system. Tax and BAS still matter; they sit on top of books you can use to run the venue.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/margin-check/">Run the free Margin Check</a>
        <a class="btn btn-outline" href="/book/">Book a 15-minute call</a>
      </div>
      <div class="grid3">
        <article class="card"><span class="eyebrow">01 · Books</span><h2>Clean source numbers</h2><p>Suppliers, bank activity, POS evidence and coding kept ready for decisions — not reconstructed at year end.</p></article>
        <article class="card"><span class="eyebrow">02 · Payroll</span><h2>Wages seen against sales</h2><p>Payroll and super workflows that respect roster reality and keep wage movement visible.</p></article>
        <article class="card"><span class="eyebrow">03 · Performance</span><h2>Margins made readable</h2><p>Monthly profit and loss visibility across wages, food cost, rent and overhead, with a clear next conversation.</p></article>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def why():
    h = head(
        "Why Pink | Bookkeeping, Payroll &amp; Margin Specialists",
        "Hospitality is our specialisation. Award rates, COGS benchmarks, weekly cash. Registered Tax Agent 26284368.",
        "/why-pink/",
    )
    body = f"""{nav("why")}
  <main id="main" class="page">
    <div class="wrap prose">
      <h1>Why Pink</h1>
      <h2>One industry, deep.</h2>
      <p>Hospitality is our specialisation — award rates, penalty loadings, COGS benchmarks, seasonal cashflow. We also act for a select group of established businesses beyond hospitality under our general engagement terms.</p>
      <h2>A system, not a service.</h2>
      <p>Your file runs on documented coding rules, GST logic and review gates. The work is checked against the source, every time.</p>
      <h2>Honest tiering.</h2>
      <p>If the entry tier is all you need, that's what we'll recommend. The ladder exists so you never pay for altitude you don't use.</p>
      <h2>Registered and accountable.</h2>
      <p>Registered Tax Agent 26284368. Our obligations to you are public — see <a href="/working-with-us/">Working with us</a>.</p>
      <h2>Who we say no to</h2>
      <p>Venues wanting “just BAS” with no system improvement. Price shopping. High transaction volumes on entry tiers. If that's you, we're the wrong firm — and we'll say so on the call.</p>
      <h2>How Pink started</h2>
      <p>Pink was founded in 2020, in the middle of COVID, helping South-East Queensland business owners through the hardest trading of their lives. Hospitality copped it worst. That work became the Hospitality Financial Performance System. The firm is led by Huong (Pinky) Bui — Master of Professional Accounting (Griffith), MIPA AFA, Registered Tax Agent 26284368.</p>
      <p>The practice began in 2020 and incorporated as Pink Accounting &amp; Tax Solutions Pty Ltd in November 2024.</p>
      <div class="cta"><a class="btn btn-primary" href="/book/">Book the call</a></div>
    </div>
  </main>
{footer()}"""
    return h + body


def book():
    h = head(
        "Book a Call | Pink Accounting, Brendale QLD",
        "Book a 15-minute call with Pink. Revenue, staff, what is hurting, where the venue sits now, and where you want it in 12 months.",
        "/book/",
    )
    body = f"""{nav("book")}
  <main id="main" class="page">
    <div class="wrap book-wide">
      <span class="eyebrow">Book</span>
      <h1>Book your 15-minute call</h1>
      <p class="lead">A few questions first so the call is not wasted. Then pick a time. Direct with the principal. Hospitality only on this page.</p>
      <h2>Before you pick a time</h2>
      <p>Revenue, staff, what is hurting, where the business sits now, and where you want it in 12 months. We read this before the call.</p>
{enquiry_form("book")}
      <section class="pick-time" id="pick-time">
        <h2>Then pick a time</h2>
        <p>Microsoft Bookings opens as a full page so the calendar is not cramped. Use the same email you put on the form.</p>
        <a class="btn btn-primary" href="{MSBOOK}" rel="noopener" data-event="book-calendar">Open full-screen booking</a>
      </section>
      <p class="creds">Rather talk now? Call <a href="tel:+61735446386">07 3544 6386</a> or email <a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a>.</p>
    </div>
  </main>
{footer()}"""
    return h + body


def contact():
    h = head(
        "Contact Pink Accounting | Bookkeeping &amp; Payroll, Brendale",
        "Talk to Pink at Shop 15A, 18-22 Kremzow Rd, Brendale QLD. 07 3544 6386. admin@pinktax.com.au.",
        "/contact/",
        extra=jsonld(business_node()),
    )
    body = f"""{nav("contact")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Contact Pink</span>
      <h1>Talk to the accountant. Not a ticket queue.</h1>
      <p class="lead">Bring the question, the messy numbers or the BAS you have been avoiding. You will speak directly with Pink.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/book/">Book a 15-minute call</a>
        <a class="btn btn-outline" href="tel:+61735446386">Call 07 3544 6386</a>
      </div>
      <div class="grid3">
        <section class="card"><span class="eyebrow">Phone</span><h2><a href="tel:+61735446386">07 3544 6386</a></h2><p>Mon–Fri, 9:00am–4:30pm. Saturday by appointment.</p></section>
        <section class="card"><span class="eyebrow">Email</span><h2><a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a></h2><p>The firm mailbox. A person reads it.</p></section>
        <section class="card"><span class="eyebrow">Visit</span><h2>Brendale QLD 4500</h2><p>Shop 15A, 18–22 Kremzow Rd. Hospitality clients of the firm sit on this site. Service Profit (HVAC, electrical, construction) is a separate site.</p></section>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def margin_check():
    h = head(
        "Free 60-Second Margin Check | Pink Accounting",
        "Five numbers off your last month. In sixty seconds you will see where your venue is most likely leaking margin.",
        "/margin-check/",
    )
    body = f"""{nav("check")}
  <main id="main" class="page">
    <div class="wrap">
      <span class="eyebrow">Margin Self-Check</span>
      <h1>Where is your venue leaking margin?</h1>
      <p class="lead">Five numbers off your last month. In sixty seconds you will see where your money is most likely going, before BAS time tells you.</p>
      <form class="enquiry hours-check" id="pmc-calc">
        <div class="fields">
          <label>Average weekly sales
            <input type="number" id="pmc-sales" min="0" step="100" required inputmode="decimal" placeholder="Total takings, excluding GST">
          </label>
          <label>Weekly wages
            <input type="number" id="pmc-wages" min="0" step="50" inputmode="decimal" placeholder="Including super and on-costs">
          </label>
          <label>Weekly food &amp; beverage cost
            <input type="number" id="pmc-cogs" min="0" step="50" inputmode="decimal">
          </label>
          <label>Monthly rent
            <input type="number" id="pmc-rent" min="0" step="100" inputmode="decimal" placeholder="Leave blank if you own it">
          </label>
          <label>Other weekly running costs
            <input type="number" id="pmc-other" min="0" step="50" inputmode="decimal">
          </label>
        </div>
        <button class="btn btn-primary" type="submit">Show me my leaks</button>
        <p class="form-note" id="pmc-err" hidden>Please enter your weekly sales. That is the number everything else is measured against.</p>
      </form>
      <section id="pmc-results" hidden>
        <p id="pmc-hl-label" class="eyebrow">Your biggest leak</p>
        <h2 id="pmc-hl-text"></h2>
        <p id="pmc-hl-note"></p>
        <div id="pmc-metrics" class="grid3"></div>
        <p>This is a sketch from the numbers you typed. Not your file. Not tax advice. On the call we look at the real books.</p>
        <a class="btn btn-primary" href="/book/">Book a 15-minute call</a>
      </section>
    </div>
  </main>
{footer()}
<script src="/margin-check.js?v=h1"></script>
"""
    return h + body


def working():
    h = head(
        "Your rights and our obligations | Pink Accounting",
        "Registered Tax Agent 26284368. How to check us, how to complain, and what we owe you.",
        "/working-with-us/",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap prose">
      <h1>Your rights and our obligations</h1>
      <p>We're a registered tax practitioner. That registration comes with public obligations to you — here they are, plainly.</p>
      <h2>The TPB public register</h2>
      <p>Search <a href="https://www.tpb.gov.au/public-register" rel="noopener">tpb.gov.au/public-register</a>. Our registration number is <strong>26284368</strong>.</p>
      <h2>How to make a complaint</h2>
      <p>Tell us first: <a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a> or 07 3544 6386. You can also complain to the TPB at <a href="https://www.tpb.gov.au/complaints" rel="noopener">tpb.gov.au/complaints</a>.</p>
      <h2>Verify us</h2>
      <ul>
        <li>Tax agent registration 26284368 — TPB public register.</li>
        <li>ABN 51 682 301 891 — ABN Lookup.</li>
        <li>Company name — ASIC.</li>
        <li>Professional membership — IPA (MIPA AFA).</li>
      </ul>
      <p>Practising as Pink since 2020; incorporated as Pink Accounting &amp; Tax Solutions Pty Ltd in November 2024 — which is why our current ABN shows a 2024 start date.</p>
      <h2>Disclosure statements</h2>
      <p>No prescribed events under section 45 of the Tax Agent Services (Code of Professional Conduct) Determination 2024 have occurred in the last 5 years. Our registration is not subject to conditions limiting the scope of services we can provide.</p>
      <div class="cta"><a class="btn btn-primary" href="/book/">Book the call</a></div>
    </div>
  </main>
{footer()}"""
    return h + body


def privacy():
    h = head(
        "Privacy policy | Pink Accounting",
        "How Pink Accounting handles personal information under the Privacy Act 1988 and the Australian Privacy Principles.",
        "/privacy/",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap prose">
      <h1>Privacy policy</h1>
      <p>Last updated 8 June 2026.</p>
      <p>Pink Accounting &amp; Tax Solutions Pty Ltd (ABN 51 682 301 891) handles personal information under the Privacy Act 1988 (Cth) and the Australian Privacy Principles, and keeps client information confidential under the Tax Agent Services Act 2009 professional code.</p>
      <h2>What we collect and why</h2>
      <p>If you book a call or contact us, we collect what you give us — name, business name, contact details, and what you tell us about your situation — to respond and provide our services. Client engagements involve further information collected under our letter of engagement.</p>
      <h2>Marketing</h2>
      <p>We only send marketing emails if you've expressly opted in. We never sell or rent your details.</p>
      <h2>Storage and disclosure</h2>
      <p>Your information is stored in our Microsoft 365 environment. We disclose personal information only as needed to deliver our services, where the law requires it, or with your consent.</p>
      <h2>Overseas disclosure</h2>
      <p>We use reputable cloud providers and may use limited offshore or virtual support staff for administrative tasks. Core professional work is performed or reviewed in Australia. Our letter of engagement sets these arrangements out in full.</p>
      <h2>Access, correction and complaints</h2>
      <p><a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a> or 07 3544 6386. You can also complain to the OAIC at oaic.gov.au.</p>
    </div>
  </main>
{footer()}"""
    return h + body


def terms():
    h = head(
        "Terms of Use | Pink Accounting",
        "Terms for using pinktax.com.au, operated by Pink Accounting & Tax Solutions Pty Ltd.",
        "/terms/",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap prose">
      <h1>Terms of Use</h1>
      <p>Last updated 14 June 2026.</p>
      <p>These terms govern your use of this website (pinktax.com.au), operated by Pink Accounting &amp; Tax Solutions Pty Ltd (ABN 51 682 301 891). By using this site you agree to these terms.</p>
      <h2>General information only</h2>
      <p>The information on this website is general in nature. It is not professional, tax, accounting, financial or legal advice. Engaging us as a client requires a signed letter of engagement.</p>
      <h2>No guarantee of outcomes</h2>
      <p>Any examples, figures or case studies on this site are illustrations only. Results vary.</p>
      <h2>Intellectual property</h2>
      <p>All content on this site is owned by or licensed to Pink Accounting &amp; Tax Solutions Pty Ltd.</p>
      <h2>Governing law</h2>
      <p>These terms are governed by the laws of Queensland, Australia.</p>
      <p>Questions: admin@pinktax.com.au or 07 3544 6386.</p>
    </div>
  </main>
{footer()}"""
    return h + body


def feedback():
    h = head(
        "Feedback | Pink Accounting",
        "Leave a Google review or tell us privately. Both come straight to Pink.",
        "/feedback/",
    )
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <h1>How did we do?</h1>
      <div class="grid3">
        <article class="card"><h2>Happy with Pink?</h2><p>A 30-second Google review helps other owners find a specialist they can trust.</p><a class="btn btn-primary" href="{REVIEW}" rel="noopener">Leave a Google review</a></article>
        <article class="card"><h2>Something we could do better?</h2><p>We'd rather hear it from you first. Tell us privately and we'll be in touch.</p><a class="btn btn-outline" href="mailto:amelia@pinktax.com.au?subject=Private%20feedback%20for%20Pink">Tell us privately</a></article>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def lander(slug, title, description, h1, lead, extra=""):
    h = head(title, description, f"/{slug}/")
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="cta">
        <a class="btn btn-primary" href="/margin-check/">Free 60-second Margin Check</a>
        <a class="btn btn-outline" href="/book/">Book a 15-minute call</a>
      </div>
      {extra}
    </div>
  </main>
{footer()}"""
    return h + body


def page_404():
    h = head("Page not found | Pink Accounting", "That page is not here. Try home, the system, or book a call.", "/404.html")
    body = f"""{nav()}
  <main id="main" class="page">
    <div class="wrap">
      <h1>That page is not here.</h1>
      <p class="lead">Try the home page, the system, or book a 15-minute call.</p>
      <div class="cta">
        <a class="btn btn-primary" href="/">Home</a>
        <a class="btn btn-outline" href="/book/">Book a call</a>
      </div>
    </div>
  </main>
{footer()}"""
    return h + body


def sitemap():
    urls = [
        "/",
        "/system/",
        "/why-pink/",
        "/book/",
        "/contact/",
        "/margin-check/",
        "/working-with-us/",
        "/privacy/",
        "/terms/",
        "/feedback/",
        "/hospitality-accountant-brisbane/",
        "/restaurant-cafe-bookkeeping-brendale/",
        "/accountant-brendale/",
    ]
    rows = "\n".join(f"  <url><loc>{ORIGIN}{u}</loc></url>" for u in urls)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "\n</urlset>\n"


def robots():
    return f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n"


if __name__ == "__main__":
    if os.environ.get("PINK_ALLOW_STALE_REGEN") != "1":
        sys.exit(
            "build_pages.py is a one-time scaffold and is out of step with the "
            "live HTML. Running it would revert hand-made changes, including "
            "the removal of Service Profit wording from /contact/, which is a "
            "hospitality-only compliance rule.\n"
            "Read the module docstring. If you have genuinely re-synced this "
            "script with the HTML, set PINK_ALLOW_STALE_REGEN=1."
        )
    write("index.html", home())
    write("system/index.html", system())
    write("why-pink/index.html", why())
    write("book/index.html", book())
    write("contact/index.html", contact())
    write("margin-check/index.html", margin_check())
    write("working-with-us/index.html", working())
    write("privacy/index.html", privacy())
    write("terms/index.html", terms())
    write("feedback/index.html", feedback())
    write(
        "hospitality-accountant-brisbane/index.html",
        lander(
            "hospitality-accountant-brisbane",
            "Hospitality Bookkeeping & Payroll Brisbane | Margins & P&L",
            "Bookkeeping, payroll and a clear P&L for Brisbane cafes and restaurants. Pink Accounting, Brendale.",
            "Hospitality bookkeeping, payroll &amp; P&amp;L for Brisbane venues.",
            "Pink Accounting is built for café and restaurant owners who need clean books, on-time payroll, and a clear profit &amp; loss — not a firm that only shows up at tax time.",
            "<p>Shop 15A, 18–22 Kremzow Rd, Brendale QLD 4500. Business clients only.</p>",
        ),
    )
    write(
        "restaurant-cafe-bookkeeping-brendale/index.html",
        lander(
            "restaurant-cafe-bookkeeping-brendale",
            "Restaurant &amp; cafe bookkeeping Brendale | Pink Accounting",
            "Bookkeeping, payroll and P&L built around venue reality. Brendale office, hospitality across Australia.",
            "Bookkeeping, payroll &amp; P&amp;L built around venue reality.",
            "Suppliers, bank, coding and payroll kept clean so the monthly numbers are usable. Brendale. Brisbane North.",
        ),
    )
    write(
        "accountant-brendale/index.html",
        lander(
            "accountant-brendale",
            "Accountant Brendale | Pink Accounting",
            "Local access. Clear books. A useful P&L. Hospitality accountant in Brendale QLD.",
            "Local access. Clear books. A useful P&amp;L.",
            "Pink Accounting is in Brendale. Hospitality bookkeeping, payroll and tax. Direct with the principal.",
        ),
    )
    write("404.html", page_404())
    write("sitemap.xml", sitemap())
    write("robots.txt", robots())
