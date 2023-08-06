import unittest

from weathon.quantization.utils.stock_codes import StockCode


class TestStockCodes(unittest.TestCase):

    def setup(self):
        self.stock_code = StockCode()

    def tearDown(self):
        pass

    def test_codes(self):
        stock_code = StockCode()
        print(stock_code.codes)


if __name__ == '__main__':
    unittest.main()
