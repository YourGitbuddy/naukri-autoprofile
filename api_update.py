import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_summary_sniper():
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

        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("Login done. Session capture kar raha hoon...")
        time.sleep(15) 

        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # --- NAYA ENDPOINT: Profile Summary Update ---
        # Ye endpoint usually 501 nahi deta
        url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-summary"
        
        headers = {
            "Content-Type": "application/json",
            "Clientid": "d36980564696075936856",
            "Appid": "121",
            "Systemid": "121",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # Azure Infrastructure Engineer Summary
        summary_base = "Azure Infrastructure and Data Engineer with expertise in Synapse, Bicep, and Kubernetes (AKS). Working on FinCrime AI platforms."
        
        # Har update ko unique banane ke liye toggle
        dot = "." if int(time.time()) % 2 == 0 else ""
        payload = {"profileSummary": f"{summary_base}{dot}"}
        
        print(f"Summary Sniper firing... (Dot status: {'On' if dot else 'Off'})")
        response = session.put(url, json=payload, headers=headers)

        if response.status_code in [200, 201, 204]:
            print(f"🏁 MISSION ACCOMPLISHED: Profile Summary updated successfully!")
        else:
            print(f"⚠️ Summary API failed (Status: {response.status_code}). Triggering Profile Visit...")
            driver.get("https://www.naukri.com/mnjuser/profile")
            time.sleep(5)
            print("🏁 Fallback success: Last Active timestamp updated.")

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_summary_sniper()
