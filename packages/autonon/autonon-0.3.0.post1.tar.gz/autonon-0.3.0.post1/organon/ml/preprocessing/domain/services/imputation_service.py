"""Includes ImputationService class."""
from typing import List, Union, Dict, Type

import pandas as pd
# this import must stay: https://github.com/scikit-learn/scikit-learn/issues/16833
# noinspection PyUnresolvedReferences
from sklearn.experimental import enable_iterative_imputer  # pylint: disable=unused-import
from sklearn.impute import IterativeImputer
from sklearn.impute import SimpleImputer

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.fl.logging.helpers.log_helper import LogHelper
from organon.ml.common.helpers.parameter_helper import get_params
from organon.ml.preprocessing.domain.objects.imputation_fit_output import ImputationFitOutput
from organon.ml.preprocessing.settings.enums.imputer_type import ImputerType
from organon.ml.preprocessing.settings.objects.imputation_settings import ImputationSettings


class ImputationService:
    """Service for null value imputation"""

    def __init__(self, settings: ImputationSettings):
        self.settings = settings
        self.fit_output: ImputationFitOutput = None
        self.numerical_col_list: List = []
        self.categorical_col_list: List = []

    def fit(self) -> ImputationFitOutput:
        """Fits train data by categorical and numeric imputers based on whether a col is numeric or not"""
        self._fill_column_lists()
        fit_output = ImputationFitOutput()
        fit_output.numerical_imputer = {}
        fit_output.categorical_imputer = {}
        categorical_imputer = self._get_imputer(self.settings.categorical_data_method)
        categorical_imputer_params = self._get_params(self.settings.categorical_data_method,
                                                      self.settings.c_strategy, self.settings.c_missing_values,
                                                      self.settings.c_fill_value)
        for col in self.categorical_col_list:
            imputer = categorical_imputer(**categorical_imputer_params)
            imputer.fit(self.settings.train_data[col].values.reshape(-1, 1))
            fit_output.categorical_imputer[col] = imputer
        numerical_imputer = self._get_imputer(self.settings.numeric_data_method)
        numerical_imputer_params = self._get_params(self.settings.numeric_data_method, self.settings.n_strategy,
                                                    self.settings.n_missing_values, self.settings.n_fill_value)

        if self.settings.numeric_data_method == ImputerType.SIMPLE:
            for col in self.numerical_col_list:
                imputer = numerical_imputer(**numerical_imputer_params)
                imputer.fit(self.settings.train_data[col].values.reshape(-1, 1))
                fit_output.numerical_imputer[col] = imputer
        else:
            imputer = numerical_imputer(**numerical_imputer_params)
            imputer.fit(self.settings.train_data[self.numerical_col_list])
            fit_output.numerical_imputer = imputer
        self.fit_output = fit_output
        return fit_output

    @staticmethod
    def _get_imputer(imputing_method: ImputerType) -> Union[Type[SimpleImputer], Type[IterativeImputer]]:
        if imputing_method is ImputerType.SIMPLE:
            return SimpleImputer
        return IterativeImputer

    @staticmethod
    def _get_params(imputing_method: ImputerType, strategy: str,
                    missing_values: Union[int, float, str, None],
                    fill_value: Union[float, str, int]) -> Dict:
        if imputing_method is ImputerType.SIMPLE:
            return get_params({"strategy": strategy, "missing_values": missing_values, "fill_value": fill_value})
        return get_params({"initial_strategy": strategy, "missing_values": missing_values})

    def transform(self, data: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:
        """Fills missing values in data and return it."""
        if self.fit_output is None:
            raise ValueError("Imputer not fitted yet. Run fit method first.")
        if not inplace:
            trans_data = data.copy()
        else:
            trans_data = data
        different_columns = [col for col in trans_data.columns if col not in self.settings.train_data.columns]
        if different_columns:
            raise ValueError(f"These columns are not found in the train data: {', '.join(different_columns)}.")
        if self.settings.included_columns is None:
            different_typed_columns = [col for col in trans_data if
                                       (get_column_native_type(trans_data, col) != get_column_native_type(
                                           self.settings.train_data, col))]
        else:
            different_typed_columns = [col for col in data if
                                       (get_column_native_type(trans_data, col) != get_column_native_type(
                                           self.settings.train_data, col)) and
                                       (col in self.settings.included_columns)]
        if different_typed_columns:
            raise ValueError(
                f"Type of these columns are different in the train data: {', '.join(different_typed_columns)}.")
        categorical_col_list = [col for col in trans_data.columns if col in self.categorical_col_list]
        numerical_col_list = [col for col in trans_data.columns if col in self.numerical_col_list]
        for col in categorical_col_list:
            self._try_set_col_after_transform(trans_data, col, self.fit_output.categorical_imputer[col])
        if isinstance(self.fit_output.numerical_imputer, IterativeImputer):
            if numerical_col_list != self.numerical_col_list:
                raise ValueError("Transformation numeric columns do not match train numeric columns.")
            trans_data[self.numerical_col_list] = self.fit_output.numerical_imputer.transform(
                trans_data[self.numerical_col_list])
        else:
            for col in numerical_col_list:
                self._try_set_col_after_transform(trans_data, col, self.fit_output.numerical_imputer[col])
        return trans_data

    @classmethod
    def _try_set_col_after_transform(cls, trans_data: pd.DataFrame, col: str, imputer):
        transformed_arr = imputer.transform(trans_data[[col]])
        if transformed_arr.shape[1] != 0:
            trans_data[col] = transformed_arr
        else:
            if trans_data[col].isna().all():
                LogHelper.warning(f"Column {col} could not be transformed by imputer since all values are NaN.")

    def _fill_column_lists(self):
        if self.settings.included_columns is None:
            columns = self.settings.train_data.columns
        else:
            columns = self.settings.included_columns
        for col in columns:
            col_type = get_column_native_type(self.settings.train_data, col)
            if col_type == ColumnNativeType.String:
                self.categorical_col_list.append(col)
            elif col_type == ColumnNativeType.Numeric:
                self.numerical_col_list.append(col)
