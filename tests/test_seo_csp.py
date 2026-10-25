"""One Content-Security-Policy, and it lets GA4 finish its collect call.

Lighthouse (25 Oct 2026, mobile, 7 pages) logged a console error on every
page: GA4 posts to https://stats.g.doubleclick.net/g/collect (the Google
signals / Ads-audience beacon) and connect-src blocked it. The CSP is a
<meta> tag copied into every page, so it must stay identical everywhere.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSP = re.compile(r'<meta http-equiv="Content-Security-Policy" content="([^"]+)">')


# individuals/ arrives on feat/individuals-booking-page-2026-10-25 (#16) with
# the old CSP. Exempt so this branch cannot block that merge; remove the
# exemption once that page carries the same policy.
EXEMPT = {"individuals/index.html"}


def policies():
    out = {}
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts or p.relative_to(ROOT).as_posix() in EXEMPT:
            continue
        m = CSP.search(p.read_text(encoding="utf-8"))
        if m:
            out[p.relative_to(ROOT).as_posix()] = m.group(1)
    return out


def test_every_page_carries_the_same_csp():
    found = policies()
    assert len(found) >= 20
    assert len(set(found.values())) == 1, sorted(found)


def test_csp_allows_the_ga4_doubleclick_beacon_and_formsubmit():
    csp = next(iter(policies().values()))
    connect = re.search(r"connect-src ([^;]+)", csp).group(1).split()
    assert "https://stats.g.doubleclick.net" in connect
    assert "https://formsubmit.co" in connect
    assert "https://region1.google-analytics.com" in connect
    assert "'unsafe-inline'" not in re.search(r"script-src ([^;]+)", csp).group(1)
