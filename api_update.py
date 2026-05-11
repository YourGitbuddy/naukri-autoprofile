import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def run_clean_update():

    chrome_options = Options()

    # STEALTH OPTIONS
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # REMOVE SELENIUM DETECTION
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    wait = WebDriverWait(driver, 40)

    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:

        print("🚀 Opening Naukri")

        driver.get("https://www.naukri.com/nlogin/login")

        time.sleep(8)

        print("🌐 Page opened")

        # EMAIL FIELD
        email = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[contains(@placeholder,'Email')]")
            )
        )

        email.send_keys(os.environ["NAUKRI_EMAIL"])

        print("✅ Email entered")

        # PASSWORD FIELD
        password = driver.find_element(
            By.XPATH,
            "//input[@type='password']"
        )

        password.send_keys(os.environ["NAUKRI_PASS"])

        print("✅ Password entered")

        # LOGIN BUTTON
        login_btn = driver.find_element(
            By.XPATH,
            "//button[@type='submit']"
        )

        login_btn.click()

        print("🔐 Login clicked")

        time.sleep(15)

        # PROFILE PAGE
        driver.get("https://www.naukri.com/mnjuser/profile")

        print("📄 Opening profile")

        time.sleep(15)

        # UPLOAD INPUT
        upload_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='file']")
            )
        )

        upload_input.send_keys(resume_path)

        print("📤 Resume uploading")

        time.sleep(20)

        print("✅ Resume uploaded successfully")

    except Exception as e:

        print(f"❌ ERROR: {str(e)}")

        driver.save_screenshot("error.png")

        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    finally:

        driver.quit()


if __name__ == "__main__":
    run_clean_update()
