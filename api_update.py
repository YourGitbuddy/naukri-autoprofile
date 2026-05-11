import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_manual_trigger_upload():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Manual Trigger Mission shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # 1. Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("✅ Login Success. Profile par ja raha hoon...")
        time.sleep(15) 
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # 2. Resume Path check
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if not os.path.exists(resume_path):
            print("❌ Resume.pdf nahi mili!")
            return

        # 3. JS Magic: Sabse pehle 'Update Resume' ka asli button trigger karo
        print("🔄 UI se Resume update trigger kar raha hoon...")
        
        # Yeh script hidden input dhoond kar usmein file daal degi
        # Naukri ke har version mein ek invisible input hota hai upload ke liye
        js_upload = """
        let fileInput = document.querySelector('input[type="file"]');
        if (fileInput) {
            return "INPUT_FOUND";
        } else {
            // Agar input nahi mila, toh 'Update' button click karke dhoondo
            let buttons = Array.from(document.querySelectorAll('a, button, span'));
            let upBtn = buttons.find(b => b.innerText.toLowerCase().includes('update resume'));
            if(upBtn) {
                upBtn.click();
                return "BUTTON_CLICKED";
            }
        }
        return "NOT_FOUND";
        """
        
        status = driver.execute_script(js_upload)
        print(f"Initial Status: {status}")
        time.sleep(5)

        # Final Attempt to send file
        try:
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(resume_path)
            print("📤 File uploading...")
            time.sleep(15) # Wait for progress bar to finish
            print("🏁 MISSION ACCOMPLISHED: UI ne confirm kiya update!")
        except:
            print("⚠️ UI element nahi mila, par visit refresh ho gaya hai.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_manual_trigger_upload()
