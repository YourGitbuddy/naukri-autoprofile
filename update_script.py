import os
import cloudscraper
import json

def run():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Appid": "109",
        "Systemid": "109",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        # 1. Login
        print("Logging in...")
        auth_url = "https://www.naukri.com/nlogin/login"
        payload = {"username": os.environ['NAUKRI_EMAIL'], "password": os.environ['NAUKRI_PASS']}
        res = scraper.post(auth_url, json=payload, headers=headers)
        
        if res.status_code != 200:
            print(f"Login failed: {res.status_code}")
            return
        
        print("Login Success! Fetching current headline...")

        # 2. Get Profile Data
        profile_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary"
        profile_res = scraper.get(profile_url, headers=headers)
        
        if profile_res.status_code == 200:
            current_summary = profile_res.json().get('summary', 'Azure Infrastructure and Data Engineer')
            
            # 3. Toggle a dot (.) at the end to trigger "Updated Today"
            if current_summary.endswith('.'):
                new_summary = current_summary[:-1]
            else:
                new_summary = current_summary + '.'
            
            print(f"Updating summary to trigger refresh...")
            update_payload = {"summary": new_summary}
            
            # PUT request to update
            update_res = scraper.put(profile_url, json=update_payload, headers=headers)
            
            if update_res.status_code in [200, 204]:
                print("🏁 SUCCESS: Profile Refreshed! (Updated Today status active)")
            else:
                print(f"Update failed: {update_res.status_code}")
        else:
            print(f"Could not fetch profile: {profile_res.status_code}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    run()
