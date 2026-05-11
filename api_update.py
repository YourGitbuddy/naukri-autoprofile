import os
import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_clean_update():

    options = uc.ChromeOptions()

    options.add_argument("--headless=old")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = uc.Chrome(
        version_main=147,
        options=options,
        use_subprocess=False
    )

    wait = WebDriverWait(driver, 40)

    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:

        print("🚀 Opening Naukri")

        driver.get("https://www.naukri.com/nlogin/login")

        time.sleep(8)

        print("🌐 Page Opened")

        # EMAIL
        email = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[contains(@placeholder,'Email')]")
            )
        )

        email.send_keys(os.environ["NAUKRI_EMAIL"])

        print("✅ Email Entered")

        # PASSWORD
        password = driver.find_element(
            By.XPATH,
            "//input[@type='password']"
        )

        password.send_keys(os.environ["NAUKRI_PASS"])

        print("✅ Password Entered")

        # LOGIN BUTTON
        login_btn = driver.find_element(
            By.XPATH,
            "//button[@type='submit']"
        )

        login_btn.click()

        print("🔐 Login Clicked")

        time.sleep(15)

        # PROFILE PAGE
        driver.get("https://www.naukri.com/mnjuser/profile")

        print("📄 Opening Profile")

        time.sleep(15)

        # FILE INPUT
        upload_input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='file']")
            )
        )

        print("📎 Upload Input Found")

        # UPLOAD
        upload_input.send_keys(resume_path)

        print("📤 Resume Uploading")

        time.sleep(25)

        print("✅ Resume Uploaded Successfully")

    except Exception as e:

        print(f"❌ ERROR: {str(e)}")

        try:
            driver.save_screenshot("error.png")

            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

        except:
            pass

    finally:

        driver.quit()


if __name__ == "__main__":
    run_clean_update()
