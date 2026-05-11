import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_naukri_automation():
    # --- Browser Setup ---
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Background mein chalega
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Naukri Automation shuru kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login via UI
        print("🔐 Logging in...")
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("✅ Login Success. Session capture kar raha hoon...")
        time.sleep(15) # Wait for dashboard to load completely

        # 2. Extract Session Cookies for API
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # 3. Step 1: Resume Upload (Backend API)
        # Isse recruiter search mein top par aoge
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print("🚀 API se Resume upload kar raha hoon...")
            upload_url = "https://www.naukri.com/mnjuser/profile/uploadResume"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.naukri.com/mnjuser/profile"
            }
            with open(resume_path, 'rb') as f:
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                payload = {'isResumeUpload': '1'}
                response = session.post(upload_url, files=files, data=payload, headers=headers)
            
            if response.status_code == 200:
                print("✅ Resume API Upload: Success!")
            else:
                print(f"⚠️ Resume API failed with status: {response.status_code}")
        else:
            print("❌ Error: Resume.pdf file nahi mili!")

        # 4. Step 2: Headline Update (To Force UI Refresh)
        # Isse dashboard par 'Updated Today' likha aayega
        print("✍️ Headline refresh kar raha hoon...")
        headline_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        
        # Azure Engineer Headline
        headline_base = "Azure Infrastructure and Data Engineer | Azure Synapse | Bicep | Kubernetes (AKS)"
        # Har baar different banane ke liye dot toggle
        headline_final = headline_base + ("." if int(time.time()) % 2 == 0 else "")
        
        h_headers = {
            "Content-Type": "application/json",
            "Clientid": "d36980564696075936856",
            "Appid": "121",
            "Systemid": "121",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        h_res = session.put(headline_url, json={"resumeHeadline": headline_final}, headers=h_headers)
        
        if h_res.status_code in [200, 201, 204]:
            print("✅ Headline Refresh: Success!")
        else:
            print(f"⚠️ Headline API Error: {h_res.status_code}")

        # 5. Final Step: Profile Page Visit
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        print("🏁 MISSION ACCOMPLISHED: Profile ek dum fresh hai!")

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_automation()
