# 📧 NotEmails - Advanced Email Management Tool

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

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation)

</div>

---

## ✨ Features

### 🔐 Bulk Password Changer
- Change passwords for multiple email accounts simultaneously
- Multi-threaded processing (5 accounts per second)
- Rate-limited to respect API constraints (10 requests/second)
- Automatic retry handling
- Export successful and failed accounts separately
- Progress tracking with beautiful visual feedback

### 📬 Email Receiver
- Retrieve emails from multiple accounts in bulk
- Search filters support (keyword search)
- Star filter (retrieve only starred emails)
- Display email previews in the terminal
- Save emails to organized directory structure
- Export accounts with emails found
- Comprehensive statistics and reporting

### 💳 Email Purchase
- Buy emails directly from the API
- Support for multiple email types:
  - **Type 0**: Limited (Лимитные)
  - **Type 1**: Unlimited (Безлимитные)
  - **Type 2**: RU Zone (RU зона)
  - **Type 3**: Personal (Личные)
- Real-time balance display
- Automatic timestamped file saving
- Instant balance updates after purchase

### 💰 Balance Checker
- View account information
- Check current balance in RUB
- Monitor rate limits
- Display account ID and username

### 🎨 Beautiful UI
- Gradient colored ASCII banner
- Rich terminal formatting
- Progress bars and spinners
- Organized panels and tables
- Color-coded status messages
- Emoji indicators for better readability

---

## 📋 Requirements

- Python 3.7 or higher
- Active NotLetters.com account
- API Key from NotLetters.com

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/notemails.git
cd notemails
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests rich
```

### 3. Configure API Key
Edit `notemails_v2.py` and replace the placeholder with your API key:

```python
# Replace this line
API_KEY = 'YOUR_API_KEY_HERE'

# With your actual API key
API_KEY = 'your_actual_api_key_from_notletters'
```

> 🔑 Get your API key from [NotLetters.com](https://notletters.com)

---

## 💻 Usage

### Starting the Application
```bash
python notemails_v2.py
```

### Main Menu Options

#### 1️⃣ Bulk Password Changer
Change passwords for multiple accounts at once.

**Input file format** (`accounts.txt`):
```
email1@notletters.com:oldpassword1
email2@notletters.com:oldpassword2
email3@notletters.com:oldpassword3
```

**Output files:**
- `updated.txt` - Only successfully updated accounts
- `updated_mail.txt` - All accounts with current passwords

**Example workflow:**
1. Select option 1 from main menu
2. Enter path to your email list file
3. Enter new password
4. Confirm the operation
5. Wait for processing
6. Check output files

#### 2️⃣ Email Receiver
Retrieve and save emails from multiple accounts.

**Features:**
- Optional search filters (keyword search)
- Star filter (retrieve only starred emails)
- Save emails to files
- Display email previews
- Export accounts with emails

**Output structure:**
```
emails_with_letters/
├── accounts_with_mail.txt
├── email1_at_notletters_com/
│   ├── letter_1_abc12345.txt
│   ├── letter_2_def67890.txt
│   └── ...
└── email2_at_notletters_com/
    └── letter_1_ghi11223.txt
```

#### 3️⃣ Buy Emails
Purchase new email accounts directly from the API.

**Email Types:**
- **0 - Limited**: Standard limited accounts
- **1 - Unlimited**: Unlimited usage accounts
- **2 - RU Zone**: Russian zone accounts
- **3 - Personal**: Personal accounts

**Output:**
- Displays purchased emails in terminal
- Saves to `purchased_emails_YYYYMMDD_HHMMSS.txt`
- Shows updated balance

#### 4️⃣ Check Balance
View your account information and current balance.

**Displays:**
- Account ID
- Username
- Balance (RUB)
- Rate limit

---

## 📡 API Documentation

### Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/change-password` | POST | Change account password |
| `/v1/letters` | POST | Retrieve emails |
| `/v1/buy-emails` | POST | Purchase new emails |
| `/v1/me` | GET | Get account information |

### Rate Limits
- **10 requests per second** maximum
- Automatic rate limiting built-in
- Respects API constraints

### Authentication
All requests use Bearer token authentication:
```
Authorization: Bearer YOUR_API_KEY
```

---

## 📊 Examples

### Changing Passwords
```bash
$ python notemails_v2.py
# Select option 1
[+] Please enter email list file path: accounts.txt
[+] Enter new password: ********

[✓] 150/150 accounts processed
[✓] 147 successful, 3 failed
[✓] Files saved: updated.txt, updated_mail.txt
```

### Retrieving Emails
```bash
$ python notemails_v2.py
# Select option 2
[+] Please enter email list file path: accounts.txt
[+] Use search filters? No
[+] Save letters to files? Yes

[✓] 50 accounts with letters
[✓] Total: 234 letters retrieved
[✓] Letters saved to: emails_with_letters/
```

### Purchasing Emails
```bash
$ python notemails_v2.py
# Select option 3
💰 Current Balance: 5000 RUB
[+] Select email type: 0
[+] How many emails do you want to buy? 10

[✓] Successfully purchased 10 email(s)!
[✓] Emails saved to: purchased_emails_20250115_143022.txt
💰 New Balance: 4000 RUB
```

---

## 📁 File Formats

### Input File (email:password)
```
user1@notletters.com:password123
user2@notletters.com:mySecurePass456
# Comments are supported with #
user3@notletters.com:anotherPassword789
```

### Output Files

**updated.txt** (successful accounts only):
```
user1@notletters.com:newPassword123
user3@notletters.com:newPassword123
```

**updated_mail.txt** (all accounts with current passwords):
```
user1@notletters.com:newPassword123
user2@notletters.com:password123
user3@notletters.com:newPassword123
```

**Letter files** (saved emails):
```
From: Sender Name <sender@example.com>
Date: 2025-01-15 14:30:22
Subject: Test Email
Starred: No

================================================================================

Email content goes here...
```

---

## 🛠️ Configuration

### Environment Variables (Optional)
You can also use environment variables instead of hardcoding the API key:

```python
import os
API_KEY = os.getenv('NOTLETTERS_API_KEY', 'YOUR_API_KEY_HERE')
```

Then run:
```bash
export NOTLETTERS_API_KEY='your_api_key'
python notemails_v2.py
```

### Batch Size Configuration
Modify the batch size in the script (default: 5 accounts per second):
```python
batch_size = 5  # Change this value
```

---

## 🐛 Troubleshooting

### Common Issues

**API Key Error**
```
⚠️  API Key Not Configured!
```
**Solution**: Edit the script and add your API key

**File Not Found**
```
[✗] Error: File 'accounts.txt' not found!
```
**Solution**: Ensure the file path is correct and file exists

**401 Unauthorized**
```
[✗] 401 Unauthorized - Wrong old password or email doesn't exist
```
**Solution**: Verify email:password combination is correct

**Request Timeout**
```
[✗] Request timeout
```
**Solution**: Check your internet connection, API may be slow

**Rate Limit Exceeded**
```
[✗] Failed with status 429
```
**Solution**: Wait a moment, the script will automatically handle rate limiting

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This tool is for educational and legitimate use only. Users are responsible for complying with NotLetters.com's Terms of Service and all applicable laws. The authors are not responsible for any misuse of this tool.

---

## 👤 Authors

**1l9n & Claude**

- Created with ❤️ using Python and Rich

---

## 🌟 Acknowledgments

- [NotLetters.com](https://notletters.com) - For providing the API
- [Rich](https://github.com/Textualize/rich) - For beautiful terminal formatting
- [Requests](https://requests.readthedocs.io/) - For HTTP requests

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an [Issue](https://github.com/yourusername/notemails/issues)
3. Contact NotLetters.com support for API-related questions

---

<div align="center">

**Made with 💜 by 1l9n & Claude**

⭐ Star this repository if you find it helpful!

</div>
