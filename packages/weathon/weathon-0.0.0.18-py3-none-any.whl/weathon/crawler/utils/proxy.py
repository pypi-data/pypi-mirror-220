from typing import Dict

import requests
from .constants import PROXY_WEB_URL


class IpProxy:

    def __init__(self):
        self.check_count = None
        self.source = None
        self.https = None
        self.ip_port = None
        self.region = None
        self.last_time = None
        self.last_status = None
        self.proxy_url = PROXY_WEB_URL

    def all(self):
        return requests.get(f"{self.proxy_url}/all").json()

    def count(self):
        count_detail = requests.get(f"{self.proxy_url}/count").json()
        return count_detail.get('count', 0)

    def set(self, proxy_dict):
        self.ip_port = proxy_dict.get('proxy', '127.0.0.1:80')
        self.region = proxy_dict.get('region', '')
        self.last_time = proxy_dict.get('last_time', '')
        self.last_status = proxy_dict.get('last_status', False)
        self.https = proxy_dict.get('https', False)
        self.source = proxy_dict.get('source', '')
        self.check_count = proxy_dict.get('check_count', 0)
        
    def pop(self):
        self.set(requests.get(f"{self.proxy_url}/pop/").json())
        return {"https": f"https://{self.ip_port}"} if self.https else {"http": f"http://{self.ip_port}"}

    def get_proxy(self):
        self.set(requests.get(f"{self.proxy_url}/get/").json())
        return {"https": f"https://{self.ip_port}"} if self.https else {"http": f"http://{self.ip_port}"}

    def delete_proxy(self):
        if not self.ip_port == '127.0.0.1:80':
            requests.get(f"{self.proxy_url}/delete/?proxy={self.ip_port}")
