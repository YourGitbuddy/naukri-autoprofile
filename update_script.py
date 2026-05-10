import os
import requests
import random
from datetime import datetime

def run_naukri_update():
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    session = requests.Session()
    
    # Random toggle taaki content har baar unique rahe
    toggle = "." if random.randint(0, 1) == 0 else ""
    current_time = datetime.now().strftime("%d %b %Y")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'appid': '135',
        'systemid': '135',
        'x-requested-with': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }

    try:
        # Step 1: Login
        print("Bhai, login start kar raha hoon...")
        login_res = session.post('https://www.naukri.com/nlogin/login', 
                                json={"username": username, "password": password}, 
                                headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Fail: {login_res.status_code}")
            return
        print("✅ Login Success!")

        # Step 2: Update Resume Headline (This triggers "Updated Today")
        print("Force refreshing Profile Status via Headline...")
        headline_url = 'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume-headline'
        headline_data = {
            "resumeHeadline": f"Azure Infrastructure and Data Engineer | Synapse | Bicep | AKS{toggle}"
        }
        
        h_res = session.put(headline_url, json=headline_data, headers=headers)
        
        # Step 3: Update Profile Summary (Double Confirmation)
        summary_url = 'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary'
        summary_data = {
            "summary": f"Azure Infrastructure Engineer specializing in Synapse, Bicep, and AKS. (Verified: {current_time})"
        }
        
        s_res = session.put(summary_url, json=summary_data, headers=headers)

        if h_res.status_code in [200, 201, 204] or s_res.status_code in [200, 201, 204]:
            print(f"🏁 Mission Accomplished! Profile refreshed with toggle '{toggle}'")
        else:
            print(f"❌ Status Update Fail! Headline: {h_res.status_code}, Summary: {s_res.status_code}")
            print(f"Response: {h_res.text}")

    except Exception as e:
        print(f"❌ Error aayi: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
