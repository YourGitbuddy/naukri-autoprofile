import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_refresh():

    options = Options()

    # Headless Config
    options.add_argument("--headless=new")

    # Stability
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")

    # Anti Detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    # SSL / Network
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")

    # User Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    print("Launching Chrome...")

    driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(60)

    print("Chrome Started Successfully")

    wait = WebDriverWait(driver, 30)

    try:

        email = os.getenv("NAUKRI_EMAIL")
        password = os.getenv("NAUKRI_PASS")

        if not email or not password:
            raise Exception("GitHub secrets missing!")

        print("Opening login page...")

        try:

            driver.get("https://www.naukri.com/nlogin/login")

        except Exception as page_error:

            print("PAGE LOAD ERROR:", str(page_error))

            driver.save_screenshot("debug_error.png")

            raise

        time.sleep(5)

        driver.save_screenshot("opened.png")

        wait.until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        )

        print("Entering credentials...")

        driver.find_element(
            By.ID,
            "usernameField"
        ).send_keys(email)

        driver.find_element(
            By.ID,
            "passwordField"
        ).send_keys(password)

        login_btn = driver.find_element(
            By.XPATH,
            "//button[contains(text(),'Login')]"
        )

        login_btn.click()

        print("Waiting after login...")

        time.sleep(10)

        driver.save_screenshot("after_login.png")

        print("Opening profile page...")

        driver.get("https://www.naukri.com/mnjuser/profile")

        time.sleep(10)

        driver.save_screenshot("profile_page.png")

        print("Trying profile refresh...")

        js_script = """

        let editBtns = document.querySelectorAll('span.edit');

        if(editBtns.length > 0){

            editBtns[0].click();

            setTimeout(() => {

                let textarea = document.querySelector('textarea');

                if(textarea){

                    textarea.value =
                        textarea.value + " ";

                    textarea.dispatchEvent(
                        new Event(
                            'input',
                            { bubbles: true }
                        )
                    );

                    let saveBtn =
                        document.querySelector(
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

        result = driver.execute_script(js_script)

        print("RESULT:", result)

        # Fallback Resume Upload
        if result != "SUCCESS":

            print("Trying Resume Upload Fallback...")

            try:

                resume_path = os.path.join(
                    os.getcwd(),
                    "Resume.pdf"
                )

                upload_input = driver.find_element(
                    By.XPATH,
                    "//input[@type='file']"
                )

                upload_input.send_keys(resume_path)

                print("Resume Uploaded Successfully!")

            except Exception as upload_error:

                print(
                    "Resume Upload Failed:",
                    str(upload_error)
                )

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
