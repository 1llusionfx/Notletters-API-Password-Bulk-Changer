import requests
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import box
from rich.markdown import Markdown

API_URL_PASSWORD = "https://api.notletters.com/v1/change-password"
API_URL_LETTERS = "https://api.notletters.com/v1/letters"
API_KEY = None

# Initialize Rich console
console = Console()

def create_gradient_text(text, start_color="purple", end_color="cyan"):
    """Create a gradient text from start_color to end_color"""
    gradient = Text()
    length = len(text)
    
    colors = {
        "purple": (128, 0, 128),
        "cyan": (0, 255, 255)
    }
    
    start_rgb = colors[start_color]
    end_rgb = colors[end_color]
    
    for i, char in enumerate(text):
        ratio = i / max(length - 1, 1)
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
        
        gradient.append(char, style=f"rgb({r},{g},{b})")
    
    return gradient

def print_banner():
    """Print the ASCII art banner with gradient"""
    banner = r"""
┏┓            ┓  ┏┓┓           
┃┃┏┓┏┏┓┏┏┏┓┏┓┏┫  ┃ ┣┓┏┓┏┓┏┓┏┓┏┓
┣┛┗┻┛┛┗┻┛┗┛┛ ┗┻  ┗┛┛┗┗┻┛┗┗┫┗ ┛ 
                          ┛    
"""
    gradient_banner = create_gradient_text(banner)
    console.print(gradient_banner, justify="center")
    
    credit_text = create_gradient_text("made by 1l9n & Claude", "purple", "cyan")
    console.print(Panel(credit_text, border_style="purple", box=box.DOUBLE))
    console.print()

def show_main_menu():
    """Display main menu and get user choice"""
    menu_text = Text()
    menu_text.append("1. ", style="bold cyan")
    menu_text.append("Bulk Password Changer\n", style="white")
    menu_text.append("2. ", style="bold magenta")
    menu_text.append("Email Receiver\n", style="white")
    menu_text.append("3. ", style="bold red")
    menu_text.append("Exit", style="white")
    
    menu_panel = Panel(
        menu_text,
        title=create_gradient_text("Main Menu", "purple", "cyan"),
        border_style="purple",
        box=box.DOUBLE
    )
    console.print(menu_panel)
    
    choice = Prompt.ask(
        "[bold cyan]Select an option[/bold cyan]",
        choices=["1", "2", "3"],
        default="1"
    )
    return choice

def load_accounts_from_file(filename):
    """Load email accounts from a text file in format email:password"""
    accounts = []
    try:
        with console.status(f"[cyan]Loading accounts from {filename}...", spinner="dots"):
            with open(filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if ':' not in line:
                        console.print(f"[yellow]⚠ Warning: Skipping invalid line {line_num}: {line}")
                        continue
                    
                    email, password = line.split(':', 1)
                    accounts.append({
                        "email": email.strip(),
                        "old_password": password.strip()
                    })
        
        console.print(f"[green]✓ Loaded {len(accounts)} accounts from {filename}[/green]\n")
        return accounts
    
    except FileNotFoundError:
        console.print(f"[red]✗ Error: File '{filename}' not found![/red]")
        return []
    except Exception as e:
        console.print(f"[red]✗ Error reading file: {e}[/red]")
        return []

def change_password(email, old_password, new_password, api_key=None):
    """Change password for a single email account"""
    payload = {
        "email": email,
        "new_password": new_password,
        "old_password": old_password
    }
    
    headers = {"Content-Type": "application/json"}
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.post(
            API_URL_PASSWORD,
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

def get_letters(email, password, search_filter=None, star_filter=None, api_key=None):
    """Retrieve letters for a single email account"""
    payload = {
        "email": email,
        "password": password,
        "filters": {}
    }
    
    if search_filter:
        payload["filters"]["search"] = search_filter
    if star_filter is not None:
        payload["filters"]["star"] = star_filter
    
    headers = {"Content-Type": "application/json"}
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.post(
            API_URL_LETTERS,
            json=payload,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "email": email,
                "success": True,
                "letters": result.get("data", {}).get("letters", []),
                "count": len(result.get("data", {}).get("letters", []))
            }
        elif response.status_code == 401:
            return {
                "email": email,
                "success": False,
                "message": "401 Unauthorized - Wrong password or email doesn't exist.",
                "letters": [],
                "count": 0
            }
        else:
            return {
                "email": email,
                "success": False,
                "message": f"Failed with status {response.status_code}",
                "letters": [],
                "count": 0
            }
    
    except requests.exceptions.Timeout:
        return {
            "email": email,
            "success": False,
            "message": "Request timeout",
            "letters": [],
            "count": 0
        }
    except Exception as e:
        return {
            "email": email,
            "success": False,
            "message": f"Error: {str(e)}",
            "letters": [],
            "count": 0
        }

def display_letter(letter, index):
    """Display a single letter in a formatted panel"""
    letter_date = datetime.fromtimestamp(letter.get("date", 0)).strftime("%Y-%m-%d %H:%M:%S")
    
    letter_info = Text()
    letter_info.append(f"📧 From: ", style="bold cyan")
    letter_info.append(f"{letter.get('sender_name', 'Unknown')} <{letter.get('sender', 'unknown')}>\n", style="white")
    letter_info.append(f"📅 Date: ", style="bold magenta")
    letter_info.append(f"{letter_date}\n", style="white")
    letter_info.append(f"⭐ Starred: ", style="bold yellow")
    letter_info.append(f"{'Yes' if letter.get('star') else 'No'}\n", style="white")
    letter_info.append(f"📝 Subject: ", style="bold green")
    letter_info.append(f"{letter.get('subject', 'No Subject')}\n\n", style="white")
    
    # Text content
    text_content = letter.get("letter", {}).get("text", "No content available")
    letter_info.append("Content:\n", style="bold purple")
    letter_info.append(text_content[:500] + ("..." if len(text_content) > 500 else ""), style="white")
    
    panel = Panel(
        letter_info,
        title=create_gradient_text(f"Letter #{index + 1}", "purple", "cyan"),
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(panel)

def save_letters_to_file(email, letters, output_dir="letters_output"):
    """Save letters to individual files"""
    import os
    
    try:
        # Create directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        email_safe = email.replace("@", "_at_").replace(".", "_")
        email_dir = os.path.join(output_dir, email_safe)
        
        if not os.path.exists(email_dir):
            os.makedirs(email_dir)
        
        for i, letter in enumerate(letters):
            filename = f"letter_{i+1}_{letter.get('id', 'unknown')[:8]}.txt"
            filepath = os.path.join(email_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"From: {letter.get('sender_name', 'Unknown')} <{letter.get('sender', 'unknown')}>\n")
                f.write(f"Date: {datetime.fromtimestamp(letter.get('date', 0)).strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Subject: {letter.get('subject', 'No Subject')}\n")
                f.write(f"Starred: {'Yes' if letter.get('star') else 'No'}\n")
                f.write(f"\n{'='*80}\n\n")
                f.write(letter.get("letter", {}).get("text", "No content available"))
                f.write(f"\n\n{'='*80}\n\nHTML Content:\n\n")
                f.write(letter.get("letter", {}).get("html", "No HTML content"))
        
        return True, email_dir
    except Exception as e:
        console.print(f"[red]✗ Error saving letters: {e}[/red]")
        return False, None

def save_updated_accounts(results, new_password, output_filename="updated.txt"):
    """Save successfully updated accounts to a file"""
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for result in results:
                if result["success"]:
                    f.write(f"{result['email']}:{new_password}\n")
        return True
    except Exception as e:
        console.print(f"[red]✗ Error saving updated accounts: {e}[/red]")
        return False

def save_all_accounts(results, original_accounts, new_password, output_filename="updated_mail.txt"):
    """Save all accounts with updated passwords for successful ones, keep old for failed"""
    try:
        results_map = {result['email']: result for result in results}
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            for account in original_accounts:
                email = account['email']
                result = results_map.get(email)
                
                if result and result['success']:
                    f.write(f"{email}:{new_password}\n")
                else:
                    f.write(f"{email}:{account['old_password']}\n")
        
        return True
    except Exception as e:
        console.print(f"[red]✗ Error saving updated_mail.txt: {e}[/red]")
        return False

def password_changer_mode(api_key):
    """Execute bulk password changing mode"""
    info_panel = Panel(
        "[cyan]API Key loaded[/cyan]\n"
        "[yellow]Rate limit: 10 requests/second[/yellow]\n"
        "[magenta]Processing: 5 accounts per second[/magenta]",
        title="[bold purple]Password Changer Configuration[/bold purple]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(info_panel)
    console.print()
    
    filename = Prompt.ask("[bold cyan]Enter the path to your email list file[/bold cyan]")
    
    accounts = load_accounts_from_file(filename)
    
    if not accounts:
        console.print("[red]✗ No valid accounts found. Exiting.[/red]")
        return
    
    new_password = Prompt.ask("[bold cyan]Enter the new password for all accounts[/bold cyan]", password=True)
    
    if not new_password:
        console.print("[red]✗ Error: New password cannot be empty![/red]")
        return
    
    console.print(f"\n[yellow]⚠ You are about to change passwords for {len(accounts)} accounts.[/yellow]")
    confirm = Confirm.ask("[bold cyan]Do you want to continue?[/bold cyan]")
    
    if not confirm:
        console.print("[yellow]Operation cancelled.[/yellow]")
        return
    
    console.print()
    
    successful = 0
    failed = 0
    results = []
    batch_size = 5
    
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[bold purple]{task.description}"),
        BarColumn(complete_style="cyan", finished_style="purple"),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Changing passwords...", total=len(accounts))
        
        for i in range(0, len(accounts), batch_size):
            batch = accounts[i:i + batch_size]
            batch_start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_account = {
                    executor.submit(change_password, account["email"], account["old_password"], new_password, api_key): account
                    for account in batch
                }
                
                for future in as_completed(future_to_account):
                    result = future.result()
                    results.append(result)
                    
                    if result["success"]:
                        console.print(f"[green]✓[/green] [{len(results)}/{len(accounts)}] {result['email']}: [green]{result['message']}[/green]")
                        successful += 1
                    else:
                        console.print(f"[red]✗[/red] [{len(results)}/{len(accounts)}] {result['email']}: [red]{result['message']}[/red]")
                        failed += 1
                    
                    progress.update(task, advance=1)
            
            elapsed = time.time() - batch_start_time
            if elapsed < 1.0 and i + batch_size < len(accounts):
                time.sleep(1.0 - elapsed)
    
    console.print()
    
    if successful > 0:
        with console.status("[cyan]Saving updated accounts to 'updated.txt'...", spinner="dots"):
            if save_updated_accounts(results, new_password):
                console.print(f"[green]✓ Successfully saved {successful} updated accounts to 'updated.txt'[/green]")
            else:
                console.print("[red]✗ Failed to save updated accounts file[/red]")
    
    with console.status("[cyan]Saving all processed accounts to 'updated_mail.txt'...", spinner="dots"):
        if save_all_accounts(results, accounts, new_password):
            console.print(f"[green]✓ Successfully saved all {len(accounts)} accounts to 'updated_mail.txt'[/green]")
        else:
            console.print("[red]✗ Failed to save updated_mail.txt file[/red]")
    
    console.print()
    
    table = Table(title=create_gradient_text("Summary", "purple", "cyan"), 
                  box=box.DOUBLE_EDGE, 
                  border_style="purple")
    
    table.add_column("Metric", style="cyan", justify="right")
    table.add_column("Count", style="magenta", justify="center")
    
    table.add_row("Total Processed", str(len(accounts)))
    table.add_row("Successful", f"[green]{successful}[/green]")
    table.add_row("Failed", f"[red]{failed}[/red]")
    
    console.print(table)
    console.print()
    
    files_panel = Panel(
        "[cyan]• updated.txt[/cyan] - Only successful accounts\n"
        "[cyan]• updated_mail.txt[/cyan] - All accounts with current passwords",
        title="[bold purple]Files Created[/bold purple]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(files_panel)

def email_receiver_mode(api_key):
    """Execute email receiving mode"""
    info_panel = Panel(
        "[cyan]API Key loaded[/cyan]\n"
        "[yellow]Rate limit: 10 requests/second[/yellow]\n"
        "[magenta]Fetching emails from accounts[/magenta]",
        title="[bold purple]Email Receiver Configuration[/bold purple]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(info_panel)
    console.print()
    
    filename = Prompt.ask("[bold cyan]Enter the path to your email list file[/bold cyan]")
    
    accounts = load_accounts_from_file(filename)
    
    if not accounts:
        console.print("[red]✗ No valid accounts found. Exiting.[/red]")
        return
    
    # Ask for filters
    use_filters = Confirm.ask("[bold cyan]Do you want to use search filters?[/bold cyan]", default=False)
    
    search_filter = None
    star_filter = None
    
    if use_filters:
        search_filter = Prompt.ask("[bold cyan]Enter search keyword (or press Enter to skip)[/bold cyan]", default="")
        if not search_filter:
            search_filter = None
        
        star_only = Confirm.ask("[bold cyan]Only fetch starred emails?[/bold cyan]", default=False)
        if star_only:
            star_filter = True
    
    save_to_files = Confirm.ask("[bold cyan]Save letters to files?[/bold cyan]", default=True)
    
    console.print()
    
    total_letters = 0
    successful_accounts = 0
    failed_accounts = 0
    
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[bold purple]{task.description}"),
        BarColumn(complete_style="cyan", finished_style="purple"),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Fetching emails...", total=len(accounts))
        
        for account in accounts:
            result = get_letters(account["email"], account["old_password"], search_filter, star_filter, api_key)
            
            if result["success"]:
                console.print(f"[green]✓[/green] {result['email']}: [green]Retrieved {result['count']} letters[/green]")
                successful_accounts += 1
                total_letters += result['count']
                
                if result['count'] > 0:
                    console.print(f"\n[bold cyan]Letters for {result['email']}:[/bold cyan]\n")
                    for i, letter in enumerate(result['letters'][:5]):  # Show first 5
                        display_letter(letter, i)
                    
                    if result['count'] > 5:
                        console.print(f"[yellow]... and {result['count'] - 5} more letters[/yellow]\n")
                    
                    if save_to_files:
                        success, output_dir = save_letters_to_file(result['email'], result['letters'])
                        if success:
                            console.print(f"[green]✓ Saved letters to: {output_dir}[/green]\n")
            else:
                console.print(f"[red]✗[/red] {result['email']}: [red]{result.get('message', 'Unknown error')}[/red]")
                failed_accounts += 1
            
            progress.update(task, advance=1)
            time.sleep(0.2)  # Small delay to respect rate limits
    
    console.print()
    
    table = Table(title=create_gradient_text("Summary", "purple", "cyan"), 
                  box=box.DOUBLE_EDGE, 
                  border_style="purple")
    
    table.add_column("Metric", style="cyan", justify="right")
    table.add_column("Count", style="magenta", justify="center")
    
    table.add_row("Total Accounts", str(len(accounts)))
    table.add_row("Successful", f"[green]{successful_accounts}[/green]")
    table.add_row("Failed", f"[red]{failed_accounts}[/red]")
    table.add_row("Total Letters Retrieved", f"[cyan]{total_letters}[/cyan]")
    
    console.print(table)
    
    if save_to_files and total_letters > 0:
        console.print()
        files_panel = Panel(
            "[cyan]Letters saved to:[/cyan] letters_output/ directory\n"
            "[yellow]Each account has its own subdirectory[/yellow]",
            title="[bold purple]Files Saved[/bold purple]",
            border_style="cyan",
            box=box.ROUNDED
        )
        console.print(files_panel)

def main():
    print_banner()
    
    api_key = "YOUR_API_KEY_HERE"
    
    while True:
        choice = show_main_menu()
        console.print()
        
        if choice == "1":
            password_changer_mode(api_key)
        elif choice == "2":
            email_receiver_mode(api_key)
        elif choice == "3":
            console.print(create_gradient_text("👋 Goodbye!", "purple", "cyan"))
            break
        
        console.print("\n" + "="*60 + "\n")
        
        if choice in ["1", "2"]:
            continue_prompt = Confirm.ask("[bold cyan]Return to main menu?[/bold cyan]", default=True)
            if not continue_prompt:
                console.print(create_gradient_text("👋 Goodbye!", "purple", "cyan"))
                break
            console.print()

if __name__ == "__main__":
    main()
