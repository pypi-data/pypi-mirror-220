from typing import List, Set

import requests

from weathon.crawler.utils.proxy import IpProxy
from .constants import stock_codes
from .stock_utils import get_stock_type


class StockCode:

    def __init__(self):
        self.ip_proxy = IpProxy()
        self._stock_codes = self._merge_stock_codes()

    @property
    def codes(self) -> Set[str]:
        return self._stock_codes

    def add(self, code: str):
        self._stock_codes.add(code)

    def _merge_stock_codes(self)-> Set[str]:
        stock_codes = []
        stock_codes += self.stock_codes_from_local()
        stock_codes += self.stock_codes_astock()
        return set(stock_codes)

    def stock_codes_astock(self) -> List[str]:
        """
        从散户大家庭获取股票代码列表
        """
        response = requests.get("http://www.shdjt.com/js/lib/astock.js")

        if not response.status_code == 200:
            response = requests.get("http://www.shdjt.com/js/lib/astock.js", proxies=self.ip_proxy.get_proxy())

        all_text = response.text.replace('var astock_suggest="~', '')
        stock_list = list(
            set([get_stock_type(i.split("`")[0]) for i in all_text.split("~") if not i.startswith('zz')]))
        return [i for i in stock_list if i is not None and i != '']

    def stock_codes_from_local(self):
        return stock_codes

