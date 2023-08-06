from typing import Dict

import numpy as np

from weathon.dl.base import BaseMetric
from weathon.dl.registry import METRICS
from weathon.dl.registry.registry import default_group
from weathon.dl.utils.constants import Metrics, OutputKeys

from weathon.dl.utils.tensor_utils import (torch_nested_detach, torch_nested_numpify)


@METRICS.register_module(group_key=default_group, module_name=Metrics.loss_metric)
class LossMetric(BaseMetric):
    """The metric class to calculate average loss of batches.

    Args:
        loss_key: The key of loss
    """

    def __init__(self, loss_key=OutputKeys.LOSS, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loss_key = loss_key
        self.losses = []

    def add(self, outputs: Dict, inputs: Dict):
        loss = outputs[self.loss_key]
        self.losses.append(torch_nested_numpify(torch_nested_detach(loss)))

    def evaluate(self):
        return {OutputKeys.LOSS: float(np.average(self.losses))}

    def merge(self, other: 'LossMetric'):
        self.losses.extend(other.losses)

    def __getstate__(self):
        return self.losses

    def __setstate__(self, state):
        self.__init__()
        self.losses = state
