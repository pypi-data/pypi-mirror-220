from typing import Any, List, Union
import torch.utils.data
from torch.utils.data import ConcatDataset as TorchConcatDataset

from weathon.dl.utils.constants import ModeKeys



class TorchCustomDataset(torch.utils.data.Dataset):
    """The custom dataset base class for all the torch-based task processors.
    """

    def __init__(self, datasets: Union[Any, List[Any]], mode=ModeKeys.TRAIN,  preprocessor=None, **kwargs):
        self.trainer = None
        self.mode = mode
        self.preprocessor = preprocessor
        self._inner_dataset = self.prepare_dataset(datasets)

    def __getitem__(self, index) -> Any:
        return self.preprocessor(self._inner_dataset[index]) if self.preprocessor else self._inner_dataset[index]

    def __len__(self):
        return len(self._inner_dataset)

    def combine_datasets(self, datasets:Union[Any, List[Any]]) -> Any:
        """
        某个模型在训练过程中需要同时加载多个训练数据集,以某种方式进行shuffle再输入dataloader.
        """
        if isinstance(datasets, List):
            if len(datasets) == 1:
                return datasets[0]
            elif len(datasets) > 1:
                return TorchConcatDataset(datasets)
        else:
            return datasets

    def prepare_dataset(self, datasets: Union[Any, List[Any]]) -> Any:
        raise NotImplementedError("prepare_dataset not implements!")
