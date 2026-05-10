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
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Anti-detection script
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    wait = WebDriverWait(driver, 40)

    try:
        print("Bhai, Login process shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Email field wait
        email_field = wait.until(EC.element_to_be_clickable((By.ID, "usernameField")))
        email_field.send_keys(os.environ['NAUKRI_EMAIL'])
        
        # Pass field
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        
        # Login click via JS (More reliable)
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login done, waiting for session sync...")
        time.sleep(15) 

        # Jump to Profile
        print("Navigating to Profile...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print(f"Uploading: {resume_path}")
            
            # Naukri ka file input aksar display:none hota hai
            # Hum usey JS se dhund kar seedha send_keys karenge
            try:
                # Targetting multiple possible IDs for resume upload
                upload_xpath = "//input[@type='file' and contains(@id, 'attachCV') or @id='attachCV']"
                attach_input = wait.until(EC.presence_of_element_located((By.XPATH, upload_xpath)))
                
                # Force visibility just in case
                driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';", attach_input)
                attach_input.send_keys(resume_path)
                
                print("Upload command sent. Waiting for confirmation...")
                time.sleep(20) 
                print("🏁 Success: Profile refreshed!")
            except Exception as upload_err:
                print(f"Upload input not found directly. Fallback to general file input...")
                driver.find_element(By.XPATH, "//input[@type='file']").send_keys(resume_path)
                time.sleep(20)
                print("🏁 Success: Profile refreshed via fallback!")
        else:
            print("❌ Error: Resume.pdf missing in repo!")

    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    update_naukri_profile()
