# Notletters-API-Password-Bulk-Changer

# Password Changer — README

Short instructions for running the password changing script (psw.py).

## Overview
This script updates passwords for a list of email accounts using an API. Use only on accounts you own or have explicit permission to modify.

## Requirements
- Python 3.8+
- A valid API key for the service used in the script (placeholder named `NOTLETTERS_API_KEY` in the code).

## Install
1. Place `psw.py` and `requirements.txt` in the same folder.
2. Open a terminal in that folder.
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Configure API key
- Open `psw.py` in a text editor.
- Replace the API key placeholder (search for `NOTLETTERS_API_KEY` or similar variable) with your actual API key before running.

## Email file format
- Plain text, one email per line:
  ```
  user1@example.com:Password1
  user2@example.com:Password2
  ```
- You may use an absolute or relative path when prompted.

## Usage
1. In the terminal (inside the script folder) run:
    ```
    python psw.py
    ```
2. Follow interactive prompts:
    - Enter the path (and filename) of your emails file.
    - Enter the new password to apply to the accounts.
3. The script will process the list and report results in the terminal (or as implemented).

## Safety & Notes
- Always test with a small set of accounts first.
- Keep your API key secret. Do not commit it to source control.
- Back up any important data before making changes.
- Use only for authorized accounts.

## License
Use according to the script’s included license (or add one if none is provided).
