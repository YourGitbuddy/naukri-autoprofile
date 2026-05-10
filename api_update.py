import os
import cloudscraper
import json

def run_skills_refresh():
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Appid": "109",
        "Systemid": "109",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        # Step 1: Login
        print("Logging in...")
        auth_url = "https://www.naukri.com/nlogin/login"
        payload = {"username": os.environ['NAUKRI_EMAIL'], "password": os.environ['NAUKRI_PASS']}
        res = scraper.post(auth_url, json=payload, headers=headers)
        
        if res.status_code != 200:
            print(f"Login Failed: {res.status_code}")
            return
        
        print("Login Success! Refreshing Skills...")

        # Step 2: Fetch Profile Detail to get current skills
        # Using the standard profile detail endpoint
        profile_url = "https://www.naukri.com/v1/jobseeker/profile"
        profile_res = scraper.get(profile_url, headers=headers)
        
        if profile_res.status_code == 200:
            profile_data = profile_res.json()
            # Extracting current skills
            skills = profile_data.get('profile', {}).get('keySkills', [])
            
            if not skills:
                print("No skills found. Adding a default skill to trigger update.")
                skills = [{"skillName": "Azure"}]
            
            # Step 3: Trigger Update by sending the same skills back
            # Naukri triggers 'Updated Today' whenever this PUT is successful
            update_url = "https://www.naukri.com/v1/jobseeker/profile/keyskills"
            update_res = scraper.put(update_url, json={"keySkills": skills}, headers=headers)
            
            if update_res.status_code in [200, 204]:
                print("🏁 SUCCESS: Skills refreshed! Profile is now Fresh.")
            else:
                print(f"Skill Update Failed: {update_res.status_code}")
                # Fallback: Just try a generic profile touch
                scraper.get("https://www.naukri.com/mnjuser/profile", headers=headers)
        else:
            print(f"Access Denied or Path Changed (404/403): {profile_res.status_code}")
            print("Try refreshing your login session or checking secrets.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    run_skills_refresh()
