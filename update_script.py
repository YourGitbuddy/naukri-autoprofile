import os
import requests

def run_naukri_update():
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    session = requests.Session()
    
    # Headers ko ek dum real browser jaisa rakha hai
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'appid': '135',
        'systemid': '135',
        'x-requested-with': 'XMLHttpRequest',
        'Referer': 'https://www.naukri.com/mnjuser/profile'
    }

    try:
        # Step 1: Login
        print("Bhai, login API hit kar raha hoon...")
        login_payload = {"username": username, "password": password}
        # Direct login endpoint
        login_res = session.post('https://www.naukri.com/nlogin/login', json=login_payload, headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Fail: {login_res.status_code}")
            return

        print("✅ Login Success!")

        # Step 2: Resume Upload (The Official Global Path)
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print("🚀 Uploading to official Naukri Profile API...")
            
            # Ye endpoint sabse stable hai (Mobile + Web common)
            # Ismein cloudgateway-jsw ki zaroorat nahi padti
            upload_url = 'https://www.naukri.com/v1/jobseeker/profile/resume'
            
            with open(resume_path, 'rb') as f:
                files = {
                    'resume': ('Resume.pdf', f, 'application/pdf')
                }
                # No 'Content-Type' header here, requests will handle multipart boundary
                upload_res = session.post(upload_url, headers=headers, files=files)
            
            if upload_res.status_code in [200, 201, 204]:
                print("🏁 Mission Accomplished! Status Updated Today.")
            else:
                # Last Fallback - Profile Sync API
                print(f"Primary API failed ({upload_res.status_code}). Trying Profile Sync API...")
                sync_url = 'https://www.naukri.com/v1/jobseeker/profile/resume/sync'
                with open(resume_path, 'rb') as f:
                    files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                    sync_res = session.post(sync_url, headers=headers, files=files)
                
                if sync_res.status_code in [200, 201]:
                    print("🏁 Mission Accomplished via Sync API!")
                else:
                    print(f"❌ Final Upload Fail! Status: {sync_res.status_code}")
                    print(f"Response Body: {sync_res.text}")
        else:
            print("❌ Error: Resume.pdf not found in root directory!")

    except Exception as e:
        print(f"❌ Error aayi hai: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
