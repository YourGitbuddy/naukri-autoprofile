import os
from playwright.sync_api import sync_playwright


EMAIL = "YOUR_EMAIL"
PASSWORD = "YOUR_PASSWORD"

RESUME_PATH = "Resume.pdf"


def run_bot():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        print("🚀 Opening Naukri")

        page.goto("https://www.naukri.com/nlogin/login")

        page.wait_for_timeout(5000)

        page.fill(
            "input[placeholder*='Email']",
            EMAIL
        )

        page.fill(
            "input[type='password']",
            PASSWORD
        )

        print("🔐 Logging in")

        page.click("button[type='submit']")

        page.wait_for_timeout(15000)

        print("📄 Opening Profile")

        page.goto("https://www.naukri.com/mnjuser/profile")

        page.wait_for_timeout(10000)

        page.set_input_files(
            "input[type='file']",
            RESUME_PATH
        )

        print("✅ Resume Uploaded")

        page.wait_for_timeout(10000)

        browser.close()


if __name__ == "__main__":
    run_bot()
