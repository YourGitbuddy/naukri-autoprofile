from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASS")

chrome_options = Options()

# GitHub Actions Stable Options
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--remote-debugging-port=9222")

# Optional anti-bot tweaks
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

wait = WebDriverWait(driver, 20)

try:
    print("🚀 Opening Naukri login")

    driver.get("https://www.naukri.com/nlogin/login")

    email_box = wait.until(
        EC.presence_of_element_located((By.ID, "usernameField"))
    )

    password_box = wait.until(
        EC.presence_of_element_located((By.ID, "passwordField"))
    )

    email_box.clear()
    email_box.send_keys(EMAIL)

    password_box.clear()
    password_box.send_keys(PASSWORD)

    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Login']")
        )
    )

    login_btn.click()

    print("⏳ Waiting for login...")
    time.sleep(8)

    # Open profile page
    driver.get("https://www.naukri.com/mnjuser/profile")

    time.sleep(5)

    print("✅ Profile opened successfully")

except Exception as e:
    print(f"❌ ERROR: {e}")

finally:
    driver.quit()
