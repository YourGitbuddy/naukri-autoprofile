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

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    wait = WebDriverWait(driver, 30)

    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:

        print("🚀 Opening Naukri login")

        driver.get("https://www.naukri.com/nlogin/login")

        # EMAIL FIELD
        email = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='text']")
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

        time.sleep(10)

        # PROFILE PAGE
        driver.get("https://www.naukri.com/mnjuser/profile")

        print("📄 Opening profile")

        time.sleep(10)

        # FILE INPUT
        upload_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='file']")
            )
        )

        upload_input.send_keys(resume_path)

        print("📤 Resume uploading...")

        time.sleep(20)

        print("✅ Resume uploaded successfully")

    except Exception as e:

        print(f"❌ ERROR: {e}")

    finally:

        driver.quit()


if __name__ == "__main__":
    run_clean_update()
