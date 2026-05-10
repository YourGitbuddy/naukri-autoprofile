import os
import cloudscraper
import random
import json

def run_naukri_update():
    # Android App Simulator
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'android',
            'desktop': False
        }
    )
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
    # Ye headers Naukri ki latest Android App (v14.x) ke hain
    headers = {
        "User-Agent": "Naukri/14.2 (Android 13; Pixel 7 Pro)",
        "Systemid": "109",
        "Appid": "109",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "com.naukri.naukriapp",
        "Host": "www.naukri.com",
        "Connection": "Keep-Alive"
    }

    try:
        print("Bhai, Mission 'Final Refresh' start...")
        
        # Step 1: Login via direct Auth API
        login_payload = {"username": username, "password": password, "client_id": "naukri_app"}
        login_res = scraper.post("https://www.naukri.com/nlogin/login", json=login_payload, headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Blocked: {login_res.status_code}")
            return
        
        print("✅ App Login Success!")

        # Step 2: Extract Auth Cookies strictly
        cookies = scraper.cookies.get_dict()

        # Step 3: Fast Profile Sync (No PUT, only POST)
        # Hum is baar resume-headline nahi, 'profile-summary' update karenge 
        # Kyunki iska POST endpoint hamesha open rehta hai refresh ke liye
        refresh_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary"
        
        toggle = " " if random.randint(0, 1) == 0 else ""
        summary_payload = {
            "summary": f"Azure Infrastructure and Data Engineer | Synapse | Bicep | AKS | Technical Specialist{toggle}"
        }

        print(f"Refreshing profile with subtle space toggle...")
        
        # POST is more stable than PUT on Akamai
        res = scraper.post(refresh_url, data=json.dumps(summary_payload), headers=headers)
        
        if res.status_code in [200, 201, 204]:
            print("🏁 Mission Accomplished! Status: Updated Today.")
        elif res.status_code == 405 or res.status_code == 501:
            print("POST not allowed, trying PUT with strict SSL...")
            res_put = scraper.put(refresh_url, data=json.dumps(summary_payload), headers=headers)
            if res_put.status_code in [200, 201, 204]:
                print("🏁 Mission Accomplished via PUT!")
            else:
                print(f"❌ Fail: {res_put.status_code}")
        else:
            print(f"❌ Final Fail Status: {res.status_code}")
            print(f"Response: {res.text[:150]}")

    except Exception as e:
        print(f"❌ Error aayi: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
