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
    wait = WebDriverWait(driver, 40)

    try:
        # 1. Login
        print("Naukri login shuru...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("Login done. Profile page par ja raha hoon...")
        time.sleep(10)

        # 2. Profile Page
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # 3. Resume Headline Edit (Ye page ke top par hota hai)
        print("Resume Headline edit karne ki koshish...")
        
        # 'Resume Headline' ke pass wale 'edit' icon ko dhoondna
        # Iska XPATH zyada stable hai kyunki ye page ke shuruat mein hota hai
        try:
            edit_headline = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Resume headline']/following-sibling::span[contains(@class, 'edit')]")))
            driver.execute_script("arguments[0].click();", edit_headline)
            print("Headline edit box khul gaya.")
            time.sleep(3)

            # Save button dabana
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Save' and @type='submit']")))
            driver.execute_script("arguments[0].click();", save_btn)
            print("Success! Profile status refresh ho gaya.")
        
        except Exception as e:
            print("Headline button nahi mila, last attempt with generic class...")
            # Agar upar wala fail ho toh page ke pehle 'edit' icon ko click karo
            driver.execute_script("document.querySelector('.icon.edit').click();")
            time.sleep(2)
            driver.execute_script("document.querySelector('button[type=\"submit\"]').click();")
            print("Generic click performed.")

    except Exception as e:
        print(f"Error: {str(e)}")
        # Debugging ke liye page ka HTML save kar raha hoon (log mein dikhega)
        print("Page Content Snippet:", driver.page_source[:500])
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
