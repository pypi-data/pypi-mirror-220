from datetime import date, datetime
from typing import Union, List

import pandas as pd
import requests
from py_mini_racer import py_mini_racer

from .constants import trade_days,hk_js_decode


class TradeDate:

    def __init__(self):
        self._trade_days = self._get_trade_days()

    @property
    def trade_days(self) -> List[str]:
        return self._trade_days

    def _get_trade_days(self) -> List[str]:
        if date.today().strftime("%Y-%m-%d") > trade_days[-1]:
            return self._get_trade_date_online()
        else:
            return trade_days

    def _get_trade_date_online(self) -> List[str]:
        url = "https://finance.sina.com.cn/realstock/company/klc_td_sh.txt"
        r = requests.get(url)
        js_code = py_mini_racer.MiniRacer()
        js_code.eval(hk_js_decode)
        dict_list = js_code.call("d", r.text.split("=")[1].split(";")[0].replace('"', ""))
        temp_df = pd.DataFrame(dict_list)
        temp_df.columns = ["trade_date"]
        temp_df["trade_date"] = pd.to_datetime(temp_df["trade_date"]).dt.date
        temp_list = temp_df["trade_date"].to_list()
        # 该日期是交易日，但是在新浪返回的交易日历缺失该日期，这里补充上
        temp_list.append(date(1992, 5, 4))
        temp_list.sort()
        temp_df = pd.DataFrame(temp_list, columns=["trade_date"])
        trade_day = [x.strftime("%Y-%m-%d") for x in temp_df.trade_date.to_list()]
        return trade_day

    def is_trade_date(self, select_day: Union[date, str] = datetime.now().date(), ) -> bool:
        if select_day in self.trade_days or select_day.strftime("%Y-%m-%d") in self.trade_days:
            return True
        else:
            return False
