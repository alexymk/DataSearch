import os
import sys
import time
from colorama import Fore, Style, init
import subprocess

init(autoreset=True)

VERSION = "2.3.5"
COPYRIGHT = "Tool Created by alex.ymk (auto-dex.fr)"
CONFIG_FILE = "config.txt"

def display_logo():
    """Affiche le logo, la version et le copyright."""
    logo = r"""
________          __           _________                           .__     
\______ \ _____ _/  |______   /   _____/ ____ _____ _______   ____ |  |__  
 |    |  \\__  \\   __\__  \  \_____  \_/ __ \\__  \\_  __ \_/ ___\|  |  \ 
 |    `   \/ __ \|  |  / __ \_/        \  ___/ / __ \|  | \/\  \___|   Y  \
/_______  (____  /__| (____  /_______  /\___  >____  /__|    \___  >___|  /
        \/     \/          \/        \/     \/     \/            \/     \/ 
"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.YELLOW + logo)
    print(Fore.RED + f"                                                            Version: {VERSION}")
    print(Fore.GREEN + "[" + Fore.WHITE + "-" + Fore.GREEN + "] " + Fore.CYAN + COPYRIGHT)
    print("")

def install_libraries():
    """Installe les bibliothèques nécessaires via pip."""
    libraries = ["colorama"]
    print(Fore.GREEN + "[INFO] Installing required libraries...")
    for lib in libraries:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(Fore.GREEN + f"[INFO] {lib} installed successfully!")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Could not install {lib}: {e}")
            sys.exit(1)

def setup_database_path():
    """Demande à l'utilisateur le chemin de la base de données et le sauvegarde dans un fichier de configuration."""
    while True:
        db_path = input(Fore.GREEN + "[" + Fore.WHITE + "-" + Fore.GREEN + "] " + Fore.CYAN + "Enter the path to your database folder: ").strip()
        if os.path.exists(db_path) and os.path.isdir(db_path):
            with open(CONFIG_FILE, "w") as f:
                f.write(f"DB_PATH={db_path}")
            print(Fore.GREEN + f"[INFO] Database path saved in {CONFIG_FILE}.")
            break
        else:
            print(Fore.RED + "[ERROR] Invalid path. Please enter a valid folder path.")

def main():
    install_libraries()

    display_logo()

    setup_database_path()

    print(Fore.GREEN + "[INFO] Setup completed successfully!")
    time.sleep(1)

if __name__ == "__main__":
    main()
