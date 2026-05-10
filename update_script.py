import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def update_naukri_profile():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=400,800") # Mobile size
    
    # Emulating a real Android Mobile Device
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 40)

    try:
        print("Bhai, Mobile site se login try kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Checking if blocked
        if "Access Denied" in driver.title or "Cloudflare" in driver.page_source:
            print("❌ IP Blocked by Naukri. Changing strategy to direct profile hit...")
        
        # Login
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login clicked, waiting for redirect...")
        time.sleep(15) 

        # Mobile Profile Page
        driver.get("https://www.naukri.com/mnjuser/profile")
        print(f"Current URL: {driver.current_url}")
        time.sleep(10)

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            # Naukri Mobile par file input dhoondna
            # Mobile site par ID 'attachCV' ki jagah simple file type hota hai
            print("Searching for Mobile Upload button...")
            
            # Pure JavaScript upload trigger
            try:
                upload_input = driver.find_element(By.CSS_VALUE, "input[type='file']")
            except:
                upload_input = driver.find_element(By.XPATH, "//input[@type='file']")
            
            driver.execute_script("arguments[0].style.display = 'block';", upload_input)
            upload_input.send_keys(resume_path)
            
            print("Wait for upload sync (20s)...")
            time.sleep(20)
            print("🏁 SUCCESS: Profile Refreshed via Mobile Site!")
        else:
            print("❌ Resume.pdf missing in repo!")

    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        driver.save_screenshot("debug_error.png")
        # Ye line help karegi dekhne mein ki exactly page par kya hai
        print("Page Title was: " + driver.title)
    finally:
        driver.quit()

if __name__ == "__main__":
    update_naukri_profile()
