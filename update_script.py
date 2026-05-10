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
    # Real user-agent taki block na ho
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        print("Login page khul raha hai...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Username aur Password fields ka intezar
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")))
        email_field.send_keys(os.environ['NAUKRI_EMAIL'])
        
        pass_field = driver.find_element(By.XPATH, "//input[@type='password']")
        pass_field.send_keys(os.environ['NAUKRI_PASS'])
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        login_btn.click()
        print("Login button dabaya gaya...")
        
        time.sleep(7) # Login refresh hone ka time

        # Profile Page
        print("Profile page par ja raha hoon...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # Summary Edit & Save
        print("Summary update kar raha hoon...")
        # Pencil icon dhoondne ke liye generic XPATH
        edit_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'edit') or contains(@class, 'pencil')]")))
        driver.execute_script("arguments[0].click();", edit_icon) # JavaScript click zyada stable hota hai
        
        time.sleep(3)
        # 'Save' button summary ke liye
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Save' or @id='submitSummary']")))
        driver.execute_script("arguments[0].click();", save_btn)
        
        print("Mubarak ho bhai! Profile Successfully refresh ho gayi.")

    except Exception as e:
        print(f"Gadbad ho gayi: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
