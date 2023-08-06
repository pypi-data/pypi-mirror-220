from weathon.dl.utils.import_utils import is_torch_available

if is_torch_available():
    from weathon.dl.base import TorchModel, TorchHead
