from typing import TYPE_CHECKING

from weathon.dl.utils.import_utils import LazyImportModule

if TYPE_CHECKING:
    from .nlp.text_classification.preprocessor import JDTextClassificationPreprocessor
    from .cv.ocr.preprocessor import Icdar2015Preprocessor

else:
    _import_structure = {
        'nlp.text_classification.preprocessor': ['JDTextClassificationPreprocessor'],
        'cv.ocr.preprocessor':['Icdar2015Preprocessor']
    }

    import sys

    sys.modules[__name__] = LazyImportModule(
        __name__,
        globals()['__file__'],
        _import_structure,
        module_spec=__spec__,
        extra_objects={},
    )
