import os
import cloudscraper
import json

def run_naukri_update():
    # Mobile App Simulation
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
    # Ye headers legacy app ke hain jo server easily bypass hone dete hain
    headers = {
        "User-Agent": "Naukri/14.2 (Android 13; Pixel 7 Pro)",
        "Systemid": "109",
        "Appid": "109",
        "X-Requested-With": "com.naukri.naukriapp"
    }

    try:
        print("Bhai, Final Attempt: Resume Sync Mission shuru...")
        
        # Step 1: Login
        login_res = scraper.post("https://www.naukri.com/nlogin/login", 
                                 json={"username": username, "password": password, "client_id": "naukri_app"}, 
                                 headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Fail: {login_res.status_code}")
            return
        
        print("✅ Login Success!")

        # Step 2: Resume Path
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        
        if os.path.exists(resume_path):
            # Sabse stable endpoint jo 'Whitelabel Error' nahi deta
            upload_url = "https://www.naukri.com/v2/jobseeker/profile/resume"
            
            print(f"Uploading Resume to Mobile-V2 endpoint...")
            
            with open(resume_path, 'rb') as f:
                # 'files' parameter requests mein automatically sahi boundary banata hai
                files = {
                    'resume': ('Resume.pdf', f, 'application/pdf')
                }
                # Hum headers mein Content-Type nahi bhejenge taaki boundary mismatch na ho
                res = scraper.post(upload_url, headers=headers, files=files)
            
            if res.status_code in [200, 201, 204]:
                print("🏁 Mission Accomplished! Resume Fresh ho gaya.")
            else:
                print(f"❌ V2 Endpoint failed ({res.status_code}). Trying Legacy Upload...")
                # Last resort legacy URL
                legacy_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v1/users/self/resume"
                with open(resume_path, 'rb') as f:
                    res_legacy = scraper.post(legacy_url, headers=headers, files={'resume': ('Resume.pdf', f, 'application/pdf')})
                
                if res_legacy.status_code in [200, 201]:
                    print("🏁 Mission Accomplished via Legacy Route!")
                else:
                    print(f"❌ Final Fail. Status: {res_legacy.status_code}")
                    print(f"Server says: {res_legacy.text[:100]}")
        else:
            print("❌ Error: Resume.pdf missing!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
