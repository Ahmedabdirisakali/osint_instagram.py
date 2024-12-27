import os
import re
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style

# Console object for rich
console = Console()

# Intro oo Quruxsan
def show_intro():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + "=" * 60)
    print(Fore.GREEN + "Welcome to the Advanced Instagram OSINT Tool".center(60))
    print(Fore.YELLOW + "Created by Ahmed Abdirisak Ali".center(60))
    print(Fore.MAGENTA + "For Educational Purposes Only".center(60))
    print(Fore.RED + "Warning: Unauthorized use is prohibited!".center(60))
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL)

# Function si loogu diro codsi Instagram username
def get_followers_info(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            description = meta_tag.attrs['content']
            parts = description.split("-")[0].strip().split(",")
            followers = parts[0].strip()
            following = parts[1].strip()
            posts = parts[2].strip()
            bio = description.split("-")[1].strip()

            # Extract emails and phone numbers
            emails, phone_numbers = extract_emails_and_numbers(description)

            # Display data as a table
            display_data_as_table(username, followers, following, posts, bio, emails, phone_numbers)
        else:
            print(Fore.RED + "Couldn't find followers or data for this user." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Error: Couldn't fetch the profile. Check the username." + Style.RESET_ALL)

# Function to extract emails and phone numbers
def extract_emails_and_numbers(text):
    # Regex for emails, including [at] and [dot] cases
    email_pattern = r'[a-zA-Z0-9._%+-]+(?:\[at\]|\@)[a-zA-Z0-9.-]+(?:\[dot\]|\.)[a-zA-Z]{2,}'
    # Regex for phone numbers, allowing various formats
    phone_pattern = r'(\+?[0-9]{1,3})?[\s\-.\(\)]?(\(?\d{1,4}\)?[\s\-.\)]?)?\d{3}[\s\-.\)]?\d{3}[\s\-.\)]?\d{4}'
    
    # Find all matches
    emails = re.findall(email_pattern, text)
    phone_numbers = re.findall(phone_pattern, text)
    
    # Clean up phone numbers (remove unnecessary characters)
    phone_numbers = [''.join(number) for number in phone_numbers]

    # Convert emails with [at] and [dot] back to normal format
    emails = [email.replace("[at]", "@").replace("[dot]", ".") for email in emails]
    
    return emails, phone_numbers

# Function to display data as a table
def display_data_as_table(username, followers, following, posts, bio, emails, phone_numbers):
    table = Table(title="Instagram OSINT Data", style="cyan")
    
    table.add_column("Field", style="green", justify="left")
    table.add_column("Data", style="magenta", justify="left")
    
    table.add_row("Username", username)
    table.add_row("Followers", followers)
    table.add_row("Following", following)
    table.add_row("Posts", posts)
    table.add_row("Bio", bio)
    table.add_row("Emails", ", ".join(emails) if emails else "Not found")
    table.add_row("Phone Numbers", ", ".join(phone_numbers) if phone_numbers else "Not found")
    
    # Display the table
    console.print(table)

# Function si loogu login user iyo password
def login_tool():
    print(Fore.YELLOW + "\nPlease login to access the OSINT tool." + Style.RESET_ALL)
    username = input(Fore.BLUE + "Enter your Instagram username: " + Style.RESET_ALL)
    password = input(Fore.BLUE + "Enter your Instagram password: " + Style.RESET_ALL)

    # Validate login (dummy validation for now)
    if username and password:
        print(Fore.GREEN + "Login successful!" + Style.RESET_ALL)
        return True
    else:
        print(Fore.RED + "Login failed. Please try again." + Style.RESET_ALL)
        return False

# Main Function
def main():
    show_intro()

    if login_tool():
        target_username = input(Fore.MAGENTA + "\nEnter the target username to investigate: " + Style.RESET_ALL)
        get_followers_info(target_username)
    else:
        print(Fore.RED + "Exiting tool..." + Style.RESET_ALL)

# Run the tool
if __name__ == "__main__":
    main()

