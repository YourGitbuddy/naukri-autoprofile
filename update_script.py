import requests
import os
import json

# GitHub Secrets se cookie uthayega
cookie = os.getenv('NAUKRI_COOKIE')

if not cookie:
    print("Error: NAUKRI_COOKIE secret nahi mila. Pehle use GitHub mein add karo.")
    exit(1)

# Naukri Campus ka exact API URL jo aapke screenshot mein tha
# Hum isi URL par PUT request bhejenge profile update karne ke liye
url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-complete?flowId=mobile-mnj"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cookie": cookie,
    "appid": "801",
    "systemid": "801",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "origin": "https://www.naukri.com",
    "referer": "https://www.naukri.com/mnjuser/profile"
}

# Ye wahi data hai jo aapke screenshot ke 'Preview' mein dikh raha tha
# Ismein hum bas summary ko refresh kar rahe hain
payload = {
    "jobseekerData": {
        "resumeMakerPersonalDetails": {
            "summary": "Azure Infrastructure Engineer with experience in Synapse and AKS."
        }
    }
}

try:
    # Update ke liye PUT request bhej rahe hain
    response = requests.put(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200 or response.status_code == 201:
        print(f"Mubarak ho bhai! Status {response.status_code}: Profile successfully refresh ho gayi.")
    elif response.status_code == 404:
        print("Error 404: URL abhi bhi galat hai. Hum POST method try karte hain...")
        # Agar PUT fail hota hai toh POST try karega
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"POST Attempt Status: {response.status_code}")
    else:
        print(f"Update fail ho gaya. Status Code: {response.status_code}")
        print("Response Text:", response.text)

except Exception as e:
    print(f"Kuch gadbad ho gayi: {e}")
