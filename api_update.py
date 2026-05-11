import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_final_ultimate_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:
        print("🚀 Final Mission: Absolute Force Update...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        driver.find_element(By.ID, "usernameField").send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(10)

        # 2. Direct API Sniper (Status 200 ke liye)
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.naukri.com/mnjuser/profile",
            "User-Agent": "Mozilla/5.0"
        }

        if os.path.exists(resume_path):
            with open(resume_path, 'rb') as f:
                res = session.post("https://www.naukri.com/mnjuser/profile/uploadResume", 
                                    files={'resume': ('Resume.pdf', f, 'application/pdf')}, 
                                    data={'isResumeUpload': '1'}, headers=headers)
                if res.status_code == 200:
                    print("✅ DATABASE: Resume successfully saved on Naukri server.")

        # 3. Forced Headline Refresh (With Error Handling)
        try:
            h_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
            h_headers = {"Clientid": "d36980564696075936856", "Appid": "121", "Systemid": "121", "Content-Type": "application/json"}
            
            get_h = session.get(h_url, headers=h_headers)
            if get_h.status_code == 200:
                data = get_h.json()
                # Safe check for key
                current_h = data.get('resumeHeadline', 'VFX Artist') 
                new_h = current_h[:-1] if current_h.endswith('.') else current_h + "."
                session.put(h_url, json={"resumeHeadline": new_h}, headers=h_headers)
                print("✅ HEADLINE: Timestamp refreshed.")
        except Exception as e:
            print(f"⚠️ Headline Skip: {str(e)}")

        print("🏁 MISSION ACCOMPLISHED: Check your profile now!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_final_ultimate_update()
