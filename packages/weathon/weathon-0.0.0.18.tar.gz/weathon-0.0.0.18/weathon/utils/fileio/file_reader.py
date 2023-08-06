import yaml
import json
from pathlib import Path
from typing import Union, List
import pandas as pd


class FileReader:

    def __init__(self, filepath: Union[str, Path], **kwargs):
        self.file_path = Path(filepath)

    def read(self,
             return_type: str = 'DataFrame',  # [pandas.DataFrame, List, Generator]
             fields: List[str] = None,
             dropna: bool = True,
             encoding: str = 'utf8',
             **kwargs
             ):
        pass

        if self.file_path.suffix in ['.json', '.jsonl']:
            return self._read_json(return_type, fields, dropna, encoding)
        elif self.file_path.suffix in ['.yml', 'yaml']:
            return self._read_yaml(encoding=encoding)
        else:
            return self._read_txt(encoding=encoding)
    def _read_txt(self, encoding:str="utf8"):
        with self.file_path.open("r",encoding=encoding) as reader:
            return reader.read()

    def _read_yaml(self, encoding='utf8'):
        """
            读取yaml格式的文件
        Returns:
        """
        with self.file_path.open('r', encoding=encoding) as handle:
            return yaml.load(handle, Loader=yaml.Loader)

    def _read_json(self,
                   return_type: str = 'DataFrame',  # [pandas.DataFrame, List, Generator]
                   fields: List[str] = None,
                   dropna: bool = True,
                   encoding: str = 'utf8',
                   **kwargs
                   ):
        """
        读取jsonl文件，并以列表的形式返回
        Args:
            return_type:
            fields:
            dropna:
            encoding:
            **kwargs:

        Returns:
        """

        if return_type == "DataFrame":
            try:
                return pd.read_json(self.file_path)
            except ValueError:
                return pd.DataFrame(self._read_jsonl_as_list(fields, dropna, encoding))

        elif return_type == "List":
            return self._read_jsonl_as_list(fields=fields, dropna=dropna, encoding=encoding)
        elif return_type == "Generator":
            return self._read_jsonl_as_generator(fields, dropna, encoding)
        else:
            raise ValueError("return_type must in [DataFrame, List, Generator]")

    def _read_jsonl_as_list(self,
                            fields: List[str] = None,
                            dropna: bool = True,
                            encoding: str = 'utf-8',
                            **kwargs
                            ):
        """
        读取jsonl文件，并以列表的形式返回
        Args:
            fields:
            dropna:
            encoding:
            **kwargs:

        Returns:

        """
        datas = []
        if fields: fields = set(fields)

        with self.file_path.open("r", encoding=encoding) as f:
            for idx, line in enumerate(f):
                data = json.loads(line.strip())
                if fields is None:
                    datas.append(data)
                    continue
                _res = {}
                for k, v in data.items():
                    if k in fields:
                        _res[k] = v
                if len(_res) < len(fields):
                    if dropna:
                        continue
                    else:
                        raise ValueError(f'invalid instance at line number: {idx}')
                datas.append(_res)
        return datas

    def _read_jsonl_as_generator(self,
                                 fields: List[str] = None,
                                 dropna: bool = True,
                                 encoding: str = 'utf-8',
                                 **kwargs
                                 ):
        """读取jsonl文件，并以列表的形式返回"""
        if fields: fields = set(fields)
        with self.file_path.open("r", encoding=encoding) as f:
            for idx, line in enumerate(f):
                data = json.loads(line.strip())
                if fields is None:
                    yield idx, data
                    continue
                _res = {}
                for k, v in data.items():
                    if k in fields:
                        _res[k] = v
                if len(_res) < len(fields):
                    if dropna:
                        continue
                    else:
                        raise ValueError(f'invalid instance at line number: {idx}')
                yield idx, _res
