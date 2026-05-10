import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_naukri_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 30)

    try:
        # 1. Login
        print("Login page khul raha hai...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("Login ho gaya, profile par ja raha hoon...")
        time.sleep(10)

        # 2. Profile Page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(7)

        # 3. Smart Scrolling (Important)
        # Summary niche hoti hai, isliye scroll karna zaroori hai
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)

        # 4. Trying Multiple XPATHs for Summary Edit Icon
        print("Summary edit icon dhoond raha hoon...")
        
        # Alag-alag tarike icon dhoondne ke
        edit_paths = [
            "//span[contains(text(), 'Profile Summary')]/following-sibling::span[contains(@class, 'edit')]",
            "//span[contains(text(), 'Profile Summary')]/parent::div//span[contains(@class, 'edit')]",
            "//div[contains(@class, 'summary')]//span[contains(@class, 'edit')]",
            "//*[@id='lazyProfileSummary']//span[contains(@class, 'edit')]"
        ]

        edit_btn = None
        for path in edit_paths:
            try:
                edit_btn = driver.find_element(By.XPATH, path)
                if edit_btn.is_displayed():
                    print(f"Icon mil gaya: {path}")
                    break
            except:
                continue

        if edit_btn:
            driver.execute_script("arguments[0].click();", edit_btn)
            time.sleep(3)
            
            # 5. Save Button
            print("Save button daba raha hoon...")
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='submitSummary' or text()='Save']")))
            driver.execute_script("arguments[0].click();", save_btn)
            
            time.sleep(3)
            print("Mubarak ho bhai! Profile Successfully update ho gayi.")
        else:
            print("Maafi bhai, Summary icon nahi mila. Screenshot save kar raha hoon.")
            driver.save_screenshot("debug_profile.png")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
