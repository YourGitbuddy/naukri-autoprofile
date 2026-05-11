import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_clean_update():

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:
        print("🚀 Starting Naukri Refresh")

        driver.get("https://www.naukri.com/nlogin/login")

        time.sleep(5)

        # LOGIN
        driver.find_element(By.ID, "usernameField").send_keys(
            os.environ['NAUKRI_EMAIL']
        )

        driver.find_element(By.ID, "passwordField").send_keys(
            os.environ['NAUKRI_PASS']
        )

        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        print("🔐 Login success")

        time.sleep(10)

        # PROFILE PAGE
        driver.get("https://www.naukri.com/mnjuser/profile")

        time.sleep(10)

        # UPLOAD
        upload_input = driver.find_element(By.XPATH, "//input[@type='file']")

        upload_input.send_keys(resume_path)

        print("📤 Resume uploading...")

        time.sleep(15)

        print("✅ Resume uploaded successfully")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_clean_update()
