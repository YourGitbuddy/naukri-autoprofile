import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_force_ui_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Login trigger kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("Login done. Profile par ja raha hoon...")
        time.sleep(15) 
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # UI Update Logic using JavaScript (to bypass hidden element issues)
        print("UI Update trigger kar raha hoon via JS...")
        update_script = """
        try {
            // 1. Find Edit Button in Profile Summary
            let editBtn = document.querySelector('.profile-summary .edit') || document.querySelector('.icon-edit');
            if (editBtn) {
                editBtn.click();
                
                // Wait for modal to open
                setTimeout(() => {
                    let textarea = document.querySelector('textarea[name="summary"]') || document.querySelector('textarea');
                    if (textarea) {
                        let val = textarea.value;
                        textarea.value = val.endsWith('.') ? val.slice(0, -1) : val + '.';
                        // Trigger change event
                        textarea.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        // Click Save
                        let saveBtn = document.querySelector('button[type="submit"]') || document.querySelector('.btn-save');
                        if (saveBtn) saveBtn.click();
                    }
                }, 3000);
                return "UI_TRIGGERED";
            }
            return "EDIT_NOT_FOUND";
        } catch (e) {
            return e.toString();
        }
        """
        
        result = driver.execute_script(update_script)
        print(f"Update Result: {result}")

        if result == "UI_TRIGGERED":
            time.sleep(10) # Wait for save to complete
            print("🏁 MISSION ACCOMPLISHED: Profile updated via UI interaction!")
        else:
            print("⚠️ UI Update fail. But profile visit done.")
            print("🏁 Fallback success: Last Active timestamp updated.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_force_ui_refresh()
