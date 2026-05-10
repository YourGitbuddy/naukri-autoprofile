import os
import time
import random
from datetime import datetime
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
    wait = WebDriverWait(driver, 45)

    try:
        # 1. Login Process
        print("Logging into Naukri...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        time.sleep(15)

        # 2. Go to Profile Page
        print("Navigating to Profile Page for Resume Upload...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # 3. Resume Upload Logic
        # Resume file ka absolute path nikalna (GitHub runner ke liye)
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        
        if os.path.exists(resume_path):
            print(f"Resume mil gaya: {resume_path}. Uploading...")
            
            # Naukri par hidden input field dhoondna jo file accept karti hai
            upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
            upload_input.send_keys(resume_path)
            
            print("Resume upload request bhej di gayi hai.")
            time.sleep(15) # Upload hone ka wait
            
            # Check success message if any (optional)
            print("Kaam ho gaya! Resume update ho chuka hai.")
        else:
            print("Error: 'Resume.pdf' file repo mein nahi mili! Please check naming.")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
