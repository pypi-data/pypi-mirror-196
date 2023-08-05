"""Includes UnivariatePerformanceFeatureReductionSettings class."""
from dataclasses import dataclass

from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import BaseFeatureReductionSettings

@dataclass
class UnivariatePerformanceFeatureReductionSettings(BaseFeatureReductionSettings):
    """Settings for univariate performance feature reduction"""

    target_type: TargetType
    target_column_name: str
    performance_metric: str
    univariate_performance_threshold: float
    random_state: int = None
