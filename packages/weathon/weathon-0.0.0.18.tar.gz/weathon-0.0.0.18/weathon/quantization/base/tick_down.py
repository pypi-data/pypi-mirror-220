import os
import shutil
import sys
from abc import ABCMeta, abstractmethod
from datetime import date, datetime, time
from multiprocessing.pool import ThreadPool

import pandas as pd
import requests
from func_timeout import func_timeout, FunctionTimedOut

from weathon.quantization.utils.stock_codes import StockCode
from weathon.quantization.utils.trade_date import TradeDate

from weathon.utils import ensure_directory, send_message


class TickDown(metaclass=ABCMeta):
    clname = None
    tick_source = ""
    stock_api = ""

    def __init__(self,
                 max_num=800,
                 timeout=1,
                 thread_cnt=3,
                 save_path="/Users/lizhen/PycharmProjects/weathon/data",
                 msg_callback=send_message,
                 stock_list=None,
                 trade_date_bypass: bool = False):
        """
        tick下载基类
        :param max_num: 单次请求的股票数量
        :param timeout: 单次请求超时时间
        :param thread_cnt: 请求线程数
        :param save_path: tick csv保存路径
        :param msg_callback: 发送信息的callback function
        :param stock_list:自定义股票清单
        :param trade_date_bypass: 旁通交易日历,即不判断交易日历
        """

        self.request_session = requests.session()
        self.msg_callback = msg_callback
        self.max_num = max_num
        self.timeout = timeout
        self.thread_cnt = min(thread_cnt, 8)

        # 交易日期
        self.trade_date = TradeDate()

        # 交易代码
        self.stock_codes = StockCode()

        # 股票清单
        self.stock_list = [] if stock_list else list(self.stock_codes.codes)
        self.stocklist()

        # 时间部分信息
        self.current_day = date.today()
        self.trd_hour_start_morning = datetime.combine(self.current_day, time(9, 8))
        self.trd_hour_end_morning = datetime.combine(self.current_day, time(11, 32))

        self.trd_hour_start_afternoon = datetime.combine(self.current_day, time(12, 58))
        self.trd_hour_end_afternoon = datetime.combine(self.current_day, time(15, 2))

        # csv文件名称
        self.today_csv_name = f"{self.current_day}-{self.tick_source}-tick.csv"
        self.today_csv_path = os.path.join(save_path, self.today_csv_name)

        # 压缩文件名称
        self.today_7z_name = f"{self.current_day}-{self.tick_source}-tick.7z"
        self.today_7z_path = os.path.join(save_path, self.today_7z_name)
        print(f"file save path: {save_path}")
        # run before

        self.if_trade(trade_date_bypass=trade_date_bypass)
        # 发送启动信息
        self.send_message(f"下载{self.tick_source}数据 -> 启动")  # 发送启动消息

    def compress(self, zip_loc='7za', password='1234'):
        """7z压缩"""
        os.system(f"""{zip_loc} a -t7z {self.today_7z_path} {self.today_csv_path} -p{password}""")

    def move_to_path(self, path):
        """移动到数据文件目录去"""
        ensure_directory(path)
        shutil.move(self.today_csv_path, os.path.join(path, self.today_csv_name))
        if os.path.exists(self.today_7z_path):
            shutil.move(self.today_7z_path, os.path.join(path, self.today_7z_name))

    def stocklist(self):
        """查询所有方法获取到股票清单"""

        self.stock_code = [",".join(self.stock_list[i: i + self.max_num]) for i in
                           range(0, len(self.stock_list) + 1, self.max_num)]

        self.stock_code = list(filter(lambda x: x and x != '', self.stock_code)) # 过滤

        self.stktime = {stki: datetime.now() for stki in self.stock_list}  # 用于时间去重的字典生成式

    def get_stock_batch(self, params):
        try:
            from weathon.crawler.utils import headers
            response = self.request_session.get(self.stock_api.format(params=params), headers=headers)
        except Exception as e:
            from weathon.crawler.utils import headers, proxy
            response = self.request_session.get(self.stock_api.format(params), headers=headers, proxies=proxy.get_proxy())
        return response

    def get_stocks_by_range(self, params):
        try:
            r = func_timeout(self.timeout, self.get_stock_batch, args=(params,))
            return r.text
        except FunctionTimedOut:
            print("batch timeout,localtime:%s" % datetime.now())
            return ''
        except Exception as e:
            print("something wrong,tell author please\n", e)
            return ''

    def tick_dl(self, if_thread=False):
        if if_thread:
            pool = ThreadPool(self.thread_cnt)
            try:
                res = pool.map(self.get_stocks_by_range, self.stock_code)
            finally:
                pool.close()
            return [d for d in res if d is not None]
        else:
            return [self.get_stocks_by_range(param) for param in self.stock_code]

    def send_message(self, msg):
        if self.msg_callback:
            self.msg_callback(title=f"tick data download start", content=msg)

    def check_file(self):
        if not os.path.exists(self.today_csv_path):
            # 如果没有这个文件，则创建这个文件并写入列名
            with open(self.today_csv_path, mode='w') as file_today:
                file_today.writelines(",".join(self.clname))
                file_today.write("\n")

    def stock_a_hour(self, current_time=datetime.now()) -> bool:
        """A股时间段判断
        :param current_time:当前时间的时间戳，eg：time.time() 或者 datetime.now().timestamp()
        """
        return (self.trd_hour_start_morning <= current_time <= self.trd_hour_end_morning) or \
            (self.trd_hour_start_afternoon <= current_time <= self.trd_hour_end_afternoon)

    def if_trade(self, selectday: date = datetime.now().date(), trade_date_bypass: bool = False):
        """判断当日是否交易日"""
        if trade_date_bypass:
            print("bypass 交易日历检查")
            return
        try:
            if self.trade_date.is_trade_date(selectday):
                print("%s 交易日,运行程序" % datetime.now().date())
            else:
                print("%s 非交易日,退出" % datetime.now().date())
                sys.exit(0)
        except Exception as err:
            print("获取akshare的交易日历失败：", err)
            self.send_message(f"获取akshare的交易日历失败,下载程序继续启动:{err}"[:50])

    def save_tick_data(self, stk_data, fmt_str:str) -> int:
        datas = []
        for stki in stk_data:
            if len(stki[31]) > 15:
                data_now_time = datetime.strptime(stki[31], fmt_str)
                if data_now_time > self.stktime[stki[0]]:  # 判断该股票的时间大于已经写入的时间
                    datas.append({key: val for key, val in zip(self.clname, stki)})
                    self.stktime[stki[0]] = data_now_time
        data_pd = pd.DataFrame(datas)
        data_pd.to_csv(self.today_csv_path, mode='a', header=False, index=False)
        return len(data_pd)
    @abstractmethod
    def formatdata(rep_data):
        pass

    @abstractmethod
    def run(self):
        self.check_file()
        pass
