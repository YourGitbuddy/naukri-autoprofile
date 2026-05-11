import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def run_ultimate_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Ultimate Login shuru kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Step 1: Login via direct JS Injection
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("Login done. Forcing Profile Update...")
        time.sleep(15)

        # Step 2: Jump directly to the Summary Edit URL if possible, else use standard profile
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Step 3: Hard-Target the textarea using JS focus then Selenium keys
        # Naukri Campus usually has a textarea for 'Profile Summary'
        print("Targeting Summary Textarea...")
        
        script = """
        let area = document.querySelector('textarea') || document.querySelector('.desc') || document.querySelector('#summary-textarea');
        if(area) {
            area.focus();
            return true;
        }
        return false;
        """
        found = driver.execute_script(script)

        if found:
            element = driver.switch_to.active_element
            val = element.get_attribute("value") or "Azure Infrastructure Engineer"
            
            # Toggle dot
            new_val = val[:-1] if val.endswith('.') else val + '.'
            
            # Select all and replace
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.BACKSPACE)
            element.send_keys(new_val)
            time.sleep(2)
            
            # Click Save using a broad search
            save_script = """
            let btns = Array.from(document.querySelectorAll('button'));
            let saveBtn = btns.find(b => b.innerText.includes('Save'));
            if(saveBtn) { saveBtn.click(); return true; }
            return false;
            """
            driver.execute_script(save_script)
            print(f"🏁 MISSION ACCOMPLISHED: Profile refreshed with value toggle!")
        else:
            # Last ditch effort: Resume upload via Input type=file
            print("Summary nahi mila, Resume re-upload try kar raha hoon...")
            resume_path = os.path.join(os.getcwd(), "Resume.pdf")
            if os.path.exists(resume_path):
                file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(resume_path)
                print("🏁 MISSION ACCOMPLISHED: Resume uploaded via generic selector!")
            else:
                raise Exception("Bhai, Resume.pdf file hi nahi mili repo mein!")

    except Exception as e:
        print(f"❌ Abhi bhi lafda hai: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_ultimate_refresh()
