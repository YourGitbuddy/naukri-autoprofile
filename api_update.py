import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_stealth_refresh():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Stealth Settings
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Bypass Webdriver Detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    wait = WebDriverWait(driver, 40)

    try:
        print("Bhai, Login page load kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Login
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(os.environ['NAUKRI_EMAIL'])
        driver.find_element(By.ID, "passwordField").send_keys(os.environ['NAUKRI_PASS'])
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Login']"))
        
        print("Login done, profile par ja raha hoon...")
        time.sleep(10)
        
        # Go to Profile
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # Update Resume Headline (This is the most stable element)
        print("Refreshing via Resume Headline...")
        
        # 1. Edit button click (Headline section)
        edit_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Resume headline']/following-sibling::span[contains(@class,'edit')]")))
        driver.execute_script("arguments[0].click();", edit_icon)
        
        # 2. Headline text box
        headline_box = wait.until(EC.presence_of_element_located((By.ID, "resumeHeadlineTxt")))
        current_headline = headline_box.get_attribute("value")
        
        # 3. Toggle Dot (.)
        if current_headline.endswith('.'):
            new_headline = current_headline[:-1]
        else:
            new_headline = current_headline + '.'
            
        headline_box.clear()
        headline_box.send_keys(new_headline)
        
        # 4. Save
        save_btn = driver.find_element(By.XPATH, "//button[text()='Save']")
        driver.execute_script("arguments[0].click();", save_btn)
        
        print(f"🏁 MISSION ACCOMPLISHED: Headline updated to trigger freshness!")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        driver.save_screenshot("debug_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_stealth_refresh()
