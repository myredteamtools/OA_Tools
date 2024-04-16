from dataclasses import dataclass
from typing import Optional
import requests

@dataclass
class Target:
    vulnerable_name:Optional[str] = ""
    url: Optional[str] = ""
    proxy: Optional[str] = ""
    session: Optional[requests.Session] = requests.Session()

    def __post_init__(self):
        if self.proxy:
            self.session = requests.Session()
            self.session.proxies = {'http': self.proxy, 'https': self.proxy}
