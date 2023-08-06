import os
from typing import Dict

import torch
from torch import nn

from weathon.dl.base import TorchModel
from weathon.dl.registry import MODELS
from weathon.dl.utils.constants import Tasks
from weathon.dl.utils.constants.metainfo import Models
from weathon.dl.utils.typing import Tensor
# from weathon.dl.base import BaseModel, Tensor, TorchModel
# from weathon.dl.registry import MODELS
# from weathon.dl.utils.config.config import Config
# from weathon.dl.utils.constants import ModelFile, Tasks
from .backbone import ClassifyRerank


@MODELS.register_module(Tasks.document_grounded_dialog_rerank, module_name=Models.doc2bot)
class DocumentGroundedDialogRerankModel(TorchModel):
    _backbone_prefix = ''

    def __init__(self, model_dir, **kwargs):
        super().__init__(model_dir, **kwargs)
        self.model = ClassifyRerank(model_dir)

    def forward(self, input: Dict[str, Tensor]):
        outputs = self.model(
            input_ids=input['input_ids'],
            attention_mask=input['attention_mask'])
        return outputs

    def resize_token_embeddings(self, size):
        self.model.base_model.resize_token_embeddings(size)

    def save_pretrained(self, addr):
        self.model.base_model.save_pretrained(addr)
