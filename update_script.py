import os
import requests

def run_naukri_update():
    username = os.environ['NAUKRI_EMAIL']
    password = os.environ['NAUKRI_PASS']
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'appid': '135',
        'systemid': '135',
        'client_id': 'naukri_app',
        'x-requested-with': 'XMLHttpRequest'
    }

    try:
        # Step 1: Login
        print("Bhai, login API hit kar raha hoon...")
        login_payload = {"username": username, "password": password}
        login_res = session.post('https://www.naukri.com/nlogin/login', json=login_payload, headers=headers)
        
        if login_res.status_code != 200:
            print(f"❌ Login Fail: {login_res.status_code}")
            return

        print("✅ Login Success!")

        # Step 2: Fetch Profile Details to get correct Upload URL
        # Naukri ab profile update ke liye 'cloudgateway-jsw' use karta hai
        print("Profile details fetch kar raha hoon...")
        profile_res = session.get('https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary', headers=headers)
        
        # Step 3: Resume Upload (Using the absolute stable path)
        resume_path = os.path.join(os.getcwd(), "Resume.pdf")
        if os.path.exists(resume_path):
            print("🚀 Resume upload process start...")
            
            # Ye URL sabse stable hai kyunki ye profile summary ke session par chalta hai
            upload_url = 'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v1/users/self/resume'
            
            with open(resume_path, 'rb') as f:
                files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                # Custom headers for upload
                upload_headers = headers.copy()
                # Content-Type ko remove karna padta hai requests.post mein taaki boundary auto-set ho
                upload_res = session.post(upload_url, headers=upload_headers, files=files)
            
            if upload_res.status_code in [200, 201, 204]:
                print("🏁 Mission Accomplished! Profile Updated Today.")
            else:
                # Fallback to legacy path if v1 fails
                print(f"v1 failed ({upload_res.status_code}), trying legacy v0...")
                upload_url_v0 = 'https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/resume'
                with open(resume_path, 'rb') as f:
                    files = {'resume': ('Resume.pdf', f, 'application/pdf')}
                    upload_res_v0 = session.post(upload_url_v0, headers=headers, files=files)
                
                if upload_res_v0.status_code in [200, 201]:
                    print("🏁 Mission Accomplished via v0!")
                else:
                    print(f"❌ Upload Fail! Status: {upload_res_v0.status_code}")
                    print(f"Response: {upload_res_v0.text}")
        else:
            print("❌ Resume.pdf not found!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    run_naukri_update()
