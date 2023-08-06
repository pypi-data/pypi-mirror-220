from weathon.dl.utils.constants import TrainerStages, Priority
from weathon.dl.utils.import_utils import is_method_overridden


class BaseHook:
    """
    The Hook base class of any modelscope trainers. You can build your own hook inherited from this class.

    回调函数支持列表：
    LrSchedulerHook lr衰减策略
    PlateauLrSchedulerHook lr衰减策略
    OptimizerHook 优化器策略
    TorchAMPOptimizerHook 优化器策略
    CheckpointHook 模型存储策略
    BestCkptSaverHook 模型存储策略
    EvaluationHook 校验策略
    TextLoggerHook 日志策略
    IterTimerHook 训练耗时策略
    TensorboardHook tensorboard实验记录策略
    DDPHook 数据并行策略
    MegatronHook megatron训练策略
    DeepSpeedHook deepspeed训练策略
    """

    stages = (
              TrainerStages.before_init,
              TrainerStages.after_init, 
              TrainerStages.before_run,
              TrainerStages.before_train_epoch,
              TrainerStages.before_train_iter, 
              TrainerStages.after_train_iter,
              TrainerStages.after_train_epoch, 

              TrainerStages.before_val, 
              TrainerStages.before_val_epoch,
              TrainerStages.before_val_iter, 
              TrainerStages.after_val_iter,
              TrainerStages.after_val_epoch, 
              TrainerStages.after_val,
              TrainerStages.after_run
            )

    PRIORITY = Priority.NORMAL

    def before_init(self, trainer):
        """
        Will be called at the begin of the trainers's `__init__` method
        """
        pass

    def after_init(self, trainer):
        """
        Will be called at the end of the trainers's `__init__` method
        """
        pass

    def before_run(self, trainer):
        """
        Will be called before trainers loop begins.
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        pass

    def after_run(self, trainer):
        """
        Will be called after trainers loop end.
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        pass

    def before_val(self, trainer):
        """
        Will be called before eval loop begins.
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        pass

    def after_val(self, trainer):
        """
        Will be called after eval loop end.
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        pass

    def before_epoch(self, trainer):
        """
        Will be called before every epoch begins.
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        pass

    def after_epoch(self, trainer):
        """
        Will be called after every epoch ends.
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        pass

    def before_iter(self, trainer):
        """
        Will be called before every loop begins.
        Args:
            trainer: The trainers instance.

        Returns: None
        """
        pass

    def after_iter(self, trainer):
        """
        Will be called after every loop ends.
        Args:
            trainer: The trainers instance.

        Returns: None
        """
        pass

    def before_train_epoch(self, trainer):
        """
        Will be called before every train epoch begins. Default call ``self.before_epoch``
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        self.before_epoch(trainer)

    def before_val_epoch(self, trainer):
        """
        Will be called before every validation epoch begins. Default call ``self.before_epoch``
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        self.before_epoch(trainer)

    def after_train_epoch(self, trainer):
        """
        Will be called after every train epoch ends. Default call ``self.after_epoch``
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        self.after_epoch(trainer)

    def after_val_epoch(self, trainer):
        """
        Will be called after every validation epoch ends. Default call ``self.after_epoch``
        Args:
            trainer: The trainers instance.

        Returns: None

        """
        self.after_epoch(trainer)

    def before_train_iter(self, trainer):
        """
        Will be called before every train loop begins. Default call ``self.before_iter``
        Args:
            trainer: The trainers instance.

        Returns: None
        """
        self.before_iter(trainer)

    def before_val_iter(self, trainer):
        """
        Will be called before every validation loop begins. Default call ``self.before_iter``
        Args:
            trainer: The trainers instance.

        Returns: None
        """
        self.before_iter(trainer)

    def after_train_iter(self, trainer):
        """
        Will be called after every train loop ends. Default call ``self.after_iter``
        Args:
            trainer: The trainers instance.

        Returns: None
        """
        self.after_iter(trainer)

    def after_val_iter(self, trainer):
        """
        Will be called after every validation loop ends. Default call ``self.after_iter``
        Args:
            trainer: The trainers instance.

        Returns: None
        """
        self.after_iter(trainer)

    @staticmethod
    def every_n_epochs(trainer, n):
        """
        Whether to reach every ``n`` epochs
        Returns: bool
        """
        return (trainer.epoch + 1) % n == 0 if n > 0 else False

    @staticmethod
    def every_n_inner_iters(runner, n):
        """
        Whether to reach every ``n`` iterations at every epoch
        Returns: bool
        """
        return (runner.inner_iter + 1) % n == 0 if n > 0 else False

    @staticmethod
    def every_n_iters(trainer, n):
        """
        Whether to reach every ``n`` iterations
        Returns: bool
        """
        return (trainer.iter + 1) % n == 0 if n > 0 else False

    @staticmethod
    def end_of_epoch(trainer):
        """
        Whether to reach the end of every epoch
        Returns: bool
        """
        return trainer.inner_iter + 1 == trainer.iters_per_epoch

    @staticmethod
    def is_last_epoch(trainer):
        """
        Whether to reach the last epoch
        Returns: bool
        """
        return trainer.epoch + 1 == trainer.max_epochs

    @staticmethod
    def is_last_iter(trainer):
        """
        Whether to reach the last iteration in the entire training process
        Returns: bool
        """
        return trainer.iter + 1 == trainer.max_iters

    def get_triggered_stages(self):
        trigger_stages = set()
        for stage in BaseHook.stages:
            if is_method_overridden(stage, BaseHook, self):
                trigger_stages.add(stage)

        return [stage for stage in BaseHook.stages if stage in trigger_stages]

    def state_dict(self):
        return {}

    def load_state_dict(self, state_dict):
        pass
