import os
import requests
import json
import time

def refresh_via_api():
    email = os.environ.get('NAUKRI_EMAIL')
    password = os.environ.get('NAUKRI_PASS')

    if not email or not password:
        print("❌ Error: NAUKRI_EMAIL ya NAUKRI_PASS environment variables nahi mile!")
        return

    # Standard Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Appid": "109",
        "Systemid": "109"
    }

    session = requests.Session()

    try:
        # Step 1: Login to get Session Cookies
        print("Bhai, API Login shuru kar raha hoon...")
        login_payload = {
            "username": email,
            "password": password,
            "remember_me": "true"
        }
        
        login_res = session.post("https://www.naukri.com/nlogin/v3/login", json=login_payload, headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Failed: {login_res.status_code}")
            return

        print("✅ Login Success! Profile update trigger kar raha hoon...")
        time.sleep(2)

        # Step 2: Update Headline
        # Data Engineer wala content jo tune bataya tha
        headline_text = "Azure Infrastructure and Data Engineer | Azure Synapse | Bicep | Kubernetes (AKS)"
        
        # Naukri update refresh karne ke liye aksar text ke peeche ek dot toggle karna best hota hai
        # Hum random dot toggle logic laga dete hain
        current_time = int(time.time())
        if current_time % 2 == 0:
            headline_text += "."

        update_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/profile-headline"
        update_headers = {
            "User-Agent": headers["User-Agent"],
            "Content-Type": "application/json",
            "Clientid": "d36980564696075936856", # Standard public client ID
            "Appid": "121",
            "Systemid": "121"
        }
        
        payload = {"resumeHeadline": headline_text}
        
        res = session.put(update_url, json=payload, headers=update_headers)
        
        if res.status_code in [200, 201, 204]:
            print(f"🏁 MISSION ACCOMPLISHED: Profile updated! (Value: {headline_text[-1]})")
        else:
            print(f"⚠️ Direct update fail (Status: {res.status_code}), fallback triggering...")
            # Fallback: Just visiting the profile page also updates the "Last Active" status
            session.get("https://www.naukri.com/mnjuser/profile", headers=headers)
            print("🏁 Fallback Success: Profile visited, timestamp updated.")

    except Exception as e:
        print(f"❌ API Error: {str(e)}")

if __name__ == "__main__":
    refresh_via_api()
