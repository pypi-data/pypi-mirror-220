from transformers import BloomConfig
from transformers import BloomModel as BloomModelTransform

from weathon.dl.registry import BACKBONES
from weathon.dl.utils.constants import Tasks
from weathon.dl.utils.constants.metainfo import Models


@BACKBONES.register_module(group_key=Tasks.backbone, module_name=Models.bloom)
class BloomModel(BloomModelTransform):

    def __init__(self, **kwargs):
        config = BloomConfig(**kwargs)
        super().__init__(config)
