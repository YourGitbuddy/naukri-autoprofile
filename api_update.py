import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_universal_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 40)

    try:
        print("Bhai, Resilient Login shuru kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Inject Credentials via JS
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login done. Waiting for dashboard...")
        time.sleep(10)
        
        # Seedha Profile Page par jump
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Handle potential popups (JS bypass)
        driver.execute_script("const popups = document.querySelectorAll('.crossIcon, .close-icon, .skip-btn'); popups.forEach(p => p.click());")

        print("Headline refresh trigger kar raha hoon...")
        
        # Try finding the edit icon with a more flexible XPATH
        try:
            edit_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Resume headline')]/..//span[contains(@class, 'edit')]")))
            driver.execute_script("arguments[0].scrollIntoView(true);", edit_icon)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", edit_icon)
        except:
            print("Standard edit button nahi mila, forcing direct element focus...")
            # Fallback: Agar edit icon nahi mila, toh try targeting the ID directly if it exists
            driver.execute_script("document.querySelector('.headline .icon').click();")

        # Edit Text
        headline_txt = wait.until(EC.presence_of_element_located((By.ID, "resumeHeadlineTxt")))
        current_val = headline_txt.get_attribute("value")
        
        # Toggle a Dot (.)
        new_val = current_val[:-1] if current_val.endswith('.') else current_val + '.'
        
        driver.execute_script("arguments[0].value = '';", headline_txt)
        headline_txt.send_keys(new_val)
        
        # Save - Multiple ways to find the save button
        try:
            save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
            driver.execute_script("arguments[0].click();", save_btn)
        except:
            driver.execute_script("document.querySelector('button[type=\"submit\"]').click();")
        
        print(f"🏁 MISSION ACCOMPLISHED: Profile refreshed! (Value: {new_val})")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Final Attempt Failed: {str(e)}")
        driver.save_screenshot("debug_error.png")
        raise e
    finally:
        driver.quit()

if __name__ == "__main__":
    run_universal_refresh()
