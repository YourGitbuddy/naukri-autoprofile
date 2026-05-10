import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_naukri_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Naya headless mode jo kam detect hota hai
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Advanced Masking: Real browser dikhne ke liye
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Automation flag hide karne ke liye
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    wait = WebDriverWait(driver, 45)

    try:
        # Step 1: Pehle Google par jao (Referrer bypass)
        print("Bypass start: Google par ja raha hoon...")
        driver.get("https://www.google.com")
        time.sleep(random.randint(2, 5))

        # Step 2: Login Page
        print("Naukri login shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(random.randint(5, 8))
        
        # Check if blocked
        if "Access Denied" in driver.title or "www.naukri.com" == driver.title:
            print("Abhi bhi block hai. Screenshot save kar raha hoon.")
            driver.save_screenshot("blocked.png")
            # Ek baar mobile login page try karte hain (kam secure hota hai)
            driver.get("https://www.naukri.com/mnjuser/profile")
        
        # Login fields fill karna
        user_input = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        user_input.send_keys(os.environ['NAUKRI_EMAIL'])
        
        pass_input = driver.find_element(By.ID, "passwordField")
        pass_input.send_keys(os.environ['NAUKRI_PASS'])
        
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        print("Login button dabaya gaya...")
        time.sleep(10)

        # Step 3: Seedha Profile Summary Update API hit karna (Browser ke andar se)
        # Kyunki login ho chuka hai, hum JS se direct profile hit kar sakte hain
        print("Direct JavaScript refresh try kar raha hoon...")
        driver.execute_script("""
            fetch('https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'appid': '135', 'systemid': '135' },
                body: json.stringify({ "summary": "Azure Infrastructure Engineer | Synapse | Bicep | AKS" })
            }).then(res => console.log('Update Status:', res.status));
        """)
        
        print("Kaam ho gaya! Refresh command bhej di gayi hai.")
        time.sleep(5)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
