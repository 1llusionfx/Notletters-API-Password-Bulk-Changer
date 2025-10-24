import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "https://api.notletters.com/v1/change-password"
API_KEY = None  # Will be set from user input

def print_banner():
    """Print the ASCII art banner"""
    banner = r"""
┏┓            ┓  ┏┓┓           
┃┃┏┓┏┏┓┏┏┏┓┏┓┏┫  ┃ ┣┓┏┓┏┓┏┓┏┓┏┓
┣┛┗┻┛┛┗┻┛┗┛┛ ┗┻  ┗┛┛┗┗┻┛┗┗┫┗ ┛ 
                          ┛    
"""
    print(banner)

def load_accounts_from_file(filename):
    """Load email accounts from a text file in format email:password"""
    accounts = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):  # Skip empty lines and comments
                    continue
                
                if ':' not in line:
                    print(f"Warning: Skipping invalid line {line_num}: {line}")
                    continue
                
                email, password = line.split(':', 1)
                accounts.append({
                    "email": email.strip(),
                    "old_password": password.strip()
                })
        
        print(f"Loaded {len(accounts)} accounts from {filename}\n")
        return accounts
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def change_password(email, old_password, new_password, api_key=None):
    """Change password for a single email account"""
    payload = {
        "email": email,
        "new_password": new_password,
        "old_password": old_password
    }
    
    headers = {"Content-Type": "application/json"}
    
    # Add API key if provided
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get("code") == 200:
            return {
                "email": email,
                "success": True,
                "message": result.get("data", "Password changed successfully.")
            }
        elif response.status_code == 401:
            return {
                "email": email,
                "success": False,
                "message": f"401 Unauthorized - Wrong old password or email doesn't exist."
            }
        else:
            return {
                "email": email,
                "success": False,
                "message": result.get("data", f"Failed with status {response.status_code}")
            }
    
    except requests.exceptions.Timeout:
        return {
            "email": email,
            "success": False,
            "message": "Request timeout"
        }
    except requests.exceptions.RequestException as e:
        return {
            "email": email,
            "success": False,
            "message": f"Request error: {str(e)}"
        }
    except json.JSONDecodeError:
        return {
            "email": email,
            "success": False,
            "message": "Invalid response format"
        }
    except Exception as e:
        return {
            "email": email,
            "success": False,
            "message": f"Error: {str(e)}"
        }

def save_updated_accounts(results, new_password, output_filename="updated.txt"):
    """Save successfully updated accounts to a file"""
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for result in results:
                if result["success"]:
                    f.write(f"{result['email']}:{new_password}\n")
        
        return True
    except Exception as e:
        print(f"Error saving updated accounts: {e}")
        return False

def save_all_accounts(results, original_accounts, new_password, output_filename="updated_mail.txt"):
    """Save all accounts with updated passwords for successful ones, keep old for failed"""
    try:
        # Create a map of results by email
        results_map = {result['email']: result for result in results}
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            for account in original_accounts:
                email = account['email']
                result = results_map.get(email)
                
                # If successful, use new password; otherwise keep old password
                if result and result['success']:
                    f.write(f"{email}:{new_password}\n")
                else:
                    f.write(f"{email}:{account['old_password']}\n")
        
        return True
    except Exception as e:
        print(f"Error saving updated_mail.txt: {e}")
        return False

def main():
    # Print ASCII art banner
    print_banner()
    
    print("*" * 21)
    print("made by 1l9n & Claude")
    print("*" * 21)
    print()
    
    # Set API key
    api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key
    print("API Key loaded (10 requests/second limit)")
    print("Processing 5 accounts per second to respect rate limit, please wait...")
    print()
    
    # Get the filename containing email:password pairs
    filename = input("Enter the path to your email list file: ").strip()
    
    # Load accounts from file
    accounts = load_accounts_from_file(filename)
    
    if not accounts:
        print("No valid accounts found. Exiting.")
        return
    
    # Get the new password
    new_password = input("Enter the new password for all accounts: ").strip()
    
    if not new_password:
        print("Error: New password cannot be empty!")
        return
    
    # Confirm action
    print(f"\nYou are about to change passwords for {len(accounts)} accounts.")
    confirm = input("Type 'yes' to continue: ").strip().lower()
    
    if confirm != 'yes':
        print("Operation cancelled.")
        return
    
    print("\nChanging passwords...\n")
    
    # Process accounts in batches of 5 per second
    successful = 0
    failed = 0
    results = []
    batch_size = 5
    
    for i in range(0, len(accounts), batch_size):
        batch = accounts[i:i + batch_size]
        batch_start_time = time.time()
        
        # Process batch concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_account = {
                executor.submit(change_password, account["email"], account["old_password"], new_password, api_key): account
                for account in batch
            }
            
            for future in as_completed(future_to_account):
                result = future.result()
                results.append(result)
                
                account_num = len(results)
                if result["success"]:
                    print(f"[{account_num}/{len(accounts)}] ✓ {result['email']}: {result['message']}")
                    successful += 1
                else:
                    print(f"[{account_num}/{len(accounts)}] ✗ {result['email']}: {result['message']}")
                    failed += 1
        
        # Wait to complete 1 second per batch (if needed)
        elapsed = time.time() - batch_start_time
        if elapsed < 1.0 and i + batch_size < len(accounts):
            time.sleep(1.0 - elapsed)
    
    # Save updated accounts to file
    if successful > 0:
        print("\nSaving updated accounts to 'updated.txt'...")
        if save_updated_accounts(results, new_password):
            print(f"✓ Successfully saved {successful} updated accounts to 'updated.txt'")
        else:
            print("✗ Failed to save updated accounts file")
    
    # Save all accounts (successful and failed) to updated_mail.txt
    print("\nSaving all processed accounts to 'updated_mail.txt'...")
    if save_all_accounts(results, accounts, new_password):
        print(f"✓ Successfully saved all {len(accounts)} accounts to 'updated_mail.txt'")
    else:
        print("✗ Failed to save updated_mail.txt file")
    
    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"Total accounts processed: {len(accounts)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"\nFiles created:")
    if successful > 0:
        print(f"  - updated.txt (only successful accounts)")
    print(f"  - updated_mail.txt (all accounts with current passwords)")
    print("=" * 50)

if __name__ == "__main__":
    main()