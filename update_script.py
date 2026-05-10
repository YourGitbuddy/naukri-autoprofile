import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def update_naukri_profile():
    # 1. Browser Setup
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Headless mode for GitHub Actions
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Anti-Bot Detection: Ye flags Naukri ko batate hain ki ye automation nahi hai
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Navigator detection bypass
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    wait = WebDriverWait(driver, 40)

    try:
        # Step 2: Login Page par jana
        print("Bhai, Login page load kar raha hoon...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        # Email & Password dalkar login karna
        email_field = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        email_field.send_keys(os.environ['NAUKRI_EMAIL'])
        
        pass_field = driver.find_element(By.ID, "passwordField")
        pass_field.send_keys(os.environ['NAUKRI_PASS'])
        
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        driver.execute_script("arguments[0].click();", login_btn)
        
        print("Login button clicked. Waiting for dashboard...")
        time.sleep(10) # Wait for page transition

        # Step 3: Seedha Profile Page par jump
        print("Navigating to Profile page...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # Step 4: Resume Upload Logic
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print(f"Uploading file: {resume_path}")
            
            # Naukri ka hidden file input locator
            # Hum wait karenge ki input load ho jaye
            attach_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            
            # File send karna
            attach_input.send_keys(resume_path)
            
            print("File bhej di hai. Processing ke liye wait kar raha hoon...")
            time.sleep(20) # 20 seconds wait taaki upload sync ho jaye
            
            print("🏁 Success: Resume upload ho gaya aur profile refresh ho gayi!")
            driver.save_screenshot("final_success.png")
        else:
            print("❌ Error: 'Resume.pdf' file repo mein nahi mili!")

    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        driver.save_screenshot("debug_error.png")
        # Page source save kar rahe hain taaki hum error dhoond sakein
        with open("error_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    
    finally:
        driver.quit()

if __name__ == "__main__":
    update_naukri_profile()
