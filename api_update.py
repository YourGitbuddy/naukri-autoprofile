import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_universal_sync():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # --- 📂 Path Finder Logic ---
    # Ye script khud dhoondegi ki Resume.pdf kahan hai
    resume_file = None
    possible_names = ["Resume.pdf", "resume.pdf"]
    
    for name in possible_names:
        if os.path.exists(name):
            resume_file = name
            break
            
    if not resume_file:
        # Agar root mein nahi mili, toh check karo agar folder ke andar hai
        current_dir_files = os.listdir('.')
        print(f"📁 Current Files in Repo: {current_dir_files}")
        print("❌ Error: Resume.pdf nahi mili. Make sure ye main folder mein hai.")
        driver.quit()
        return

    print(f"🎯 Target Found: {resume_file}. Starting Sync...")

    try:
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        driver.find_element(By.ID, "usernameField").send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(10)

        # 2. Session Capture
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # 3. Privacy-Friendly Headline Toggle
        # (Koi VFX ya Azure text hardcoded nahi hai)
        h_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        h_headers = {"Clientid": "d36980564696075936856", "Appid": "121", "Systemid": "121", "Content-Type": "application/json"}
        
        get_res = session.get(h_url, headers=h_headers)
        if get_res.status_code == 200:
            curr = get_res.json().get('resumeHeadline', 'Professional')
            new_h = curr[:-1] if curr.endswith('.') else curr + "."
            session.put(h_url, json={"resumeHeadline": new_h}, headers=h_headers)
            print("✅ Profile Activity: Timestamp Updated.")

        # 4. Final Resume Upload
        with open(resume_file, 'rb') as f:
            u_res = session.post(
                "https://www.naukri.com/mnjuser/profile/uploadResume", 
                files={'resume': (resume_file, f, 'application/pdf')}, 
                data={'isResumeUpload': '1'}, 
                headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}
            )
            if u_res.status_code == 200:
                print(f"🏁 MISSION ACCOMPLISHED: {resume_file} is now live!")

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_universal_sync()
