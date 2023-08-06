from http.cookiejar import CookieJar
from typing import Tuple, Optional, Union

from datasets import DownloadConfig



class BaseAuthConfig(object):
    """Base authorization config class."""

    def __init__(self, cookies: CookieJar, git_token: str,
                 user_info: Tuple[str, str]):
        self.cookies = cookies
        self.git_token = git_token
        self.user_info = user_info


class OssAuthConfig(BaseAuthConfig):
    """The authorization config for oss dataset."""

    def __init__(self, cookies: CookieJar, git_token: str,
                 user_info: Tuple[str, str]):
        super().__init__(
            cookies=cookies, git_token=git_token, user_info=user_info)


class VirgoAuthConfig(BaseAuthConfig):
    """The authorization config for virgo dataset."""

    def __init__(self, cookies: CookieJar, git_token: str,
                 user_info: Tuple[str, str]):
        super().__init__(
            cookies=cookies, git_token=git_token, user_info=user_info)


class MaxComputeAuthConfig(BaseAuthConfig):
    def __init__(self, cookies: CookieJar, git_token: str,
                 user_info: Tuple[str, str]):
        super().__init__(
            cookies=cookies, git_token=git_token, user_info=user_info)

        self.max_compute_grant_cmd = None



class DataMetaConfig(object):
    """Modelscope data-meta config class.

    Attributes:
        dataset_scripts(str): The local path of dataset scripts.
        dataset_formation(:obj:`enum.Enum`): Dataset formation, refer to modelscope.utils.constant.DatasetFormations.
        meta_cache_dir(str): Meta cache path.
        meta_data_files(dict): Meta data mapping, Example: {'test': 'https://xxx/mytest.csv'}
        zip_data_files(dict): Data files mapping, Example: {'test': 'pictures.zip'}
        meta_args_map(dict): Meta arguments mapping, Example: {'test': {'file': 'pictures.zip'}, ...}
        target_dataset_structure(dict): Dataset Structure, like
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
        dataset_py_script(str): The python script path of dataset.
        meta_type_map(dict): The custom dataset mapping in meta data,
            Example: {"type": "MovieSceneSegmentationCustomDataset",
                        "preprocessor": "movie-scene-segmentation-preprocessor"}
    """

    def __init__(self):
        self.dataset_scripts = None
        self.dataset_formation = None
        self.meta_cache_dir = None
        self.meta_data_files = None
        self.zip_data_files = None
        self.meta_args_map = None
        self.target_dataset_structure = None
        self.dataset_py_script = None
        self.meta_type_map = {}


class DataDownloadConfig(DownloadConfig):

    def __init__(self):
        self.dataset_name: Optional[str] = None
        self.namespace: Optional[str] = None
        self.version: Optional[str] = None
        self.split: Optional[Union[str, list]] = None
        self.data_dir: Optional[str] = None
        self.oss_config: Optional[dict] = {}
        self.meta_args_map: Optional[dict] = {}

    def copy(self) -> 'DataDownloadConfig':
        return self


#
# class DatasetContextConfig:
#     """Context configuration of dataset."""
#
#     def __init__(self, dataset_name: Union[str, list], namespace: str,
#                  version: str, subset_name: str, split: Union[str, list],
#                  target: str, hub: Hubs, data_dir: str,
#                  data_files: Union[str, Sequence[str],
#                                    Mapping[str, Union[str, Sequence[str]]]],
#                  download_mode: DownloadMode, cache_root_dir: str,
#                  use_streaming: bool, **kwargs):
#
#         self._download_config = None
#         self._data_meta_config = None
#         self._config_kwargs = kwargs
#         self._dataset_version_cache_root_dir = None
#         self._auth_config = None
#
#         # The lock file path for meta-files and data-files
#         self._global_meta_lock_file_path = None
#         self._global_data_lock_file_path = None
#
#         # General arguments for dataset
#         self.hub = hub
#         self.download_mode = download_mode
#         self.dataset_name = dataset_name
#         self.namespace = namespace
#         self.version = version
#         self.subset_name = subset_name
#         self.split = split
#         self.target = target
#         self.data_dir = data_dir
#         self.data_files = data_files
#         self.cache_root_dir = cache_root_dir
#         self.use_streaming = use_streaming
#         self.download_virgo_files: bool = False
#
#     @property
#     def config_kwargs(self) -> dict:
#         return self._config_kwargs
#
#     @config_kwargs.setter
#     def config_kwargs(self, val: dict):
#         self._config_kwargs = val
#
#     @property
#     def download_config(self) -> DataDownloadConfig:
#         return self._download_config
#
#     @download_config.setter
#     def download_config(self, val: DataDownloadConfig):
#         self._download_config = val
#
#     @property
#     def data_meta_config(self) -> DataMetaConfig:
#         return self._data_meta_config
#
#     @data_meta_config.setter
#     def data_meta_config(self, val: DataMetaConfig):
#         self._data_meta_config = val
#
#     @property
#     def dataset_version_cache_root_dir(self) -> str:
#         return self._dataset_version_cache_root_dir
#
#     @dataset_version_cache_root_dir.setter
#     def dataset_version_cache_root_dir(self, val: str):
#         self._dataset_version_cache_root_dir = val
#
#     @property
#     def global_meta_lock_file_path(self) -> str:
#         return self._global_meta_lock_file_path
#
#     @global_meta_lock_file_path.setter
#     def global_meta_lock_file_path(self, val: str):
#         self._global_meta_lock_file_path = val
#
#     @property
#     def global_data_lock_file_path(self) -> str:
#         return self._global_data_lock_file_path
#
#     @global_data_lock_file_path.setter
#     def global_data_lock_file_path(self, val: str):
#         self._global_data_lock_file_path = val
#
#     @property
#     def auth_config(self) -> BaseAuthConfig:
#         return self._auth_config
#
#     @auth_config.setter
#     def auth_config(self, val: BaseAuthConfig):
#         self._auth_config = val