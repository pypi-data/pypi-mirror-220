import enum
from pathlib import Path
import os

MODELSCOPE_URL_SCHEME = 'http://'
DEFAULT_MODELSCOPE_DOMAIN = 'www.modelscope.cn'
DEFAULT_MODELSCOPE_DATA_ENDPOINT = MODELSCOPE_URL_SCHEME + DEFAULT_MODELSCOPE_DOMAIN

DEFAULT_MODELSCOPE_GROUP = 'damo'
MODEL_ID_SEPARATOR = '/'
FILE_HASH = 'Sha256'
LOGGER_NAME = 'ModelScopeHub'
DEFAULT_CREDENTIALS_PATH = Path.home().joinpath('.modelscope', 'credentials')
REQUESTS_API_HTTP_METHOD = ['get', 'head', 'post', 'put', 'patch', 'delete']
API_HTTP_CLIENT_TIMEOUT = 60
API_RESPONSE_FIELD_DATA = 'Data'
API_FILE_DOWNLOAD_RETRY_TIMES = 5
API_FILE_DOWNLOAD_TIMEOUT = 60 * 5
API_FILE_DOWNLOAD_CHUNK_SIZE = 4096
API_RESPONSE_FIELD_GIT_ACCESS_TOKEN = 'AccessToken'
API_RESPONSE_FIELD_USERNAME = 'Username'
API_RESPONSE_FIELD_EMAIL = 'Email'
API_RESPONSE_FIELD_MESSAGE = 'Message'
MODELSCOPE_CLOUD_ENVIRONMENT = 'MODELSCOPE_ENVIRONMENT'
MODELSCOPE_CLOUD_USERNAME = 'MODELSCOPE_USERNAME'
MODELSCOPE_SDK_DEBUG = 'MODELSCOPE_SDK_DEBUG'
ONE_YEAR_SECONDS = 24 * 365 * 60 * 60
MODEL_META_FILE_NAME = '.mdl'
MODEL_META_MODEL_ID = 'id'

END_POINT = MODELSCOPE_URL_SCHEME + os.getenv('MODELSCOPE_DOMAIN', DEFAULT_MODELSCOPE_DOMAIN)


import os
from pathlib import Path

# Cache location

MODELSCOPE_URL_SCHEME = 'http://'
DEFAULT_MODELSCOPE_DOMAIN = 'www.modelscope.cn'
DEFAULT_MODELSCOPE_DATA_ENDPOINT = MODELSCOPE_URL_SCHEME + DEFAULT_MODELSCOPE_DOMAIN

DEFAULT_CACHE_HOME = Path.home().joinpath('.cache')
CACHE_HOME = os.getenv('CACHE_HOME', DEFAULT_CACHE_HOME)
DEFAULT_MS_CACHE_HOME = os.path.join(CACHE_HOME, 'weathon', 'hub')
MS_CACHE_HOME = os.path.expanduser(os.getenv('MS_CACHE_HOME', DEFAULT_MS_CACHE_HOME))

DEFAULT_MS_DATASETS_CACHE = os.path.join(MS_CACHE_HOME, 'dataset')
MS_DATASETS_CACHE = Path(os.getenv('MS_DATASETS_CACHE', DEFAULT_MS_DATASETS_CACHE))

DOWNLOADED_DATASETS_DIR = 'downloads'
DEFAULT_DOWNLOADED_DATASETS_PATH = os.path.join(MS_DATASETS_CACHE,DOWNLOADED_DATASETS_DIR)
DOWNLOADED_DATASETS_PATH = Path(os.getenv('DOWNLOADED_DATASETS_PATH', DEFAULT_DOWNLOADED_DATASETS_PATH))

HUB_DATASET_ENDPOINT = os.environ.get('HUB_DATASET_ENDPOINT',DEFAULT_MODELSCOPE_DATA_ENDPOINT)



class Licenses(object):
    APACHE_V2 = 'Apache License 2.0'
    GPL_V2 = 'GPL-2.0'
    GPL_V3 = 'GPL-3.0'
    LGPL_V2_1 = 'LGPL-2.1'
    LGPL_V3 = 'LGPL-3.0'
    AFL_V3 = 'AFL-3.0'
    ECL_V2 = 'ECL-2.0'
    MIT = 'MIT'


class ModelVisibility(object):
    PRIVATE = 1
    INTERNAL = 3
    PUBLIC = 5





class InputFields(object):
    """ Names for input data fields in the input data for pipelines
    """
    img = 'img'
    text = 'text'
    audio = 'audio'


class Hubs(enum.Enum):
    """ Source from which an entity (such as a Dataset or Model) is stored
    """
    modelscope = 'modelscope'
    huggingface = 'huggingface'
    virgo = 'virgo'


class DownloadMode(enum.Enum):
    """ How to treat existing dataset
    """
    REUSE_DATASET_IF_EXISTS = 'reuse_dataset_if_exists'
    FORCE_REDOWNLOAD = 'force_redownload'


class DownloadChannel(enum.Enum):
    """ Channels of dataset downloading for uv/pv counting.
    """
    LOCAL = 'local'
    DSW = 'dsw'
    EAIS = 'eais'


class UploadMode(enum.Enum):
    """ How to upload object to remote.
    """
    # Upload all objects from local, existing remote objects may be overwritten. (Default)
    OVERWRITE = 'overwrite'
    # Upload local objects in append mode, skipping all existing remote objects.
    APPEND = 'append'


class DatasetFormations(enum.Enum):
    """ How a dataset is organized and interpreted
    """
    # formation that is compatible with official huggingface dataset, which
    # organizes whole dataset into one single (zip) file.
    hf_compatible = 1
    # native modelscope formation that supports, among other things,
    # multiple files in a dataset
    native = 2
    # for local meta cache mark
    formation_mark_ext = '.formation_mark'


DatasetMetaFormats = {
    DatasetFormations.native: ['.json'],
    DatasetFormations.hf_compatible: ['.py'],
}


class ModelFile(object):
    CONFIGURATION = 'configuration.json'
    CONFIGURATION_YAML = 'configuration.yaml'
    README = 'README.md'
    TF_SAVED_MODEL_FILE = 'saved_model.pb'
    TF_GRAPH_FILE = 'tf_graph.pb'
    TF_CHECKPOINT_FOLDER = 'tf_ckpts'
    TF_CKPT_PREFIX = 'ckpt-'
    TORCH_MODEL_FILE = 'pytorch_model.pt'
    TORCH_MODEL_BIN_FILE = 'pytorch_model.bin'
    VOCAB_FILE = 'vocab.txt'
    ONNX_MODEL_FILE = 'model.onnx'
    LABEL_MAPPING = 'label_mapping.json'
    TRAIN_OUTPUT_DIR = 'output'
    TRAIN_BEST_OUTPUT_DIR = 'output_best'
    TS_MODEL_FILE = 'model.ts'
    YAML_FILE = 'model.yaml'
    TOKENIZER_FOLDER = 'tokenizer'
    CONFIG = 'config.json'


class Invoke(object):
    KEY = 'invoked_by'
    PRETRAINED = 'from_pretrained'
    PIPELINE = 'pipeline'
    TRAINER = 'trainers'
    LOCAL_TRAINER = 'local_trainer'
    PREPROCESSOR = 'preprocessor'


class ThirdParty(object):
    KEY = 'third_party'
    EASYCV = 'easycv'
    ADASEQ = 'adaseq'
    ADADET = 'adadet'


class ConfigFields(object):
    """ First level keyword in configuration file
    """
    framework = 'framework'
    task = 'task'
    pipeline = 'pipeline'
    model = 'model'
    dataset = 'dataset'
    preprocessor = 'preprocessor'
    train = 'train'
    evaluation = 'evaluation'
    postprocessor = 'postprocessor'


class ConfigKeys(object):
    """Fixed keywords in configuration file"""
    train = 'train'
    val = 'val'
    test = 'test'


class Requirements(object):
    """Requirement names for each module
    """
    protobuf = 'protobuf'
    sentencepiece = 'sentencepiece'
    sklearn = 'sklearn'
    scipy = 'scipy'
    timm = 'timm'
    tokenizers = 'tokenizers'
    tf = 'tf'
    torch = 'torch'


class Frameworks(object):
    tf = 'tensorflow'
    torch = 'pytorch'
    kaldi = 'kaldi'


DEFAULT_MODEL_REVISION = None
MASTER_MODEL_BRANCH = 'master'
DEFAULT_REPOSITORY_REVISION = 'master'
DEFAULT_DATASET_REVISION = 'master'
DEFAULT_DATASET_NAMESPACE = 'modelscope'
DEFAULT_DATA_ACCELERATION_ENDPOINT = 'https://oss-accelerate.aliyuncs.com'


class ModeKeys:
    TRAIN = 'train'
    EVAL = 'eval'
    VALID = 'valid'
    INFERENCE = 'inference'


class LogKeys:
    ITER = 'iter'
    ITER_TIME = 'iter_time'
    EPOCH = 'epoch'
    LR = 'lr'  # learning rate
    MODE = 'mode'
    DATA_LOAD_TIME = 'data_load_time'
    ETA = 'eta'  # estimated time of arrival
    MEMORY = 'memory'
    LOSS = 'loss'





class ColorCodes:
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


class Devices:
    """device used for training and inference"""
    cpu = 'cpu'
    gpu = 'gpu'


# Supported extensions for text dataset.
EXTENSIONS_TO_LOAD = {
    'csv': 'csv',
    'tsv': 'csv',
    'json': 'json',
    'jsonl': 'json',
    'parquet': 'parquet',
    'txt': 'text'
}


class DatasetPathName:
    META_NAME = 'meta'
    DATA_FILES_NAME = 'data_files'
    LOCK_FILE_NAME_ANY = 'any'
    LOCK_FILE_NAME_DELIMITER = '-'


class MetaDataFields:
    ARGS_BIG_DATA = 'big_data'


DatasetVisibilityMap = {1: 'private', 3: 'internal', 5: 'public'}


class DistributedParallelType(object):
    """Parallel Strategies for Distributed Models"""
    DP = 'data_parallel'
    TP = 'tensor_model_parallel'
    PP = 'pipeline_model_parallel'


class DatasetTensorflowConfig:
    BATCH_SIZE = 'batch_size'
    DEFAULT_BATCH_SIZE_VALUE = 5


class VirgoDatasetConfig:

    default_virgo_namespace = 'default_namespace'

    default_dataset_version = '1'

    env_virgo_endpoint = 'VIRGO_ENDPOINT'

    # Columns for meta request
    meta_content = 'metaContent'
    sampling_type = 'samplingType'

    # Columns for meta content
    col_id = 'id'
    col_meta_info = 'meta_info'
    col_analysis_result = 'analysis_result'
    col_external_info = 'external_info'
    col_cache_file = 'cache_file'


DEFAULT_MAXCOMPUTE_ENDPOINT = 'http://service-corp.odps.aliyun-inc.com/api'


class MaxComputeEnvs:

    ACCESS_ID = 'ODPS_ACCESS_ID'

    ACCESS_SECRET_KEY = 'ODPS_ACCESS_SECRET_KEY'

    PROJECT_NAME = 'ODPS_PROJECT_NAME'

    ENDPOINT = 'ODPS_ENDPOINT'
