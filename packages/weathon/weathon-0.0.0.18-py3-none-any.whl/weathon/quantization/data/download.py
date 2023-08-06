from .tick_data import TencentTickDown, SinaTickDown, NetEasyTickDown


def download_tick_data():
    tencent_dwonloader = TencentTickDown()
    sina_downloader = SinaTickDown()
    neteasy_downloader = NetEasyTickDown()

    tencent_dwonloader.run()
    sina_downloader.run()
    neteasy_downloader.run()


if __name__ == '__main__':
    download_tick_data()