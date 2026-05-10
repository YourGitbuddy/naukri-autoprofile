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

def run_hardened_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 30)

    try:
        print("Bhai, Resilient login shuru kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Use JS to inject credentials directly (Bypasses "Not Interactable" errors)
        email = os.environ['NAUKRI_EMAIL']
        password = os.environ['NAUKRI_PASS']
        
        driver.execute_script(f"document.getElementById('usernameField').value='{email}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{password}';")
        
        print("Credentials injected. Clicking Login...")
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        time.sleep(10)
        
        # Step 2: Session verify aur Cookies nikalna
        selenium_cookies = driver.get_cookies()
        if not selenium_cookies:
            raise Exception("Cookies empty hain, login fail hua shayad.")

        session = requests.Session()
        for cookie in selenium_cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Step 3: API Update (Headline)
        profile_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-headline"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Appid": "109",
            "Systemid": "109",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.naukri.com/mnjuser/profile"
        }

        res = session.get(profile_url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            headline = data.get('resumeHeadline', 'Azure Infrastructure Engineer')
            new_headline = headline[:-1] if headline.endswith('.') else headline + '.'
            
            update_res = session.put(profile_url, json={"resumeHeadline": new_headline}, headers=headers)
            if update_res.status_code in [200, 204]:
                print("🏁 MISSION ACCOMPLISHED: Profile refresh success via JS injection!")
            else:
                print(f"❌ API Update failed: {update_res.status_code}")
        else:
            print(f"❌ Failed to fetch headline: {res.status_code}. Response: {res.text[:100]}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_hardened_refresh()
