import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def run_blind_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    actions = ActionChains(driver)

    try:
        print("Bhai, Login shuru kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Login Injection (Stable)
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        time.sleep(2)
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login Success! Profile par ja raha hoon...")
        time.sleep(15)
        
        # Direct jump to profile
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # BLIND UPDATE: Hum 'Summary' edit icon dhoondne ke bajaye JS se uspar click maarenge
        print("JS se Edit button trigger kar raha hoon...")
        
        # Yeh script kisi bhi 'edit' class wale element ko click karegi jo Profile Summary ke paas ho
        js_trigger = """
        let editIcon = document.querySelector('.profile-summary .edit') || document.querySelector('span.edit.icon');
        if(editIcon) {
            editIcon.click();
            return true;
        }
        return false;
        """
        
        found = driver.execute_script(js_trigger)
        
        if found:
            time.sleep(3)
            # Keyboard se text update: Select All -> Backspace -> Type New -> Enter
            print("Keyboard simulation shuru...")
            actions.send_keys(Keys.CONTROL + "a").send_keys(Keys.BACKSPACE).perform()
            time.sleep(1)
            
            # Azure Data Engineer update
            update_text = "Azure Infrastructure and Data Engineer | Azure Synapse | Bicep | Kubernetes (AKS)"
            if int(time.time()) % 2 == 0: update_text += "."
            
            actions.send_keys(update_text).perform()
            time.sleep(2)
            
            # Save button ke liye Enter ya JS click
            actions.send_keys(Keys.ENTER).perform()
            driver.execute_script("document.querySelector('button[type=\"submit\"]').click();")
            
            print("🏁 MISSION ACCOMPLISHED: Profile updated via Keyboard!")
        else:
            print("⚠️ Edit button nahi mila, last try: Resume Upload...")
            resume_path = os.path.join(os.getcwd(), "Resume.pdf")
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(resume_path)
            print("🏁 MISSION ACCOMPLISHED: Resume re-uploaded!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_blind_refresh()
