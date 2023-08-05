"""Includes FeatureReductionService class"""
from typing import List

from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.domain.reductions.high_correlated_feature_reduction import \
    HighCorrelatedFeatureReduction
from organon.ml.feature_reduction.domain.reductions.null_feature_reduction import NullFeatureReduction
from organon.ml.feature_reduction.domain.reductions.similar_distribution_feature_reduction import \
    SimilarDistributionFeatureReduction
from organon.ml.feature_reduction.domain.reductions.stability_feature_reduction import StabilityFeatureReduction
from organon.ml.feature_reduction.domain.reductions.univariate_performance_feature_reduction import \
    UnivariatePerformanceFeatureReduction
from organon.ml.feature_reduction.settings.objects.base_feature_reduction_settings import BaseFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.high_correlated_feature_reduction_settings import \
    HighCorrelatedFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.null_feature_reduction_settings import NullFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.similar_distribution_feature_reduction_settings import \
    SimilarDistributionFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.stability_feature_reduction_settings import \
    StabilityFeatureReductionSettings
from organon.ml.feature_reduction.settings.objects.univariate_performance_feature_reduction_settings import \
    UnivariatePerformanceFeatureReductionSettings


class FeatureReductionService:
    """Domain service for feature reduction"""

    @classmethod
    def get_reduction_classes_ordered(cls):
        """Returns all control classes for executor
        """
        # NOTE: Please do not change dict order. Because order is important!
        feature_reduction_dict = {
            NullFeatureReductionSettings: NullFeatureReduction,
            StabilityFeatureReductionSettings: StabilityFeatureReduction,
            UnivariatePerformanceFeatureReductionSettings: UnivariatePerformanceFeatureReduction,
            SimilarDistributionFeatureReductionSettings: SimilarDistributionFeatureReduction,
            HighCorrelatedFeatureReductionSettings: HighCorrelatedFeatureReduction
        }
        return feature_reduction_dict

    @classmethod
    def execute(cls, settings: List[BaseFeatureReductionSettings]) -> List[FeatureReductionOutput]:
        """
        Executes feature reduction with given feature reduction type and settings.
        :param settings:
        :return:
        """

        feature_reduction_dict = cls.get_reduction_classes_ordered()
        result_list: List[FeatureReductionOutput] = []
        performance_result = None
        for feature_reduction_settings, feature_reduction_settings_service in feature_reduction_dict.items():
            for setting in settings:
                if isinstance(setting, feature_reduction_settings):
                    if isinstance(setting, UnivariatePerformanceFeatureReductionSettings):
                        result = feature_reduction_settings_service(setting).execute()
                        performance_result = result.univariate_performance_result
                        result_list.append(result)
                    if isinstance(setting, SimilarDistributionFeatureReductionSettings):
                        setting.univariate_performance_result = performance_result
                    if isinstance(setting, HighCorrelatedFeatureReductionSettings):
                        setting.univariate_performance_result = performance_result
                    if isinstance(setting, UnivariatePerformanceFeatureReductionSettings):
                        continue
                    result_list.append(feature_reduction_settings_service(setting).execute())
        return result_list
