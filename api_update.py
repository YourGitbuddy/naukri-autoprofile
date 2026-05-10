import os
import time
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

def run_refresh():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-web-security")
    options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    print("Launching Chrome...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)
    wait = WebDriverWait(driver, 30)

    try:
        email = os.getenv("NAUKRI_EMAIL")
        password = os.getenv("NAUKRI_PASS")

        if not email or not password:
            raise Exception("GitHub secrets missing!")

        # Always start from login page and perform login
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(2)

        # Fill credentials and click login
        try:
            wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
            driver.find_element(By.ID, "usernameField").clear()
            driver.find_element(By.ID, "usernameField").send_keys(email)
            driver.find_element(By.ID, "passwordField").clear()
            driver.find_element(By.ID, "passwordField").send_keys(password)
            # click login button (try multiple possible texts)
            login_btn = None
            try:
                login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login') or contains(., 'Sign in') or contains(., 'Log in')]")))
            except:
                # fallback: first button on form
                buttons = driver.find_elements(By.TAG_NAME, "button")
                if buttons:
                    login_btn = buttons[0]
            if login_btn:
                login_btn.click()
            else:
                raise Exception("Login button not found")
        except Exception as e:
            print("Error during filling login form:", str(e))
            driver.save_screenshot("login_fill_error.png")
            with open("login_fill_error.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            raise

        # Save immediate debug artifacts after clicking login
        time.sleep(5)
        driver.save_screenshot("after_login.png")
        with open("after_login.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Robust login detection: wait for profile URL or profile-specific element
        logged_in = False
        try:
            wait_long = WebDriverWait(driver, 30)
            wait_long.until(EC.url_contains("/mnjuser/profile"))
            logged_in = True
        except:
            try:
                # look for profile-specific selectors (adjust if site uses different classes)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mnjuserName, .userName, a.logout, .profile-container")))
                logged_in = True
            except:
                logged_in = False

        if not logged_in:
            print("Login failed, still on login page or unexpected page.")
            # Save extra debug info
            driver.save_screenshot("login_failed.png")
            with open("login_failed.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            # Stop further actions since we are not authenticated
            return
        else:
            print("Login successful, proceeding to profile refresh.")

        # Navigate to profile page to be safe
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        driver.save_screenshot("profile_page.png")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Only run the edit/save JS if we are on the profile page
        if "/mnjuser/profile" not in driver.current_url:
            print("Not on profile page; skipping JS refresh.")
            return

        print("Trying profile refresh...")

        js_script = """
        function tryEdit(){
            let profileContainer = document.querySelector('.profile-container') || document.body;
            let allButtons = profileContainer.querySelectorAll('button, a');
            for(let btn of allButtons){
                let text = (btn.innerText || '').toLowerCase();
                let cls = (btn.className || '').toLowerCase();
                if(text.includes('edit') || cls.includes('edit') || text.includes('update')){
                    try{ btn.click(); return true; }catch(e){}
                }
            }
            return false;
        }

        let clicked = tryEdit();

        if(clicked){
            setTimeout(() => {
                let textarea = document.querySelector('textarea');
                if(textarea){
                    textarea.value = textarea.value + " ";
                    textarea.dispatchEvent(new Event('input', { bubbles: true }));
                    let buttons = document.querySelectorAll('button');
                    for(let btn of buttons){
                        let txt = (btn.innerText || '').toLowerCase();
                        if(txt.includes('save') || txt.includes('update')){
                            try{ btn.click(); }catch(e){}
                            break;
                        }
                    }
                }
            }, 2000);
            return "SUCCESS";
        }
        return "FAILED";
        """

        result = driver.execute_script(js_script)
        print("RESULT:", result)

        time.sleep(8)
        driver.save_screenshot("success.png")
        print("Profile refresh completed.")

    except Exception as e:
        print("ERROR:", str(e))
        try:
            driver.save_screenshot("debug_error.png")
        except:
            pass
    finally:
        driver.quit()

if __name__ == "__main__":
    run_refresh()
