import os
from typing import Optional, Union

from weathon.dl.utils.logger import get_logger

logger = get_logger()


def format_dataset_structure(dataset_structure):
    return {
        k: v
        for k, v in dataset_structure.items()
        if (v.get('meta') or v.get('file'))
    }


def get_target_dataset_structure(dataset_structure: dict,
                                 subset_name: Optional[str] = None,
                                 split: Optional[str] = None):
    """
    Args:
        dataset_structure (dict): Dataset Structure, like
         {
            "default":{
                "train":{
                    "meta":"my_train.csv",
                    "file":"pictures.zip"
                }
            },
            "subsetA":{
                "test":{
                    "meta":"mytest.csv",
                    "file":"pictures.zip"
                }
            }
        }
        subset_name (str, optional): Defining the subset_name of the dataset.
        split (str, optional): Which split of the data to load.
    Returns:
           target_subset_name (str): Name of the chosen subset.
           target_dataset_structure (dict): Structure of the chosen split(s), like
           {
               "test":{
                        "meta":"mytest.csv",
                        "file":"pictures.zip"
                    }
            }
    """
    # verify dataset subset
    if (subset_name and subset_name not in dataset_structure) or (
            not subset_name and len(dataset_structure.keys()) > 1):
        raise ValueError(
            f'subset_name {subset_name} not found. Available: {dataset_structure.keys()}'
        )
    target_subset_name = subset_name
    if not subset_name:
        target_subset_name = next(iter(dataset_structure.keys()))
        logger.info(
            f'No subset_name specified, defaulting to the {target_subset_name}'
        )
    # verify dataset split
    target_dataset_structure = format_dataset_structure(
        dataset_structure[target_subset_name])
    if split and split not in target_dataset_structure:
        raise ValueError(
            f'split {split} not found. Available: {target_dataset_structure.keys()}'
        )
    if split:
        target_dataset_structure = {split: target_dataset_structure[split]}
    return target_subset_name, target_dataset_structure



def contains_dir(file_map) -> bool:
    """
    To check whether input contains at least one directory.

    Args:
        file_map (dict): Structure of data files. e.g., {'train': 'train.zip', 'validation': 'val.zip'}
    Returns:
        True if input contains at least one directory, False otherwise.
    """
    res = False
    for k, v in file_map.items():
        if isinstance(v, str) and not v.endswith('.zip'):
            res = True
            break
    return res


def get_subdir_hash_from_split(split: Union[str, list], version: str) -> str:
    if isinstance(split, str):
        split = [split]
    return os.path.join(version, '_'.join(split))


def get_split_list(split: Union[str, list]) -> list:
    """ Unify the split to list-format. """
    if isinstance(split, str):
        return [split]
    elif isinstance(split, list):
        return split
    else:
        raise f'Expected format of split: str or list, but got {type(split)}.'


def get_split_objects_map(file_map, objects):
    """
    Get the map between dataset split and oss objects.

    Args:
        file_map (dict): Structure of data files. e.g., {'train': 'train', 'validation': 'val'}, both of train and val
            are dirs.
        objects (list): List of oss objects. e.g., ['train/001/1_123.png', 'train/001/1_124.png', 'val/003/3_38.png']
    Returns:
        A map of split-objects. e.g., {'train': ['train/001/1_123.png', 'train/001/1_124.png'],
            'validation':['val/003/3_38.png']}
    """
    res = {}
    for k, v in file_map.items():
        res[k] = []

    for obj_key in objects:
        for k, v in file_map.items():
            if obj_key.startswith(v.rstrip('/') + '/'):
                res[k].append(obj_key)

    return res
