# -*- coding: utf-8 -*-
# @Time    : 2023/3/18 14:17
# @Author  : LiZhen
# @FileName: wav_note.py
# @github  : https://github.com/Lizhen0628
# @Description:
import os
from pathlib import Path

from weathon.dl.utils.fileio.file_utils import ensure_directory


class WavNote:
    """音频转乐谱"""

    def __init__(self, wav_file, note_file):
        self.record_dir = ensure_directory(Path(os.environ["DATA_DIR"]) / "weathon" / "record_wav")
        self.note_dir = ensure_directory(Path(os.environ["DATA_DIR"]) / "weathon" / "melody_note")

