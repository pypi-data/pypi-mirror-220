from typing import Dict

import torch
import torch.nn.functional as F
from torch import nn

from weathon.dl.base import TorchHead
from weathon.dl.registry import HEADS
from weathon.dl.utils.constants import Tasks, Heads



@HEADS.register_module(Tasks.text_generation, module_name=Heads.text_generation)
class TextGenerationHead(TorchHead):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = self.config
        self.linear = nn.Linear(
            config['hidden_size'], config['vocab_size'], bias=False)

    def get_output_embeddings(self):
        return self.linear

    def forward(self, inputs=None, **kwargs):
        logits = self.linear(inputs)
        return logits

    def compute_loss(self, logits: torch.Tensor,
                     labels) -> Dict[str, torch.Tensor]:
        return F.cross_entropy(logits, labels)
