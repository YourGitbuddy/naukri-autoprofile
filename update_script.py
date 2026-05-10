import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_naukri_update():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Background mein chalega
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Real user-agent taki Akamai block na kare
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)

    try:
        # 1. Login
        print("Login page khul raha hai...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Email aur Pass fields ka intezar
        user_input = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        user_input.send_keys(os.environ['NAUKRI_EMAIL'])
        
        pass_input = driver.find_element(By.ID, "passwordField")
        pass_input.send_keys(os.environ['NAUKRI_PASS'])
        
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Login successful, profile par ja raha hoon...")
        time.sleep(10) # Profile load hone ka time

        # 2. Profile Page par jana
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # 3. Summary Refresh
        # Hum summary dhoond kar 'Save' dabayenge
        print("Summary section dhoond raha hoon...")
        # Pencil icon click karna
        edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'edit') or contains(@class, 'pencil')]")))
        driver.execute_script("arguments[0].click();", edit_btn)
        
        time.sleep(3)
        # Save button dabana
        save_btn = wait.until(EC.element_to_be_clickable((By.ID, "submitSummary")))
        driver.execute_script("arguments[0].click();", save_btn)
        
        print("Mubarak ho bhai! Profile successfully update ho gayi.")

    except Exception as e:
        print(f"Gadbad ho gayi: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
