from playwright.sync_api import sync_playwright


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=20000)
        pages = [pg for ctx in browser.contexts for pg in ctx.pages]
        print("contexts", len(browser.contexts), "pages", len(pages))
        for i, pg in enumerate(pages):
            try:
                title = (pg.title() or "")[:80]
            except Exception as exc:
                title = str(exc)[:80]
            print(f"[{i}] {pg.url[:160]} | {title}")


if __name__ == "__main__":
    main()
