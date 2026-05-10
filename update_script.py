import os
import cloudscraper
import random
from datetime import datetime

def run_naukri_update():
    # cloudscraper cloudflare aur akamai bypass karne mein help karta hai
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    toggle = "." if random.randint(0, 1) == 0 else ""
    current_time = datetime.now().strftime("%d %b %Y")
    
    # Ye headers exactly wahi hain jo real browser bhejta hai
    headers = {
        'accept': 'application/json',
        'appid': '135',
        'systemid': '135',
        'content-type': 'application/json',
        'origin': 'https://www.naukri.com',
        'referer': 'https://www.naukri.com/mnjuser/profile',
        'x-requested-with': 'XMLHttpRequest'
    }

    try:
        print("Bhai, Akamai bypass ke saath login shuru...")
        # Step 1: Login
        login_url = "https://www.naukri.com/nlogin/login"
        login_payload = {"username": username, "password": password}
        
        res = scraper.post(login_url, json=login_payload, headers=headers)
        
        if res.status_code != 200:
            print(f"❌ Login Blocked by Akamai: {res.status_code}")
            return
        
        print("✅ Login Success! Session secure.")

        # Step 2: Headline Update (Using HTTPS strictly)
        # Note: 501 error often comes when API expects HTTPS but gets HTTP
        headline_url = 'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume-headline'
        headline_data = {
            "resumeHeadline": f"Azure Infrastructure and Data Engineer | Synapse | Bicep | AKS{toggle}"
        }
        
        print("Pushing Headline update...")
        h_res = scraper.put(headline_url, json=headline_data, headers=headers)
        
        if h_res.status_code in [200, 201, 204]:
            print(f"🏁 Mission Accomplished! Profile refreshed with toggle '{toggle}'")
        else:
            print(f"❌ Update Fail: {h_res.status_code}")
            print(f"Server Message: {h_res.text[:200]}") # Pehle 200 chars debug ke liye

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
