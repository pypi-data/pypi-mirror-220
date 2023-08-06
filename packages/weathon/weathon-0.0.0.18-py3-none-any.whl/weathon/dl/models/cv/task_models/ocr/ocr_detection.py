import copy
import os

import torch
from torch import nn
from addict import Dict
from dataclasses import dataclass

from weathon.dl.base import TorchModel, BaseOutput
from weathon.dl.registry import MODELS, build_model, build_loss, build_postprocessor
from weathon.dl.utils.constants import Tasks, Datasets
from weathon.dl.utils.typing import Tensor


@dataclass
class DBModelOutput(BaseOutput):
    logit: Tensor = None
    loss: Tensor = None
    loss_threshold_maps: Tensor = None
    loss_shrink_maps: Tensor = None


@MODELS.register_module(Tasks.ocr_detection, module_name=Datasets.icdar2015_ocr_detection)
class DetModel(TorchModel):

    def __init__(self, model_dir: str, **kwargs):
        """initialize the ocr recognition model from the `model_dir` path.

        Args:
            model_dir (str): the model path.
        """
        super().__init__(model_dir, **kwargs)

        self.backbone = build_model(kwargs.get("backbone"), task_name=kwargs.get("task"))
        self.neck = build_model(kwargs.get("neck"), task_name=kwargs.get("task"),
                                default_args=dict(in_channels=self.backbone.out_channels))
        self.head = build_model(kwargs.get("head"), task_name=kwargs.get("task"),
                                default_args=dict(in_channels=self.neck.out_channels))
        self.criterion = build_loss(kwargs.get("loss"), task_name=kwargs.get("task"))

        self.postprocessor = build_postprocessor(kwargs.get("postprocess"), task_name=kwargs.get("task"))

    def forward(self, **inputs):
        x = inputs["img"]
        x = self.backbone(x)
        x = self.neck(x)
        x = self.head(x)
        output = dict(logit=x, loss=None)
        if self.training:
            loss_dict = self.criterion(x, inputs)
            output.update(**loss_dict)

        return DBModelOutput(**output)

    def pose_process(self, **inputs) -> dict:
        if not self.training:
            boxes, scores = self.postprocess(self.forward(inputs).logit, inputs["shape"])
            inputs.update(dict(boxes=boxes, scores=scores))
        return inputs


def load_pretrained_params(_model, _path):
    if _path is None:
        return False
    if not os.path.exists(_path):
        print(f'The pretrained_model {_path} does not exists')
        return False
    params = torch.load(_path)
    state_dict = params['state_dict']
    state_dict_no_module = {k.replace('module.', ''): v for k, v in state_dict.items()}
    _model.load_state_dict(state_dict_no_module)
    return _model


class DistillationModel(nn.Module):
    def __init__(self, config):
        super(DistillationModel, self).__init__()
        self.model_dict = nn.ModuleDict()
        self.model_name_list = []

        sub_model_cfgs = config['models']
        for key in sub_model_cfgs:
            sub_cfg = copy.deepcopy(sub_model_cfgs[key])
            sub_cfg.pop('type')
            freeze_params = False
            pretrained = None

            if 'freeze_params' in sub_cfg:
                freeze_params = sub_cfg.pop('freeze_params')
            if 'pretrained' in sub_cfg:
                pretrained = sub_cfg.pop('pretrained')
            model = DetModel(Dict(sub_cfg))
            if pretrained is not None:
                model = load_pretrained_params(model, pretrained)
            if freeze_params:
                for para in model.parameters():
                    para.requires_grad = False
                model.training = False

            self.model_dict[key] = model
            self.model_name_list.append(key)

    def forward(self, x):
        result_dict = dict()
        for idx, model_name in enumerate(self.model_name_list):
            result_dict[model_name] = self.model_dict[model_name](x)
        return result_dict

#
# if __name__ == '__main__':
#     import torch
#
#     # db_config = AttrDict(
#     #     in_channels=3,
#     #     backbone=AttrDict(type='MobileNetV3', layers=50, model_name='large',pretrained=True),
#     #     neck=AttrDict(type='FPN', out_channels=256),
#     #     head=AttrDict(type='DBHead')
#     # )
#     # x = torch.zeros(1, 3, 640, 640)
#     # model = DetModel(db_config)
#
#     db_config = AttrDict(
#         in_channels=3,
#         backbone=AttrDict(type='ResNet', layers=50, pretrained=True),
#         neck=AttrDict(type='pse_fpn', out_channels=256),
#         head=AttrDict(type='PseHead', H=640, W=640, scale=1)
#     )
#     x = torch.zeros(1, 3, 640, 640)
#     model = DetModel(db_config)
