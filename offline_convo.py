import requests
import time
import os
import sqlite3
from colorama import init, Fore, Style

init(autoreset=True)

# Initialize database
DB_NAME = "offline_database.db"

def initialize_database():
    """Initialize the SQLite database and create tables if not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hater_name TEXT,
            target_id TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message_to_database(hater_name, target_id, message):
    """Save a sent message to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = time.strftime("%Y-%m-%d %I:%M:%S %p")
    cursor.execute("INSERT INTO messages (hater_name, target_id, message, timestamp) VALUES (?, ?, ?, ?)",
                   (hater_name, target_id, message, timestamp))
    conn.commit()
    conn.close()

def fetch_messages_from_database():
    """Fetch all messages from the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return messages

def approval():
    """Clear the terminal screen."""
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux/macOS
        os.system('clear')

def raj_logo():
    """Display the logo and clear the screen after displaying it."""
    logo = r"""
    
\033[1;33m/$$      /$$ /$$$$$$$     
\033[1;32m| $$$    /$$$| $$__  $$    
\033[1;36m| $$$$  /$$$$| $$  \ $$    
\033[1;36m| $$ $$/$$ $$| $$$$$$$/    
\033[1;33m| $$  $$$| $$| $$__  $$    
\033[1;35m| $$\  $ | $$| $$  \ $$    
\033[1;34m| $$ \/  | $$| $$  | $$ /$$\ 
\033[1;37m|__/     |__/|__/  |__/ |__/    
    
    
           \033[1;36m$$$$$$$\   $$$$$$\     $$$$$\ 
           \033[1;36m$$  __$$\ $$  __$$\    \__$$ |
           \033[1;34m$$ |  $$ |$$ /  $$ |      $$ |
           \033[1;34m$$$$$$$  |$$$$$$$$ |      $$ |
           \033[1;36m$$  __$$< $$  __$$ |$$\   $$ |
           \033[1;32m$$ |  $$ |$$ |  $$ |$$ |  $$ |
           \033[1;33m$$ |  $$ |$$ |  $$ |\$$$$$$  |
           \033[1;33m\__|  \__|\__|  \__| \______/ 
"""
    print(Fore.MAGENTA + Style.BRIGHT + logo)

def show_termux_message():
    """Display the custom message after the logo."""
    termux_message = r"""
╔═════════════════════════════════════════════════════════════╗
║  \033[1;31mN4M3       : MR RAJ THAK9R                   
║  \033[1;32mRULL3X     : UP FIRE RUL3X
║  \033[1;32mRULL3X     : UP FIRE RUL3X
║  \033[1;34mBR9ND      : MR D R9J  H3R3
║  \033[1;37mGitHub     : https://github.com/Raj-Thakur420
║  \033[1;32mWH9TS9P    : +994 405322645
╚═════════════════════════════════════════════════════════════╝
"""
    print(Fore.GREEN + Style.BRIGHT + termux_message)

def send_messages(tokens_file, target_id, messages_file, haters_name, speed):
    """Send messages to the target profile."""
    with open(messages_file, "r") as file:
        messages = file.readlines()

    while True:
        for message_index, message in enumerate(messages):
            full_message = f"{haters_name} {message.strip()}"
            save_message_to_database(haters_name, target_id, full_message)  # Save to database

            current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
            print(Fore.GREEN + f"\n┌────────────────────────────────────────────────────────────────────┐")
            print(Fore.CYAN + f"[✔] {Fore.YELLOW}Message {message_index + 1} Saved to Database!")
            print(Fore.CYAN + f"[📩] Target: {Fore.MAGENTA}{target_id}")
            print(Fore.CYAN + f"[📨] Message: {Fore.LIGHTGREEN_EX}{full_message}")
            print(Fore.CYAN + f"[⏰] Time: {Fore.LIGHTBLUE_EX}{current_time}")
            print(Fore.GREEN + f"└────────────────────────────────────────────────────────────────────┘\n")
            time.sleep(speed)

def main():
    approval()  # Clear screen before displaying the logo
    raj_logo()  # Display logo
    show_termux_message()  # Show the custom message

    # Initialize the SQLite database
    initialize_database()

    approval()  # Clear screen before starting inputs
    tokens_file = input(Fore.GREEN + "[+] ENTER-THE-TOKENS-FILE=>> ").strip()

    approval()  # Clear screen before further inputs
    target_id = input(Fore.YELLOW + "[+] ENTER-THE-TARGET-ID=>> ").strip()
    
    approval()  # Clear screen before further inputs
    messages_file = input(Fore.YELLOW + "[+] ENTER-----GALI-FILE=>> ").strip()

    approval()  # Clear screen before further inputs
    haters_name = input(Fore.YELLOW + "[+] ENTER-HATER-NAME=>> ").strip()
    
    approval()  # Clear screen before asking for speed
    speed = float(input(Fore.GREEN + "[+] ENTER THE SPEED (IN SECONDS) BETWEEN MESSAGES=>> ").strip())

    send_messages(tokens_file, target_id, messages_file, haters_name, speed)

if __name__ == "__main__":
    main()
