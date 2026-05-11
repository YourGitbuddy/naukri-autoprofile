import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_force_resume_uploader():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Force Resume Upload mission shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("✅ Login Success. Profile par ja raha hoon...")
        time.sleep(15) 
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        
        if os.path.exists(resume_path):
            print(f"📄 Resume mil gaya. Hidden input trigger kar raha hoon...")
            
            # Naukri ke naye UI mein kai baar input hidden hota hai. 
            # Hum JS se use dhoond kar visible karenge aur phir upload karenge.
            upload_js = """
            var input = document.querySelector('input[type="file"]');
            if(!input) {
                // Agar hidden hai toh button ke aas paas dhoondo
                let btns = document.querySelectorAll('button, a, span');
                for(let b of btns) {
                    if(b.innerText.toLowerCase().includes('upload') || b.innerText.toLowerCase().includes('update')) {
                        b.click(); // Click to trigger modal
                    }
                }
            }
            return document.querySelector('input[type="file"]') ? true : false;
            """
            
            ready = driver.execute_script(upload_js)
            time.sleep(5)
            
            try:
                # Try multiple selectors for the file input
                selectors = ["input[type='file']", "#attachCV", "input[name='resume']"]
                file_input = None
                
                for selector in selectors:
                    try:
                        file_input = driver.find_element(By.CSS_SELECTOR, selector)
                        if file_input: break
                    except: continue

                if file_input:
                    file_input.send_keys(resume_path)
                    print("⏳ Upload process initiated...")
                    time.sleep(15) # Wait for upload to complete
                    print("🏁 MISSION ACCOMPLISHED: Resume updated!")
                else:
                    print("⚠️ Element nahi mila, par profile visit success. Active status updated.")
            except Exception as inner_e:
                print(f"⚠️ Upload interaction fail: {str(inner_e)}")
        else:
            print("❌ Error: Resume.pdf missing in repo!")

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_force_resume_uploader()
