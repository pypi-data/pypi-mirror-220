from typing import Dict, Any

from torchvision import transforms

from weathon.dl.base import BaseProcessor
from weathon.dl.registry import PREPROCESSORS
from weathon.dl.utils.config.config import Config
from weathon.dl.utils.constants import Tasks, Datasets, ModeKeys
from weathon.dl.utils.processor.preprocessors.cv.ocr import ResizeShortSize
from weathon.dl.utils.processor.preprocessors.cv.ocr import IaaAugment
from weathon.dl.utils.processor.preprocessors.cv.ocr import MakeBorderMap
from weathon.dl.utils.processor.preprocessors.cv.ocr import MakeShrinkMap
from weathon.dl.utils.processor.preprocessors.cv.ocr import EastRandomCropData


@PREPROCESSORS.register_module(group_key=Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
class Icdar2015Preprocessor(BaseProcessor):

    def __init__(self, preprocessor_cfg: Config = None, *args, **kwargs):
        preprocessor_cfg = preprocessor_cfg if preprocessor_cfg else dict()

        self.processes = kwargs.get("processes", preprocessor_cfg.get("transforms", None))
        self.filter_keys = kwargs.get("filter_keys", [])
        self._mode = kwargs.get('mode', preprocessor_cfg.get('mode', ModeKeys.TRAIN))
        self.is_training = (self._mode == ModeKeys.TRAIN)
        self.mean = kwargs.get("mean", preprocessor_cfg.get("mean", [0.485, 0.456, 0.406]))
        self.std = kwargs.get("std", preprocessor_cfg.get("std", [0.229, 0.224, 0.225]))
        self.tranforms = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=self.mean, std=self.std)
        ])

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.processes and not self.tranforms:
            return data
        if hasattr(self.processes, "IaaAugment"):
            data_process0 = IaaAugment(self.processes.IaaAugment)
            data = data_process0(data)

        if hasattr(self.processes, "EastRandomCropData"):
            data_process1 = EastRandomCropData(**self.processes.EastRandomCropData)
            data = data_process1(data)

        if hasattr(self.processes, "MakeShrinkMap"):
            data_process2 = MakeShrinkMap(**self.processes.MakeShrinkMap)
            data = data_process2(data)

        if hasattr(self.processes, "MakeBorderMap"):
            data_process3 = MakeBorderMap(**self.processes.MakeBorderMap)
            data = data_process3(data)

        if hasattr(self.processes, "ResizeShortSize"):
            data_process4 = ResizeShortSize(**self.processes.ResizeShortSize)
            data = data_process4(data)

        data["img"] = self.tranforms(data["img"])

        if self.is_training:
            for key in self.filter_keys:
                del data[key]
        return data
