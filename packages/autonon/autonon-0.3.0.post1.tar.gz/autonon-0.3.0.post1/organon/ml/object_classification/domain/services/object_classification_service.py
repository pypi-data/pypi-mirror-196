"""Includes ObjectClassificationService class"""
from organon.ml.object_classification.domain.objects.object_clf_settings import ObjectClfSettings


class ObjectClassificationService:
    """Object classification service"""
    def __init__(self, settings: ObjectClfSettings):
        self._settings = settings

    def fit(self):
        """Fit classifier"""

    def predict(self, directory: str):
        """Predict object in image"""

    def predict_proba(self, directory: str):
        """Predict probabilities of object in image"""
