# 🚀 Naukri Profile Auto-Refresh Bot

An automated solution for **Azure Infrastructure & Data Engineers** to keep their Naukri.com profile active 24/7. This bot uses Selenium and GitHub Actions to bypass bot detection and refresh your profile status daily.

## 🌟 Features
- **Daily Automated Refresh:** Keeps you at the top of recruiter search results.
- **Bot Detection Bypass:** Uses advanced masking (Undetected Headless Chrome) to avoid Akamai blocks.
- **CI/CD Integration:** Powered by GitHub Actions - no local machine required.
- **Secure Credentials:** Uses GitHub Secrets to manage sensitive data.

## 🛠 Tech Stack
- **Language:** Python 3.9+
- **Automation:** Selenium WebDriver
- **CI/CD:** GitHub Actions
- **Infrastructure:** Linux (Ubuntu Runner)

## 📁 Project Structure
- `update_script.py`: The core automation logic using Selenium and JS injection.
- `.github/workflows/naukri_update.yml`: The automation schedule (Cron Job).

## 🚀 Setup Instructions

### 1. Repository Setup
Copy the `update_script.py` and the workflow file into your GitHub repository.

### 2. Configure GitHub Secrets
Go to your Repo **Settings > Secrets and variables > Actions** and add the following:
- `NAUKRI_EMAIL`: Your Naukri Login Email.
- `NAUKRI_PASS`: Your Naukri Password.

### 3. Schedule
The bot is scheduled to run at **04:00 UTC (09:30 AM IST)** daily. You can also trigger it manually from the **Actions** tab.

## 🧠 Behind the Scenes
As an **Azure Engineer**, I designed this to handle modern web security:
1. **Masking:** Modified navigator objects to hide automation flags.
2. **Referrer Bypass:** Starts from Google to simulate organic traffic.
3. **JS Injection:** Instead of fragile UI clicking, it uses direct `fetch` API calls within the browser session for 100% stability.

---
**Note:** This project is for educational and personal career management purposes only.
