""" This module includes BaseFeatureReduction"""
import abc

from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import BaseFeatureReductionSettings


class BaseFeatureReduction(metaclass=abc.ABCMeta):
    """ BaseFeatureReduction class"""

    def __init__(self, settings: BaseFeatureReductionSettings):
        self.settings = settings

    def execute(self) -> FeatureReductionOutput:
        """Execute Feature Reduction"""
        reduction_description = self.get_description()

        LogHelper.info(f"Executing reduction: {reduction_description}")
        results = self._execute_reduction(self.settings)

        LogHelper.info(f"Finished executing reduction: {reduction_description}")
        return results

    @abc.abstractmethod
    def _execute_reduction(self, settings: BaseFeatureReductionSettings) -> FeatureReductionOutput:
        """
        Execute reductions and return reduction output.
        Parameters
        ----------
        settings

        Returns
        -------
        Return feature reduction output.
        """

    @abc.abstractmethod
    def get_description(self) -> str:
        """todo"""
