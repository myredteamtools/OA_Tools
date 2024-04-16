from Scanner.Scanner import Scanner
from model.model import Target
from typing import List


Product = 0
Thread:int = 5
def mainmenu() -> None:
    try:
        global Product
        Product = input("OA_Tools:\n[1]\tUfida\n[2]\tEcology\n\n\nInput:")
        Selector(Product)
    except KeyboardInterrupt:
        print("KeyBoard Interrupted!!")

def Selector(flag) -> None:
    global Product
    Options = input("Options:\n[1]\tSingle_URL\n[2]\tMulti URL\n[Others]\tMain Menu\n\n\nInput:  ")
    print(Options)
    if Options == "1":
        url = input("URL:")
        proxy = input("HTTP Proxy[Optional]: ")
        target = Target(url=url,proxy=proxy)
        Instance = Scanner(target=target,flag=flag)
        Single_Check(Instance=Instance,target=target)
    elif Options == "2":
        input_path = input("Input_path:   ")
        output_path = input("Output_path[Optional]:   ")
        proxy = input("HTTP Proxy[Optional]:")
        target = Target(url="",proxy=proxy)
        Instance = Scanner(target=target, flag=flag)
        Multi_Check(target=target,Instance=Instance,input_path=input_path,output_path=output_path)
        
    return


def Single_Check(Instance,target) -> None:
    try:
        Options = input(f"Target:{target.url}\nProxy:{target.proxy}\n[1]\tCheck\n[2]\tInactiveshell\n[3]\tUpload_Webshell\n[Other]\tMain Menu\n\n\nInput:   ")
        if Options == "1":
            Instance.check_single_url(url=target.url)
            Single_Check(Instance,target)
        elif Options == "2":
            Instance.interactive_shell()
            Single_Check(Instance,target)
        elif Options == "3":
            file_path = input("File_Path:  ")
            Instance.upload_webshell(target=target,file_path=file_path)
            Single_Check(Instance,target)
        else:
            mainmenu()
    except KeyboardInterrupt:
        print("KeyBoard Interrupted!!")


def Multi_Check(target,Instance,input_path,output_path) -> None:
    try:
        global Thread
        Options = input(f"Proxy:{target.proxy}\nTargets:\n[1]\tStart Scan\n[2]\tSet Threads: [{Thread}]\n[3]\tSet Proxy\n[Others]\tMain Menu\n\n\nInput:   ")
        if Options == "1":
            with open (input_path,"r") as f:
                myurls:List[str] = f.read().splitlines()
            Instance.check_multi_urls(urls=myurls,max_workers=Thread,output_path=output_path)
            Multi_Check(target,Instance,input_path,output_path)
        elif Options == "2":
            Thread = int(input("Set Threads:"))
            Multi_Check(target,Instance,input_path,output_path)
        elif Options == "3":
            target.proxy = input("Set Your Proxy:")
            Multi_Check(target,Instance,input_path,output_path)
        else:
            mainmenu()
    except KeyboardInterrupt:
        print("KeyBoard Interrupted!!")
    

def main() -> None:
    mainmenu()

    
if __name__ == "__main__":
    main()


