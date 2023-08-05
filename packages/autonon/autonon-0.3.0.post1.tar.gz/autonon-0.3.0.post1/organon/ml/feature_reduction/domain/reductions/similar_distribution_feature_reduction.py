""" This module includes SimilarDistributionFeatureReduction"""
from typing import List, Dict

import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.model_selection import cross_val_score

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.ml.common.enums.target_type import TargetType
from organon.ml.feature_reduction.domain.enums.feature_reduction_types import FeatureReductionType
from organon.ml.feature_reduction.domain.objects.feature_reduction_output import FeatureReductionOutput
from organon.ml.feature_reduction.domain.objects.numeric_column_stats import NumericColumnStats
from organon.ml.feature_reduction.domain.reductions.base_feature_reduction import BaseFeatureReduction
from organon.ml.feature_reduction.settings.objects.similar_distribution_feature_reduction_settings import \
    SimilarDistributionFeatureReductionSettings


class SimilarDistributionFeatureReduction(BaseFeatureReduction):
    """SimilarDistributionFeatureReduction class"""

    def _execute_reduction(self, settings: SimilarDistributionFeatureReductionSettings) -> FeatureReductionOutput:
        data = settings.data
        numeric_columns = [col for col in data.columns if
                           (get_column_native_type(data, col) == ColumnNativeType.Numeric)
                           and (col != settings.target_column_name)
                           and (data[col].nunique() > settings.nunique_count)]
        numeric_columns_stats = self._get_stats(data, numeric_columns)
        similar_distribution_columns = self._get_similar_distribution_columns(numeric_columns_stats)
        reduced_columns = self._find_reduced_columns(settings, similar_distribution_columns)
        settings.data.drop(reduced_columns, axis=1, inplace=True)
        output = FeatureReductionOutput()
        output.feature_reduction_type = FeatureReductionType.SIMILAR_DISTRIBUTION
        output.reduced_column_list = reduced_columns
        return output

    @staticmethod
    def _get_stats(data: pd.DataFrame, numeric_columns: List[str]) -> List[NumericColumnStats]:
        """
        Return numeric column stats which includes mean,std, percentile 25, percentile 50, percentile 75.
        Parameters
        ----------
        data
        numeric_columns

        Returns
        -------
        Return numeric columns stats list
        """

        stats_df = data[numeric_columns].describe()
        numeric_columns_stats = []
        for col in numeric_columns:
            numeric_column_stats = NumericColumnStats(col, stats_df[col]["mean"], stats_df[col]["std"],
                                                      stats_df[col]["25%"],
                                                      stats_df[col]["50%"],
                                                      stats_df[col]["75%"])
            numeric_columns_stats.append(numeric_column_stats)
        return numeric_columns_stats

    @staticmethod
    def _get_similar_distribution_columns(numeric_columns_stats: List[NumericColumnStats]) -> Dict[str, List[str]]:
        """
        Finds columns with similar distribution using numerical column statistics.        Parameters
        ----------
        numeric_columns_stats

        Returns
        -------
        Returns columns with the same distribution.
        """
        similar_distribution_columns = {}

        similar_distribution_columns_set = set()
        for count, value in enumerate(numeric_columns_stats):
            if value.column_name in similar_distribution_columns_set:
                continue
            column_list = []
            column_list.append(numeric_columns_stats[count].column_name)
            for j in range(count + 1, len(numeric_columns_stats)):

                if numeric_columns_stats[count] == numeric_columns_stats[j]:
                    column_list.append(numeric_columns_stats[j].column_name)
                    similar_distribution_columns_set.add(numeric_columns_stats[j].column_name)

            similar_distribution_columns[numeric_columns_stats[count].column_name] = column_list
        return similar_distribution_columns

    def _find_reduced_columns(self, settings: SimilarDistributionFeatureReductionSettings,
                              similar_distribution_columns: Dict[str, List[str]]) -> List[str]:
        """
        Find reduced columns.
        Parameters
        ----------
        settings
        similar_distribution_columns
        numeric_columns_list

        Returns
        -------
        Returns columns list which reduced.
        """
        reduced_columns = []
        if settings.target_column_name is not None and settings.target_type is not None:
            reduced_columns = self._get_reduced_columns_via_performance(settings, similar_distribution_columns)
            return reduced_columns

        for column_list in similar_distribution_columns.values():
            column_list.sort()
            reduced_columns.extend(column_list[1:])
        return reduced_columns

    @staticmethod
    def _get_reduced_columns_via_performance(
            settings: SimilarDistributionFeatureReductionSettings,
            similar_distribution_columns: Dict[str, List[str]]) -> List[str]:
        """
        Finds the reduced column using the univariate performance result.
        Parameters
        ----------
        settings
        similar_distribution_columns

        Returns
        -------
        Returns columns list which reduced.

        """
        data = settings.data
        target_type = settings.target_type.name
        target_column_name = settings.target_column_name

        model = SimilarDistributionFeatureReduction._get_model(target_type, settings.random_state)

        reduced_columns = []
        for column_list in similar_distribution_columns.values():
            score_result = {}
            if settings.univariate_performance_result is None:
                for column in column_list:
                    score = cross_val_score(model, data[[column]], data[target_column_name], cv=3,
                                            scoring=settings.performance_metric).mean()
                    score_result[column] = score
            else:
                for column in column_list:
                    score_result[column] = settings.univariate_performance_result[column]
            best_score_column = max(score_result, key=score_result.get)
            for column in column_list:
                if column != best_score_column:
                    reduced_columns.append(column)
        return reduced_columns

    @staticmethod
    def _get_model(target_type: str, random_state: int):
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
            model = LGBMClassifier(random_state=random_state)
        else:
            model = LGBMRegressor(random_state=random_state)
        return model

    def get_description(self) -> str:
        return "Similar Distribution Feature Reduction"
