import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_clean_universal_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:
        print("🌐 Universal Mode: Starting Profile Refresh...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login (Using Env Variables)
        driver.find_element(By.ID, "usernameField").send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(10)

        # 2. Capture Cookies
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

        # 3. Universal Headline Update (Fetch & Toggle)
        # Ye koi naya text nahi dalega, jo hai usi ko refresh karega
        h_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        get_res = session.get(h_url, headers=headers)
        
        if get_res.status_code == 200:
            current_h = get_res.json().get('resumeHeadline', 'Professional')
            # Just toggle a dot at the end to trigger "Last Updated"
            new_h = current_h[:-1] if current_h.endswith('.') else current_h + "."
            session.put(h_url, json={"resumeHeadline": new_h}, headers=headers)
            print("✅ Headline Refreshed (Privacy Maintained).")

        # 4. Universal Resume Upload
        if os.path.exists(resume_path):
            with open(resume_path, 'rb') as f:
                upload_res = session.post(
                    "https://www.naukri.com/mnjuser/profile/uploadResume", 
                    files={'resume': ('Resume.pdf', f, 'application/pdf')}, 
                    data={'isResumeUpload': '1'}, 
                    headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}
                )
                if upload_res.status_code == 200:
                    print("✅ Resume Sync: Success.")

        print("🏁 MISSION ACCOMPLISHED: Profile is now Fresh & Private.")

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_clean_universal_update()
