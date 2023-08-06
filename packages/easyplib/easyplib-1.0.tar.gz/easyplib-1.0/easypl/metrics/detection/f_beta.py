from typing import Union, List, Optional, Dict

import numpy as np
import torch

from easypl.metrics.detection.base import BaseDetectionMetric


class FBetaDetection(BaseDetectionMetric):
    """
    Evaluate optimal confidence by F beta metric and return with precision, recall values.

    Attributes
    ----------------
    iou_threshold: Union[float, List[float]]
        Iou threshold/thresholds for boxes.

    confidence: Optional[List[float]]
        Confidence/confidences thresholds or None. If is None then evaluate as arange from 0 to 1 with step 0.05.

    num_classes: Optional[int]
        Number of classes.

    beta: float
        Parameter of F metric.

    eps: float
        Epsilon.

    kwargs
        Torchmetrics Metric args.

    """
    def __init__(
            self,
            iou_threshold: Union[float, List[float]],
            confidence: Optional[List[float]] = None,
            num_classes: Optional[int] = None,
            beta: float = 1.0,
            eps: float = 1e-9,
            **kwargs
    ):
        confidence = confidence if confidence is not None else list(np.arange(0.0, 1.0, 0.05))
        super().__init__(
            iou_threshold=iou_threshold,
            confidence=confidence,
            num_classes=num_classes,
            **kwargs
        )
        self.beta = beta
        self.eps = eps

    def compute(
            self
    ) -> Dict:
        precision = (self.tp / (self.tp + self.fp + self.eps)).mean(-1)
        recall = (self.tp / (self.tp + self.fn + self.eps)).mean(-1)
        fbeta = (1 + self.beta ** 2) * precision * recall / (self.beta ** 2 * precision + recall + self.eps)
        optimal_fbeta, conf_idx = torch.max(fbeta, dim=-1)
        conf = self.confidences[conf_idx]
        optimal_precision = torch.index_select(precision, dim=-1, index=conf_idx)
        optimal_recall = torch.index_select(recall, dim=-1, index=conf_idx)
        return {
            'F{}'.format('{' + '{:.2f}'.format(self.beta) + '}'): optimal_fbeta,
            'precision': optimal_precision,
            'recall': optimal_recall,
            'optimal_confidence': conf
        }
