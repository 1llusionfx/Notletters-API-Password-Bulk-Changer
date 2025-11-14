# Password Changer & Email Receiver — README

Comprehensive guide for the multi-functional email management script (`notemails.py`).

## Overview
This Python script provides two powerful features for managing NotLetters email accounts:
1. **Bulk Password Changer** - Automate password updates for multiple accounts
2. **Email Receiver** - Retrieve and save emails from multiple accounts with filtering options

The script features a beautiful terminal interface with purple-to-cyan gradient colors powered by the Rich library. **Important:** Use this script only on accounts you own or have explicit permission to access. Unauthorized use may violate terms of service or laws.

## Features

### 🎨 **Beautiful Terminal UI**
- Purple to cyan gradient colors throughout the interface
- Animated progress bars with custom styling
- Elegant panels and tables for organized information display
- Spinner animations during operations
- Color-coded success/failure indicators
- Interactive menu system

### 🔐 **Bulk Password Changer**
- Processes accounts in batches of 5 per second to comply with API rate limits
- Concurrent execution using threading for efficiency
- Robust error handling for timeouts and API errors
- Saves results to organized output files
- Real-time progress tracking with visual feedback

### 📧 **Email Receiver**
- Retrieve emails from multiple accounts simultaneously
- **Search filtering** - Filter emails by keyword
- **Star filtering** - Fetch only starred emails
- Display emails in formatted, readable panels
- **Auto-save** - Save emails to organized files by account
- Support for both text and HTML content
- Timestamp formatting for easy reading

### 🛡️ **Safety Features**
- File format validation
- Interactive confirmation prompts
- Rate limit compliance
- Password masking during input
- Comprehensive error handling

## Requirements
- Python 3.8 or higher
- Internet connection for API calls
- A valid API key from NotLetters
- Dependencies:
  - `requests` - For API communication
  - `rich` - For enhanced terminal UI

## Installation
1. Download or clone the repository containing `passwordchanger.py`, `requirements.txt`, and optionally `emails.txt`.
2. Place all files in the same directory.
3. Open a terminal in that directory.
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### API Key Setup
- The script uses the NotLetters API endpoints:
  - Password Change: `https://api.notletters.com/v1/change-password`
  - Email Retrieval: `https://api.notletters.com/v1/letters`
- Open `passwordchanger.py` in a text editor.
- Locate: `api_key = "YOUR_API_KEY_HERE"`
- Replace with your actual API key from NotLetters.
- **Security Note:** Never commit your API key to version control.

### Email File Format
Create a plain text file (e.g., `emails.txt`) with one account per line:
```
email:password
```

Example:
```
user1@example.com:Password123
user2@example.com:SecurePass456
# This is a comment (ignored)
```

- Lines starting with `#` are comments
- Invalid lines (without `:`) are skipped with warnings
- Use UTF-8 encoding
- Supports both absolute and relative paths

## Usage

### Starting the Script
```bash
python passwordchanger.py
```

### Main Menu
You'll see a beautiful gradient menu with three options:

**1. Bulk Password Changer**
- Change passwords for multiple accounts at once
- Interactive prompts guide you through the process
- Results saved to `updated.txt` and `updated_mail.txt`

**2. Email Receiver**
- Retrieve emails from multiple accounts
- Optional search and star filters
- View emails in terminal or save to files
- Organized by account in `letters_output/` directory

**3. Exit**
- Gracefully exit the program

## Mode 1: Bulk Password Changer

### How to Use
1. Select option `1` from main menu
2. Enter path to your email list file
3. Enter the new password (input is hidden)
4. Confirm the operation
5. Watch the animated progress bar
6. View the summary table

### Output Files
- **updated.txt** - Only successfully updated accounts with new passwords
- **updated_mail.txt** - All accounts (successful with new password, failed with old password)

### Example Session
```
Enter the path to your email list file: emails.txt
✓ Loaded 100 accounts from emails.txt

Enter the new password for all accounts: ********

⚠ You are about to change passwords for 100 accounts.
Do you want to continue? (y/n): y

✓ [1/100] user1@example.com: Password changed successfully.
✓ [2/100] user2@example.com: Password changed successfully.
...
```

## Mode 2: Email Receiver

### How to Use
1. Select option `2` from main menu
2. Enter path to your email list file
3. Choose whether to use filters:
   - **Search filter** - Enter keyword to search in emails
   - **Star filter** - Fetch only starred emails
4. Choose whether to save letters to files
5. View emails in terminal (first 5 per account shown)
6. Check the summary table

### Output Structure
```
letters_output/
├── user1_at_example_com/
│   ├── letter_1_89917e2b.txt
│   ├── letter_2_a3b5c7d9.txt
│   └── ...
├── user2_at_example_com/
│   ├── letter_1_12345678.txt
│   └── ...
└── ...
```

### Letter Display Format
Each email is displayed in a beautiful panel showing:
- 📧 Sender name and email
- 📅 Date and time
- ⭐ Starred status
- 📝 Subject
- Content preview (first 500 characters)

### Saved Letter Format
Each saved `.txt` file contains:
- Full email headers (From, Date, Subject, Starred)
- Complete text content
- Complete HTML content
- Separated sections with dividers

### Example Session
```
Enter the path to your email list file: emails.txt
✓ Loaded 50 accounts from emails.txt

Do you want to use search filters? (y/n): y
Enter search keyword (or press Enter to skip): invoice
Only fetch starred emails? (y/n): n

Save letters to files? (y/n): y

✓ user1@example.com: Retrieved 15 letters

Letters for user1@example.com:

┌─ Letter #1 ──────────────────────┐
│ 📧 From: Company <no-reply@...>  │
│ 📅 Date: 2024-11-14 10:30:45     │
│ ⭐ Starred: No                   │
│ 📝 Subject: Your Invoice         │
│                                   │
│ Content:                          │
│ Dear customer, your invoice...    │
└───────────────────────────────────┘
```

## API Features

### Password Change API
- **Endpoint:** `POST https://api.notletters.com/v1/change-password`
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "old_password": "OldPass123",
    "new_password": "NewPass456"
  }
  ```
- **Rate Limit:** 10 requests/second (script uses 5/sec for safety)

### Email Retrieval API
- **Endpoint:** `POST https://api.notletters.com/v1/letters`
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "Password123",
    "filters": {
      "search": "keyword",
      "star": false
    }
  }
  ```
- **Response:** Array of letter objects with full content
- **Rate Limit:** 10 requests/second

## Troubleshooting

### Common Issues

**File Not Found**
- Verify the file path is correct
- Check file exists in the specified location

**Invalid File Format**
- Ensure each line follows `email:password` format
- Check for missing colons
- Yellow warnings show which lines are skipped

**API Errors**
- **401 Unauthorized:** Wrong password or email doesn't exist
- **Timeout:** Network issues or slow connection
- **Rate Limit:** Script already handles this, but if you see errors, wait a moment

**No Emails Retrieved**
- Check account credentials are correct
- Verify the account has emails
- Try without filters to see all emails

**Dependencies Missing**
```bash
pip install -r requirements.txt
```

**Python Version**
- Requires Python 3.8+ for Rich library compatibility

**Terminal Compatibility**
- Works best with modern terminals supporting true color
- Recommended: Windows Terminal, iTerm2, modern Linux terminals

**Permission Issues**
- Ensure you have write permissions in the script directory
- Check you can create the `letters_output/` folder

## Terminal UI Color Guide

### Color Meanings
- 🟣 **Purple** - Headers, titles, branding
- 🔵 **Cyan** - Information, prompts, general text
- 🟢 **Green** - Success messages, confirmations
- 🔴 **Red** - Errors, failures
- 🟡 **Yellow** - Warnings, cautions
- 🟣 **Magenta** - Statistics, counts

### Visual Elements
- **Gradient Text** - Purple to cyan fade for branding
- **Panels** - Bordered information boxes
- **Progress Bars** - Animated with gradient styling
- **Spinners** - Loading indicators for operations
- **Tables** - Organized data display with borders
- **Emoji** - Visual indicators (✓, ✗, ⚠, 📧, etc.)

## Best Practices

### Security
- **Never share** your API key
- **Don't commit** API keys to version control
- **Store passwords** securely
- **Use strong passwords** when changing passwords
- **Backup** account credentials before bulk operations

### Testing
- **Start small** - Test with 2-3 accounts first
- **Verify** one password change manually before bulk operations
- **Check filters** work as expected in email receiver mode

### Data Management
- **Keep backups** of original email files
- **Organize output** - Review saved letters periodically
- **Clean up** old output files to save space
- **Monitor usage** - Keep track of API rate limits

### Rate Limiting
- Script automatically respects rate limits
- 5 requests/second for password changes (safe margin)
- Small delays between email retrievals
- Don't run multiple instances simultaneously

## Advanced Usage

### Custom Filters
When using Email Receiver mode:
- **Search filter:** Searches in subject, sender, and content
- **Star filter:** Only retrieves starred/important emails
- **Combine both:** Get starred emails matching a keyword

### Batch Operations
For very large account lists:
1. Split the file into smaller batches
2. Process each batch separately
3. Combine results if needed

### Automation
The script can be called programmatically:
```python
from passwordchanger import password_changer_mod
