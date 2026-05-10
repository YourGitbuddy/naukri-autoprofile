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
            u_field
