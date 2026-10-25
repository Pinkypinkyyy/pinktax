"""Enquiry emails must say where the visitor came from.

nav.js keeps the first marketing touch of the browser session (UTMs, gclid,
fbclid, landing path, referring host) and adds it to the relay post. The
behaviour test runs the real nav.js under Node with a stubbed browser, so it
is skipped where Node is not installed (GitHub's ubuntu runners have it).
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NAV = ROOT / "nav.js"

HARNESS = r"""
const fs = require("fs");
const store = {};
const el = () => ({ addEventListener() {}, classList: { toggle() {}, add() {}, contains() { return false; } }, contains() { return false; } });
global.window = global;
global.location = { search: process.argv[2], pathname: process.argv[3], hostname: "pinktax.com.au" };
global.window.location = global.location;
global.sessionStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = v; } };
global.window.matchMedia = () => ({ matches: true });
global.document = {
  referrer: process.argv[4],
  getElementById: () => null,
  querySelector: () => null,
  querySelectorAll: () => [],
  addEventListener() {},
};
eval(fs.readFileSync(process.argv[1], "utf8").replace("ATTRIBUTION_ENABLED = false", "ATTRIBUTION_ENABLED = true"));
const first = window.pinkAttribution();
// a later page in the same session, with no query string, must keep the first touch
global.location = { search: "", pathname: "/contact/", hostname: "pinktax.com.au" };
global.window.location = global.location;
console.log(JSON.stringify({ first, later: window.pinkAttribution() }));
"""


def run(search, path, referrer):
    out = subprocess.run(
        ["node", "-e", HARNESS, str(NAV), search, path, referrer],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)


def test_relay_post_includes_attribution():
    nav = NAV.read_text(encoding="utf-8")
    assert "Object.assign({}, data, attribution())" in nav
    # the mailto fallback body is built from `data` only, so attribution stays out of it
    assert "attribution()" not in nav[nav.index(".catch(function () {"):]


def test_attribution_ships_switched_off():
    # Ready to enable, nothing live until the privacy wording is approved.
    assert "var ATTRIBUTION_ENABLED = false;" in NAV.read_text(encoding="utf-8")


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_first_touch_is_kept_for_the_session():
    r = run("?utm_source=google&utm_medium=cpc&utm_campaign=margin&gclid=abc123&junk=1", "/margin-check/",
            "https://www.google.com/search?q=secret+query")
    assert r["first"] == {
        "utm_source": "google", "utm_medium": "cpc", "utm_campaign": "margin",
        "gclid": "abc123", "landing_page": "/margin-check/", "referrer": "www.google.com",
    }
    assert r["later"] == r["first"], "a second page view overwrote the first touch"


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_direct_visit_records_only_the_landing_path():
    r = run("", "/", "")
    assert r["first"] == {"landing_page": "/"}
