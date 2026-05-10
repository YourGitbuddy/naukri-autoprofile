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
    
    # Mobile Emulation: Isse Akamai ko lagta hai aap phone se manually kar rahe ho
    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 30)

    try:
        print("Bhai, Mobile mode mein login shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Login
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        
        # Click Login
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        time.sleep(10)

        # Direct URL to "Attach Resume" page
        print("Navigating directly to Resume Section...")
        driver.get("https://www.naukri.com/mnjuser/profile?isEditResume=1")
        time.sleep(5)

        # Upload Resume
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print(f"Uploading: {resume_path}")
            # Mobile UI mein input field hamesha present hoti hai
            attach_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            attach_input.send_keys(resume_path)
            
            print("Processing upload...")
            time.sleep(15) # Wait for upload to complete
            print("✅ Mission Accomplished! Profile refreshed.")
        else:
            print("❌ Resume.pdf missing in repo!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("error_mobile.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
