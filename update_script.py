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
        # 1. Login to get Session Cookies
        print("Logging into Naukri to capture session...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        time.sleep(15)

        # 2. Extract Session Cookies and Tokens
        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # System and App Headers (Naukri standard)
        headers = {
            'x-requested-with': 'XMLHttpRequest',
            'appid': '135',
            'systemid': '135',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        # 3. Upload Resume via API
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print(f"Resume uploading via API: {resume_path}")
            
            with open(resume_path, 'rb') as f:
                files = {
                    'resume': ('Resume.pdf', f, 'application/pdf')
                }
                # Naukri's official upload endpoint
                response = session.post(
                    'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume',
                    headers=headers,
                    files=files
                )
            
            if response.status_code in [200, 201]:
                print("✅ Success! Resume uploaded and profile refreshed.")
            else:
                print(f"❌ Upload failed. Status: {response.status_code}, Response: {response.text}")
        else:
            print("❌ Error: 'Resume.pdf' not found in repository.")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
