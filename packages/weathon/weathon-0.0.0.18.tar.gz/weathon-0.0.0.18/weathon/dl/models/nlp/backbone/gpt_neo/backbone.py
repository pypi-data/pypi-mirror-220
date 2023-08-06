from transformers import GPTNeoConfig
from transformers import GPTNeoModel as GPTNeoModelTransform

from weathon.dl.registry import BACKBONES
from weathon.dl.utils.constants import Tasks
from weathon.dl.utils.constants.metainfo import Models


@BACKBONES.register_module(group_key=Tasks.backbone, module_name=Models.gpt_neo)
class GPTNeoModel(GPTNeoModelTransform):

    def __init__(self, **kwargs):
        config = GPTNeoConfig(**kwargs)
        super().__init__(config)
