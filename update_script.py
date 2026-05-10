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
        # 1. Login Process
        print("Login page khul raha hai...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("Login successful! Profile page par ja raha hoon...")
        time.sleep(15) 

        # 2. Go directly to Edit Profile
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # 3. Scroll Down to force load elements
        driver.execute_script("window.scrollTo(0, 1000);")
        print("Page scroll kar diya hai...")
        time.sleep(5)

        # 4. Target the 'Profile Summary' Edit button by text and class
        # Naukri ke naye UI mein ye 'edit' class ke sath hota hai
        print("Summary edit icon dhoond raha hoon...")
        
        try:
            # Method 1: Find by XPATH contains text
            edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Profile Summary')]/following-sibling::span[contains(@class, 'edit')] | //*[contains(text(), 'Profile Summary')]//following::span[1]")))
            driver.execute_script("arguments[0].click();", edit_btn)
            print("Edit button mil gaya aur click kar diya!")
        except:
            # Method 2: JavaScript fallback (Find all edit icons and click the second one, usually summary)
            print("XPATH fail hua, JS fallback try kar raha hoon...")
            driver.execute_script("document.querySelectorAll('.edit.icon')[1].click();") # Index 1 is usually Summary
        
        time.sleep(3)

        # 5. Save the summary
        print("Save button ki talash...")
        save_btn = wait.until(EC.element_to_be_clickable((By.ID, "submitSummary")))
        driver.execute_script("arguments[0].click();", save_btn)
        
        print("Kaam ho gaya! Profile successfully update ho gayi.")

    except Exception as e:
        print(f"Abhi bhi issue hai: {str(e)}")
        # Debugging ke liye source print kar dete hain agar fail ho toh
        print("Current Page Title:", driver.title)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
    
