import os
import time
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
    
    # Anti-bot detection flags
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Bypassing navigator.webdriver property
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    wait = WebDriverWait(driver, 40)

    try:
        print("Starting Stealth Browser Login...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Login
        email_input = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        email_input.send_keys(os.environ['NAUKRI_EMAIL'])
        
        pass_input = driver.find_element(By.ID, "passwordField")
        pass_input.send_keys(os.environ['NAUKRI_PASS'])
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login done, waiting for Dashboard...")
        time.sleep(10)

        # Profile Page Jump
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print(f"Uploading Resume from: {resume_path}")
            
            # Naukri ka hidden file input dhoondna
            # Mobile/Desktop dono mein ye locator kaam karta hai
            attach_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            attach_input.send_keys(resume_path)
            
            print("Wait for upload synchronization (15s)...")
            time.sleep(15) 
            
            print("SUCCESS: Resume uploaded and Profile refreshed!")
        else:
            print("Error: Resume.pdf not found in repo!")

    except Exception as e:
        print(f"FAILED: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
