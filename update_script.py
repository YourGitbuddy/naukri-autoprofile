import os
import cloudscraper
import json

def run_naukri_update():
    # Browser ko Desktop Chrome mimic karne ke liye set kiya hai
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
    # Desktop Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Origin": "https://www.naukri.com",
        "Referer": "https://www.naukri.com/mnjuser/profile",
        "X-Requested-With": "XMLHttpRequest",
        "Appid": "135",
        "Systemid": "135"
    }

    try:
        print("Starting Login...")
        
        # Step 1: Login
        login_res = scraper.post("https://www.naukri.com/nlogin/login", 
                                 json={"username": username, "password": password}, 
                                 headers=headers)
        
        if login_res.status_code != 200:
            print(f"Login failed: {login_res.status_code}")
            return
        
        print("Login Successful!")

        # Step 2: Resume Upload via Legacy V0 Endpoint
        # Ye endpoint 404 hone ke chances bohot kam hain
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            # Naukri Legacy Resume Upload URL
            upload_url = "https://www.naukri.com/v0/jobseeker/profile/resume"
            
            print("Attempting Legacy Upload...")
            with open(resume_path, 'rb') as f:
                # 'resume' key important hai
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                
                # We do NOT set Content-Type header here
                res = scraper.post(upload_url, headers=headers, files=files)
            
            if res.status_code in [200, 201, 204]:
                print("SUCCESS: Profile refreshed via Legacy API!")
            else:
                print(f"Legacy failed ({res.status_code}). Trying Profile Refresh instead...")
                
                # PLAN B: Agar upload block hai, toh Headline update karke date refresh karte hain
                headline_url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume-headline"
                headline_data = {"resumeHeadline": "Azure Infrastructure and Data Engineer | Synapse | Bicep | AKS."}
                
                res_h = scraper.put(headline_url, json=headline_data, headers=headers)
                if res_h.status_code in [200, 201, 204]:
                    print("SUCCESS: Profile updated via Headline Refresh!")
                else:
                    print(f"All methods failed. Final Status: {res_h.status_code}")

        else:
            print("Error: Resume.pdf not found!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
