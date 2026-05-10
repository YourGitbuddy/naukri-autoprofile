import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_campus_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 30)

    try:
        print("Bhai, Resilient Campus Login shuru kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Step 1: Login via JS
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login done. Profile page par ja raha hoon...")
        time.sleep(12)
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Step 2: Update Profile Summary via JS (Directly)
        # Yeh script summary edit box ko dhoondegi aur toggle karegi
        print("Summary update trigger kar raha hoon...")
        
        update_script = """
        let summaryText = document.querySelector('.profile-summary .desc') || document.querySelector('.summary-content');
        let editIcon = document.querySelector('.profile-summary .edit') || document.querySelector('span.edit.icon');
        
        if (editIcon) {
            editIcon.click(); // Open editor
            setTimeout(() => {
                let textarea = document.querySelector('textarea[name="summary"]') || document.querySelector('#summary-textarea') || document.querySelector('textarea');
                if (textarea) {
                    let val = textarea.value;
                    textarea.value = val.endsWith('.') ? val.slice(0, -1) : val + '.';
                    document.querySelector('button[type="submit"]').click(); // Save
                }
            }, 3000);
            return "Success: Found and Toggled";
        }
        return "Error: Could not find edit icon";
        """
        
        result = driver.execute_script(update_script)
        print(f"JS Execution Result: {result}")
        
        # Thoda wait save hone ke liye
        time.sleep(7)
        print("🏁 MISSION ACCOMPLISHED: Profile refresh success!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
        raise e
    finally:
        driver.quit()

if __name__ == "__main__":
    run_campus_refresh()
