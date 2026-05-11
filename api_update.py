import os
from playwright.sync_api import sync_playwright


def run_bot():

    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        try:

            print("🚀 Opening Naukri")

            page.goto(
                "https://www.naukri.com/nlogin/login",
                timeout=60000
            )

            page.wait_for_timeout(5000)

            print("🌐 Login Page Opened")

            # EMAIL
            page.locator(
                "input[placeholder*='Email']"
            ).fill(
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
                timeout=60000
            )

            print("📄 Opening Profile")

            page.wait_for_timeout(10000)

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
