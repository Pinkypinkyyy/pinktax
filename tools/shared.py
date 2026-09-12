"""Shared HTML chrome for the Pink Accounting hospitality site."""

ORIGIN = "https://pinktax.com.au"
BOOK = "/book/"
MSBOOK = "https://outlook.office.com/book/PinkAccountingTaxSolutionsClientBookings@pinktax.com.au/"
GBP = "https://www.google.com/maps?cid=17544456102082616748"
REVIEW = "https://g.page/r/CSblVT4S46n9EBM/review"
ASSET = "h1"
GA4 = "G-8T6SXPNSCW"
GTAG = "GT-WVXQ29L2"
META_PIXEL = ""

CSP = (
    "default-src 'self'; "
    "img-src 'self' data: https://www.google-analytics.com https://www.googletagmanager.com "
    "https://www.google.com https://www.google.com.au https://www.facebook.com https://lh3.googleusercontent.com "
    "https://cdn.trustindex.io; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "script-src 'self' https://www.googletagmanager.com https://connect.facebook.net; "
    "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com "
    "https://region1.google-analytics.com https://www.facebook.com https://formsubmit.co; "
    "form-action 'self' mailto: https://formsubmit.co; "
    "media-src 'self'; "
    "base-uri 'self'"
)


def head(title, description, canonical, og_image="/assets/og.png", extra=""):
    if not canonical.startswith("http"):
        canonical = ORIGIN + (canonical if canonical.startswith("/") else "/" + canonical)
    extra_block = extra if extra else ""
    return f"""<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index,follow">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{ORIGIN}{og_image}">
  <meta property="og:locale" content="en_AU">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <link rel="icon" type="image/png" href="/assets/logo.png">
  <link rel="apple-touch-icon" href="/assets/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;1,9..144,500&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v={ASSET}">
{extra_block}</head>
"""


def jsonld(obj):
    import json
    payload = json.dumps(obj, ensure_ascii=True, separators=(",", ":"))
    return f'  <script type="application/ld+json">\n  {payload}\n  </script>\n'


def business_node():
    return {
        "@context": "https://schema.org",
        "@type": "AccountingService",
        "@id": f"{ORIGIN}/#business",
        "name": "Pink Accounting & Tax Solutions",
        "url": f"{ORIGIN}/",
        "telephone": "+61735446386",
        "email": "admin@pinktax.com.au",
        "image": f"{ORIGIN}/assets/og.png",
        "logo": f"{ORIGIN}/assets/logo.png",
        "priceRange": "$$",
        "knowsAbout": [
            "hospitality bookkeeping",
            "restaurant payroll",
            "cafe margins",
            "BAS",
            "GST",
        ],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Shop 15A, 18-22 Kremzow Rd",
            "addressLocality": "Brendale",
            "addressRegion": "QLD",
            "postalCode": "4500",
            "addressCountry": "AU",
        },
        "areaServed": {"@type": "Country", "name": "Australia"},
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00",
            "closes": "16:30",
        },
        "founder": {"@type": "Person", "name": "Huong Bui"},
        "taxID": "51682301891",
        "identifier": "26284368",
        "sameAs": [
            "https://www.google.com/maps?cid=17544456102082616748",
        ],
    }


def faq_node(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }


def nav(current=""):
    def item(href, label, key):
        cur = ' aria-current="page"' if current == key else ""
        return f'        <a href="{href}"{cur}>{label}</a>'

    return f"""<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="nav" id="pinkNav">
    <div class="wrap">
      <a class="brand" href="/" aria-label="Pink Accounting">
        <img src="/assets/logo-white.png" alt="pink">
      </a>
      <nav class="links" aria-label="Primary">
{item("/system/", "The system", "system")}
{item("/why-pink/", "Why Pink", "why")}
{item("/margin-check/", "Margin Check", "check")}
{item("/contact/", "Contact", "contact")}
      </nav>
      <div class="navr">
        <a class="phone" href="tel:+61735446386">(07) 3544 6386</a>
        <a class="btn btn-primary" href="/book/" data-event="nav-book"><span class="full">Book a call</span><span class="short">Book</span></a>
        <button class="burger" id="pinkBurger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="pinkNav"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>
"""


def footer():
    return f"""  <footer class="foot">
    <div class="wrap">
      <div class="grid">
        <div>
          <img src="/assets/logo-white.png" alt="pink">
          <p class="blurb">Margin protection, bookkeeping, payroll and tax for hospitality businesses across Australia. Brendale office. Registered Tax Agent 26284368.</p>
        </div>
        <div>
          <h4>Explore</h4>
          <a href="/">Home</a>
          <a href="/system/">The system</a>
          <a href="/why-pink/">Why Pink</a>
          <a href="/margin-check/">Margin Check</a>
          <a href="/book/">Book a call</a>
          <a href="/contact/">Contact</a>
        </div>
        <div>
          <h4>Contact and legal</h4>
          <a href="tel:+61735446386">(07) 3544 6386</a>
          <a href="mailto:admin@pinktax.com.au">admin@pinktax.com.au</a>
          <a href="/working-with-us/">Your rights</a>
          <a href="/privacy/">Privacy</a>
          <a href="/terms/">Terms</a>
          <a href="/feedback/">Feedback</a>
          <p class="addr" style="margin-top:12px;line-height:1.8">Shop 15A, 18-22 Kremzow Rd<br>Brendale QLD 4500</p>
        </div>
      </div>
      <p class="legal">© 2026 Pink Accounting &amp; Tax Solutions Pty Ltd. ABN 51 682 301 891. Business clients only. Registered Tax Agent No. 26284368 · ASIC Registered Agent No. 52580 · <a href="https://www.tpb.gov.au/public-register" rel="noopener">TPB Register</a><br>Liability limited by a scheme approved under Professional Standards Legislation.</p>
    </div>
  </footer>
  <script src="/track.js?v={ASSET}"></script>
  <script src="/nav.js?v={ASSET}"></script>
</body>
</html>
"""


def enquiry_form(prefix="book"):
    return f"""      <form class="enquiry" id="enquiryForm" action="https://formsubmit.co/admin@pinktax.com.au" method="POST" data-event="{prefix}-form">
        <input type="hidden" name="_subject" value="Pink Accounting hospitality intake">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="{ORIGIN}/book/?sent=1">
        <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="fields">
          <label>Your name
            <input type="text" name="name" required autocomplete="name">
          </label>
          <label>Venue name
            <input type="text" name="venue" required autocomplete="organization">
          </label>
          <label>Email
            <input type="email" name="email" required autocomplete="email">
          </label>
          <label>Mobile
            <input type="tel" name="mobile" required autocomplete="tel">
          </label>
          <label>Annual revenue
            <select name="revenue" required>
              <option value="">Choose one</option>
              <option>Under $1M</option>
              <option>$1M-$3M</option>
              <option>$3M-$5M</option>
              <option>$5M+</option>
              <option>Multi-venue</option>
            </select>
          </label>
          <label>Staff
            <select name="staff" required>
              <option value="">Choose one</option>
              <option>Just me</option>
              <option>1-5</option>
              <option>6-15</option>
              <option>16-30</option>
              <option>30+</option>
            </select>
          </label>
        </div>
        <label>What is hurting
          <textarea class="short" name="hurt" rows="4" maxlength="1000" required placeholder="Wages %. Food cost. Cash surprises. Books behind. Multi-venue chaos."></textarea>
        </label>
        <label>Where is the business now
          <textarea class="short" name="position" rows="4" maxlength="1000" required placeholder="Who does the books. Last BAS. What a normal week looks like."></textarea>
        </label>
        <label>Where do you want it in 12 months
          <textarea class="short" name="vision" rows="4" maxlength="1000" required placeholder="Second venue. Off the floor. Tighter wages. What a good year looks like."></textarea>
        </label>
        <button class="btn btn-primary" type="submit">Send this, then pick a time</button>
        <p class="form-note">Goes to admin@pinktax.com.au. We read it before the call. By sending you agree to our <a href="/terms/">terms</a> and <a href="/privacy/">privacy</a> pages.</p>
      </form>
      <p class="enquiry-ok" id="enquiryOk" hidden>Got it. Pick a time below with the same email so we are not chasing you.</p>
"""
