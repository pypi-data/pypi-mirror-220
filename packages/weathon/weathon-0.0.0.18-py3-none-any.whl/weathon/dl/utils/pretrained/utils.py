import os.path as osp

from weathon.dl.utils.config.config import Config
from weathon.dl.utils.constants import ModelFile
from weathon.dl.utils.logger import get_logger

logger = get_logger()



def get_model_type(model_dir):
    """Get the model type from the configuration.

    This method will try to get the model type from 'model.backbone.type',
    'model.type' or 'model.model_type' field in the configuration.json file. If
    this file does not exist, the method will try to get the 'model_type' field
    from the config.json.

    Args:
        model_dir: The local model dir to use. @return: The model type
    string, returns None if nothing is found.
    """
    try:
        yaml_file = osp.join(model_dir, ModelFile.CONFIGURATION_YAML)
        json_file = osp.join(model_dir, ModelFile.CONFIGURATION)

        config_file = osp.join(model_dir, 'config.json')

        if osp.isfile(yaml_file) or osp.isfile(json_file):
            cfg = Config.from_file(yaml_file)
            if hasattr(cfg.model, 'backbone'):
                return cfg.model.backbone.type
            elif hasattr(cfg.model,
                         'model_type') and not hasattr(cfg.model, 'type'):
                return cfg.model.model_type
            else:
                return cfg.model.type

        elif osp.isfile(config_file):
            cfg = Config.from_file(config_file)
            return cfg.model_type if hasattr(cfg, 'model_type') else None

    except Exception as e:
        logger.error(f'parse config file failed with error: {e}')