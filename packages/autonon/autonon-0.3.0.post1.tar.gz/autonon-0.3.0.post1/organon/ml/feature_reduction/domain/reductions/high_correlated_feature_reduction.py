""" This module includes HighCorrelatedFeatureReduction"""
from typing import List, Tuple

import random
import pandas as pd
import numpy as np
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.model_selection import cross_val_score

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.domain.reductions.base_feature_reduction import BaseFeatureReduction
from organon.ml.feature_reduction.settings.objects.high_correlated_feature_reduction_settings import \
    HighCorrelatedFeatureReductionSettings


class HighCorrelatedFeatureReduction(BaseFeatureReduction):
    """HighCorrelatedFeatureReduction class"""

    def _execute_reduction(self, settings: HighCorrelatedFeatureReductionSettings) -> FeatureReductionOutput:
        data = settings.data
        numeric_columns = [col for col in data.columns if
                           (get_column_native_type(data, col) == ColumnNativeType.Numeric)
                           and (col != settings.target_column_name)]
        high_correlated_columns_info = self._get_high_correlated_columns(data, numeric_columns,
                                                                         settings.correlation_threshold)
        reduced_columns = self._find_reduced_columns(settings, high_correlated_columns_info)
        settings.data.drop(reduced_columns, axis=1, inplace=True)
        output = FeatureReductionOutput()
        output.feature_reduction_type = FeatureReductionType.HIGH_CORRELATION
        output.reduced_column_list = reduced_columns
        return output

    @staticmethod
    def _get_high_correlated_columns(data: pd.DataFrame, numeric_columns: List[str],
                                     correlation_threshold: float) -> List[Tuple[str, str]]:
        """
        Find high correlated numeric features
        Parameters
        ----------
        data
        numeric_columns
        correlation_threshold

        Returns
        -------

        """

        corr_matrix = data[numeric_columns].corr(method="spearman").abs()
        high_corr_var = np.where(corr_matrix > correlation_threshold)
        high_corr_var = [(corr_matrix.columns[x], corr_matrix.columns[y]) for x, y in zip(*high_corr_var) if
                         x != y and x < y]
        return high_corr_var

    def _find_reduced_columns(self, settings: HighCorrelatedFeatureReductionSettings,
                              high_correlated_columns_info: List[Tuple[str, str]]) -> List[str]:
        """
        Find reduced columns.
        Parameters
        ----------
        settings
        high_correlated_columns_info


        Returns
        -------
        Returns columns list which reduced.
        """
        reduced_columns = []
        if settings.target_column_name is not None and settings.target_type is not None:
            reduced_columns = self._get_reduced_columns_via_performance(settings, high_correlated_columns_info)
            return reduced_columns

        for column_pair in high_correlated_columns_info:
            value = random.sample(list([column_pair[0], column_pair[1]]), 1)[0]
            if value not in reduced_columns:
                reduced_columns.append(value)

        return reduced_columns

    @staticmethod
    def _get_reduced_columns_via_performance(
            settings: HighCorrelatedFeatureReductionSettings,
            high_correlated_columns_info: List[Tuple[str, str]]) -> List[str]:
        """
        Finds the reduced column using the univariate performance result.
        Parameters
        ----------
        settings
        high_correlated_columns_info

        Returns
        -------
        Returns columns list which reduced.

        """
        data = settings.data
        target_type = settings.target_type.name
        target_column_name = settings.target_column_name

        model = HighCorrelatedFeatureReduction._get_model(target_type)

        reduced_columns = []
        for column_pair in high_correlated_columns_info:
            score_result = {}
            if settings.univariate_performance_result is None:
                for column in column_pair:
                    score = cross_val_score(model, data[[column]], data[target_column_name], cv=3,
                                            scoring=settings.performance_metric).mean()
                    score_result[column] = score
            else:
                for column in column_pair:
                    score_result[column] = settings.univariate_performance_result[column]
            best_score_column = max(score_result, key=score_result.get)
            for column in column_pair:
                if column != best_score_column:
                    if column not in reduced_columns:
                        reduced_columns.append(column)
        return reduced_columns

    @staticmethod
    def _get_model(target_type: str):
        """
        Return Model with using target type.
        Parameters
        ----------
        target_type

        Returns
        -------
        Returns Model object for LGBM
        """

        if target_type in (TargetType.BINARY.name, TargetType.MULTICLASS.name):
            model = LGBMClassifier(random_state=42)
        else:
            model = LGBMRegressor(random_state=42)
        return model

    def get_description(self) -> str:
        return "High Correlated Feature Reduction"
