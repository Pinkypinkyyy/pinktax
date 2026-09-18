from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[1] / "docs"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        ctx = browser.contexts[0]
        pages = ctx.pages
        pages[0].screenshot(path=str(OUT / "_cdp_signin.png"), full_page=False)
        print("signin url", pages[0].url)
        print("signin text", pages[0].evaluate("() => document.body.innerText.slice(0,1500)"))
        pg = ctx.new_page()
        pg.goto("chrome://version", wait_until="domcontentloaded", timeout=15000)
        print("version", pg.evaluate("() => document.body.innerText.slice(0,2500)"))


if __name__ == "__main__":
    main()
