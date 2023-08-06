import time

from weathon.dl.base import BaseHook
from weathon.dl.registry import HOOKS
from weathon.dl.utils.constants import Priority, LogKeys
from weathon.dl.utils.constants import Hooks



@HOOKS.register_module(module_name=Hooks.IterTimerHook)
class IterTimerHook(BaseHook):
    PRIORITY = Priority.LOW

    def before_epoch(self, trainer):
        self.start_time = time.time()

    def before_iter(self, trainer):
        trainer.log_buffer.update({LogKeys.DATA_LOAD_TIME: time.time() - self.start_time})

    def after_iter(self, trainer):
        trainer.log_buffer.update(
            {LogKeys.ITER_TIME: time.time() - self.start_time})
        self.start_time = time.time()
