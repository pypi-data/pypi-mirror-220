import json
from pathlib import Path
from typing import Union

import yaml


class FileWriter:

    def __init__(self, filepath: Union[str, Path]):
        self.file_path = Path(filepath)

    def write_yaml(self, content):
        """
        将文件内容写入yaml文件
        Args:
            content: 文件内容
            infile: yaml文件名称
        Returns:

        """
        with self.file_path.open('w', encoding='utf8') as handle:
            yaml.dump(content, handle, )

    def write_json(self, content):
        with self.file_path.open('wt') as handle:
            json.dump(content, handle, indent=4, sort_keys=False)
