import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_bazooka_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    resume_path = os.path.join(os.getcwd(), "Resume.pdf")

    try:
        print("🚀 Bazooka Mission: Forced UI Injection Shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        driver.find_element(By.ID, "usernameField").send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(10)

        # 2. Go to Profile
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(7)

        # 3. Forced JavaScript Injection (The Bazooka)
        # Ye direct browser ke backend se file input ko dhund ke file attach karega
        print("💉 Injecting File via JavaScript...")
        script = """
        var input = document.querySelector("input[type='file']");
        if (input) {
            console.log('Input found, triggering upload...');
            return true;
        } else {
            // Agar Campus UI hai toh shadow root dhoondo
            var shadowHost = document.querySelector('naukri-resume-upload'); 
            if(shadowHost) return 'shadow_found';
            return false;
        }
        """
        result = driver.execute_script(script)
        
        # UI upload trigger
        file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        for f_in in file_inputs:
            try:
                f_in.send_keys(resume_path)
                print("✅ JavaScript Force Upload: Done!")
            except:
                continue

        # 4. Backend API Fallback (Double Confirmation)
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.naukri.com/mnjuser/profile",
            "User-Agent": "Mozilla/5.0"
        }

        with open(resume_path, 'rb') as f:
            files = {'resume': ('Resume.pdf', f, 'application/pdf')}
            response = session.post("https://www.naukri.com/mnjuser/profile/uploadResume", 
                                    files=files, data={'isResumeUpload': '1'}, headers=headers)

        if response.status_code == 200:
            print("🏁 FINAL STATUS: Server Accept (200). UI Refresh Triggered.")
        
        # 5. Headline Update (To confirm activity)
        h_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        h_headers = {"Clientid": "d36980564696075936856", "Appid": "121", "Systemid": "121", "Content-Type": "application/json"}
        res = session.get(h_url, headers=h_headers).json()
        new_h = res['resumeHeadline'][:-1] if res['resumeHeadline'].endswith('.') else res['resumeHeadline'] + "."
        session.put(h_url, json={"resumeHeadline": new_h}, headers=h_headers)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bazooka_update()
