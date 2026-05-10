import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_naukri_update():
    # Dynamic dot ya space add karne ke liye taaki content har baar badle
    toggle = "." if random.randint(0, 1) == 0 else "" 
    current_time = datetime.now().strftime("%d %b %Y")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 45)

    try:
        print("Bypass start...")
        driver.get("https://www.google.com")
        time.sleep(2)

        print("Naukri login...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("Login done. Waiting for session...")
        time.sleep(15)

        # Content for update
        # Headline update sabse powerful hai date refresh karne ke liye
        headline = f"Azure Infrastructure and Data Engineer | Synapse | Bicep | AKS{toggle}"
        summary = f"Azure Infrastructure Engineer specializing in Synapse, Bicep, and AKS. (Last updated: {current_time})"

        print("Force Refreshing Headline and Summary via API...")
        
        driver.execute_script(f"""
            // 1. Update Resume Headline (Status change ke liye sabse best)
            fetch('https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume-headline', {{
                method: 'PUT',
                headers: {{ 'Content-Type': 'application/json', 'appid': '135', 'systemid': '135' }},
                body: JSON.stringify({{ "resumeHeadline": "{headline}" }})
            }});

            // 2. Update Profile Summary
            fetch('https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary', {{
                method: 'PUT',
                headers: {{ 'Content-Type': 'application/json', 'appid': '135', 'systemid': '135' }},
                body: JSON.stringify({{ "summary": "{summary}" }})
            }});
        """)
        
        print(f"Success! Headline updated with toggle '{toggle}'")
        time.sleep(5)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
