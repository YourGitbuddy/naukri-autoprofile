import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_clean_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Auto-detect path
    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:
        print("🚀 Starting Clean Sync...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Login
        driver.find_element(By.ID, "usernameField").send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(10)

        # Session Setup
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # API Sniper (Status 200 = Success)
        if os.path.exists(resume_path):
            with open(resume_path, 'rb') as f:
                res = session.post("https://www.naukri.com/mnjuser/profile/uploadResume", 
                                    files={'resume': ('Resume.pdf', f, 'application/pdf')}, 
                                    data={'isResumeUpload': '1'}, 
                                    headers={"X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0"})
                
                if res.status_code == 200:
                    print("🏁 FINAL STATUS: Resume pushed to server successfully.")
        
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_clean_update()
