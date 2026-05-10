import os
import cloudscraper
import json

def run_naukri_update():
    # Android App Simulator
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
    # Headers - Content-Type yahan nahi likhenge kyunki file upload hai
    headers = {
        "User-Agent": "Naukri/14.2 (Android 13; Pixel 7 Pro)",
        "Systemid": "109",
        "Appid": "109",
        "X-Requested-With": "com.naukri.naukriapp"
    }

    try:
        print("Bhai, Resume Upload Mission shuru...")
        
        # Step 1: Login
        login_res = scraper.post("https://www.naukri.com/nlogin/login", 
                                 json={"username": username, "password": password, "client_id": "naukri_app"}, 
                                 headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Fail: {login_res.status_code}")
            return
        
        print("✅ Login Success! Session active hai.")

        # Step 2: Resume Upload Path
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        
        if os.path.exists(resume_path):
            # Naukri ke do sabse stable endpoints
            urls = [
                "https://www.naukri.com/v1/jobseeker/profile/resume",
                "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v1/users/self/resume"
            ]
            
            success = False
            for url in urls:
                print(f"Trying upload on: {url}")
                with open(resume_path, 'rb') as f:
                    files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                    # Note: Yahan headers mein 'Content-Type' nahi bhejenge
                    res = scraper.post(url, headers=headers, files=files)
                
                if res.status_code in [200, 201, 204]:
                    print(f"🏁 Mission Accomplished! Resume uploaded via {url.split('/')[-1]}")
                    success = True
                    break
                else:
                    print(f"❌ Failed on this URL (Status: {res.status_code})")
            
            if not success:
                print("❌ Dono endpoints fail ho gaye. Response Check karo.")
                print(f"Last Response: {res.text[:150]}")
        else:
            print("❌ Error: Resume.pdf nahi mili root folder mein!")

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
