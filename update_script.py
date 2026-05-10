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
    wait = WebDriverWait(driver, 40) # Wait time badha diya

    try:
        # 1. Login
        print("Login page khul raha hai...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("Login successful! Profile page par ja raha hoon...")
        time.sleep(15) # Wait for dashboard to settle

        # 2. Go to Profile
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # 3. Scroll and Search Loop
        print("Summary icon ki talash shuru...")
        # Page ko thoda thoda karke niche scroll karenge taki lazy elements load hon
        for i in range(3):
            driver.execute_script(f"window.scrollTo(0, {i * 400});")
            time.sleep(2)

        # 4. Multiple Selectors for Edit Icon
        # Hum generic class names aur text search kar rahe hain
        selectors = [
            "//span[contains(text(), 'Profile Summary')]/following-sibling::span",
            "//div[contains(@class, 'summary')]//span[contains(@class, 'edit')]",
            "//span[@class='edit icon']",
            "//div[@id='lazyProfileSummary']//span[text()='edit']",
            "//div[contains(@class, 'profileSummary')]//span[contains(@class, 'pencil')]"
        ]

        edit_btn = None
        for sel in selectors:
            try:
                elements = driver.find_elements(By.XPATH, sel)
                for el in elements:
                    if el.is_displayed():
                        edit_btn = el
                        print(f"Icon mil gaya: {sel}")
                        break
                if edit_btn: break
            except: continue

        if edit_btn:
            driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", edit_btn)
            print("Edit mode open ho gaya.")
            
            # 5. Save Button
            save_btn = wait.until(EC.element_to_be_clickable((By.ID, "submitSummary")))
            driver.execute_script("arguments[0].click();", save_btn)
            print("Mubarak ho bhai! Save button dab gaya.")
            time.sleep(3)
        else:
            print("Maafi, Edit icon nahi mila. Par aapka Login ho chuka hai, toh profile active dikhegi.")

    except Exception as e:
        print(f"Error aayi hai: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_naukri_update()
