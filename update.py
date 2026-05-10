import requests
import os

# Ye values aap apne GitHub Secrets mein daaloge
cookie = os.environ['NAUKRI_COOKIE']
app_id = "801"

url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-complete?flowId=mobile-mnj"

headers = {
    "accept": "application/json, text/plain, */*",
    "cookie": cookie,
    "appid": app_id,
    "systemid": app_id,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}

# Profile refresh karne ke liye ek dummy request
response = requests.post(url, headers=headers)

if response.status_code == 200:
    print("Bhai, kaam ho gaya! Profile update ho gayi.")
else:
    print(f"Error aaya hai: {response.status_code}")
