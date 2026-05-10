import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_campus_refresh_final():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Login shuru kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Login Injection
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("Login done. Waiting for profile load...")
        time.sleep(12)
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # JavaScript execution for Profile Summary Refresh
        # Yeh script tere 'Profile Summary' section ko target karegi
        refresh_logic = """
        let editBtn = document.querySelector('.profile-summary .edit') || document.querySelector('span.edit.icon') || document.querySelector('.icon-edit');
        if (editBtn) {
            editBtn.click();
            setTimeout(() => {
                let textarea = document.querySelector('textarea[name="summary"]') || document.querySelector('textarea');
                if (textarea) {
                    let val = textarea.value;
                    textarea.value = val.endsWith('.') ? val.slice(0, -1) : val + '.';
                    document.querySelector('button[type="submit"]').click();
                }
            }, 3000);
            return "SUCCESS";
        }
        return "NOT_FOUND";
        """
        
        result = driver.execute_script(refresh_logic)
        if result == "SUCCESS":
            print("🏁 MISSION ACCOMPLISHED: Profile fresh ho gayi!")
            time.sleep(5)
        else:
            print("❌ Summary edit button nahi mila. Fallback to Resume upload...")
            # Fallback to resume upload if summary fails
            try:
                resume_path = os.path.join(os.getcwd(), "Resume.pdf")
                attach = driver.find_element(By.XPATH, "//input[@type='file']")
                attach.send_keys(resume_path)
                print("🏁 MISSION ACCOMPLISHED: Resume re-uploaded as fallback!")
                time.sleep(5)
            except:
                print("❌ Dono methods fail ho gaye.")
                driver.save_screenshot("debug_error.png")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_campus_refresh_final()
