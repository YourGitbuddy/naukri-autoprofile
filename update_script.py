import os
import cloudscraper
import json

def run_naukri_update():
    # Android Chrome fingerprint
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json",
        "Appid": "135",
        "Systemid": "135",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.naukri.com",
        "Referer": "https://www.naukri.com/nlogin/login"
    }

    try:
        print("Starting API Login...")
        
        # Step 1: Login to get Session Cookies
        login_data = {"username": username, "password": password}
        res_login = scraper.post("https://www.naukri.com/nlogin/login", json=login_data, headers=headers)
        
        if res_login.status_code != 200:
            print(f"Login Blocked (Status: {res_login.status_code}). Server might be rejecting GitHub IP.")
            return

        print("Login Successful! Refreshing profile status...")

        # Step 2: Touch Profile Activity (This triggers 'Updated Today')
        # Hum resume upload ke bajaye 'Profile Summary' ko ek dot (.) se update karenge
        # Ye hamesha kaam karta hai aur 404/501 nahi deta
        
        refresh_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary"
        
        # We fetch current summary first to keep it safe
        current_data = scraper.get(refresh_url, headers=headers).json()
        summary = current_data.get('summary', 'Azure Infrastructure and Data Engineer')
        
        # Adding/Removing a dot to trigger update
        new_summary = summary[:-1] if summary.endswith('.') else summary + '.'
        
        payload = {"summary": new_summary}
        
        # Method override for PUT via POST (To bypass firewall)
        headers["X-HTTP-Method-Override"] = "PUT"
        res_refresh = scraper.post(refresh_url, json=payload, headers=headers)

        if res_refresh.status_code in [200, 204]:
            print("🏁 SUCCESS: Profile Refreshed! Status: Updated Today.")
        else:
            print(f"Refresh failed (Status: {res_refresh.status_code}).")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
