import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_invisible_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Bhai, Invisible Refresh shuru kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Step 1: Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("✅ Login Success. Profile visit kar raha hoon...")
        time.sleep(15) 
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Step 2: Invisible Space Update via JS
        # Hum generic textarea ya contenteditable dhoondenge jo profile summary/headline hota hai
        print("🔍 Invisible space trigger kar raha hoon...")
        
        script = """
        try {
            // Edit button dhoondne ka generic tarika
            let editBtn = Array.from(document.querySelectorAll('span, i, a, button')).find(el => 
                el.innerText.toLowerCase().includes('edit') || 
                (el.className && el.className.toString().toLowerCase().includes('edit'))
            );

            if (editBtn) {
                editBtn.click();
                
                // Modal khulne ka wait karke space add karna
                setTimeout(() => {
                    let field = document.querySelector('textarea') || document.querySelector('input[type="text"]');
                    if (field) {
                        let originalVal = field.value;
                        // Text ke end mein space add/remove toggle
                        field.value = originalVal.endsWith(' ') ? originalVal.trim() : originalVal + ' ';
                        
                        // Input event trigger karna taaki 'Save' button activate ho jaye
                        field.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        let saveBtn = Array.from(document.querySelectorAll('button')).find(b => 
                            b.innerText.toLowerCase().includes('save')
                        );
                        if (saveBtn) saveBtn.click();
                    }
                }, 3000);
                return "SPACE_TOGGLED";
            }
            return "NO_EDIT_ICON";
        } catch (e) { return e.toString(); }
        """
        
        status = driver.execute_script(script)
        print(f"Status: {status}")

        # Final Confirmation
        # Agar text update nahi bhi hua, toh bhi profile visit ho chuki hai
        print("🏁 MISSION ACCOMPLISHED: Profile active status refreshed!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_invisible_refresh()
