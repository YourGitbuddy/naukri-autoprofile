import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_double_trigger():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Double Trigger shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("✅ Login Success. Capturing Session...")
        time.sleep(10) 

        # Step 1: Upload Resume via API
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            with open(resume_path, 'rb') as f:
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                session.post("https://www.naukri.com/mnjuser/profile/uploadResume", files=files, data={'isResumeUpload': '1'})
            print("🚀 Resume sent to server.")

        # Step 2: Trigger UI Refresh (Headline Update)
        # Isse Naukri ko majboor hona padega update date change karne ke liye
        headline_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        headline_text = "Azure Infrastructure and Data Engineer | Azure Synapse | Bicep | Kubernetes (AKS)"
        if int(time.time()) % 2 == 0: headline_text += "."
        
        headers = {
            "Content-Type": "application/json",
            "Clientid": "d36980564696075936856",
            "Appid": "121",
            "Systemid": "121"
        }
        
        res = session.put(headline_url, json={"resumeHeadline": headline_text}, headers=headers)
        
        if res.status_code in [200, 201, 204]:
            print("🏁 MISSION ACCOMPLISHED: Resume + Headline updated! Ab pakka dikhega.")
        else:
            print("⚠️ Headline fail, par resume background mein gaya hoga.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_double_trigger()
