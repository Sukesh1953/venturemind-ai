from playwright.sync_api import sync_playwright


def read_website(url):

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(3000)

            text = page.locator("body").inner_text()

            browser.close()

            return text[:5000]

    except Exception as e:
        return f"Error: {str(e)}"