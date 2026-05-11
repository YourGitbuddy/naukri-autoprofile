from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASS")

chrome_options = Options()

# REQUIRED FOR GITHUB ACTIONS
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Anti detection
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

print("🚀 Starting Chrome")

driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 30)

try:
    print("🚀 Opening Naukri login")

    driver.get("https://www.naukri.com/nlogin/login")

    print("✅ Login page opened")

    email_box = wait.until(
        EC.presence_of_element_located((By.ID, "usernameField"))
    )

    password_box = wait.until(
        EC.presence_of_element_located((By.ID, "passwordField"))
    )

    email_box.send_keys(EMAIL)
    password_box.send_keys(PASSWORD)

    print("✅ Credentials entered")

    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Login']")
        )
    )

    login_btn.click()

    print("⏳ Waiting after login")
    time.sleep(10)

    print("✅ Login successful")

    driver.get("https://www.naukri.com/mnjuser/profile")

    time.sleep(5)

    print("✅ Profile page opened")

except Exception as e:
    print(f"❌ ERROR: {str(e)}")

    # Save screenshot for debugging
    driver.save_screenshot("error.png")
    print("📸 Screenshot saved")

finally:
    driver.quit()
