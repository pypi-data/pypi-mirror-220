import shutil
from pathlib import Path
from typing import Union


def ensure_directory(dirname: Union[str, Path]) -> Path:
    """
    判断文件夹是否存在，如果不存在就创建，返回文件夹路径
    Args:
        dirname: 文件夹 路径
    Returns:
    """
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)
    return dirname


def clear_directory(dirname: Union[str, Path]) -> Path:
    """
    清空dirname 内容
    Args:
        dirname:

    Returns:

    """
    dirname = Path(dirname)
    if dirname.exists():
        shutil.rmtree(dirname)  # clear the directory
    ensure_directory(dirname)


def copy_directory(source: Union[Path, str] = None, target: Union[Path, str] = None):
    """
    复制文件夹
    Args:
        source: 原文件夹
        target: 目标文件夹
    Returns: 返回目标文件夹路径
    """
    source, target = Path(source), Path(target)
    if not target.exists():
        target.mkdir()

    files = list(source.glob("*"))
    for source_file in files:
        target_file = target / source_file.name
        if source_file.is_file():
            target_file.write_bytes(source_file.read_bytes())
        else:
            copy_directory(source_file, target_file)


def ensure_file(file_name: Union[str, Path]) -> Path:
    """
    判断文件是否存在，如果文件不存在就创建文件，返回文件路径
    Args:
        file_name:文件名
    Returns:
    """
    file_name = Path(file_name)
    ensure_directory(file_name.parent)
    if not file_name.exists():
        file_name.touch(exist_ok=False)
    return file_name
