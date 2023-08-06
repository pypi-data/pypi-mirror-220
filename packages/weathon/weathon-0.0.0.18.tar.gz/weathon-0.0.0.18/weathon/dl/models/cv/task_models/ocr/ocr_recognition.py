from weathon.dl.base import TorchModel
from weathon.dl.registry import MODELS, build_model, build_loss
from weathon.dl.utils.constants import Tasks, Datasets


@MODELS.register_module(Tasks.ocr_recognition, module_name=Datasets.icdar2015_ocr_detection)
class RecModel(TorchModel):
    def __init__(self, model_dir: str, **kwargs):
        super().__init__(model_dir, **kwargs)
        self.backbone = build_model(kwargs.get("backbone"), task_name=kwargs.get("task"))
        self.neck = build_model(kwargs.get("neck"), task_name=kwargs.get("task"),
                                default_args=dict(in_channels=self.backbone.out_channels))
        self.head = build_model(kwargs.get("head"), task_name=kwargs.get("task"),
                                default_args=dict(in_channels=self.neck.out_channels))

        self.criterion = build_loss(kwargs.get("loss"), task_name=kwargs.get("task"))

    def forward(self, x):
        x = self.backbone(x)
        x = self.neck(x)
        x = self.head(x)
        return x
