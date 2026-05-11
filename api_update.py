import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_naukri_clean_sweep():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Clean Sweep Mission shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login to get Fresh Cookies
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.find_element("xpath", "//button[text()='Login']").click()
        
        print("✅ Login Success. Cookies capture kar raha hoon...")
        time.sleep(15) 

        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # 2. Direct API Hit (Jo pichli baar 200 OK de gaya)
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print("🚀 API Sniper Se Resume bhej raha hoon...")
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.naukri.com/mnjuser/profile"
            }

            with open(resume_path, 'rb') as f:
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                data = {'isResumeUpload': '1'}
                response = session.post("https://www.naukri.com/mnjuser/profile/uploadResume", 
                                        files=files, data=data, headers=headers)

            if response.status_code == 200:
                print("🏁 MISSION ACCOMPLISHED: Server ne 200 OK diya. Resume update ho gaya!")
            else:
                print(f"⚠️ API Response: {response.status_code}")
        
        # 3. Last Touch: Profile Visit
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_clean_sweep()
