import os
import requests

def run_naukri_update():
    # Credentials from GitHub Secrets
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    
    session = requests.Session()
    
    # Common Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'appid': '135',
        'systemid': '135'
    }

    try:
        # Step 1: Get Login Token
        print("Bhai, login API hit kar raha hoon...")
        payload = {
            "username": username,
            "password": password,
            "client_id": "naukri_app"
        }
        
        # Naukri Login API
        login_res = session.post('https://www.naukri.com/nlogin/login', json=payload, headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Fail! Status: {login_res.status_code}")
            return

        print("✅ Login Success! Cookies capture ho gayi hain.")

        # Step 2: Resume Upload
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        
        if os.path.exists(resume_path):
            print("🚀 Resume upload kar raha hoon...")
            
            with open(resume_path, 'rb') as f:
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                # Direct API Endpoint
                upload_res = session.post(
                    'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume',
                    headers=headers,
                    files=files
                )
            
            if upload_res.status_code in [200, 201, 204]:
                print("🏁 Mission Accomplished! Profile Updated.")
            else:
                print(f"❌ Upload Fail! Status: {upload_res.status_code}")
        else:
            print("❌ Resume.pdf repo mein nahi mili!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
