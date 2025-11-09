import bcrypt
import getpass
import sys
import os
from time import sleep
from tqdm import tqdm

# Colors
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

# Banner
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{CYAN}
╔══════════════════════════════════╗
║      🔥 Advanced Bcrypt Tool 🔥  ║
╚══════════════════════════════════╝
{RESET}""")

# Function: Generate Bcrypt Hash
def generate_bcrypt_hash():
    password = getpass.getpass(f"{GREEN}Enter a password to hash: {RESET}")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    print(f"\n{YELLOW}Generated Bcrypt Hash:{RESET} {hashed.decode()}")

# Function: Verify Password against Bcrypt Hash
def verify_bcrypt_hash():
    hashed_password = input(f"{GREEN}Enter the bcrypt hash: {RESET}").encode()
    password = getpass.getpass(f"{GREEN}Enter the password to verify: {RESET}")
    try:
        if bcrypt.checkpw(password.encode(), hashed_password):
            print(f"\n{GREEN}✅ Password matches the hash!{RESET}")
        else:
            print(f"\n{RED}❌ Password does not match the hash.{RESET}")
    except Exception as e:
        print(f"{RED}Error: Invalid bcrypt hash format.{RESET}")
        
        
# Function: Brute Force Bcrypt Hash
def bcrypt_brute_force():
    hashed_password = input(f"{GREEN}Enter the bcrypt hash: {RESET}")
    wordlist_path = input(f"{GREEN}Enter the path to your wordlist: {RESET}")

    # Fix $2y$ to $2b$
    if hashed_password.startswith("$2y$"):
        hashed_password = "$2b$" + hashed_password[4:]
    hashed_password = hashed_password.encode()

    if not os.path.isfile(wordlist_path):
        print(f"{RED}Wordlist file not found!{RESET}")
        return

    print(f"{BLUE}Starting Brute Force...{RESET}")
    sleep(1)
    try:
        with open(wordlist_path, "r", encoding="latin-1") as wordlist:
            passwords = [line.strip() for line in wordlist.readlines()]

        for password in tqdm(passwords, desc="🔍 Attempting", unit="password"):
            try:
                if bcrypt.checkpw(password.encode(), hashed_password):
                    print(f"\n{GREEN}🎯 Password found: {password}{RESET}")
                    return
            except ValueError:
                print(f"\n{RED}Invalid bcrypt hash format provided.{RESET}")
                return

        print(f"\n{RED}❌ Password not found in the wordlist.{RESET}")
    except Exception as e:
        print(f"{RED}Error during brute-force: {e}{RESET}")

# Function: Help Menu
def help_menu():
    print(f"""{BLUE}
[1] Generate Random Bcrypt Hash
[2] Verify Password against Bcrypt Hash
[3] Brute Force a Bcrypt Hash (Wordlist Attack)
[4] Help
[5] Exit
{RESET}""")

# Main Menu
def main():
    while True:
        banner()
        help_menu()
        choice = input(f"{CYAN}Choose an option (1-5): {RESET}")

        if choice == '1':
            generate_bcrypt_hash()
        elif choice == '2':
            verify_bcrypt_hash()
        elif choice == '3':
            bcrypt_brute_force()
        elif choice == '4':
            help_menu()
        elif choice == '5':
            print(f"{YELLOW}Exiting... Stay safe! 👋{RESET}")
            sys.exit()
        else:
            print(f"{RED}Invalid option. Please select a valid choice.{RESET}")

        input(f"\n{CYAN}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main()
