import os
import cloudscraper
import random

def run_naukri_update():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
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
        print("Bhai, login shuru...")
        login_res = scraper.post("https://www.naukri.com/nlogin/login", 
                                 json={"username": username, "password": password}, 
                                 headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Fail: {login_res.status_code}")
            return
        
        print("✅ Login Success!")

        # Step 2: Fetch existing skills
        print("Existing skills dhoond raha hoon...")
        profile_res = scraper.get("https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary", headers=headers)
        
        # Step 3: Fast Refresh via Profile Summary Update (POST instead of PUT)
        # Hum is baar 'cloudgateway' ke bajaye seedha main domain hit karenge
        print("Profile status refresh kar raha hoon...")
        
        # POST request aksar gateways easily pass kar dete hain
        refresh_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary"
        
        # Hum summary mein ek chota sa change karenge
        # "Azure Infrastructure" ke aage ek extra space ya dot
        dot = "." if random.randint(0, 1) == 0 else " "
        payload = {
            "summary": f"Azure Infrastructure and Data Engineer specialized in Synapse, Bicep, and AKS{dot}"
        }
        
        # Kuch cases mein POST as PUT override kaam kar jata hai
        headers['X-HTTP-Method-Override'] = 'PUT' 
        
        res = scraper.post(refresh_url, json=payload, headers=headers)
        
        if res.status_code in [200, 201, 204]:
            print(f"🏁 Mission Accomplished! Profile refreshed with '{dot}'")
        else:
            print(f"❌ Refresh Fail: {res.status_code}")
            print(f"Server Message: {res.text[:100]}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
