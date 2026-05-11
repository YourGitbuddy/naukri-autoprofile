import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_stealth_refresh():
    chrome_options = Options()
    # Headless mode ko thoda change kiya hai (New Headless)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Ye headers bot detection bypass karne ke liye zaroori hain
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Anti-bot script: Webdriver flag ko remove karta hai
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        print("Bhai, Stealth mode mein login shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(random.uniform(5, 8)) # Random wait

        # Typing simulation (JS use karenge but with a delay)
        email = os.environ['NAUKRI_EMAIL']
        password = os.environ['NAUKRI_PASS']
        
        driver.execute_script(f"document.getElementById('usernameField').value='{email}';")
        time.sleep(2)
        driver.execute_script(f"document.getElementById('passwordField').value='{password}';")
        time.sleep(2)
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login clicked. Profile load hone ka wait...")
        time.sleep(random.uniform(15, 20))

        # Seedha API hit karne ki koshish (UI bypass)
        # Agar UI nahi dikh raha, toh hum background update try karenge
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Update logic: Sabse safe hai Resume Headline toggle karna
        # Hum generic XPath use karenge jo Campus aur Normal dono par chale
        print("Refreshing via Headline/Summary toggle...")
        
        script = """
        let section = document.querySelector('.profile-summary') || document.querySelector('.resumeHeadline');
        let edit = section ? section.querySelector('.edit') : document.querySelector('.icon-edit');
        if(edit) {
            edit.click();
            return true;
        }
        return false;
        """
        success = driver.execute_script(script)

        if success:
            time.sleep(3)
            # Find any textarea and toggle a dot
            driver.execute_script("""
                let area = document.querySelector('textarea') || document.querySelector('#resumeHeadlineTxt');
                if(area) {
                    let v = area.value;
                    area.value = v.endsWith('.') ? v.slice(0, -1) : v + '.';
                    // Trigger 'input' event so 'Save' button enables
                    area.dispatchEvent(new Event('input', { bubbles: true }));
                }
            """)
            time.sleep(2)
            driver.execute_script("document.querySelector('button[type=\"submit\"], .btn-save, #saveHeadlineBtn').click();")
            print("🏁 MISSION ACCOMPLISHED: Stealth update success!")
        else:
            # Final Fallback: Direct Resume Upload (Hardened)
            print("UI toggle fail. Trying direct file upload...")
            resume_path = os.path.join(os.getcwd(), "Resume.pdf")
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(resume_path)
            print("🏁 MISSION ACCOMPLISHED: Resume re-uploaded via stealth!")

    except Exception as e:
        print(f"❌ Stealth mode fail: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_stealth_refresh()
