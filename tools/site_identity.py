"""Renders identity.json into the site.

identity.json is generated from the firm's canonical identity file and is the
only place this site takes its business name, legal entity, office details,
Google profile and the cross-link to the trades service from. Never edit it
by hand here.

Most pages are hand-maintained HTML, so this does not rebuild them. It
rewrites the identity-owned parts of each page in place and leaves every other
byte alone:

  * the AccountingService JSON-LD node (home and /contact/)
  * the one cross-link line at the foot of every page
  * the office and two-doors blocks on /contact/, between identity markers

apply() is pure, so tests can check that every committed page already equals
its own rebuild. build_landing_pages.py calls sync() before it lifts the
footer out of index.html.
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://pinktax.com.au"
ID = json.loads((ROOT / "identity.json").read_text(encoding="utf-8"))

OFFICE = ID["office"]
HOURS = OFFICE["hours"]
LEGAL = ID["legal"]
TRADES = ID["service_lines"]["trades"]
XLINK = ID["cross_links"]["on_hospitality_site"]

LD = re.compile(r'(<script type="application/ld\+json">\s*)(\{"@context":"https://schema\.org","@type":"AccountingService".*?\})(\s*</script>)', re.S)
SISTER = re.compile(r'[ \t]*<p class="sister-line"[^>]*>.*?</p>\n')


def e(text):
    return html.escape(text, quote=True)


def org_node():
    return {
        "@context": "https://schema.org",
        "@type": ID["schema"]["type"],
        "@id": ID["schema"]["organization_id"],
        "name": ID["public_name"],
        "legalName": LEGAL["entity"],
        "url": f"{ORIGIN}/",
        "telephone": OFFICE["phone_e164"],
        "email": OFFICE["email"],
        "image": f"{ORIGIN}/assets/og.png",
        "logo": f"{ORIGIN}/assets/logo.png",
        "priceRange": "$$",
        "knowsAbout": ["hospitality bookkeeping", "restaurant payroll", "cafe margins", "BAS", "GST"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": OFFICE["street"],
            "addressLocality": OFFICE["locality"],
            "addressRegion": OFFICE["region"],
            "postalCode": OFFICE["postcode"],
            "addressCountry": OFFICE["country"],
        },
        "areaServed": {"@type": "Country", "name": "Australia"},
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": HOURS["days"],
            "opens": HOURS["opens"],
            "closes": HOURS["closes"],
        },
        "founder": {"@type": "Person", "name": "Huong Bui"},
        "taxID": LEGAL["abn"].replace(" ", ""),
        "identifier": LEGAL["tax_agent_number"],
        "sameAs": [ID["google_profile"]["maps_url"]],
        "department": [{"@type": "AccountingService", "name": TRADES["service_name"], "url": TRADES["site"]}],
    }


def sister_line():
    return (
        f'<p class="sister-line" data-identity="cross-link">{e(XLINK["text"])} '
        f'<a href="{e(XLINK["href"])}">{e(XLINK["link_text"])}</a></p>'
    )


def office_block():
    tel, mail = OFFICE["phone_e164"], OFFICE["email"]
    town = f'{OFFICE["locality"]} {OFFICE["region"]} {OFFICE["postcode"]}'
    return f"""      <div class="grid3" data-identity="office">
        <section class="card"><span class="eyebrow">Phone</span><h2><a href="tel:{tel}">{e(OFFICE["phone_display"])}</a></h2><p>Answered during office hours.</p></section>
        <section class="card"><span class="eyebrow">Email</span><h2><a href="mailto:{mail}">{mail}</a></h2><p>The firm mailbox. A person reads it.</p></section>
        <section class="card"><span class="eyebrow">Office</span><h2>{e(town)}</h2><p>{e(OFFICE["one_line"])}. Open {e(HOURS["display"])}. <a href="{e(ID["google_profile"]["maps_url"])}" rel="noopener">Find us on Google Maps</a>.</p></section>
      </div>"""


def two_doors_block():
    return f"""      <section class="two-doors" data-identity="two-doors">
        <h2>Two services, one office</h2>
        <div class="doors">
          <div class="card"><span class="eyebrow">Hospitality</span><h3>{e(ID["public_name"])}</h3><p>Cafes, restaurants, bars and venues. Everything on this site is for you.</p></div>
          <div class="card"><span class="eyebrow">Trades</span><h3>{e(TRADES["display"])}</h3><p>For {e(TRADES["audience"])}. <a href="{e(TRADES["site"])}">Visit the site</a>.</p></div>
        </div>
      </section>"""


def fill(text, name, body):
    start, end = f"<!-- identity:{name} -->\n", f"\n      <!-- /identity:{name} -->"
    i, j = text.find(start), text.find(end)
    if i < 0 or j < 0:
        raise SystemExit(f"identity markers for {name} are missing")
    return text[: i + len(start)] + body + text[j:]


def apply(text, rel):
    text = LD.sub(lambda m: m.group(1) + json.dumps(org_node(), ensure_ascii=True, separators=(",", ":")) + m.group(3), text)

    # One cross-link line, last thing inside the footer's wrap.
    text = SISTER.sub("", text)
    end = text.rfind("</footer>")
    if end >= 0:
        close = text.rfind("</div>", 0, end)
        line_start = text.rfind("\n", 0, close) + 1
        indent = text[line_start:close]
        text = text[:line_start] + indent + "  " + sister_line() + "\n" + text[line_start:]

    if rel == "contact/index.html":
        text = fill(text, "office", office_block())
        text = fill(text, "two-doors", two_doors_block())
    return text


def pages():
    return sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)


def sync():
    changed = 0
    for p in pages():
        rel = p.relative_to(ROOT).as_posix()
        old = p.read_text(encoding="utf-8")
        new = apply(old, rel)
        if new != old:
            p.write_text(new, encoding="utf-8")
            changed += 1
    print(f"identity: {changed} page(s) updated")


if __name__ == "__main__":
    sync()
