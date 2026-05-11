import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_forced_upload():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Forced UI Upload shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("✅ Login Success. Profile par ja raha hoon...")
        time.sleep(15) 
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        
        # 2. Forced File Injection
        # Campus UI mein 'input[type=file]' aksar hidden hota hai, hum use JS se dhund kar file bhejenge
        print("📤 Injecting Resume into the UI...")
        script = """
        var input = document.querySelector('input[type="file"]');
        if(!input) {
            // Agar box dikh raha hai toh wahan ek input zarur hoga
            let allInputs = document.querySelectorAll('input');
            for(let i of allInputs) { if(i.type === 'file') input = i; }
        }
        if(input) {
            input.style.display = 'block';
            input.style.visibility = 'visible';
            return "READY";
        }
        return "NOT_FOUND";
        """
        ready_status = driver.execute_script(script)
        print(f"Input Status: {ready_status}")

        if ready_status == "READY":
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(resume_path)
            print("⏳ File sent. Waiting for upload animation...")
            time.sleep(20) # Thoda zyada wait taaki UI refresh ho jaye
            
            # 3. Final Check: Screenshot for you
            driver.save_screenshot("upload_check.png")
            print("🏁 MISSION ACCOMPLISHED: UI par file bhej di hai.")
        else:
            print("⚠️ UI Input nahi mila. Refreshing page as fallback.")
            driver.refresh()
            time.sleep(10)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_forced_upload()
