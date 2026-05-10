import requests
import os

def refresh_naukri():
    # GitHub Secrets se cookie uthayega
    cookie = os.getenv('NAUKRI_COOKIE')
    
    if not cookie:
        print("Error: NAUKRI_COOKIE nahi mila. Secrets check karein.")
        return

    # Naukri Campus ka exact URL jo aapke screenshot mein tha
    url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-complete?flowId=mobile-mnj"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cookie": cookie,
        "appid": "801",
        "systemid": "801",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "origin": "https://www.naukri.com",
        "referer": "https://www.naukri.com/mnjuser/profile"
    }

    # Dummy data update (Azure Engineer profile refresh)
    payload = {
        "jobseekerData": {
            "resumeMakerPersonalDetails": {
                "summary": "Azure Infrastructure Engineer with experience in Synapse and AKS."
            }
        }
    }

    print("Request bhej raha hoon...")
    # Naukri Campus aksar POST ya PUT leta hai profile status refresh ke liye
    # Hum pehle POST try karenge
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Success! Status: {response.status_code}. Profile refresh ho gayi.")
    else:
        print(f"Post fail hua (Status: {response.status_code}), ab PUT try kar raha hoon...")
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Success with PUT! Profile refresh ho gayi.")
        else:
            print(f"Dono fail ho gaye. Final Status: {response.status_code}")
            print(f"Response: {response.text}")

if __name__ == "__main__":
    refresh_naukri()
