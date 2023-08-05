"""Includes NullFeatureReductionSettings class."""
from dataclasses import dataclass

from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import BaseFeatureReductionSettings

@dataclass
class NullFeatureReductionSettings(BaseFeatureReductionSettings):
    """Settings for null feature reduction"""
    null_ratio_threshold: float
