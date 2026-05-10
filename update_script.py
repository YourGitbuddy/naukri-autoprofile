import os
import cloudscraper
import json

def run_naukri_update():
    # Android App TLS Fingerprint bypass
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
    headers = {
        "User-Agent": "Naukri/14.2 (Android 13; Pixel 7 Pro)",
        "Systemid": "109",
        "Appid": "109",
        "Accept": "application/json",
        "X-Requested-With": "com.naukri.naukriapp",
        "Referer": "https://www.naukri.com/mnjuser/profile"
    }

    try:
        print("Starting Login process...")
        
        # Step 1: Login
        login_payload = {"username": username, "password": password, "client_id": "naukri_app"}
        login_res = scraper.post("https://www.naukri.com/nlogin/login", 
                                 json=login_payload, 
                                 headers=headers)
        
        if login_res.status_code != 200:
            print(f"Login failed with status: {login_res.status_code}")
            return
        
        print("Login Successful!")

        # Step 2: Dynamic Resume Upload
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            # Universal Mobile API path
            upload_url = "https://www.naukri.com/v1/jobseeker/profile/resume"
            
            print("Attempting Resume Upload...")
            with open(resume_path, 'rb') as f:
                # 'files' parameter handles multipart/form-data boundary automatically
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                
                # Removing Content-Type from headers to let requests handle boundary
                res = scraper.post(upload_url, headers=headers, files=files)
            
            if res.status_code in [200, 201, 204]:
                print("SUCCESS: Profile refreshed and Resume uploaded!")
            else:
                print(f"Upload failed (Status: {res.status_code}). Trying Sync route...")
                with open(resume_path, 'rb') as f:
                    res_sync = scraper.put(f"{upload_url}/sync", headers=headers, files={'resume': f})
                
                if res_sync.status_code in [200, 201]:
                    print("SUCCESS: Profile refreshed via Sync route!")
                else:
                    print(f"All routes failed. Last Status: {res_sync.status_code}")
                    print(f"Response Body: {res_sync.text[:150]}")
        else:
            print("Error: Resume.pdf not found in the repository root.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
