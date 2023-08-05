"""Includes CoarseClassSettings class."""
from dataclasses import dataclass

import pandas as pd

from organon.ml.common.enums.target_type import TargetType


@dataclass
class CoarseClassSettings:
    """Settings for CoarseClass service"""
    fit_data: pd.DataFrame
    target_data: pd.Series
    test_ratio: float
    min_class_size: int
    target_type: TargetType
    max_leaf_nodes: int
    stability_check_data: pd.DataFrame
    stability_check_target_data: pd.Series
    stability_check: bool
    stability_threshold: float
    random_state: int
    positive_class: str
    negative_class: str
