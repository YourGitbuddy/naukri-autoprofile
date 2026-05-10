import requests
import os

def refresh_naukri():
    cookie = os.getenv('NAUKRI_COOKIE')
    
    if not cookie:
        print("Error: NAUKRI_COOKIE nahi mila.")
        return

    # Naukri Campus ka Generic Summary Update URL
    url = "https://www.naukri.com/cloudgateway-jsw/jobseeker-profile-services/v0/users/self/profile-summary"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "cookie": cookie,
        "appid": "135", # Naukri Campus/Web ke liye aksar 135 ya 801 hota hai
        "systemid": "135",
        "origin": "https://www.naukri.com",
        "referer": "https://www.naukri.com/mnjuser/profile",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    # Summary payload
    payload = {
        "summary": "Azure Infrastructure Engineer with expertise in Azure Synapse Analytics, Bicep, and Kubernetes (AKS)."
    }

    print("Request bhej raha hoon...")
    
    # Naukri hamesha PUT use karta hai update ke liye
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Mubarak ho bhai! Success {response.status_code}. Profile refresh ho gayi.")
    else:
        print(f"Failed! Status: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    refresh_naukri()
