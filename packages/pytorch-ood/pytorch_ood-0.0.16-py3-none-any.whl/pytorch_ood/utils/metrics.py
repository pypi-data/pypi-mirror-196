"""
..  autoclass:: pytorch_ood.utils.OODMetrics
    :members:

"""
from typing import Dict, TypeVar

import numpy as np
import torch
import torchmetrics
from torch import Tensor
from torchmetrics.functional.classification import (
    binary_accuracy,
    binary_auroc,
    binary_roc,
    precision_recall_curve,
)

from .utils import TensorBuffer, is_unknown

Self = TypeVar("Self")


def calibration_error(
    confidence: torch.Tensor, correct: torch.Tensor, p: str = "2", beta: int = 100
) -> float:
    """
    :see Implementation: `GitHub <https://github.com/hendrycks/natural-adv-examples/>`__

    :param confidence: predicted confidence
    :param correct: ground truth
    :param p: p for norm. Can be one of ``1``, ``2``, or ``infty``
    :param beta: target bin size
    :return: calculated calibration error
    """

    confidence = confidence.numpy()
    correct = correct.numpy()

    idxs = np.argsort(confidence)
    confidence = confidence[idxs]
    correct = correct[idxs]
    bins = [[i * beta, (i + 1) * beta] for i in range(len(confidence) // beta)]
    bins[-1] = [bins[-1][0], len(confidence)]

    cerr = 0
    total_examples = len(confidence)
    for i in range(len(bins) - 1):
        bin_confidence = confidence[bins[i][0] : bins[i][1]]
        bin_correct = correct[bins[i][0] : bins[i][1]]
        num_examples_in_bin = len(bin_confidence)

        if num_examples_in_bin > 0:
            difference = np.abs(np.nanmean(bin_confidence) - np.nanmean(bin_correct))

            if p == "2":
                cerr += num_examples_in_bin / total_examples * np.square(difference)
            elif p == "1":
                cerr += num_examples_in_bin / total_examples * difference
            elif p == "infty" or p == "infinity" or p == "max":
                cerr = np.maximum(cerr, difference)
            else:
                assert False, "p must be '1', '2', or 'infty'"

    if p == "2":
        cerr = np.sqrt(cerr)

    return float(cerr)


def aurra(confidence: torch.Tensor, correct: torch.Tensor) -> float:
    """
    :see Implementation: `GitHub <https://github.com/hendrycks/natural-adv-examples/>`__

    :param confidence: predicted confidence values
    :param correct: ground truth

    :return: score
    """
    conf_ranks = np.argsort(confidence.numpy())[::-1]  # indices from greatest to least confidence
    rra_curve = np.cumsum(np.asarray(correct.numpy())[conf_ranks])
    rra_curve = rra_curve / np.arange(1, len(rra_curve) + 1)  # accuracy at each response rate
    return float(np.mean(rra_curve))


def fpr_at_tpr(pred, target, k=0.95):
    """
    Calculate the False Positive Rate at a certain True Positive Rate

    :param pred: outlier scores
    :param target: target label
    :param k: cutoff value
    :return:
    """
    # results will be sorted in reverse order
    fpr, tpr, _ = binary_roc(pred, target)
    idx = torch.searchsorted(tpr, k)
    return fpr[idx]


class OODMetrics(object):
    """
    Calculates various metrics used in OOD detection experiments.

    - AUROC
    - AUPR IN
    - AUPR OUT
    - FPR\\@95TPR

    The interface is similar to ``torchmetrics``.

    .. code :: python

        metrics = OODMetrics()
        outlier_scores = torch.Tensor([0.5, 1.0, -10])
        labels = torch.Tensor([1,2,-1])
        metrics.update(outlier_scores, labels)
        metric_dict = metrics.compute()
    """

    def __init__(self, device="cpu"):
        """
        :param device: where tensors should be stored
        """
        super(OODMetrics, self).__init__()
        self.device = device
        self.buffer = TensorBuffer(device=self.device)

    def update(self: Self, outlier_scores: Tensor, y: Tensor) -> Self:
        """
        Add batch of results to collection.

        :param outlier_scores: outlier score
        :param y: target label
        """
        label = is_unknown(y).detach().to(self.device).long()
        self.buffer.append("scores", outlier_scores)
        self.buffer.append("labels", label)
        return self

    def compute(self) -> Dict[str, float]:
        """
        Calculate metrics

        :return: dictionary with different metrics
        :raise: ValueError if data does not contain IN and OOD points or buffer is empty
        """
        if self.buffer.is_empty():
            raise ValueError("Must be given data to calculate metrics.")

        labels = self.buffer.get("labels").view(-1)
        scores = self.buffer.get("scores").view(-1)

        if len(torch.unique(labels)) != 2:
            raise ValueError("Data must contain IN and OOD samples.")

        scores, scores_idx = torch.sort(scores, stable=True)
        labels = labels[scores_idx]

        auroc = binary_auroc(scores, labels)

        # num_classes=None for binary
        p, r, t = precision_recall_curve(scores, labels, pos_label=1, num_classes=None)
        aupr_in = torchmetrics.functional.auc(r, p)

        p, r, t = precision_recall_curve(-scores, labels, pos_label=0, num_classes=None)
        aupr_out = torchmetrics.functional.auc(r, p)

        fpr = fpr_at_tpr(scores, labels)

        return {
            "AUROC": auroc.item(),
            "AUPR-IN": aupr_in.item(),
            "AUPR-OUT": aupr_out.item(),
            "FPR95TPR": fpr.item(),
        }

    def reset(self: Self) -> Self:
        """
        Resets collected metrics
        """
        self.buffer.clear()
        return self
