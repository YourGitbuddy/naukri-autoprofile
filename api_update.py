from playwright.sync_api import sync_playwright
import os
import time

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASS")

PROXY_SERVER = os.getenv("PROXY_SERVER")   # http://host:port
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            proxy={
                "server": PROXY_SERVER,
                "username": PROXY_USER,
                "password": PROXY_PASS
            },
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )

        page = context.new_page()

        try:
            print("🚀 Opening Naukri")
            page.goto("https://www.naukri.com/nlogin/login", timeout=60000)

            page.wait_for_selector("#usernameField", timeout=30000)

            page.fill("#usernameField", EMAIL)
            page.fill("#passwordField", PASSWORD)

            print("✅ Credentials entered")

            page.click("button[type='submit']")
            time.sleep(10)

            page.goto("https://www.naukri.com/mnjuser/profile")
            time.sleep(5)
            page.reload()

            print("✅ Profile refreshed")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            page.screenshot(path="error.png")

        finally:
            browser.close()

run_bot()
