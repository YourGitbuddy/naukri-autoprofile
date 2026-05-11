import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def run_brute_force_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    actions = ActionChains(driver)

    try:
        print("Bhai, Brute Force Login shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Step 1: Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("Login done. Profile page par ja raha hoon...")
        time.sleep(15)
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Step 2: Try updating Headline/Summary via standard JS injection first (Fastest)
        # Using a very broad script to find ANY text container
        print("Finding ANY updateable field...")
        update_success = driver.execute_script("""
            let fields = document.querySelectorAll('textarea, [contenteditable="true"], #resumeHeadlineTxt, .desc');
            if (fields.length > 0) {
                let area = fields[0];
                area.focus();
                let val = area.value || area.innerText;
                let newVal = val.endsWith('.') ? val.slice(0, -1) : val + '.';
                if(area.value !== undefined) area.value = newVal;
                else area.innerText = newVal;
                return true;
            }
            return false;
        """)

        if update_success:
            print("Field mil gaya! Saving...")
            # Try to hit Enter or find a Save button
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(5)
            driver.execute_script("Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Save')).click();")
            print("🏁 MISSION ACCOMPLISHED: Updated via JS Injection!")
        else:
            # Step 3: Keyboard Brute Force (The "Tab-Tab-Enter" Method)
            print("JS fail ho gaya. Keyboard simulation shuru...")
            # Profile page par resume upload button aksar first few tabs mein hota hai
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            
            # Send Keys to the 'body' directly
            body = driver.find_element(By.TAG_NAME, "body")
            resume_path = os.path.join(os.getcwd(), "Resume.pdf")
            
            # Hum saare file inputs dhoond kar sabme path bhej denge (Shotgun approach)
            file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
            if file_inputs:
                for f_input in file_inputs:
                    try:
                        f_input.send_keys(resume_path)
                        print(f"File sent to an input field!")
                    except:
                        continue
                print("🏁 MISSION ACCOMPLISHED: Resume sent to all available file slots!")
            else:
                # If still nothing, take a screenshot and bail
                driver.save_screenshot("debug_error.png")
                print("❌ Bhai, page par kuch mil hi nahi raha. Screenshot check kar.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_brute_force_refresh()
