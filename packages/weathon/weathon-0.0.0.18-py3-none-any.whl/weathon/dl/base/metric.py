from abc import ABC, abstractmethod
from typing import Dict


class BaseMetric(ABC):
    """Metric的基类定义非常简单,仅有add和evaluate两个方法。

    不同任务的评价指标参考:task_default_metrics

    
    使用:
    @METRICS.register_module(group_key=default_group, module_name='my-custom-metric')
    class MyCustomMetric(BaseMetric):

        def add(self, outputs, inputs):
            # outputs是模型输出，inputs为模型输入，在这里取出所需要的value并存下来
            eval_results = outputs["result"]
            ground_truths = inputs["label"]
            self.preds.append(eval_results)
            self.labels.append(ground_truths)

        def evaluate(self):
            # 在数据集验证完成时调用，根据add存下来的value进行计算
            from sklearn.metrics import accuracy_score
            from modelscope.metrics.builder import MetricKeys
            return {MetricKeys.ACCURACY: accuracy_score(self.labels, self.preds)}

    """

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def add(self, outputs: Dict, inputs: Dict):
        """ 在每个batch结束时,手机模型的预测和labels
        add方法用于收集每一个mini-batch的模型输入和输出信息,并从中遴选出需要用于计算指标的信息,比如inputs中的labels字段,以及outputs中的logits字段。
        add方法会在每次mini-batch执行完调用,且不存在多线程问题。

        Args:
            outputs: The model prediction outputs.
            inputs: The mini batch inputs from the dataloader.

        Returns: None

        返回格式：
            # 二分类
            {"accuracy": 0.90, "f1":  0.90}

            # 多分类, 其中的f1是兼容性字段,值和macro-f1是相同的
            {"accuracy": 0.90, "f1":  0.90, "macro-f1": 0.90, "micro-f1": 0.90}

        """
        pass

    @abstractmethod
    def evaluate(self):
        """evaluate方法会在整个数据集跑完之后执行,它没有输入参数.
        evaluate内部会对add收集的数值进行汇总和计算,并给出Dict形式的指标输出。

        Returns: The actual metric dict with standard names.

        """
        pass

    @abstractmethod
    def merge(self, other: 'Metric'):
        """ 当数据并行计算时，
        When using data parallel, the data required for different metric calculations

        are stored in their respective Metric classes,

        and we need to merge these data to uniformly calculate metric.

        Args:
            other: Another Metric instance.

        Returns: None

        """
        pass
