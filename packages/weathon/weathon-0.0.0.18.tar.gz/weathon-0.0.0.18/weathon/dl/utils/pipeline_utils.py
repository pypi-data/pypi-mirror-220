import os
import os.path as osp
from typing import List, Optional, Union

from weathon.dl.utils.constants import DEFAULT_MODEL_FOR_PIPELINE
from weathon.dl.utils.constants.pipeline_inputs import INPUT_TYPE, InputType
from weathon.dl.utils.config.config import Config
from weathon.dl.utils.logger import get_logger

logger = get_logger()


def check_input_type(input_type, input):
    expected_type = INPUT_TYPE[input_type]
    if input_type == InputType.VIDEO:
        # special type checking using class name, to avoid introduction of opencv dependency into fundamental framework.
        assert type(input).__name__ == 'VideoCapture' or isinstance(input, expected_type), \
            f'invalid input type for {input_type}, expected {expected_type} but got {type(input)}\n {input}'
    else:
        assert isinstance(input, expected_type), \
            f'invalid input type for {input_type}, expected {expected_type} but got {type(input)}\n {input}'


def is_config_has_model(cfg_file):
    try:
        cfg = Config.from_file(cfg_file)
        return hasattr(cfg, 'model')
    except Exception as e:
        logger.error(f'parse config file {cfg_file} failed: {e}')
        return False


def batch_process(model, data):
    import torch
    if model.__class__.__name__ == 'OfaForAllTasks':
        # collate batch data due to the nested data structure
        assert isinstance(data, list)
        batch_data = {
            'nsentences': len(data),
            'samples': [d['samples'][0] for d in data],
            'net_input': {}
        }
        for k in data[0]['net_input'].keys():
            batch_data['net_input'][k] = torch.cat(
                [d['net_input'][k] for d in data])
        if 'w_resize_ratios' in data[0]:
            batch_data['w_resize_ratios'] = torch.cat(
                [d['w_resize_ratios'] for d in data])
        if 'h_resize_ratios' in data[0]:
            batch_data['h_resize_ratios'] = torch.cat(
                [d['h_resize_ratios'] for d in data])

        return batch_data


def add_default_pipeline_info(task: str,
                              model_name: str,
                              modelhub_name: str = None,
                              overwrite: bool = False):
    """ Add default model for a task.

    Args:
        task (str): task name.
        model_name (str): model_name.
        modelhub_name (str): name for default modelhub.
        overwrite (bool): overwrite default info.
    """
    if not overwrite:
        assert task not in DEFAULT_MODEL_FOR_PIPELINE, \
            f'task {task} already has default model.'

    DEFAULT_MODEL_FOR_PIPELINE[task] = (model_name, modelhub_name)


def get_default_pipeline_info(task):
    """ Get default info for certain task.

    Args:
        task (str): task name.

    Return:
        A tuple: first element is pipeline name(model_name), second element
            is modelhub name.
    """
    from weathon.dl.registry import PIPELINES
    if task not in DEFAULT_MODEL_FOR_PIPELINE:
        # support pipeline which does not register default model
        pipeline_name = list(PIPELINES.modules[task].keys())[0]
        default_model = None
    else:
        pipeline_name, default_model = DEFAULT_MODEL_FOR_PIPELINE[task]
    return pipeline_name, default_model
