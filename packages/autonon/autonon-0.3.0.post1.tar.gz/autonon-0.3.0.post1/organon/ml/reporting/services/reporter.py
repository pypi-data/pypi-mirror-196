"""Includes Reporter class."""
from typing import Union

import pandas as pd

from organon.ml.common.enums.target_type import TargetType
from organon.ml.common.helpers.user_input_service_helper import get_enum
from organon.ml.reporting.domain.objects.binary_report import BinaryReport
from organon.ml.reporting.domain.objects.multiclass_report import MulticlassReport
from organon.ml.reporting.domain.objects.regression_report import RegressionReport
from organon.ml.reporting.domain.services.base_reporter_service import BaseReporterService
from organon.ml.reporting.domain.services.binary_reporter_service import BinaryReporterService
from organon.ml.reporting.domain.services.multiclass_reporter_service import MulticlassReporterService
from organon.ml.reporting.domain.services.regression_reporter_service import RegressionReporterService
from organon.ml.reporting.settings.objects.reporter_settings import ReporterSettings


class Reporter:
    """Modelling performance reporter"""

    def __init__(self, data: pd.DataFrame, target_column: str, score_column: str, target_type: str,
                 id_str_column: str = None, split_column: str = None, num_bins: int = 10):
        # pylint: disable=too-many-arguments
        self._settings = ReporterSettings(data, target_column, score_column, get_enum(target_type, TargetType),
                                          id_str_column, split_column, num_bins)
        self.report: Union[BinaryReport, MulticlassReport, RegressionReport] = None

    def execute(self):
        """Generates and returns report"""
        service = self._get_reporter_service()
        self.report = service.execute(self._settings)
        return self.report

    def _get_reporter_service(self) -> BaseReporterService:
        if self._settings.target_type == TargetType.BINARY:
            return BinaryReporterService()
        if self._settings.target_type == TargetType.MULTICLASS:
            return MulticlassReporterService()
        return RegressionReporterService()
