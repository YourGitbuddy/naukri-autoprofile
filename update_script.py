import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_naukri_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 45)

    try:
        print("Bhai, login start ho raha hai...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        email_field = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        time.sleep(15)

        print("Cookies transfer kar raha hoon...")
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://www.naukri.com/mnjuser/profile',
            'x-requested-with': 'XMLHttpRequest',
            'appid': '135',
            'systemid': '135'
        }

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            # API Retry Logic
            urls = [
                'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v1/users/self/resume',
                'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume'
            ]
            
            success = False
            for url in urls:
                print(f"Trying API: {url}")
                # File ko har baar naye siray se open karenge taaki 'closed file' error na aaye
                with open(resume_path, 'rb') as f:
                    files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                    response = session.post(url, headers=headers, files=files)
                
                if response.status_code in [200, 201, 204]:
                    print(f"✅ Mission Success! Profile updated via {url.split('/')[-2]}.")
                    success = True
                    break
                else:
                    print(f"❌ Failed for {url.split('/')[-2]} (Status: {response.status_code})")
            
            if not success:
                print("❌ Dono API fail ho gayi hain.")
        else:
            print("❌ Resume.pdf nahi mili repo mein.")

    except Exception as e:
        print(f"❌ Error aayi: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
