from typing import Optional, Mapping, Union

from weathon.dl.base import BaseProcessor
from weathon.dl.base.trainer import ConfigTrainer
from weathon.dl.registry import TRAINERS
from weathon.dl.utils.config.config import Config
from weathon.dl.utils.constants import Tasks, Datasets


@TRAINERS.register_module(group_key=Tasks.text_classification, module_name=Datasets.jd_sentiment_text_classification)
class JDTextClassificationTrainer(ConfigTrainer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def build_model(self) -> Union[nn.Module, TorchModel]:
    #     """实例化pytorch模型.
    #     根据配置文件来构建模型
    #     """
    #     model_cfg = self.cfg.model
    #     model_args = dict(
    #         num_labels=model_cfg.num_labels,
    #         label2id=model_cfg.label2id,
    #         id2label=model_cfg.id2label
    #     )
    #     model = BaseModel.from_pretrained(self.model_dir, cfg_dict=self.cfg, **model_args)
    #     if not isinstance(model, nn.Module) and hasattr(model, 'model'):
    #         return model.model
    #     elif isinstance(model, nn.Module):
    #         return model

    def get_preprocessors(self, preprocessor: Union[BaseProcessor, Mapping, Config]) -> Optional[BaseProcessor]:
        return self.build_preprocessor()
    #
    #
    # def build_dataset(self, dataset: Union[Dataset, WtDataset, List[Dataset]], cfg: Config,
    #                   mode: str, preprocessor: Optional[BasePreprocessor] = None, **kwargs):
    #     dataset_cfg = self.cfg.safe_get(f"dataset.{mode}")
    #     return build_custom_dataset(dataset_cfg, task_name=dataset_cfg.task, default_args=dict(preprocessor=preprocessor))
