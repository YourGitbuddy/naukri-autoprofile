import os
import time
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_refresh():

    options = Options()

    # REQUIRED FOR GITHUB ACTIONS
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

    wait = WebDriverWait(driver, 30)

    print("Chrome Started Successfully")

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
            EC.presence_of_element_located(
                (By.ID, "usernameField")
            )
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

        driver.find_element(
            By.XPATH,
            "//button[contains(text(),'Login')]"
        ).click()

        print("Waiting after login...")

        time.sleep(15)

        driver.save_screenshot("after_login.png")

        print("Opening profile page...")

        driver.get(
            "https://www.naukri.com/mnjuser/profile"
        )

        time.sleep(10)

        print("Current URL:", driver.current_url)

        print("Page Title:", driver.title)

        with open(
            "page_source.html",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(driver.page_source)

        driver.save_screenshot("profile_page.png")

        print("Trying profile refresh...")

        js_script = """

        function tryEdit(){

            let allButtons =
                document.querySelectorAll('*');

            for(let btn of allButtons){

                let text =
                    btn.innerText || "";

                let cls =
                    btn.className || "";

                if(
                    text.toLowerCase().includes('edit') ||
                    cls.toLowerCase().includes('edit')
                ){

                    try{
                        btn.click();
                        return true;
                    }catch(e){}
                }
            }

            return false;
        }

        let clicked = tryEdit();

        if(clicked){

            setTimeout(() => {

                let textarea =
                    document.querySelector('textarea');

                if(textarea){

                    textarea.value =
                        textarea.value + " ";

                    textarea.dispatchEvent(
                        new Event(
                            'input',
                            { bubbles: true }
                        )
                    );

                    let buttons =
                        document.querySelectorAll('button');

                    for(let btn of buttons){

                        let txt =
                            btn.innerText || "";

                        if(
                            txt.toLowerCase()
                            .includes('save')
                        ){

                            btn.click();
                            break;
                        }
                    }
                }

            }, 3000);

            return "SUCCESS";
        }

        return "FAILED";
        """

        result = driver.execute_script(js_script)

        print("RESULT:", result)

        time.sleep(10)

        driver.save_screenshot("success.png")

        print("Profile refresh completed.")

    except Exception as e:

        print("ERROR:", str(e))

        driver.save_screenshot("debug_error.png")

    finally:

        driver.quit()


if __name__ == "__main__":
    run_refresh()
