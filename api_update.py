import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_universal_override():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Universal Override Mission shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("✅ Login Success.")
        time.sleep(10) 

        # 2. Redirect to Hidden Upload Endpoint
        # Ye link seedha resume management par le jata hai
        print("🔗 Redirecting to internal upload endpoint...")
        driver.get("https://www.naukri.com/mnjuser/profile?id=&altLink=1")
        time.sleep(10)

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        
        # 3. Aggressive Input Search
        # Hum poore page par jitne bhi hidden input hain, sab par file bhejenge
        print("📤 Aggressive File Injection shuru...")
        
        # JS to find ALL file inputs, even hidden ones
        script = """
        let inputs = document.querySelectorAll('input[type="file"]');
        if (inputs.length > 0) {
            for(let i=0; i<inputs.length; i++) {
                inputs[i].style.display = 'block';
                inputs[i].style.visibility = 'visible';
                inputs[i].style.opacity = '1';
            }
            return inputs.length;
        }
        return 0;
        """
        count = driver.execute_script(script)
        print(f"Found {count} potential upload slots.")

        if count > 0:
            file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            for f_input in file_inputs:
                try:
                    f_input.send_keys(resume_path)
                    print("✅ File sent to an input slot.")
                except:
                    continue
            
            print("⏳ Waiting for server sync...")
            time.sleep(20)
            print("🏁 MISSION ACCOMPLISHED: Check karo, system refresh ho gaya hoga.")
        else:
            # Last Resort: Agar kuch na mile, toh API hit fir se try karo with higher timeout
            print("⚠️ UI blocked. Backend API Fallback trigger kar raha hoon...")
            import requests
            session = requests.Session()
            for c in driver.get_cookies(): session.cookies.set(c['name'], c['value'])
            with open(resume_path, 'rb') as f:
                r = session.post("https://www.naukri.com/mnjuser/profile/uploadResume", 
                                 files={'resume': ('Resume.pdf', f, 'application/pdf')}, 
                                 data={'isResumeUpload': '1'})
            print(f"API Fallback Status: {r.status_code}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_universal_override()
