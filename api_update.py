import os
import cloudscraper
import json

def run_invisible_refresh():
    # Chrome Desktop mimic kar rahe hain
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Appid": "109",
        "Systemid": "109",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.naukri.com"
    }
    
    try:
        # Step 1: Login
        print("Logging in...")
        auth_url = "https://www.naukri.com/nlogin/login"
        login_payload = {"username": os.environ['NAUKRI_EMAIL'], "password": os.environ['NAUKRI_PASS']}
        res = scraper.post(auth_url, json=login_payload, headers=headers)
        
        if res.status_code != 200:
            print(f"Login Failed: {res.status_code}")
            return
        
        print("Login Success! Toggling Invisible Space...")

        # Step 2: Fetch current Summary
        summary_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary"
        get_res = scraper.get(summary_url, headers=headers)
        
        if get_res.status_code == 200:
            current_data = get_res.json()
            summary_text = current_data.get('summary', 'Azure Infrastructure and Data Engineer')
            
            # Logic: Agar last mein space hai toh hata do, nahi hai toh add kar do.
            # Ye recruiter ko UI par bilkul nahi dikhega.
            if summary_text.endswith(' '):
                new_summary = summary_text.rstrip()
                print("Removing trailing space...")
            else:
                new_summary = summary_text + ' '
                print("Adding trailing space...")
            
            # Step 3: PUT request to trigger "Updated Today"
            update_payload = {"summary": new_summary}
            update_res = scraper.put(summary_url, json=update_payload, headers=headers)
            
            if update_res.status_code in [200, 204]:
                print("🏁 SUCCESS: Invisible update complete! Profile is now Fresh.")
            else:
                print(f"Update failed with status: {update_res.status_code}")
        else:
            print(f"Could not fetch summary: {get_res.status_code}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    run_invisible_refresh()
