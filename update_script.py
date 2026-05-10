import os
import cloudscraper
import random

def run_naukri_update():
    # App simulator headers
    scraper = cloudscraper.create_scraper()
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
    app_headers = {
        "Content-Type": "application/json",
        "Systemid": "109",  # Mobile App System ID
        "Appid": "109",     # Mobile App ID
        "User-Agent": "Naukri/14.2 (Android 13; Pixel 6)",
        "X-Requested-With": "com.naukri.naukriapp"
    }

    try:
        print("Bhai, App API se login try kar raha hoon...")
        # Step 1: Login via Mobile API
        login_payload = {
            "username": username,
            "password": password,
            "client_id": "naukri_app"
        }
        
        # Akamai bypass ke liye direct hitting nlogin
        login_res = scraper.post("https://www.naukri.com/nlogin/login", 
                                 json=login_payload, 
                                 headers=app_headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Blocked: {login_res.status_code}")
            return
        
        print("✅ App Login Success!")

        # Step 2: Update Profile Status (Quick Refresh)
        # Hum 'Resume Headline' update karenge mobile endpoint se
        print("Profile refresh trigger kar raha hoon...")
        
        headline_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume-headline"
        
        # Thoda variation taaki change detect ho
        toggle = "." if random.randint(0, 1) == 0 else ""
        headline_payload = {
            "resumeHeadline": f"Azure Infrastructure and Data Engineer | Synapse | Bicep | AKS{toggle}"
        }
        
        # Mobile API usually supports PUT easily
        res = scraper.put(headline_url, json=headline_payload, headers=app_headers)
        
        if res.status_code in [200, 201, 204]:
            print(f"🏁 Mission Accomplished! Profile Updated Today (Mode: App Simulator)")
        else:
            print(f"❌ Final Fail: {res.status_code}")
            print(f"Debug: {res.text[:150]}")

    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
