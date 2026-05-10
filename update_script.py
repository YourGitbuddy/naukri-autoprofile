import requests
import os

# GitHub Secrets se cookie uthayega
cookie_data = os.getenv('NAUKRI_COOKIE')

# Naukri Campus API URL
url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-complete?flowId=mobile-mnj"

headers = {
    "accept": "application/json, text/plain, */*",
    "cookie": cookie_data,
    "appid": "801",
    "systemid": "801",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}

response = requests.post(url, headers=headers)

if response.status_code == 200:
    print("Mubarak ho bhai! Profile refresh ho gayi.")
else:
    print(f"Update fail ho gaya. Status: {response.status_code}")
