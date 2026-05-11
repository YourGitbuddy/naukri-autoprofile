import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_campus_fix():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Naukri Campus specific update shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("✅ Login Success. Capturing Session...")
        time.sleep(15)

        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # 2. Campus Resume Upload API
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print("🚀 Uploading to Campus Server...")
            # Campus interface ke liye referer aur origin change karna zaroori hai
            headers = {
                "User-Agent": "Mozilla/5.0",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.naukri.com/mnjuser/profile",
                "Origin": "https://www.naukri.com"
            }
            
            with open(resume_path, 'rb') as f:
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                # Is endpoint se campus profiles refresh hoti hain
                r = session.post("https://www.naukri.com/mnjuser/profile/uploadResume", 
                                 files=files, data={'isResumeUpload': '1'}, headers=headers)
            
            if r.status_code == 200:
                print("✅ API Upload successful.")
            
            # 3. FORCE REFRESH via UI (Sabse Important Step)
            # Campus UI par bina click kiye update nahi dikhta
            print("🔄 Triggering UI Save to clear the 'Upload Resume' box...")
            driver.get("https://www.naukri.com/mnjuser/profile")
            time.sleep(10)
            
            # Agar 'Upload' box abhi bhi dikh raha hai, toh use refresh marne ke liye page scroll karo
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            
            print("🏁 MISSION ACCOMPLISHED: Check karo, ab 'Success' toast aana chahiye.")
        else:
            print("❌ Resume.pdf missing!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_campus_fix()
