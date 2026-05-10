import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_naukri_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 30) # Precise wait

    try:
        # 1. Login
        print("Logging into Naukri...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        # Dashboard load hone ka wait
        time.sleep(10)

        # 2. Navigate to Profile with Refresh
        print("Navigating to Profile Section...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        driver.refresh() # Page ko refresh karna zaroori hai session sync ke liye
        time.sleep(10)

        # 3. Target the Specific Upload Input
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        
        print("Searching for Resume Upload input...")
        # Naukri ke naye UI mein hidden input ka ID 'attachCV' hota hai
        # Hum wait karenge jab tak ye DOM mein na aa jaye
        try:
            upload_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='attachCV' or @type='file']")))
            
            print(f"Uploading: {resume_path}")
            upload_input.send_keys(resume_path)
            
            # Success confirmation wait
            print("Wait for upload processing...")
            time.sleep(20) 
            print("✅ Mission Accomplished! Resume updated.")
            
        except Exception as e:
            print("Direct input nahi mila. Trying secondary method...")
            # Agar input hidden hai toh JS se unhide karke try karenge
            driver.execute_script("document.querySelector('input[type=\"file\"]').style.display='block';")
            time.sleep(2)
            driver.find_element(By.XPATH, "//input[@type='file']").send_keys(resume_path)
            print("✅ Secondary Method Success!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("error_debug.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
