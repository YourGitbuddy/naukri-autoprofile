import requests
import os

def refresh_naukri():
    cookie = os.getenv('NAUKRI_COOKIE')
    
    if not cookie:
        print("Error: NAUKRI_COOKIE nahi mila.")
        return

    # Wahi URL jo aapke screenshot mein 200 OK de raha tha
    url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-complete?flowId=mobile-mnj"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "cookie": cookie,
        "appid": "801", # Jo aapke screenshot mein tha
        "systemid": "801",
        "origin": "https://www.naukri.com",
        "referer": "https://www.naukri.com/mnjuser/profile",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    # Naukri Campus refresh ke liye empty ya minimal payload bhi leta hai POST par
    payload = {}

    print("Naukri Campus refresh request bhej raha hoon...")
    
    # Hum POST try kar rahe hain kyunki aapke screenshot mein profile-complete POST hi tha
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Mubarak ho bhai! Status {response.status_code}: Profile update ho gayi.")
    else:
        print(f"Failed! Status: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    refresh_naukri()
