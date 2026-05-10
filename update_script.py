import os
import time
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
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Ye line automation detection ko bypass karti hai
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Overriding the navigator.webdriver property
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    wait = WebDriverWait(driver, 40)

    try:
        print("Bhai, Stealth mode mein login shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Human-like typing delay
        user_input = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        user_input.send_keys(os.environ['NAUKRI_EMAIL'])
        time.sleep(2)
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login done, waiting for Dashboard...")
        time.sleep(10)

        # Profile page par jaao
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print(f"Uploading Resume: {resume_path}")
            
            # Naukri ka hidden input dhoondne ka aakhri rasta
            # Hum JS se input dhundenge aur seedha path bhejenge
            script = """
            var input = document.querySelector('input[type="file"]');
            if(!input) {
                input = document.querySelector('#attachCV');
            }
            return input;
            """
            file_input = driver.execute_script(script)
            
            if file_input:
                file_input.send_keys(resume_path)
                print("Wait kar raha hoon upload finish hone ka...")
                time.sleep(20) 
                print("✅ Mission Accomplished! Profile is now Fresh.")
            else:
                print("❌ Element nahi mila, screenshot le raha hoon.")
                driver.save_screenshot("no_element.png")
        else:
            print("❌ Resume.pdf missing!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("final_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
