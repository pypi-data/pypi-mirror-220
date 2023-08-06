from weathon.dl.registry import MODELS
from weathon.dl.utils.constants import Tasks
from weathon.dl.utils.constants.metainfo import Heads, Models
from weathon.dl.models.nlp.task_models.fill_mask import ModelForFillMask
from weathon.dl.utils import logger as logging

logger = logging.get_logger()


@MODELS.register_module(Tasks.fill_mask, module_name=Models.bert)
class BertForMaskedLM(ModelForFillMask):

    base_model_type = Models.bert
    head_type = Heads.bert_mlm
