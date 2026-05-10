import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_refresh():

    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # IMPORTANT
    chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(options=chrome_options)

    wait = WebDriverWait(driver, 30)

    try:

        email = os.getenv("NAUKRI_EMAIL")
        password = os.getenv("NAUKRI_PASS")

        print("Opening login page...")

        driver.get("https://www.naukri.com/nlogin/login")

        wait.until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        )

        driver.find_element(By.ID, "usernameField").send_keys(email)

        driver.find_element(By.ID, "passwordField").send_keys(password)

        driver.find_element(
            By.XPATH,
            "//button[contains(text(),'Login')]"
        ).click()

        print("Waiting after login...")

        time.sleep(10)

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

        print(result)

        driver.save_screenshot("success.png")

        time.sleep(5)

    except Exception as e:

        print("ERROR:", e)

        driver.save_screenshot("debug_error.png")

    finally:

        driver.quit()


if __name__ == "__main__":
    run_refresh()
