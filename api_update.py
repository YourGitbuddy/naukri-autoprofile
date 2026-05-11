import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_nuke_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Final Nuke Mission shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.find_element("xpath", "//button[text()='Login']").click()
        
        print("✅ Login Success.")
        time.sleep(15) 

        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print("🚀 Uploading + Syncing Resume...")
            
            # Ye headers Campus/Professional dono ke liye 'Real' lagte hain
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.naukri.com/mnjuser/profile",
                "Origin": "https://www.naukri.com",
                "Accept": "application/json, text/javascript, */*; q=0.01"
            }

            with open(resume_path, 'rb') as f:
                # 1. First Hit: The Upload
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                data = {
                    'isResumeUpload': '1',
                    'm_id': '', # Campus profiles often need this empty or dynamic
                    'appId': '121'
                }
                res = session.post("https://www.naukri.com/mnjuser/profile/uploadResume", 
                                   files=files, data=data, headers=headers)
                
            if res.status_code == 200:
                print("✅ Server accepted file. Now triggering Profile Sync...")
                
                # 2. Second Hit: Profile Save Trigger (The missing piece)
                # Ye Naukri ko bolta hai ki "Changes save karo"
                sync_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile/refresh"
                sync_res = session.post(sync_url, headers={"Clientid": "d36980564696075936856", "Appid": "121", "Systemid": "121"})
                
                print(f"🏁 Sync Status: {sync_res.status_code}. Mission Finished!")
            else:
                print(f"❌ Upload Fail: {res.status_code}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_nuke_update()
