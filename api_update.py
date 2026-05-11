import os
import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_hybrid_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:
        print("🚀 Hybrid Mission: UI + Backend Update Shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        print("🔐 Logging in...")
        driver.find_element(By.ID, "usernameField").send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(10)

        # 2. UI Path: Forcing the "Upload Button"
        print("📤 Attempting UI Upload to clear the dashboard box...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        try:
            # Dashboard par hidden file input dhoond raha hoon
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            file_input.send_keys(resume_path)
            print("✅ UI Upload Triggered! Box ab hat jana chahiye.")
            time.sleep(10) 
        except Exception as ui_err:
            print(f"⚠️ UI Input nahi mila (Shadow DOM issue). Moving to Backend Sniper...")

        # 3. Backend Path: Status 200 Confirmation
        print("🎯 Sniper Mode: Direct API Hit...")
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.naukri.com/mnjuser/profile",
            "User-Agent": "Mozilla/5.0"
        }

        with open(resume_path, 'rb') as f:
            files = {'resume': ('Resume.pdf', f, 'application/pdf')}
            data = {'isResumeUpload': '1'}
            response = session.post("https://www.naukri.com/mnjuser/profile/uploadResume", 
                                    files=files, data=data, headers=headers)

        if response.status_code == 200:
            print("🏁 MISSION ACCOMPLISHED: Server ne file accept kar li hai!")
        else:
            print(f"❌ API Error: {response.status_code}")

        # 4. Headline Refresh (For Visibility)
        print("🔄 Refreshing Headline for Recruiter Alert...")
        h_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        h_headers = {"Clientid": "d36980564696075936856", "Appid": "121", "Systemid": "121", "Content-Type": "application/json"}
        
        current_data = session.get(h_url, headers=h_headers).json()
        current_headline = current_data.get('resumeHeadline', '')
        new_headline = current_headline[:-1] if current_headline.endswith('.') else current_headline + "."
        
        session.put(h_url, json={"resumeHeadline": new_headline}, headers=h_headers)
        print("✅ Profile Timestamp Updated.")

    except Exception as e:
        print(f"💥 Fatal Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_hybrid_update()
