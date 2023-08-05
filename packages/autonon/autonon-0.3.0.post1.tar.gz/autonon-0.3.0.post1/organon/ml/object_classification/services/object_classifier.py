"""Includes ObjectClassifier class."""
from typing import Optional, Tuple

from organon.ml.common.enums.classification_type import ClassificationType
from organon.ml.common.enums.pretrained_model_type import PretrainedModelType
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.object_classification.domain.objects.fine_tuning_settings import FineTuningSettings
from organon.ml.object_classification.domain.objects.object_clf_settings import ObjectClfSettings
from organon.ml.object_classification.domain.objects.pretrained_model_settings import PretrainedModelSettings
from organon.ml.object_classification.domain.objects.transfer_learning_settings import TransferLearningSettings
from organon.ml.object_classification.domain.services.object_classification_service import ObjectClassificationService


class ObjectClassifier:
    """Image object classifier"""

    def __init__(self, train_data_dir: str, clf_mode: str, validation_data_dir: str = None,
                 validation_data_ratio: float = 0.2, image_size: Tuple[int, int] = (150, 150),
                 batch_size: int = 50, image_data_gen_args: dict = None, random_seed: int = None):
        # pylint: disable=too-many-arguments
        clf_mode_enum = get_enum(clf_mode, ClassificationType)
        self._settings = ObjectClfSettings(train_data_dir, clf_mode_enum, validation_data_dir=validation_data_dir,
                                           validation_data_ratio=validation_data_ratio, image_size=image_size,
                                           image_data_gen_args=image_data_gen_args,
                                           batch_size=batch_size, random_seed=random_seed)

        self._service: ObjectClassificationService = None
        self._settings: ObjectClfSettings = None
        self._fine_tuning_settings: FineTuningSettings = None
        self._transfer_lrn_settings: TransferLearningSettings = None
        self._pretrained_model_settings: PretrainedModelSettings = None

    def fit(self):
        """Fits classifier"""
        self._set_full_settings()
        self._service = ObjectClassificationService(self._settings)
        self._service.fit()

    def predict(self, directory: str):
        """Predict object in image"""
        return self._service.predict(directory)

    def predict_proba(self, directory: str):
        """Predict probabilities for object in image"""
        return self._service.predict_proba(directory)

    def _set_full_settings(self):
        if self._fine_tuning_settings is not None:
            self._settings.fine_tuning_settings = self._fine_tuning_settings
        if self._transfer_lrn_settings is not None:
            self._settings.transfer_learning_settings = self._transfer_lrn_settings
        if self._pretrained_model_settings is not None:
            self._settings.pretrained_model_settings = self._pretrained_model_settings

    def set_fine_tuning_settings(self, epoch: int = 10, early_stopping_patience: int = 2, early_stopping_min_delta=0):
        """Sets fine tuning settings for fitting"""
        self._fine_tuning_settings = FineTuningSettings(epoch, early_stopping_patience, early_stopping_min_delta)

    def set_transfer_learning_settings(self, epoch: int = 20, early_stopping: int = 2, optimizer: str = "adam",
                                       steps_per_epoch: int = None):
        """Sets transfer learning settings for fitting"""
        self._transfer_lrn_settings = TransferLearningSettings(epoch, early_stopping, optimizer, steps_per_epoch)

    def set_pretrained_model_settings(self, model: str = PretrainedModelType.XCEPTION.name,
                                      weights: Optional[str] = "imagenet"):
        """Sets pretrained model settings for fitting"""
        model_enum_val = get_enum(model, PretrainedModelType)
        self._pretrained_model_settings = PretrainedModelSettings(model_enum_val, weights)
