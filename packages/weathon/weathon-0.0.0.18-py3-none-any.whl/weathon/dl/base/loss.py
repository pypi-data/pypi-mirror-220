from abc import ABC, abstractmethod
from typing import Dict,Any



class BaseLoss(ABC):
    """The head base class is for the tasks loss method definition

    """

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def forward(self, *args, **kwargs) -> Dict[str, Any]:
        """
        """
        pass
    