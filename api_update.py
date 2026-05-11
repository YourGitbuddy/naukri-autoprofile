import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_silent_sniper():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Silent Sniper Mission shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login via Selenium
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.find_element("xpath", "//button[text()='Login']").click()
        
        print("✅ Login Success. Cookies extract kar raha hoon...")
        time.sleep(15) 

        # 2. Extract Cookies
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # 3. Direct API Upload
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print(f"🚀 Resume mil gaya. API Tunneling shuru...")
            
            # Naukri Profile Update API
            url = "https://www.naukri.com/mnjuser/profile/uploadResume"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.naukri.com",
                "Referer": "https://www.naukri.com/mnjuser/profile"
            }

            with open(resume_path, 'rb') as f:
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                data = {'isResumeUpload': '1'}
                response = session.post(url, files=files, data=data, headers=headers)

            # Verification logic
            if response.status_code == 200:
                print("🏁 MISSION ACCOMPLISHED: Resume updated successfully via Backend!")
                # Optional: Ek baar profile visit kar lo 'Last Active' update karne ke liye
                driver.get("https://www.naukri.com/mnjuser/profile")
                time.sleep(5)
            else:
                print(f"❌ API Error: {response.status_code}. Profile status: {response.text[:100]}")
        else:
            print("❌ Error: Resume.pdf nahi mili!")

    except Exception as e:
        print(f"❌ Critical Exception: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_silent_sniper()
