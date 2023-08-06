from typing import TYPE_CHECKING

from weathon.dl.utils.import_utils import LazyImportModule
from .child_tuning_adamw_optimizer import ChildTuningAdamW

if TYPE_CHECKING:
    from .warmup import BaseWarmup, ConstantWarmup, ExponentialWarmup, LinearWarmup

else:
    _import_structure = {
        'warmup':['BaseWarmup', 'ConstantWarmup', 'ExponentialWarmup', 'LinearWarmup']
    }

    import sys

    sys.modules[__name__] = LazyImportModule(
        __name__,
        globals()['__file__'],
        _import_structure,
        module_spec=__spec__,
        extra_objects={},
    )
