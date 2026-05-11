import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_universal_clean_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Auto-detect path
    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:
        print("🌐 Universal Clean Mode: Starting...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        driver.find_element(By.ID, "usernameField").send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(10)

        # 2. Session Setup
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            "Clientid": "d36980564696075936856",
            "Appid": "121",
            "Systemid": "121",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest"
        }

        # 3. Privacy Headline Refresh (No VFX/Azure hardcoding)
        h_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        res = session.get(h_url, headers=headers)
        if res.status_code == 200:
            curr = res.json().get('resumeHeadline', 'Professional')
            new_h = curr[:-1] if curr.endswith('.') else curr + "."
            session.put(h_url, json={"resumeHeadline": new_h}, headers=headers)
            print("✅ Profile Activity: Refreshed.")

        # 4. Forced Resume Upload (API Sniper)
        if os.path.exists(resume_path):
            with open(resume_path, 'rb') as f:
                u_res = session.post(
                    "https://www.naukri.com/mnjuser/profile/uploadResume", 
                    files={'resume': ('Resume.pdf', f, 'application/pdf')}, 
                    data={'isResumeUpload': '1'}, 
                    headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}
                )
                if u_res.status_code == 200:
                    print("🏁 FINAL STATUS: Resume pushed to server successfully.")
        
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_universal_clean_update()
