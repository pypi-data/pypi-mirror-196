"""Includes MulticlassReporterService class."""
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix

from organon.ml.reporting.domain.objects.multiclass_report import MulticlassReport
from organon.ml.reporting.domain.services.base_reporter_service import BaseReporterService
from organon.ml.reporting.settings.objects.reporter_settings import ReporterSettings


class MulticlassReporterService(BaseReporterService[MulticlassReport]):
    """Reporter service for multiclass classification"""

    def execute(self, settings: ReporterSettings) -> MulticlassReport:
        """returns multiclass report"""
        report = MulticlassReport()
        id_str_exists = settings.id_str_column is not None
        split_col_exists = settings.split_column is not None
        group_by_columns = []
        if id_str_exists:
            group_by_columns.append(settings.id_str_column)
        if split_col_exists:
            group_by_columns.append(settings.split_column)
        accuracy_table, confusion_matrix_dict = self._generate_reports(settings, id_str_exists, split_col_exists,
                                                                       group_by_columns)
        report.accuracy = accuracy_table
        report.confusion_matrices = confusion_matrix_dict
        return report

    def _generate_reports(self, settings: ReporterSettings, id_str_exists, split_col_exists, group_by_columns):
        accuracy_table_cols = self._initialize_acc_table_cols(id_str_exists, split_col_exists)
        confusion_matrix_dict = {}
        acc_list = []
        if group_by_columns:
            for groups, indices in settings.data.groupby(group_by_columns).indices.items():
                index_vals = list(set(list(settings.data.loc[indices][settings.target_column].unique()) +
                                      list(settings.data.loc[indices][settings.score_column].unique())))
                index_vals.sort()
                group_tuple = groups if isinstance(groups, tuple) else (groups,)
                group_frame = settings.data.loc[indices]
                confusion_matrix_dict[group_tuple] = pd.DataFrame(
                    data=confusion_matrix(group_frame[settings.target_column], group_frame[settings.score_column],
                                          labels=index_vals), columns=index_vals, index=index_vals)
                acc_score = accuracy_score(group_frame[settings.target_column], group_frame[settings.score_column])
                acc_list.append([*list(group_tuple), *[acc_score]])
            return pd.DataFrame(data=acc_list, columns=accuracy_table_cols), confusion_matrix_dict
        index_vals = settings.data[settings.target_column].unique()
        confusion_matrix_dict[("ALL",)] = pd.DataFrame(
            data=confusion_matrix(settings.data[settings.target_column], settings.data[settings.score_column],
                                  labels=index_vals), columns=index_vals, index=index_vals)
        return pd.DataFrame(data=[accuracy_score(settings.data[settings.target_column],
                                                 settings.data[settings.score_column])],
                            columns=["Accuracy"]), confusion_matrix_dict

    @staticmethod
    def _initialize_acc_table_cols(id_str_exists, split_col_exists):
        columns = ["Accuracy"]
        if split_col_exists:
            columns.insert(0, "Data")
        if id_str_exists:
            columns.insert(0, "IdStr")
        return columns
