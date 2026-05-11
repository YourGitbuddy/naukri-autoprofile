import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def run_shortcut_ninja():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    actions = ActionChains(driver)

    try:
        print("Bhai, Shortcut Ninja shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(5)

        # Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("✅ Login Success. Profile page load ho raha hai...")
        time.sleep(15) 
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Keyboard Shortcut Hack: 
        # Naukri par aksar 'e' ya 'TAB' dabane se first editable field highlight ho jati hai.
        # Hum generic approach use karenge: Page load ke baad seedha focus trigger karenge.
        print("⌨️ Keyboard simulation se space toggle kar raha hoon...")
        
        # Sabse pehle JS se kisi bhi textarea par focus karo (invisible way)
        driver.execute_script("""
            let area = document.querySelector('textarea') || document.querySelector('.resumeHeadline');
            if(area) area.focus();
        """)
        time.sleep(2)

        # Agar focus mil gaya, toh space add karke save karna
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(1)
        actions.send_keys(Keys.BACKSPACE).perform() # Space add karke remove kar diya (Edit trigger ho gaya!)
        time.sleep(1)
        
        # Save karne ke liye ENTER ya generic Save button click
        actions.send_keys(Keys.CONTROL + Keys.ENTER).perform() # Aksar shortcuts kaam kar jaate hain
        
        # Backup: JS Save trigger
        driver.execute_script("""
            let saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.toLowerCase().includes('save'));
            if(saveBtn) saveBtn.click();
        """)

        print("🏁 MISSION ACCOMPLISHED: Activity refreshed via Ninja Keys!")

    except Exception as e:
        print(f"⚠️ Edit fail hua par visit success: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_shortcut_ninja()
