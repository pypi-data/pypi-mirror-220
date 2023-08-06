from weathon.dl.registry.registry import build_from_cfg, Registry
from weathon.dl.utils.config.config import ConfigDict
from weathon.dl.utils.constants import Trainers

TRAINERS = Registry('trainers')


def build_trainer(cfg: ConfigDict, task_name: str = None, default_args: dict = None):
    """ build trainers given a trainers name

    Args:
        name (str, optional):  Trainer name, if None, default trainers
            will be used.
        default_args (dict, optional): Default initialization arguments.
    """
    cfg["type"] = default_args.get("type", cfg.get("type", Trainers.default))
    cfg = cfg.to_dict()
    return build_from_cfg(cfg, TRAINERS, group_key=task_name, default_args=default_args)
