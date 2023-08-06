from typing import TYPE_CHECKING

from weathon.dl.utils.import_utils import LazyImportModule

if TYPE_CHECKING:
    from .nlp.text_classification import JDTextClassificationTrainer
    from .cv.ocr import OcrDetectionTrainer
else:
    _import_structure = {
        'nlp.text_classification': ['JDTextClassificationTrainer'],

        'cv.ocr': ['OcrDetectionTrainer']
    }

    import sys

    sys.modules[__name__] = LazyImportModule(
        __name__,
        globals()['__file__'],
        _import_structure,
        module_spec=__spec__,
        extra_objects={},
    )
