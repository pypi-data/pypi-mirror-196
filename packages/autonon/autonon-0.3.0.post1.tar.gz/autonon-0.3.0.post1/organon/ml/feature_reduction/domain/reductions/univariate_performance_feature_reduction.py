""" This module includes UnivariatePerformanceFeatureReduction"""
from typing import List

from lightgbm import LGBMRegressor, LGBMClassifier
from sklearn.model_selection import cross_val_score

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.domain.objects.univariate_performance_reduction_output import \
    UnivariatePerformanceFeatureReductionOutput
from organon.ml.feature_reduction.domain.reductions.base_feature_reduction import BaseFeatureReduction

from organon.ml.feature_reduction.settings.objects.univariate_performance_feature_reduction_settings import \
    UnivariatePerformanceFeatureReductionSettings


class UnivariatePerformanceFeatureReduction(BaseFeatureReduction):
    """UnivariatePerformanceFeatureReduction class"""

    def _execute_reduction(self, settings: UnivariatePerformanceFeatureReductionSettings) -> FeatureReductionOutput:
        data = settings.data
        numeric_columns = [col for col in data.columns if
                           (get_column_native_type(data, col) == ColumnNativeType.Numeric)
                           and (col != settings.target_column_name)]

        output = self._find_reduced_columns(settings, numeric_columns)
        settings.data.drop(output.reduced_column_list, axis=1, inplace=True)
        return output

    @staticmethod
    def _find_reduced_columns(settings: UnivariatePerformanceFeatureReductionSettings,
                              numeric_columns_list: List[str]) -> UnivariatePerformanceFeatureReductionOutput:
        """
        Find reduced columns with using numeric column univariate performance result
        Parameters
        ----------
        settings
        numeric_columns_list

        Returns
        -------
        Return UnivariatePerformanceFeatureReductionOutput
        """
        data = settings.data
        target_type = settings.target_type.name
        target_column_name = settings.target_column_name

        model = UnivariatePerformanceFeatureReduction._get_model(target_type, settings.random_state)
        reduced_columns = []
        score_result = {}
        for column in numeric_columns_list:
            score = cross_val_score(model, data[[column]], data[target_column_name], cv=3,
                                    scoring=settings.performance_metric).mean()
            score_result[column] = score
            if score < settings.univariate_performance_threshold:
                reduced_columns.append(column)
        output = UnivariatePerformanceFeatureReduction._get_output(reduced_columns, score_result)
        return output

    @staticmethod
    def _get_model(target_type: str, random_state: int):
        """
        Return Model with using target type.
        Parameters
        ----------
        target_type
        random_state

        Returns
        -------
        Returns Model object for LGBM
        """

        if target_type in (TargetType.BINARY.name, TargetType.MULTICLASS.name):
            model = LGBMClassifier(random_state=random_state)
        else:
            model = LGBMRegressor(random_state=random_state)
        return model

    @staticmethod
    def _get_output(reduced_columns: List[str], score_result) -> UnivariatePerformanceFeatureReductionOutput:
        """
        Get output for univariate performance feature reduction.
        Parameters
        ----------
        reduced_columns
        score_result

        Returns
        -------
        Returns UnivariatePerformanceFeatureReductionOutput
        """
        output = UnivariatePerformanceFeatureReductionOutput()
        output.feature_reduction_type = FeatureReductionType.UNIVARIATE_PERFORMANCE
        output.reduced_column_list = reduced_columns
        output.univariate_performance_result = score_result
        return output

    def get_description(self) -> str:
        return "Univariate Performance Feature Reduction"
