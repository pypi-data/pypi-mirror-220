from typing import TYPE_CHECKING

from weathon.dl.utils.import_utils import LazyImportModule

if TYPE_CHECKING:
    from .text_classification.trainer import JDTextClassificationTrainer

else:
    _import_structure = {
        'text_classification.trainers': ['JDTextClassificationTrainer'],
    }

    import sys

    sys.modules[__name__] = LazyImportModule(
        __name__,
        globals()['__file__'],
        _import_structure,
        module_spec=__spec__,
        extra_objects={},
    )
