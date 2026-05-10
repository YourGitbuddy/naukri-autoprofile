import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


def run_refresh():

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    wait = WebDriverWait(driver, 20)

    try:

        email = os.getenv("NAUKRI_EMAIL")
        password = os.getenv("NAUKRI_PASS")

        if not email or not password:
            raise Exception("Secrets missing!")

        print("Opening login page...")

        driver.get("https://www.naukri.com/nlogin/login")

        wait.until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        )

        driver.find_element(By.ID, "usernameField").send_keys(email)
        driver.find_element(By.ID, "passwordField").send_keys(password)

        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        print("Waiting for login success...")

        wait.until(
            EC.url_contains("naukri.com")
        )

        time.sleep(5)

        driver.get("https://www.naukri.com/mnjuser/profile")

        time.sleep(8)

        print("Trying profile refresh...")

        js_script = """
        let editBtns = document.querySelectorAll('span.edit');

        if(editBtns.length > 0){
            editBtns[0].click();

            setTimeout(() => {

                let textarea = document.querySelector('textarea');

                if(textarea){

                    let val = textarea.value;

                    textarea.value = val + " ";

                    textarea.dispatchEvent(new Event('input', { bubbles: true }));

                    let saveBtn = document.querySelector('button[type="submit"]');

                    if(saveBtn){
                        saveBtn.click();
                    }

                }

            }, 3000);

            return "SUCCESS";
        }

        return "FAILED";
        """

        result = driver.execute_script(js_script)

        print("Result:", result)

        time.sleep(10)

        driver.save_screenshot("success.png")

    except Exception as e:
        print("ERROR:", str(e))
        driver.save_screenshot("debug_error.png")

    finally:
        driver.quit()


if __name__ == "__main__":
    run_refresh()
