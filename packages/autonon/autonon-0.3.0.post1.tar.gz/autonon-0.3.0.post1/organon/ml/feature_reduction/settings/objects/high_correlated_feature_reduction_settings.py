"""Includes HighCorrelatedFeatureReductionSettings class."""
from dataclasses import dataclass
from typing import Dict

from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import BaseFeatureReductionSettings


@dataclass
class HighCorrelatedFeatureReductionSettings(BaseFeatureReductionSettings):
    """Settings for high correlated feature reduction"""
    target_type: TargetType = None
    target_column_name: str = None
    performance_metric: str = None
    correlation_threshold: float = None
    univariate_performance_result: Dict[str, float] = None
    random_state: int = None
