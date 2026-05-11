import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_nuclear_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Login trigger kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Login process
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("Login done. Cookies extract kar raha hoon...")
        time.sleep(15) # Wait for session to establish

        # Step 1: Extract Cookies from Selenium to use in Requests
        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Step 2: Push Direct Profile Update via Cloudgateway API
        # Yeh wahi API hai jo Naukri ka 'Save' button dabane par chalti hai
        url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        
        headers = {
            "Content-Type": "application/json",
            "Clientid": "d36980564696075936856",
            "Appid": "121",
            "Systemid": "121",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # Azure Infrastructure Engineer headline refresh logic
        headline = "Azure Infrastructure and Data Engineer | Azure Synapse | Bicep | Kubernetes (AKS)"
        if int(time.time()) % 2 == 0:
            headline += "."

        payload = {"resumeHeadline": headline}
        
        print("API Sniper firing...")
        response = session.put(url, json=payload, headers=headers)

        if response.status_code in [200, 201, 204]:
            print(f"🏁 MISSION ACCOMPLISHED: Profile updated via API Tunneling! Status: {response.status_code}")
        else:
            print(f"⚠️ API Tunneling failed (Status: {response.status_code}). Trying Fallback...")
            # Fallback: Just hit the profile URL to update 'Last Active'
            driver.get("https://www.naukri.com/mnjuser/profile")
            time.sleep(5)
            print("🏁 Fallback success: Profile visited.")

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_nuclear_refresh()
