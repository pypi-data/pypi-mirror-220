import bz2
import gzip
import tarfile
from pathlib import Path
from typing import Union
from zipfile import ZipFile

from .file_utils import ensure_directory


class FileDecomposer:
    """
    文件解压缩工具类
    """

    @staticmethod
    def unzip_file(source: Union[str, Path], target: Union[str, Path] = None) -> None:
        """
        解压缩zip文件
        Args:
            source: 压缩文件路径
            target: 解压缩路径，如果为空，解压到当前路径
        """
        source = Path(source)
        target = ensure_directory(target) if target else source.parent
        with ZipFile(source, "r") as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall(target)

    @staticmethod
    def untar_gz_file(source: Union[str, Path], target: Union[str, Path] = None) -> None:
        """
        解压缩tar.gz 文件
        Args:
            source: 压缩文件路径
            target: 解压缩路径，如果为空，解压到当前路径
        """
        source = Path(source)
        target = ensure_directory(target) if target else source.parent
        with tarfile.open(source, 'r:gz') as tar:
            tar.extractall(target)

    @staticmethod
    def ungzip_file(source: Union[str, Path], target: Union[str, Path] = None,
                    target_filename: Union[str] = None) -> None:
        """
        解压缩gzip文件
        Args:
            source: 压缩文件路径
            target: 解压缩文件夹，如果为空，解压到当前路径
            target_filename: 解压缩文件名称
        """
        source = Path(source)
        target_dir = ensure_directory(target) if target else source.parent
        target_filename = target_filename if target_filename else source.stem
        target_file = target_dir / target_filename
        with gzip.GzipFile(source, "rb") as source_reader, target_file.open("wb") as target_writer:
            for data in iter(lambda: source_reader.read(100 * 1024), b""):
                target_writer.write(data)

    @staticmethod
    def unbz2_file(source: Union[str, Path], target: Union[str, Path] = None,
                   target_filename: Union[str] = None) -> None:
        """
        解压缩gzip文件
        Args:
            source: 压缩文件路径
            target: 解压缩文件夹，如果为空，解压到当前路径
            target_filename: 解压缩文件名称
        """
        source = Path(source)
        target_dir = ensure_directory(target) if target else source.parent
        target_filename = target_filename if target_filename else source.stem
        target_file = target_dir / target_filename

        with bz2.BZ2File(source, "rb") as source_reader, target_file.open("wb") as target_writer:
            for data in iter(lambda: source_reader.read(100 * 1024), b""):
                target_writer.write(data)

    @staticmethod
    def add_start_docstrings(*docstr):
        def docstring_decorator(fn):
            fn.__doc__ = "".join(docstr) + (fn.__doc__ if fn.__doc__ is not None else "")
            return fn

        return docstring_decorator
