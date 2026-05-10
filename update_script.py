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
    wait = WebDriverWait(driver, 60) # Timeout badha diya hai

    try:
        # 1. Login
        print("Logging into Naukri...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        email_field = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        time.sleep(15)

        # 2. Direct Profile Navigation
        print("Going to Profile Section...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # 3. Resume Upload (Finding the Hidden Input)
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print(f"Uploading Resume from: {resume_path}")
            
            # Naukri ka upload input dhoondne ka sabse robust tarika
            # Hum CSS Selector use karenge jo 'Attach Resume' section ko target karta hai
            try:
                # Kai baar input hidden hota hai, isliye hum use find karenge
                attach_input = driver.find_element(By.CSS_SELECTOR, "input[type='file'][id='attachCV']")
                attach_input.send_keys(resume_path)
            except:
                # Agar ID kaam na kare toh generic type='file' dhoondo
                print("ID 'attachCV' nahi mila, generic file input try kar raha hoon...")
                attach_input = driver.find_element(By.XPATH, "//input[@type='file']")
                attach_input.send_keys(resume_path)

            print("Waiting for upload to finish...")
            time.sleep(20) # Thoda extra time upload hone ke liye
            
            print("✅ Success! Resume upload action completed.")
        else:
            print("❌ Resume.pdf not found in repo!")

    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        driver.save_screenshot("error_debug.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
