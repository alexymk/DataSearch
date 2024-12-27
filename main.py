import os
import time
import sys
from colorama import Fore, Style, init

init(autoreset=True)

CONFIG_FILE = "config.txt"

PREDEFINED_PATH = ""

def load_config():
    """
    Charge le chemin des bases de données à partir du fichier de configuration.
    """
    global PREDEFINED_PATH
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                for line in f:
                    if line.startswith("DB_PATH="):
                        PREDEFINED_PATH = line.split("=", 1)[1].strip()
                        if not os.path.exists(PREDEFINED_PATH):
                            raise ValueError(f"Invalid path in config: {PREDEFINED_PATH}")
                        return
        raise FileNotFoundError(f"{CONFIG_FILE} not found. Please run 'setup.py' first.")
    except Exception as e:
        print(Fore.RED + f"[ERROR] {e}")
        sys.exit(1)

load_config()

def reveal_lines(lines, delay=0.1):
    """
    Affiche les lignes une par une avec un effet de révélation de haut en bas, avec style et couleur.

    :param lines: Liste de chaînes à afficher.
    :param delay: Temps (en secondes) entre l'affichage de chaque ligne.
    """
    os.system('clear' if os.name == 'posix' else 'cls')
    for line in lines:
        print(Fore.YELLOW + Style.BRIGHT + line, flush=True)
        time.sleep(delay)

def list_subdirectories(path):
    """
    Liste les sous-dossiers dans un chemin donné.

    :param path: Chemin du dossier parent.
    :return: Liste des sous-dossiers.
    """
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def search_in_files(directory, search_term, extensions):
    """
    Recherche un terme dans les fichiers d'un dossier donné.

    :param directory: Chemin du dossier où chercher.
    :param search_term: Terme à rechercher.
    :param extensions: Extensions de fichiers à analyser.
    :return: Liste des fichiers contenant le terme.
    """
    matches = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if search_term in f.read():
                            matches.append(file_path)
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='ISO-8859-1') as f:
                            if search_term in f.read():
                                matches.append(file_path)
                    except Exception as e:
                        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
    return matches

def ask_to_continue():
    """
    Demande à l'utilisateur s'il souhaite continuer avec l'option Y/n sans avoir à appuyer sur Entrée.
    """
    if sys.platform == "win32":
        import msvcrt
        while True:
            print(Fore.RED + "[" + Fore.WHITE + "-" + Fore.RED + "]" + Fore.CYAN + " Do you want to continue? (Y/n): ", end="", flush=True)
            choice = msvcrt.getch().decode("utf-8").lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                return False
            else:
                print("\n" + Fore.RED + "[" + Fore.WHITE + "!" + Fore.RED + "] Invalid input, please press Y or n.")
    else:
        import tty
        import termios
        while True:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                print("\n" + Fore.RED + "[" + Fore.WHITE + "-" + Fore.RED + "]" + Fore.CYAN + " Do you want to continue? (Y/n): ")
                choice = sys.stdin.read(1).lower()
                if choice == 'y':
                    return True
                elif choice == 'n':
                    return False
                else:
                    print(Fore.RED + "[" + Fore.WHITE + "!" + Fore.RED + "] Invalid input, please press Y or n.")
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    while True:
        text = r"""
________          __           _________                           .__     
\______ \ _____ _/  |______   /   _____/ ____ _____ _______   ____ |  |__  
 |    |  \\__  \\   __\__  \  \_____  \_/ __ \\__  \\_  __ \_/ ___\|  |  \ 
 |    `   \/ __ \|  |  / __ \_/        \  ___/ / __ \|  | \/\  \___|   Y  \
/_______  (____  /__| (____  /_______  /\___  >____  /__|    \___  >___|  /
        \/     \/          \/        \/     \/     \/            \/     \/ 
"""
        lines = text.split("\n")
        reveal_lines(lines, delay=0.060)

        print(Fore.RED + "                                                            Version : 2.3.5")

        print("")

        print(Fore.GREEN + "[" + Fore.WHITE + "-" + Fore.GREEN + "]" + Fore.CYAN + " Tool Created by figwix (figwix.eu)")

        print("")

        print(Fore.RED + "[" + Fore.WHITE + "::" + Fore.RED + "]" + Fore.YELLOW + " Select An Available Folder " + Fore.RED + "[" + Fore.WHITE + "::" + Fore.RED + "]" + Fore.WHITE)

        print("")

        subdirs = list_subdirectories(PREDEFINED_PATH)
        if not subdirs:
            print(Fore.RED + "[" + Fore.WHITE + "!" + Fore.RED + "] No subfolders found, Try Later..." + Fore.WHITE)
            print("")
            continue

        for i, subdir in enumerate(subdirs, start=1):
            print(Fore.RED + "[" + Fore.WHITE + f"{str(i).zfill(2)}" + Fore.RED + "]" + Fore.YELLOW + f" {subdir}" + Fore.WHITE)

        print("\n" + Fore.RED + "[" + Fore.WHITE + "00" + Fore.RED + "]" + Fore.YELLOW + " Exit " + Fore.WHITE)
        print("")

        while True:
            try:
                choice = input(Fore.RED + "[" + Fore.WHITE + "-" + Fore.RED + "]" + Fore.GREEN + " Select an option : " + Fore.BLUE).strip()
                print("")
                if choice.isdigit() and int(choice) == 0:
                    print(Fore.RED + "[" + Fore.WHITE + "::" + Fore.RED + "] Exiting the program...")
                    return
                elif choice.isdigit() and 1 <= int(choice) <= len(subdirs):
                    selected_dir = os.path.join(PREDEFINED_PATH, subdirs[int(choice)-1])
                    break
                else:
                    print(Fore.RED + "[" + Fore.WHITE + "!" + Fore.RED + "] Invalid Option, Try Again..." + Fore.WHITE)
                    print("")
            except Exception as e:
                print(Fore.RED + "[" + Fore.WHITE + "!" + Fore.RED + "] Error: " + str(e))
                time.sleep(1)
                continue

        while True:
            try:
                search_term = input(Fore.RED + "[" + Fore.WHITE + "-" + Fore.RED + "]" + Fore.GREEN + " Search Term : " + Fore.BLUE).strip()
                print("")
                if not search_term:
                    print(Fore.RED + "[" + Fore.WHITE + "!" + Fore.RED + "] Invalid Search, Try Again..." + Fore.WHITE)
                    print("")
                    continue
                break
            except Exception as e:
                print(Fore.RED + "[" + Fore.WHITE + "!" + Fore.RED + "] Error: " + str(e))
                time.sleep(1)
                continue

        extensions = ('.txt', '.sql', '.csv')
        matches = search_in_files(selected_dir, search_term, extensions)

        if matches:
            print(Fore.RED + "[" + Fore.WHITE + "::" + Fore.RED + "]" + Fore.GREEN + " Files containing the term '" + Style.BRIGHT + f"{search_term}" + Style.NORMAL + "' " + Fore.RED + "[" + Fore.WHITE + "::" + Fore.RED + "]")
            for match in matches:
                print(Fore.GREEN + match)
        else:
            print(Fore.RED + "[" + Fore.WHITE + "!" + Fore.RED + "] No file contains the term '" + Style.BRIGHT + f"{search_term}" + Style.NORMAL + "'" + Fore.WHITE)

        if not ask_to_continue():
            break

if __name__ == "__main__":
    main()
