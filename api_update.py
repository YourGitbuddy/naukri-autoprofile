import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_refresh():

    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")

    print("Launching Chrome...")

    driver = webdriver.Chrome(options=options)

    print("Chrome Started Successfully")

    wait = WebDriverWait(driver, 30)

    try:

        email = os.getenv("NAUKRI_EMAIL")
        password = os.getenv("NAUKRI_PASS")

        if not email or not password:
            raise Exception("GitHub secrets missing!")

        print("Opening login page...")

        driver.get("https://www.naukri.com/nlogin/login")

        time.sleep(5)

        driver.save_screenshot("opened.png")

        wait.until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        )

        print("Entering credentials...")

        driver.find_element(By.ID, "usernameField").send_keys(email)

        driver.find_element(By.ID, "passwordField").send_keys(password)

        login_btn = driver.find_element(
            By.XPATH,
            "//button[contains(text(),'Login')]"
        )

        login_btn.click()

        print("Waiting after login...")

        time.sleep(10)

        print("Opening profile page...")

        driver.get("https://www.naukri.com/mnjuser/profile")

        time.sleep(10)

        print("Refreshing profile...")

        js = """

        let btns = document.querySelectorAll('span.edit');

        if(btns.length > 0){

            btns[0].click();

            setTimeout(() => {

                let textarea = document.querySelector('textarea');

                if(textarea){

                    textarea.value += " ";

                    textarea.dispatchEvent(
                        new Event('input', { bubbles: true })
                    );

                    let saveBtn = document.querySelector(
                        'button[type="submit"]'
                    );

                    if(saveBtn){
                        saveBtn.click();
                    }

                }

            }, 3000);

            return "SUCCESS";
        }

        return "FAILED";
        """

        result = driver.execute_script(js)

        print("RESULT:", result)

        time.sleep(8)

        driver.save_screenshot("success.png")

        print("Profile refresh completed.")

    except Exception as e:

        print("ERROR:", str(e))

        driver.save_screenshot("debug_error.png")

    finally:

        driver.quit()


if __name__ == "__main__":
    run_refresh()
