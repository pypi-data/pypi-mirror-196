"""Includes StabilityFeatureReduction class."""
from dataclasses import dataclass

from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import BaseFeatureReductionSettings

@dataclass
class StabilityFeatureReductionSettings(BaseFeatureReductionSettings):
    """Settings for stability feature reduction"""
