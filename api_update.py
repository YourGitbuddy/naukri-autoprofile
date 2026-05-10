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
    wait = WebDriverWait(driver, 45)

    try:
        print("Bhai, Naukri Campus login shuru kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Inject Credentials via JS
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login done. Profile page par ja raha hoon...")
        time.sleep(12)
        
        # Direct jump to profile
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Target: Profile Summary (as seen in your screenshot)
        print("Profile Summary section dhoond raha hoon...")
        
        # Edit icon for Profile Summary
        edit_icon = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Profile Summary')]/..//span[contains(@class, 'edit')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", edit_icon)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", edit_icon)
        
        # Textarea handle (Naukri Campus uses textarea for summary)
        summary_txt = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[contains(@id, 'summary')] | //textarea[contains(@class, 'desc')] | //textarea")))
        current_val = summary_txt.get_attribute("value")
        
        # Toggle a Dot (.)
        new_val = current_val[:-1] if current_val.endswith('.') else current_val + '.'
        
        driver.execute_script("arguments[0].value = '';", summary_txt)
        summary_txt.send_keys(new_val)
        
        # Save Button
        save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
        driver.execute_script("arguments[0].click();", save_btn)
        
        print(f"🏁 MISSION ACCOMPLISHED: Campus Profile updated! New Summary ends with: '{new_val[-1]}'")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
        raise e
    finally:
        driver.quit()

if __name__ == "__main__":
    run_campus_refresh()
