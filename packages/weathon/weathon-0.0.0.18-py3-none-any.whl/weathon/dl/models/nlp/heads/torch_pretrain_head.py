from typing import Dict

import torch
from transformers.models.bert.modeling_bert import BertOnlyMLMHead
from transformers.models.roberta.modeling_roberta import RobertaLMHead

from weathon.dl.base import TorchHead
from weathon.dl.registry import HEADS
from weathon.dl.utils.constants import Tasks, Heads


@HEADS.register_module(Tasks.fill_mask, module_name=Heads.bert_mlm)
class BertMLMHead(BertOnlyMLMHead, TorchHead):

    def compute_loss(self, outputs: Dict[str, torch.Tensor], labels) -> Dict[str, torch.Tensor]:
        raise NotImplementedError()


@HEADS.register_module(Tasks.fill_mask, module_name=Heads.roberta_mlm)
class RobertaMLMHead(RobertaLMHead, TorchHead):

    def compute_loss(self, outputs: Dict[str, torch.Tensor], labels) -> Dict[str, torch.Tensor]:
        raise NotImplementedError()
