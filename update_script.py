import os
import cloudscraper
import random
import json

def run_naukri_update():
    # Browser fingerprint ko ek dum real Android App jaisa banaya hai
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'android',
            'desktop': False
        }
    )
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
    # App Specific Headers
    headers = {
        "User-Agent": "Naukri/14.2 (Android 13; Pixel 7 Pro)",
        "Systemid": "109",
        "Appid": "109",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "com.naukri.naukriapp"
    }

    try:
        print("Bhai, Final Mission start ho raha hai...")
        
        # Step 1: Login
        login_payload = {"username": username, "password": password, "client_id": "naukri_app"}
        login_res = scraper.post("https://www.naukri.com/nlogin/login", json=login_payload, headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Fail: {login_res.status_code}")
            return
        
        print("✅ Login Success! Fresh Session captured.")

        # Step 2: Fetch Profile Summary (To get session binding)
        # Isse Naukri ke server ko lagta hai humne profile view ki hai
        scraper.get("https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary", headers=headers)

        # Step 3: The "Magic" Update (Resume Headline)
        # 501 bypass karne ke liye hum HTTPS force kar rahe hain aur Method Override headers use kar rahe hain
        headline_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume-headline"
        
        toggle = "." if random.randint(0, 1) == 0 else " "
        headline_payload = {
            "resumeHeadline": f"Azure Infrastructure and Data Engineer | Synapse | Bicep | AKS{toggle}"
        }

        # Akamai Bypass: Kuch servers PUT block karte hain par POST with Override allow karte hain
        headers["X-HTTP-Method-Override"] = "PUT"
        
        print(f"Pushing refresh signal with toggle '{toggle}'...")
        # Hum 'put' method hi use karenge par headers ke saath
        res = scraper.put(headline_url, data=json.dumps(headline_payload), headers=headers, verify=True)
        
        if res.status_code in [200, 201, 204]:
            print("🏁 Mission Accomplished! Profile 'Updated Today' mark ho gayi hai.")
        else:
            # Last Ditch Effort: Agar PUT fail ho toh POST try karo usi URL par
            print(f"PUT failed ({res.status_code}), trying direct POST fallback...")
            res_post = scraper.post(headline_url, data=json.dumps(headline_payload), headers=headers)
            
            if res_post.status_code in [200, 201, 204]:
                print("🏁 Mission Accomplished via POST Fallback!")
            else:
                print(f"❌ Final Fail! Status: {res_post.status_code}")
                print(f"Response: {res_post.text[:100]}")

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
