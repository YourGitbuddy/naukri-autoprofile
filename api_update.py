import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_universal_automation():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("🌐 Universal Automation: Initializing...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        print("🔐 Logging in...")
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("✅ Login Success.")
        time.sleep(12) 

        # Capture Cookies for Requests
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # Common Headers for Naukri APIs
        headers = {
            "Clientid": "d36980564696075936856",
            "Appid": "121",
            "Systemid": "121",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        # 2. Fetch Current Headline (Dynamic Fetch)
        print("📡 Fetching current profile data...")
        headline_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        get_res = session.get(headline_url, headers=headers)
        
        if get_res.status_code == 200:
            current_headline = get_res.json().get('resumeHeadline', '')
            
            # 3. Dynamic Refresh (Just toggle a dot to update 'Last Updated' date)
            # Agar last mein dot hai toh hata do, nahi hai toh laga do
            if current_headline.endswith('.'):
                new_headline = current_headline[:-1]
            else:
                new_headline = current_headline + "."
            
            print(f"🔄 Refreshing Headline: {new_headline[:30]}...")
            session.put(headline_url, json={"resumeHeadline": new_headline}, headers=headers)
            print("✅ Profile Status: Refresh Triggered.")

        # 4. Universal Resume Upload
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print("🚀 Uploading Resume.pdf from repository...")
            upload_url = "https://www.naukri.com/mnjuser/profile/uploadResume"
            api_headers = {
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.naukri.com/mnjuser/profile",
                "User-Agent": "Mozilla/5.0"
            }
            with open(resume_path, 'rb') as f:
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                session.post(upload_url, files=files, data={'isResumeUpload': '1'}, headers=api_headers)
            print("🏁 MISSION ACCOMPLISHED: Resume & Profile Updated Universally!")
        else:
            print("⚠️ Warning: Resume.pdf not found. Only headline refreshed.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_universal_automation()
