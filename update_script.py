import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_naukri_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Bina window ke chalega
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. Login Page
        print("Login kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(5) # Login hone ka intezar

        # 2. Profile Page par jana
        print("Profile page par ja raha hoon...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # 3. Summary Edit aur Save karna
        # Hum summary dhoond kar sirf 'Save' dabayenge taki 'Last Updated' refresh ho jaye
        print("Summary update kar raha hoon...")
        edit_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Profile Summary')]/following-sibling::span")))
        edit_icon.click()
        
        time.sleep(2)
        save_btn = wait.until(EC.element_to_be_clickable((By.ID, "submitSummary")))
        save_btn.click()
        
        print("Mubarak ho bhai! Profile successfully update ho gayi.")

    except Exception as e:
        print(f"Gadbad ho gayi: {str(e)}")
        driver.save_screenshot("error.png") # Debugging ke liye
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
