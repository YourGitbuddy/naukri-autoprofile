from playwright.sync_api import sync_playwright
import os
import time

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASS")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    )

    page = browser.new_page()

    try:
        print("🚀 Opening Naukri")

        page.goto("https://www.naukri.com/nlogin/login", wait_until="networkidle")

        print("🌐 Login Page Opened")

        # exact selectors
        page.locator("#usernameField").fill(EMAIL)
        page.locator("#passwordField").fill(PASSWORD)

        print("✅ Credentials entered")

        page.locator("button[type='submit']").click()

        time.sleep(8)

        print("✅ Login successful")

        page.goto("https://www.naukri.com/mnjuser/profile", wait_until="networkidle")

        print("✅ Profile opened")

        # update profile timestamp trick
        page.reload()

        print("✅ Profile refreshed")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        page.screenshot(path="error.png")

    finally:
        browser.close()


if __name__ == "__main__":
    run_bot()
