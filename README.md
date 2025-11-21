# NotEmails - Advanced Email Management Tool

<div align="center">

```
 _   _       _   _____                 _ _     
| \ | | ___ | |_| ____|_ __ ___   __ _(_) |___ 
|  \| |/ _ \| __|  _| | '_ ` _ \ / _` | | / __|
| |\  | (_) | |_| |___| | | | | | (_| | | \__ \
|_| \_|\___/ \__|_____|_| |_| |_|\__,_|_|_|___/
```

**A powerful command-line tool for managing NotLetters.com email accounts**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Rich](https://img.shields.io/badge/Rich-Terminal-orange.svg)](https://github.com/Textualize/rich)

</div>

---

## Features

### Bulk Password Changer

### Email Receiver

### Email Purchase

### Balance Checker

### Beautiful UI

---

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/1llusionfx/NotLetters-Email-Tool
cd Notletters-Email-Tool

# Install dependencies
pip install -r requirements.txt
```

**Requirements:**
```
requests
rich
```

### 2. Configuration

**First run:** The script will ask for your API Key and will save it to `config.json`

```bash
python notemails.py
```

You'll be prompted:
```
[+] Please enter your NotLetters.com API Key: ********
[+] Save API Key to config file? Yes
```

**To change API Key:** Simply delete `config.json` or answer "Yes" when asked to change it on startup.

Get your API key from [NotLetters.com](https://notletters.com)

---

## Usage

### Input File Format
Create a text file with email:password combinations (e.g., `accounts.txt`):

```
email1@notletters.com:password1
email2@notletters.com:password2
email3@notletters.com:password3
```

### Main Menu Options

**1️⃣ Bulk Password Changer**
- Changes passwords for all accounts in your file
- Creates `updated.txt` (successful accounts only)
- Creates `updated_mail.txt` (all accounts with current passwords)

**2️⃣ Email Receiver**
- Retrieves emails from all accounts
- Optional search and star filters
- Saves to `emails_with_letters/` directory
- Each account gets its own subdirectory

**3️⃣ Buy Emails**
- Purchase new email accounts
- Choose from 4 types:
  - **0** - Limited (Лимитные)
  - **1** - Unlimited (Безлимитные)
  - **2** - RU Zone (RU зона)
  - **3** - Personal (Личные)
- Saves to timestamped file

**4️⃣ Check Balance**
- View your account details and balance

---

## Output Files

### Password Changer
```
updated.txt           # Successfully updated accounts
updated_mail.txt      # All accounts with current passwords
```

### Email Receiver
```
emails_with_letters/
├── accounts_with_mail.txt
├── email1_at_notletters_com/
│   ├── letter_1_abc12345.txt
│   └── letter_2_def67890.txt
└── email2_at_notletters_com/
    └── letter_1_ghi11223.txt
```

### Email Purchase
```
purchased_emails_20250118_143022.txt
```

---

## Configuration File

After first run, `config.json` is created:

```json
{
  "api_key": "your_api_key_here"
}
```

**If you want to reset the KEY:** Delete `config.json` and restart the script.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `API Key Not Configured` | Run script and then enter your API key when prompted |
| `File not found` | Check if file path is correct |
| `401 Unauthorized` | Verify 'email:password' format and combi. is correct |
| `Rate Limit Exceeded` | Script handles this automatically, please wait |

---

## API Information

- **Base URL:** `https://api.notletters.com`
- **Rate Limit:** 10 requests/second (handled automatically)
- **Authentication:** Bearer token

---

## Disclaimer

This tool is for educational and legitimate use only. Users are responsible for complying with NotLetters.com's Terms of Service and all applicable laws.

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made by 1l9n**

⭐ Star this repository if you find it helpful!

</div>
