from playwright.sync_api import sync_playwright
import os
import time

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASS")

def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )

        page = context.new_page()

        try:
            print("🚀 Opening Naukri")

            page.goto("https://www.naukri.com/nlogin/login", timeout=60000)

            print("🌐 Login Page Opened")

            time.sleep(5)

            # fallback selectors
            email = page.locator("input[placeholder*='Email']").first
            password = page.locator("input[type='password']").first

            email.fill(EMAIL)
            password.fill(PASSWORD)

            print("✅ Credentials entered")

            page.locator("button:has-text('Login')").click()

            time.sleep(10)

            print("✅ Login successful")

            page.goto("https://www.naukri.com/mnjuser/profile")

            time.sleep(8)

            page.reload()

            print("✅ Profile refreshed")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            page.screenshot(path="error.png")

        finally:
            browser.close()


run_bot()
