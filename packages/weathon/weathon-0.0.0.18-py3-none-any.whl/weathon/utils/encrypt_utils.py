# -*- coding: utf-8 -*-
# @Time    : 2022/10/3 00:15
# @Author  : LiZhen
# @FileName: encrypt_utils.py
# @github  : https://github.com/Lizhen0628
# @Description:

from hashlib import md5


class Encrypter:
    """
    加密工具类
    """
    def __init__(self, instr:str, salt:str="CMyMxC4rHv"):
        self.instr = instr
        self.salt = salt

    def encrypt(self,type='md5') -> str:
        if type in ['md5']:
            return self._md5()
        else:
            return self.instr




    def _md5(self) -> str:
        """
        输入 字符串，对字符串采用md5算法加密，
        :param in_str:  需要加密的字符串
        :param salt:  盐，防止被撞库
        :return:  对字符串加密后的结果
        """
        obj = md5(self.salt.encode("utf8"))
        obj.update(self.instr.encode("utf8"))
        return obj.hexdigest()
