from typing import Any, Dict

import numpy as np

from weathon.dl.utils.constants.metainfo import Heads, TaskModels
from weathon.dl.registry import MODELS
from weathon.dl.models.nlp.task_models.task_model import EncoderModel
from weathon.dl.utils.constants import Tasks

__all__ = ['ModelForInformationExtraction']


@MODELS.register_module(
    Tasks.information_extraction,
    module_name=TaskModels.information_extraction)
@MODELS.register_module(
    Tasks.relation_extraction, module_name=TaskModels.information_extraction)
class ModelForInformationExtraction(EncoderModel):
    task = Tasks.information_extraction

    # The default base head type is fill-mask for this head
    head_type = Heads.information_extraction
