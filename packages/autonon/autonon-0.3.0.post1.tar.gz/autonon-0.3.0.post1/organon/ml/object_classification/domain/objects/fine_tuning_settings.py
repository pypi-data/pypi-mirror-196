"""Includes FineTuningSettings class."""


class FineTuningSettings:
    """Settings for fine tuning in object classification"""

    def __init__(self, epoch: int = 10, early_stopping_patience: int = 2, early_stopping_min_delta: int = 0):
        self.epoch = epoch
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_min_delta = early_stopping_min_delta
