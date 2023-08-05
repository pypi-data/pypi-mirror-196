""" This module includes StabilityFeatureReduction"""
from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.domain.reductions.base_feature_reduction import BaseFeatureReduction
from organon.ml.feature_reduction.settings.objects.stability_feature_reduction_settings import \
    StabilityFeatureReductionSettings


class StabilityFeatureReduction(BaseFeatureReduction):
    """StabilityFeatureReduction class"""

    def _execute_reduction(self, settings: StabilityFeatureReductionSettings) -> FeatureReductionOutput:
        data = settings.data
        reduced_columns = [col for col in data.columns if len(data[col].value_counts()) == 1]
        settings.data.drop(reduced_columns, axis=1, inplace=True)
        output = FeatureReductionOutput()
        output.feature_reduction_type = FeatureReductionType.STABILITY
        output.reduced_column_list = reduced_columns
        return output

    def get_description(self) -> str:
        return "Stability Feature Reduction"
