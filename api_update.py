import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def run_easiest_refresh():
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

        # Simple JS Login
        driver.execute_script(f"document.getElementById('usernameField').value='{os.environ['NAUKRI_EMAIL']}';")
        driver.execute_script(f"document.getElementById('passwordField').value='{os.environ['NAUKRI_PASS']}';")
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("Login Success! Resume re-upload kar raha hoon...")
        time.sleep(10)

        # Seedha Profile page par jahan resume upload ka option hota hai
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Sabse important step: Resume file path dhoondna aur upload karna
        # Naukri par 'attachCV' id wali input field hamesha hidden hoti hai par kaam karti hai
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        
        if os.path.exists(resume_path):
            attach_field = driver.find_element(By.ID, "attachCV")
            attach_field.send_keys(resume_path)
            print("🏁 MISSION ACCOMPLISHED: Resume re-uploaded! Profile is now fresh.")
            time.sleep(10) # Upload complete hone ka wait
        else:
            print("❌ Error: 'Resume.pdf' file nahi mili repo mein!")

    except Exception as e:
        print(f"❌ Kuch gadbad hui: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_easiest_refresh()
