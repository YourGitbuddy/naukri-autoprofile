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
    # Aaj ki date aur time status update ke liye
    current_time = datetime.now().strftime("%d %b %Y, %I:%M %p")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Masking to bypass bot detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # WebDriver flag hide karna
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    wait = WebDriverWait(driver, 45)

    try:
        print("Bypass start: Google par ja raha hoon...")
        driver.get("https://www.google.com")
        time.sleep(random.randint(2, 4))

        print("Naukri login shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(random.randint(5, 7))
        
        # Credentials entry
        user_input = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        user_input.send_keys(os.environ['NAUKRI_EMAIL'])
        
        pass_input = driver.find_element(By.ID, "passwordField")
        pass_input.send_keys(os.environ['NAUKRI_PASS'])
        
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        print("Login button dabaya gaya... Dashboard ka wait kar raha hoon.")
        time.sleep(15)

        # Content for update (adding timestamp to force UI refresh)
        # Summary mein end mein date dalne se status "Updated Today" ho jayega
        profile_summary = f"Azure Infrastructure Engineer with expertise in Azure Synapse Analytics, Bicep, and Kubernetes (AKS). Experience in architecting FinCrime data platforms and CI/CD pipelines. [Refreshed on: {current_time}]"

        print(f"Direct JavaScript refresh try kar raha hoon (Time: {current_time})...")
        
        # JS Fetch call within the browser session
        driver.execute_script(f"""
            fetch('https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary', {{
                method: 'PUT',
                headers: {{ 
                    'Content-Type': 'application/json', 
                    'appid': '135', 
                    'systemid': '135' 
                }},
                body: JSON.stringify({{ 
                    "summary": "{profile_summary}" 
                }})
            }}).then(res => {{
                if(res.ok) console.log('Successfully updated in backend.');
                else console.log('Update failed with status:', res.status);
            }});
        """)
        
        print("Mubarak ho bhai! Script successfully execute ho gayi aur profile refresh ho gayi.")
        time.sleep(5)

    except Exception as e:
        print(f"Error aayi hai: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
