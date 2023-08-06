from datetime import datetime
from time import sleep

from weathon.quantization.base.tick_down import TickDown
from weathon.utils.logger import get_logger


class SinaTickDown(TickDown):
    # 列名tuple
    clname = ("code", "name", "open", "close", "now", "high", "low", "buy", "sell", "turnover", "volume", "bid1_volume",
              "bid1", "bid2_volume", "bid2", "bid3_volume", "bid3", "bid4_volume", "bid4", "bid5_volume", "bid5",
              "ask1_volume", "ask1", "ask2_volume", "ask2", "ask3_volume", "ask3", "ask4_volume", "ask4", "ask5_volume",
              "ask5",
              "datetime")
    tick_source = "sina"
    stock_api = 'http://hq.sinajs.cn/list={params}'
    logger = get_logger("SinaTickDown")


    @staticmethod
    def formatdata(rep_data: list) -> tuple:
        """
        将取得的数据格式化后以生成器返回
        :param rep_data: 取得的数据
        :return: 生成器的数据
        """
        stocks_detail = "".join(rep_data).split(";")
        for stocki in stocks_detail:
            stock = stocki.split(",")
            if len(stock) <= 30:
                continue
            stockcodenam = stock[0].split("=")
            yield (stockcodenam[0][-8:], stockcodenam[1].replace('"', ''), stock[1], stock[2], stock[3], stock[4],
                   stock[5], stock[6], stock[7], stock[8], stock[9], stock[10], stock[11], stock[12], stock[13],
                   stock[14], stock[15], stock[16], stock[17], stock[18], stock[19], stock[20], stock[21], stock[22],
                   stock[23], stock[24], stock[25], stock[26], stock[27], stock[28], stock[29],
                   str(stock[30]) + " " + str(stock[31]))

    def run(self):
        self.check_file()  # 创建下载文件
        while True:
            t1 = datetime.now()
            if self.stock_a_hour(t1):  # 判断A股时间段
                try:
                    stk_data = self.formatdata(self.tick_dl(if_thread=True))  # 下载数据
                    t3 = datetime.now()
                    write_cnt = self.save_tick_data(stk_data, "%Y-%m-%d %H:%M:%S")
                    t4 = datetime.now()
                    self.logger.info(f"localtime: {t4} all:{t4 - t1} tocsv:{t4 - t3} download:{t3 - t1} cnt:{write_cnt}")
                except Exception as error_downdata:
                    self.logger.error(f"error_downdata: {error_downdata}")
            elif datetime.now() > self.trd_hour_end_afternoon:  # 下午3：02退出循环
                self.logger.info("download complete -> %s" % self.today_csv_path)
                break
            else:
                self.logger.info("relax 10s , localtime: %s" % datetime.now())  # 未退出前休息
                sleep(10)

        self.send_message(f"下载{self.tick_source}数据 -> 完成")  # 发送完成消息


