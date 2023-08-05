"""Includes TransferLearningSettings class"""


class TransferLearningSettings:
    """Settings for transfer learning in object classification"""

    def __init__(self, epoch: int = 20, early_stopping: int = 2, optimizer: str = "adam", steps_per_epoch: int = None):
        self.epoch = epoch
        self.early_stopping = early_stopping
        self.optimizer = optimizer
        self.steps_per_epoch = steps_per_epoch
