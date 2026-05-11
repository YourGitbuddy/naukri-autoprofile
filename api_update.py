import os
from playwright.sync_api import sync_playwright


def run_bot():

    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080}
        )

        page = context.new_page()

        try:

            print("🚀 Opening Naukri")

            page.goto(
                "https://www.naukri.com/nlogin/login",
                wait_until="networkidle",
                timeout=60000
            )

            page.wait_for_timeout(10000)

            print("🌐 Login Page Opened")

            # DEBUG SCREENSHOT
            page.screenshot(path="before_login.png")

            # EMAIL
            page.locator(
                "input[type='text']"
            ).first.fill(
                os.environ["NAUKRI_EMAIL"]
            )

            print("✅ Email Entered")

            # PASSWORD
            page.locator(
                "input[type='password']"
            ).fill(
                os.environ["NAUKRI_PASS"]
            )

            print("✅ Password Entered")

            # LOGIN
            page.locator(
                "button[type='submit']"
            ).click()

            print("🔐 Login Clicked")

            page.wait_for_timeout(15000)

            # PROFILE PAGE
            page.goto(
                "https://www.naukri.com/mnjuser/profile",
                wait_until="networkidle",
                timeout=60000
            )

            print("📄 Profile Opened")

            page.wait_for_timeout(10000)

            # PROFILE SCREENSHOT
            page.screenshot(path="profile.png")

            # UPLOAD RESUME
            page.set_input_files(
                "input[type='file']",
                resume_path
            )

            print("📤 Resume Uploading")

            page.wait_for_timeout(20000)

            print("✅ Resume Uploaded Successfully")

        except Exception as e:

            print(f"❌ ERROR: {str(e)}")

            page.screenshot(path="error.png")

            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(page.content())

        finally:

            browser.close()


if __name__ == "__main__":
    run_bot()
