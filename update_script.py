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
        # Step 1: Login via Selenium to get fresh cookies
        print("Bhai, login start ho raha hai...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        email_field = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        # Wait for dashboard to ensure login is complete
        time.sleep(15)

        # Step 2: Transfer cookies from Selenium to Requests
        print("Cookies transfer kar raha hoon...")
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        # Step 3: Fetch unique App-ID/Token if needed (Optional but safe)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Referer': 'https://www.naukri.com/mnjuser/profile',
            'X-Requested-With': 'XMLHttpRequest',
            'appid': '135',
            'systemid': '135'
        }

        # Step 4: Final Upload via API
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print(f"API se Resume bhej raha hoon: {resume_path}")
            
            with open(resume_path, 'rb') as f:
                # Naukri ka primary resume upload endpoint
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                # Is URL ko Naukri ne v1/users/self/resume par update kiya hai
                response = session.post(
                    'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v1/users/self/resume',
                    headers=headers,
                    files=files
                )
            
            if response.status_code in [200, 201, 204]:
                print("✅ Mission Success! Resume upload ho gaya.")
            else:
                # Retry with fallback URL v0 if v1 fails
                print(f"v1 failed ({response.status_code}), trying v0...")
                response_v0 = session.post(
                    'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume',
                    headers=headers,
                    files=files
                )
                if response_v0.status_code in [200, 201]:
                    print("✅ Mission Success via v0!")
                else:
                    print(f"❌ Dono API fail ho gayi: {response_v0.status_code}")
        else:
            print("❌ Error: Resume.pdf nahi mili repo mein.")

    except Exception as e:
        print(f"❌ Error aayi: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
