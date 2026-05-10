import os
import sys
import time
import re
import imaplib
import email
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# --- IMAP OTP fetcher (unchanged logic, returns 4-6 digit OTP or None) ---
def fetch_latest_otp(imap_host, user, password, timeout=90):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            m = imaplib.IMAP4_SSL(imap_host)
            m.login(user, password)
            m.select("INBOX")
            typ, data = m.search(None, '(UNSEEN)')
            ids = data[0].split()
            if not ids:
                typ, data = m.search(None, 'ALL')
                ids = data[0].split()
            for msgid in reversed(ids):
                typ, msg_data = m.fetch(msgid, '(RFC822)')
                if not msg_data or not msg_data[0]:
                    continue
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        disp = str(part.get("Content-Disposition"))
                        if ctype == "text/plain" and "attachment" not in disp:
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode(errors='ignore')
                                break
                else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                        body = payload.decode(errors='ignore')
                if not body:
                    body = msg.get("Subject", "") or ""
                m_otp = re.search(r'\b(\d{4,6})\b', body)
                if m_otp:
                    otp = m_otp.group(1)
                    try:
                        m.logout()
                    except:
                        pass
                    return otp
            try:
                m.logout()
            except:
                pass
        except Exception as e:
            print("IMAP read error:", e)
        time.sleep(3)
    return None

# --- helper to dump page info for debugging ---
def dump_page_debug(driver, prefix):
    try:
        url = driver.current_url
    except:
        url = "UNAVAILABLE"
    try:
        title = driver.title
    except:
        title = "UNAVAILABLE"
    try:
        body_text = driver.execute_script("return document.documentElement.innerText.slice(0, 20000);")
    except:
        body_text = ""
    try:
        html = driver.page_source
    except:
        html = ""
    # write files
    try:
        with open(f"{prefix}_url.txt", "w", encoding="utf-8") as f:
            f.write(url + "\n")
            f.write(title + "\n")
    except:
        pass
    try:
        with open(f"{prefix}_body.txt", "w", encoding="utf-8") as f:
            f.write(body_text)
    except:
        pass
    try:
        with open(f"{prefix}_page.html", "w", encoding="utf-8") as f:
            f.write(html)
    except:
        pass
    # screenshot
    try:
        driver.save_screenshot(f"{prefix}.png")
    except:
        pass
    print(f"[DEBUG] dumped page debug with prefix: {prefix}")

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
    wait = WebDriverWait(driver, 60)  # increased wait

    try:
        naukri_email = os.getenv("NAUKRI_EMAIL")
        naukri_pass = os.getenv("NAUKRI_PASS")
        imap_user = os.getenv("EMAIL_USER")
        imap_pass = os.getenv("EMAIL_PASS")
        imap_host = os.getenv("IMAP_HOST", "imap.gmail.com")

        if not naukri_email or not naukri_pass:
            raise Exception("NAUKRI_EMAIL or NAUKRI_PASS missing in environment")

        # Start at login page and perform login every run
        driver.get("https://www.naukri.com/nlogin/login")
        time.sleep(2)
        dump_page_debug(driver, "opened")  # dump initial login page

        # Fill credentials and click login
        try:
            wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
            u_field = driver.find_element(By.ID, "usernameField")
            p_field = driver.find_element(By.ID, "passwordField")
            u_field.clear()
            u_field.send_keys(naukri_email)
            p_field.clear()
            p_field.send_keys(naukri_pass)

            login_btn = None
            try:
                login_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'log in')]")
                ))
            except:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                if buttons:
                    login_btn = buttons[0]
            if login_btn:
                login_btn.click()
            else:
                raise Exception("Login button not found")
        except Exception as e:
            print("Error during filling login form:", str(e))
            dump_page_debug(driver, "login_fill_error")
            raise

        # Save immediate debug artifacts after clicking login
        time.sleep(6)
        dump_page_debug(driver, "after_login")

        # Detect OTP prompt or direct login success
        logged_in = False
        try:
            # If profile URL appears quickly, consider logged in
            wait.until(EC.url_contains("/mnjuser/profile"))
            logged_in = True
        except:
            # Not redirected yet; dump page and look for OTP
            dump_page_debug(driver, "after_login_check")
            otp_selectors = [
                "input[placeholder*='OTP']",
                "input[placeholder*='Enter OTP']",
                "input[type='tel']",
                "input[name*='otp']",
                "input[id*='otp']"
            ]
            otp_found = None
            for sel in otp_selectors:
                try:
                    elems = driver.find_elements(By.CSS_SELECTOR, sel)
                    if elems:
                        otp_found = sel
                        break
                except:
                    continue

            if otp_found and imap_user and imap_pass:
                print("OTP prompt detected, fetching OTP from email...")
                otp = fetch_latest_otp(imap_host, imap_user, imap_pass, timeout=120)
                if otp:
                    print("OTP fetched (masked):", otp[:2] + "*"*(len(otp)-2))
                    try:
                        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='tel'], input[type='text'], input")
                        filled = False
                        for inp in inputs:
                            try:
                                if inp.is_displayed() and inp.is_enabled():
                                    inp.clear()
                                    inp.send_keys(otp)
                                    filled = True
                                    break
                            except:
                                continue
                        if not filled:
                            inp = driver.find_element(By.CSS_SELECTOR, otp_found)
                            inp.clear()
                            inp.send_keys(otp)
                    except Exception as e:
                        print("Error filling OTP into single input:", e)
                        try:
                            digit_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='tel'], input.otp, input[class*='otp']")
                            for i, ch in enumerate(otp):
                                if i < len(digit_inputs):
                                    try:
                                        digit_inputs[i].clear()
                                        digit_inputs[i].send_keys(ch)
                                    except:
                                        pass
                        except:
                            pass

                    try:
                        verify_btn = None
                        try:
                            verify_btn = driver.find_element(By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'verify') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')]")
                        except:
                            buttons = driver.find_elements(By.TAG_NAME, "button")
                            if buttons:
                                verify_btn = buttons[-1]
                        if verify_btn:
                            verify_btn.click()
                            time.sleep(6)
                            dump_page_debug(driver, "after_otp_click")
                            try:
                                wait.until(EC.url_contains("/mnjuser/profile"))
                                logged_in = True
                            except:
                                logged_in = False
                        else:
                            print("Verify button not found after OTP fill.")
                    except Exception as e:
                        print("Error clicking verify:", e)
                else:
                    print("OTP not found within timeout.")
                    dump_page_debug(driver, "otp_not_found")
            else:
                logged_in = False

        if not logged_in:
            print("Login failed, still on login page or unexpected page.")
            dump_page_debug(driver, "login_failed")
            # Exit with non-zero so workflow marks failure clearly
            sys.exit(2)
        else:
            print("Login successful, proceeding to profile refresh.")

        # Navigate to profile page to be safe
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)
        dump_page_debug(driver, "profile_page")

        if "/mnjuser/profile" not in driver.current_url:
            print("Not on profile page; skipping JS refresh.")
            dump_page_debug(driver, "not_on_profile")
            sys.exit(3)

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
        dump_page_debug(driver, "success")
        print("Profile refresh completed.")

    except SystemExit as se:
        # re-raise to preserve exit code
        raise
    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        dump_page_debug(driver, "debug_error")
        # ensure non-zero exit
        sys.exit(1)
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    run_refresh()
