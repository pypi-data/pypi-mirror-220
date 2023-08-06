import random
from .header import weibo_header, header_list
from .proxy import IpProxy


headers = random.choice(header_list)
proxy = IpProxy
