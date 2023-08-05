"""Includes FeatureReductionSettings class."""
from dataclasses import dataclass

import pandas as pd


@dataclass
class BaseFeatureReductionSettings:
    """Settings for base feature reduction"""
    data: pd.DataFrame
