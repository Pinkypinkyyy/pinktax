"""Builds the hospitality search-architecture landing pages.

Unlike build_pages.py, this one IS maintained and safe to run. It owns only
the pages listed in PAGES below. Header, footer and the asset cache-buster are
lifted out of index.html at build time, so a nav or footer change on the home
page flows through here instead of drifting.

It runs site_identity.sync() first, so identity.json reaches every page
(including the footer this lifts) before anything is built. This script is
the site rebuild: after running it, git status should be clean.

Run from the repo root:  python3 tools/build_landing_pages.py
"""

import re
from pathlib import Path

import site_identity

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = site_identity.ORIGIN
AGENT = site_identity.LEGAL["tax_agent_number"]
ASIC = site_identity.LEGAL["asic_agent_number"]
OG = f"{ORIGIN}/assets/og.png"

CSP = (
    "default-src 'self'; img-src 'self' data: https://www.google-analytics.com "
    "https://www.googletagmanager.com https://www.google.com https://www.google.com.au "
    "https://www.facebook.com https://lh3.googleusercontent.com https://cdn.trustindex.io; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "script-src 'self' https://www.googletagmanager.com https://connect.facebook.net; "
    "connect-src 'self' https://www.google-analytics.com https://analytics.google.com "
    "https://www.googletagmanager.com https://region1.google-analytics.com https://www.google.com "
    "https://www.google.com.au https://www.facebook.com https://formsubmit.co; "
    "form-action 'self' mailto: https://formsubmit.co; media-src 'self'; base-uri 'self'"
)

BANDS = [
    ("Wage cost", "at or under 30% of sales", "35% is where we start calling it a leak"),
    ("Food and beverage cost", "at or under 36% of sales", "40% and the menu needs work"),
    ("Prime cost, wages plus stock", "at or under 62% of sales", "68% and the venue is running for someone else"),
    ("Rent", "at or under 10% of sales", "15% and the site has to earn its keep"),
]


def home_parts():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    header = home[home.index("  <header class=\"nav\""):home.index("</header>") + len("</header>")]
    # Search for </footer> from the site footer onwards: the reviews on the
    # home page use <footer> for the reviewer's name, and matching the first
    # one left every landing page with no footer at all.
    start = home.index("  <footer class=\"foot\"")
    footer = home[start:home.index("</footer>", start) + len("</footer>")]
    ver = {
        n: re.search(rf"/{n}\.(?:css|js)\?v=([a-z0-9]+)", home).group(1)
        for n in ("styles", "track", "nav")
    }
    return header, footer, ver


def head(slug, title, desc, ver, faqs):
    url = f"{ORIGIN}/{slug}/"
    faq_ld = ""
    if faqs:
        items = ",".join(
            '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
            % (json_str(q), json_str(a))
            for q, a in faqs
        )
        faq_ld = (
            '\n  <script type="application/ld+json">\n  '
            '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}\n  </script>' % items
        )
    return f"""<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index,follow">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG}">
  <meta property="og:locale" content="en_AU">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v={ver['styles']}">{faq_ld}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
"""


def json_str(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def bands_table():
    rows = "".join(
        f"<tr><td><strong>{name}</strong></td><td>{aim}</td><td>{warn}</td></tr>"
        for name, aim, warn in BANDS
    )
    return (
        '<div class="table-scroll" tabindex="0"><table class="scope">'
        "<thead><tr><th>Line</th><th>Where we want it</th><th>Where it starts costing you</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></div>"
        '<p class="table-hint">The bands we work to on a standard single-site venue. '
        "Licensed venues, function work and heavy takeaway sit differently, which is part of the conversation.</p>"
    )


def prose(sections):
    out = []
    for heading, body in sections:
        out.append(f"        <h2>{heading}</h2>")
        for item in body:
            out.append(f"        {item}")
    return "\n".join(out)


def faq_block(faqs):
    if not faqs:
        return ""
    items = "\n".join(
        f"          <details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    return f"""
    <section class="page">
      <div class="wrap">
        <span class="eyebrow">Questions we get</span>
        <h2>Straight answers.</h2>
        <div class="faq">
{items}
        </div>
      </div>
    </section>
"""


def page(slug, title, desc, h1, lead, sections, faqs, related):
    header, footer, ver = home_parts()
    rel = "".join(
        f'<a class="tier" href="/{r_slug}/"><span class="tname">{r_name}</span><p>{r_note}</p></a>'
        for r_slug, r_name, r_note in related
    )
    body = f"""{head(slug, title, desc, ver, faqs)}{header}

  <main id="main">
    <section class="page">
      <div class="wrap">
        <span class="eyebrow">Accountants · Bookkeepers · Tax agents · Hospitality</span>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        <div class="cta">
          <a class="btn btn-primary" href="/book/" data-event="{slug}-book">Book a 15-minute call</a>
          <a class="btn btn-outline" href="/margin-check/">Check your margin in 60 seconds</a>
        </div>
        <p class="trust-line">Accountants, bookkeepers and tax agents for hospitality. Most venues $990 + GST a month; from $550. Registered tax agent 26284368.</p>
      </div>
    </section>
    <section class="band band-bone">
      <div class="wrap">
        <div class="prose">
{prose(sections)}
        </div>
      </div>
    </section>{faq_block(faqs)}
    <section class="page">
      <div class="wrap">
        <span class="eyebrow">Keep reading</span>
        <h2>Related.</h2>
        <div class="tiers">{rel}</div>
      </div>
    </section>
    <section class="page close">
      <div class="wrap">
        <h2>Stop finding out in July.</h2>
        <p class="lead">Fifteen minutes, direct with Pink. We look at your real numbers and tell you where the margin is going.</p>
        <div class="cta">
          <a class="btn btn-primary" href="/book/">Book a 15-minute call</a>
          <a class="btn btn-outline" href="/margin-check/">Run the Margin Check</a>
        </div>
      </div>
    </section>
  </main>
{footer}
  <script src="/track.js?v={ver['track']}"></script>
  <script src="/nav.js?v={ver['nav']}"></script>
</body>
</html>
"""
    out = ROOT / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    return slug


CHECK = '<p><a href="/margin-check/">Run the 60-second Margin Check</a> on your own figures. It runs in your browser, and nothing is sent unless you choose to send it.</p>'
PLAN = '<p>Most venues sit on <a href="/#pink-pricing">Hospitality Margin Protection at $990 + GST a month</a>, which carries the bookkeeping, payroll for up to five staff and BAS oversight underneath the monthly margin review.</p>'

R_ACCT = ("restaurant-accountant", "Restaurant accountant", "What a specialist actually does for a restaurant.")
R_CAFE = ("cafe-accountant", "Cafe accountant", "Small tickets, high volume, thin margin.")
R_HBK = ("hospitality-bookkeeping", "Hospitality bookkeeping", "Books you can run a venue from.")
R_RBK = ("restaurant-bookkeeping", "Restaurant bookkeeping", "POS, suppliers and stock, reconciled weekly.")
R_PAY = ("hospitality-payroll", "Hospitality payroll", "Awards, penalties, STP and super.")
R_FOOD = ("restaurant-food-cost-percentage", "Food cost percentage", "How to work it out and where it should sit.")
R_WAGE = ("hospitality-wage-percentage", "Wage percentage", "The number that decides your month.")
R_MARGIN = ("restaurant-profit-margin", "Restaurant profit margin", "What is left after everything.")
R_BRIS = ("hospitality-accountant-brisbane", "Brisbane venues", "Local, Brendale office, Australia-wide clients.")

PAGES = [
    dict(
        slug="restaurant-accountant",
        title="Restaurant Accountant | Margin, Payroll, BAS | Pink Accounting",
        desc="A restaurant accountant who reads wages, food cost and prime cost every month, not once a year. Registered tax agent, hospitality only.",
        h1="A restaurant accountant who reads the month, not just the year.",
        lead="A restaurant's costs move week to week, so we work to that rhythm. The books stay current, the margin gets read every month, and the tax work happens on top of numbers you have already seen.",
        sections=[
            ("What a restaurant accountant does each month", [
                "<p>A restaurant is not a retail shop with a kitchen. The cost base moves weekly, the labour is rostered against trade that changes with the weather, and a supplier price rise lands without an email. So the job is not just lodgement. It is keeping the four numbers that decide the business visible while you can still act on them.</p>",
                bands_table(),
            ]),
            ("What we do every month", [
                "<ul><li>Bookkeeping kept current, including POS takings, supplier bills and stock movements</li>"
                "<li>Payroll run against the award, with wages read as a share of sales, not in isolation</li>"
                "<li>A margin review that names the line that moved and what it is worth over a year</li>"
                "<li>BAS and IAS prepared from books that are already reconciled</li>"
                "<li>Tax planning before 30 June, while there is still something to plan</li></ul>",
                PLAN,
            ]),
            ("Where restaurants actually lose money", [
                "<p>In our experience it is rarely one dramatic thing. It is shift design that puts staff on before the trade arrives, a menu that has not been recosted since the last supplier rise, waste that nobody measures because nobody owns it, and trading hours that cost more to keep open than they return. Each one is small. Together they are the difference between a profitable year and a tight one.</p>",
                "<p>In one $1M venue those three ordinary causes came to about $70,000 a year. That is one engagement, not a promise. Your number will be different.</p>",
                CHECK,
            ]),
            ("Working with Pink", [
                f"<p>We are a small specialist firm. You deal with the person responsible for your numbers, and you get them on WhatsApp between meetings. Registered Tax Agent {AGENT}, ASIC Registered Agent {ASIC}, based in Brendale and working with venues across Australia.</p>",
            ]),
        ],
        faqs=[
            ("Do you replace my bookkeeper?", "Usually yes. The margin work depends on the books being coded a particular way, so we prefer to run them. If you have a bookkeeper who is doing well, we can work alongside them instead."),
            ("Can you take over mid-year?", "Yes. We do a catch-up on the current year first so the comparatives mean something, then start the monthly cycle."),
            ("Do you work with more than one venue?", "Yes. Multi-venue groups get the same review per site plus a consolidated read, which is where Ready to Scale sits."),
        ],
        related=[R_CAFE, R_WAGE, R_FOOD],
    ),
    dict(
        slug="cafe-accountant",
        title="Cafe Accountant Australia | Wages, Food Cost, BAS | Pink",
        desc="A cafe accountant for high-volume, small-ticket venues. Monthly margin review, payroll, bookkeeping and BAS. Registered tax agent.",
        h1="Cafe accounting, where the margin is measured in cents.",
        lead="A cafe turns over a lot of small transactions on a thin margin. Twenty cents of milk, a barista rostered half an hour early, a supplier rise nobody noticed: none of it looks like much until you multiply it by a year of cups.",
        sections=[
            ("Why cafes need a tighter read than most businesses", [
                "<p>On a $3.50 flat white a few cents of drift is a rounding error. Across 300 coffees a day it is real money, and it never shows up as a line item you can point at. It shows up as a bank balance that does not match the profit and loss.</p>",
                "<p>The way to catch it is to read ratios rather than dollars, every month, against the same bands.</p>",
                bands_table(),
            ]),
            ("The cafe-specific traps", [
                "<ul><li><b>Open hours that do not pay.</b> The first and last ninety minutes of trade often carry full labour and almost no sales.</li>"
                "<li><b>Milk, cups and takeaway packaging.</b> These sit in cost of goods and creep quietly with supplier changes.</li>"
                "<li><b>Staff coffee and comps.</b> Small, constant, and almost never measured.</li>"
                "<li><b>GST coding on retail lines.</b> Some packaged goods are GST-free while anything sold for consumption on the premises is taxable, and a POS mapped once and never checked will quietly get it wrong.</li>"
                "<li><b>Casual loading and penalties.</b> A roster that works at ordinary rates can stop working on a Sunday.</li></ul>",
                CHECK,
            ]),
            ("What you get from us", [
                "<p>Books kept current from the POS and the bank, payroll run against the award, a monthly review that tells you what moved, and the compliance handled underneath it.</p>",
                PLAN,
            ]),
        ],
        faqs=[
            ("We are a small cafe. Is $990 a month worth it?", "A single point of wage cost or food cost on a $700,000 venue is $7,000 a year. That is the arithmetic the plan has to beat, and it is the first thing we look at on the call."),
            ("Do you set up the POS mapping?", "Yes, we check how takings, GST codes and tips flow into the file before the first review, because everything after that depends on it."),
        ],
        related=[R_HBK, R_FOOD, R_WAGE],
    ),
    dict(
        slug="hospitality-bookkeeping",
        title="Hospitality Bookkeeping Australia | Pink Accounting",
        desc="Hospitality bookkeeping that produces numbers you can run a venue from: POS takings, supplier bills, stock, payroll and reconciled bank.",
        h1="Bookkeeping you can actually run a venue from.",
        lead="Getting the BAS right is the minimum. Hospitality books also have to tell you, this month, whether the roster and the menu are still working.",
        sections=[
            ("The difference between compliant and useful", [
                "<p>A file can be perfectly compliant and still useless for running a venue. If every supplier invoice is coded to one catch-all cost of sales account, the BAS will be right and the margin work will be impossible. If takings land as a single deposit with no split between food, beverage and tips, nobody can tell you why last month moved.</p>",
                "<p>So we set the file up to answer operational questions first, and the compliance falls out of it.</p>",
            ]),
            ("What we keep current", [
                "<ul><li>POS takings, split by revenue stream, reconciled to the money that actually arrived</li>"
                "<li>Supplier bills coded to food, beverage, packaging and consumables separately</li>"
                "<li>Stock movements and counts where the venue runs them</li>"
                "<li>Payroll, super and STP filings</li>"
                "<li>Bank, card and delivery-platform settlements reconciled, including the fees taken out before the money lands</li>"
                "<li>Owner drawings, loans and related-party transactions kept clean for year end</li></ul>",
                "<p>Delivery platforms deserve their own mention. The deposit in your bank is net of commission, and if it is booked as revenue, your sales are understated and your margin looks better than it is.</p>",
            ]),
            ("Two people check the books before anything is lodged", [
                "<p>Before a BAS, a monthly report or a tax return goes out, the period is checked twice. One of us works through it. A second person, who did not do that work, reviews it in live Xero and signs it off the same day. Anything they disagree on goes back and is fixed in Xero, not explained away.</p>",
                "<ul><li>The bank in Xero agrees to your bank statement, to the cent</li>"
                "<li>Food, beverage and other supplier accounts agree to the suppliers' own statements, or each difference is named</li>"
                "<li>Every pay run is traced through STP, the bank and the super fund</li>"
                "<li>The BAS figures agree to the file and to what was lodged before</li>"
                "<li>Opening balances are checked against last year's finished figures, so an old period cannot quietly change</li></ul>",
                "<p>Once a BAS is lodged, that period is locked in Xero. Changing a locked period is the principal's decision, made in writing. The principal signs off every BAS and return before it is lodged.</p>",
            ]),
            ("Then the numbers get read", [
                "<p>Clean books are the input, not the output. Every month we read them against the bands below and tell you what changed.</p>",
                bands_table(),
                PLAN,
                CHECK,
            ]),
        ],
        faqs=[
            ("Which software do you work in?", "Xero, with the venue's POS feeding it. We can work with what you have if it is already in place and doing the job."),
            ("How far behind can we be?", "We have picked up files more than a year behind. It costs more to catch up than to maintain, but it is normal work."),
        ],
        related=[R_RBK, R_PAY, R_ACCT],
    ),
    dict(
        slug="restaurant-bookkeeping",
        title="Restaurant Bookkeeping | POS, Suppliers, Stock | Pink",
        desc="Restaurant bookkeeping done weekly: POS reconciliation, supplier bills, stock, payroll and a monthly margin read. Brendale and Australia-wide.",
        h1="Restaurant bookkeeping, done weekly, read monthly.",
        lead="A restaurant generates more transactions in a week than most small businesses do in a quarter. Left to the end of the quarter, it becomes a reconstruction job, and reconstruction tells you nothing you can use.",
        sections=[
            ("The weekly rhythm", [
                "<ul><li><b>Takings.</b> POS to bank, every day accounted for, card settlements matched net of fees.</li>"
                "<li><b>Suppliers.</b> Bills in as they arrive, coded by category, so food cost is a real number rather than an estimate.</li>"
                "<li><b>Payroll.</b> Run against the roster and the award, filed through STP.</li>"
                "<li><b>Stock.</b> Opening and closing counts where you run them, because without them food cost is only ever an approximation of purchases.</li></ul>",
                "<p>Purchases are not food cost. If you bought heavily in the last week of the month, purchases overstate what you actually used. Stock movement is what turns one into the other.</p>",
            ]),
            ("What it lets us tell you", [
                bands_table(),
                "<p>Once the file is current, the monthly review stops being a history lesson. It becomes a short conversation about two or three things worth changing.</p>",
                PLAN,
            ]),
            ("Common mess we fix on takeover", [
                "<ul><li>Everything coded to one cost of sales account</li>"
                "<li>Delivery platform deposits booked as gross sales, or as net sales with the commission lost</li>"
                "<li>Tips and surcharges treated as revenue when they are not</li>"
                "<li>Wages posted from the bank rather than from payroll, so super and PAYG do not tie out</li>"
                "<li>Owner purchases mixed through the business card with no separation</li></ul>",
                CHECK,
            ]),
        ],
        faqs=[
            ("Do we need to do stocktakes?", "For a real food cost number, yes, at least monthly. Without counts you have a purchases ratio, which tells you direction and not much else."),
            ("Can you deal with our suppliers directly?", "We handle the paperwork and the coding. Ordering and negotiation stay with you, though we will tell you which supplier moved and by how much."),
        ],
        related=[R_HBK, R_FOOD, R_MARGIN],
    ),
    dict(
        slug="hospitality-payroll",
        title="Hospitality Payroll | Awards, Penalties, STP, Super | Pink",
        desc="Hospitality payroll run against the award: penalties, casual loading, STP Phase 2 and super at 12%. Wages read as a share of sales every month.",
        h1="Hospitality payroll, run against the award and against your sales.",
        lead="Payroll is the biggest number in most venues and the easiest one to get quietly wrong. Two things have to be true at once: it has to be compliant, and it has to be affordable against the trade it is covering.",
        sections=[
            ("Compliant", [
                "<p>Most venues sit under the Hospitality Industry (General) Award 2020 or the Restaurant Industry Award 2020. Between them they carry casual loading, evening and weekend penalties, public holidays, split shifts, overtime and minimum engagement periods. Getting a classification wrong is not a rounding error, because it repeats every pay run until someone catches it.</p>",
                "<ul><li>Award interpretation and classification checked at setup, not assumed</li>"
                "<li>Single Touch Payroll Phase 2 reporting on every run</li>"
                "<li>Super guarantee at 12%, paid on time, because late super is not deductible</li>"
                "<li>Leave and long service accruals kept on the books instead of appearing as a surprise</li>"
                "<li>Termination pay, redundancy and final pay calculations when they come up</li></ul>",
            ]),
            ("Affordable", [
                "<p>Compliance tells you the wage bill is correct. It does not tell you whether you can carry it. That is a ratio question, and it is the one we answer every month.</p>",
                bands_table(),
                "<p>When wage cost runs hot, the cause is almost always structural rather than a rate problem: staff rostered before the trade arrives, too many hands on a shift that does not need them, or a split that would work better as two shorter shifts. We work it back to the roster rather than telling you to cut hours.</p>",
                CHECK,
            ]),
            ("What it costs", [PLAN]),
        ],
        faqs=[
            ("How many staff does the $990 plan cover?", "Payroll for up to five staff sits inside it. Beyond that we price the payroll separately so you are not paying for a tier you do not need."),
            ("Can you fix historic underpayments?", "We can calculate the exposure and help you correct it. Whether and how you disclose it is a decision we walk through with you."),
            ("Do you do rosters?", "No, the roster is yours. We tell you what it cost and where the structure is expensive."),
        ],
        related=[R_WAGE, R_HBK, R_ACCT],
    ),
    dict(
        slug="restaurant-food-cost-percentage",
        title="Restaurant Food Cost Percentage | How to Calculate It | Pink",
        desc="How to calculate food cost percentage properly using opening and closing stock, where it should sit, and what to do when it drifts.",
        h1="Food cost percentage, calculated properly.",
        lead="Food cost percentage is the number most owners quote and the one most often worked out wrong. Most owners work it out as purchases divided by sales. Food cost is what you used, not what you bought, and in a heavy buying month the quick version will mislead you.",
        sections=[
            ("The calculation", [
                "<p>Cost of goods used, not bought:</p>",
                "<p><b>Opening stock + purchases &minus; closing stock = cost of goods used.</b><br>"
                "<b>Cost of goods used &divide; sales for the same period &times; 100 = food cost percentage.</b></p>",
                "<p>Worked through: you start the month with $8,000 of stock, buy $34,000 and finish with $9,500. Cost of goods used is $32,500. On $90,000 of sales, that is 36.1%. If you had used purchases alone you would have read 37.8% and gone looking for a problem that was sitting in your coolroom.</p>",
                "<p>Use figures excluding GST, and keep beverage separate from food if you want the number to be actionable. A venue with strong bar trade and weak kitchen margin looks fine on a blended number and is not fine.</p>",
            ]),
            ("Where it should sit", [
                bands_table(),
                "<p>These are the bands we work to on a standard single-site venue. A pizza shop and a fine dining room are different businesses, and a venue with heavy function trade is different again. The band matters less than the direction it is moving.</p>",
            ]),
            ("When it drifts, look here first", [
                "<ul><li><b>Supplier price rises.</b> They arrive without notice. Compare unit prices on your three biggest lines quarterly.</li>"
                "<li><b>Portion control.</b> A protein portion 15% heavier than the recipe is a permanent margin cut.</li>"
                "<li><b>Waste and spoilage.</b> If nobody records it, it is invisible, and invisible costs do not get fixed.</li>"
                "<li><b>Menu mix.</b> Your margin can fall while every recipe stays the same, if customers move toward the dishes that cost you more.</li>"
                "<li><b>Theft and comps.</b> Unmeasured staff meals and comped dishes are real food cost.</li>"
                "<li><b>Stale menu pricing.</b> A menu costed two years ago is priced against two-year-old inputs.</li></ul>",
                CHECK,
                PLAN,
            ]),
        ],
        faqs=[
            ("What if we do not count stock?", "Then you have a purchases ratio, not a food cost. It is still worth watching for direction, but do not make pricing decisions on it."),
            ("How often should we recost the menu?", "At least twice a year, and immediately after a significant supplier rise on a main protein or dairy line."),
            ("Should beverage be in the same number?", "Keep them separate. Beverage typically runs at a very different cost percentage, and blending them hides whichever one is in trouble."),
        ],
        related=[R_WAGE, R_MARGIN, R_RBK],
    ),
    dict(
        slug="hospitality-wage-percentage",
        title="Hospitality Wage Percentage | What It Should Be | Pink",
        desc="How to calculate wage percentage in a hospitality venue, where it should sit, and what to do when it runs hot. Australian award context.",
        h1="Wage percentage: the number that decides your month.",
        lead="Wages are the largest controllable cost in most venues and the one that moves fastest. A roster that worked in June can be expensive by September without anything visibly changing.",
        sections=[
            ("The calculation", [
                "<p><b>Total wage cost &divide; sales for the same period &times; 100 = wage percentage.</b></p>",
                "<p>Total wage cost means the real cost of employing people: gross wages, superannuation at 12%, and the on-costs you actually carry such as workers compensation and leave accrual. Gross wages alone will understate your labour by roughly a seventh, which is the difference between a comfortable month and a tight one.</p>",
                "<p>Use sales excluding GST. Compare like with like: a week against a week, not a four-week month against a five-week one.</p>",
            ]),
            ("Where it should sit", [
                bands_table(),
                "<p>Prime cost, wages plus stock together, is the number we watch hardest. A venue can carry high wages with a tight kitchen, or a generous menu with a lean roster. It cannot carry both.</p>",
            ]),
            ("When wages run hot, it is usually structure", [
                "<ul><li><b>Opening and closing labour.</b> Full staffing for trade that has not arrived yet or has already gone.</li>"
                "<li><b>Shift length.</b> Two four-hour shifts often cost less than one eight-hour shift that spans a dead middle.</li>"
                "<li><b>Weekend and penalty exposure.</b> A Sunday roster built like a Wednesday roster costs substantially more.</li>"
                "<li><b>Classification drift.</b> Staff doing work above their classification, paid below it, which is a liability as well as a cost.</li>"
                "<li><b>Salaried managers absorbing hours.</b> The cost is real even when the roster looks lean.</li></ul>",
                "<p>Cutting hours is the blunt fix and usually the wrong one, because it costs you service. Reshaping when the hours sit is the better one, and it is the conversation we have with the numbers in front of us.</p>",
                CHECK,
                PLAN,
            ]),
        ],
        faqs=[
            ("Should wage percentage include the owner?", "If you work in the venue, cost your own labour at what it would take to replace you. A business that only works because you are unpaid is not a business that works."),
            ("Weekly or monthly?", "Weekly for running the venue, monthly for the trend. Weekly figures bounce around too much on their own."),
            ("What about agency and contract staff?", "Include them. They are labour covering trade, whatever the invoice says."),
        ],
        related=[R_PAY, R_FOOD, R_MARGIN],
    ),
    dict(
        slug="restaurant-profit-margin",
        title="Restaurant Profit Margin Australia | What Is Normal | Pink",
        desc="What restaurant profit margin should look like in Australia, how to read it against prime cost and rent, and why profit and cash differ.",
        h1="Restaurant profit margin, and why yours may be lying to you.",
        lead="Profit margin is what is left after everything: stock, labour, rent, overhead and the cost of being open. It is also the number that most often disagrees with your bank balance, which is what sends owners looking for an explanation.",
        sections=[
            ("Reading the margin", [
                "<p><b>(Sales &minus; all operating costs) &divide; sales &times; 100 = operating margin.</b></p>",
                "<p>An operating margin above about 15% on a single-site venue is a healthy result. Under about 5% and the venue is exposed: one bad quarter, one equipment failure or one rent review and there is nothing to absorb it.</p>",
                "<p>But the headline is not where the answer lives. Work backwards through the four lines underneath it.</p>",
                bands_table(),
            ]),
            ("Profit and cash are not the same thing", [
                "<p>A profit and loss can show a good month while the account runs dry. The usual causes:</p>",
                "<ul><li><b>GST and PAYG.</b> They sit in your account and they are not yours.</li>"
                "<li><b>Superannuation.</b> Accrued each pay, paid quarterly, and easy to spend in between.</li>"
                "<li><b>Stock build.</b> Money converted into a coolroom rather than into sales.</li>"
                "<li><b>Loan principal.</b> The interest is an expense; the principal is not, and it still leaves the account.</li>"
                "<li><b>Equipment.</b> Paid in full this month, expensed over years.</li>"
                "<li><b>Owner drawings.</b> Not an expense, very much a withdrawal.</li></ul>",
                "<p>Every one of those is normal. Together they are why the P&amp;L and the bank balance tell different stories, and why a venue can feel broke in a profitable year.</p>",
            ]),
            ("Getting the margin back", [
                "<p>Margin recovery is rarely one large move. It is a point off wage cost by reshaping a shift, a point off food cost by recosting the top ten dishes, and a hard look at hours that cost more to stay open than they return. On $1.5M of sales, two points is $30,000 a year.</p>",
                CHECK,
                PLAN,
            ]),
        ],
        faqs=[
            ("What is a normal profit margin for an Australian restaurant?", "It varies widely by format and site. We work to above 15% as healthy and under 5% as exposed for a single-site venue, and we read prime cost and rent to explain why a venue sits where it does."),
            ("Our revenue grew but profit did not. Why?", "Almost always prime cost. If wages and food cost grew with sales rather than more slowly, extra volume buys you work rather than profit."),
            ("Does rent really matter that much?", "Yes. Rent is fixed while trade is not, so a site above roughly 15% of sales sets a floor on how bad a quarter you can survive."),
        ],
        related=[R_FOOD, R_WAGE, R_ACCT],
    ),
    dict(
        slug="hospitality-accountant-brisbane",
        title="Hospitality Accountant Brisbane | Cafes & Restaurants | Pink",
        desc="Hospitality accountant in Brisbane. Monthly margin review, bookkeeping, payroll and BAS for cafes, restaurants and bars. Brendale office.",
        h1="Hospitality accountant in Brisbane.",
        lead="Pink Accounting works with cafes, restaurants, bars and multi-venue groups across Brisbane and greater South East Queensland, from an office at Brendale.",
        sections=[
            ("Local, and specialist", [
                "<p>We read your venue every month against the same bands, so you know why wage cost moved two points in August while August can still be fixed. The conversation is about what to change, not what happened.</p>",
                bands_table(),
            ]),
            ("Who we work with", [
                "<ul><li>Cafes and coffee shops, from single sites to small groups</li>"
                "<li>Restaurants, including family-run and Vietnamese and Asian venues across Brisbane</li>"
                "<li>Bars and licensed venues</li>"
                "<li>Takeaway and delivery-led businesses carrying platform commission</li>"
                "<li>Operators opening a second or third site</li></ul>",
                "<p>We meet in Brendale, on site at your venue, or on a call. Most of the monthly work happens without you needing to be anywhere.</p>",
            ]),
            ("What it costs", [PLAN, CHECK]),
        ],
        faqs=[
            ("Do we have to be in Brisbane?", "No. The office is at Brendale and we work with venues across Australia. Brisbane and South East Queensland clients simply get the option of meeting in person."),
            ("Can you visit the venue?", "Yes, and for a new engagement we prefer to, at least once. Seeing the floor at trade explains numbers that a file never will."),
            ("Are you a registered tax agent?", f"Yes. Registered Tax Agent {AGENT} and ASIC Registered Agent {ASIC}, listed on the TPB public register."),
        ],
        related=[R_ACCT, R_CAFE, R_HBK],
    ),
]


def main():
    site_identity.sync()
    built = [page(**spec) for spec in PAGES]
    locs = [
        "/", "/system/", "/why-pink/", "/book/", "/contact/", "/margin-check/",
        "/switching/", "/working-with-us/", "/privacy/", "/terms/", "/feedback/",
        "/restaurant-cafe-bookkeeping-brendale/", "/accountant-brendale/",
    ] + [f"/{slug}/" for slug in built]
    seen, ordered = set(), []
    for loc in locs:
        if loc not in seen:
            seen.add(loc)
            ordered.append(loc)
    body = "\n".join(f"  <url><loc>{ORIGIN}{loc}</loc></url>" for loc in ordered)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n",
        encoding="utf-8",
    )
    print(f"built {len(built)} landing pages, sitemap has {len(ordered)} urls")


if __name__ == "__main__":
    main()
