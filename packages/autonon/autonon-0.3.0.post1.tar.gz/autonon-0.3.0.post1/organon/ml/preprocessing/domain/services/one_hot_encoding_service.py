"""Includes OneHotEncodingService class"""
from typing import List, Dict

import numpy as np
import pandas as pd

from organon.fl.core.enums.column_native_type import ColumnNativeType
from organon.fl.core.helpers.data_frame_helper import get_column_native_type
from organon.fl.mathematics.constants import INT_MAX
from organon.ml.preprocessing.settings.objects.one_hot_encoding_settings import OneHotEncodingSettings


class OneHotEncodingService:
    """Service for one hot encoding"""

    def __init__(self, settings: OneHotEncodingSettings):
        self._settings = settings
        self._categorical_cols = None
        self._features_dict: Dict[str, List[str]] = None
        self._columns_dict: Dict[str, List[str]] = None

    @property
    def features_dict(self):
        """Returns selected features per categorical column"""
        return self._features_dict

    @property
    def columns_dict(self):
        """Returns generated columns per categorical columns (after transform)"""
        return self._columns_dict

    def fit(self, data: pd.DataFrame):
        """Fit encoder"""
        if self._settings.threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if self._settings.max_bin < 0:
            raise ValueError("Maximum number of features cannot be negative.")
        if data is None or data.empty:
            raise ValueError("Train data cannot be null or empty.")
        self._categorical_cols = [col for col in data if get_column_native_type(data, col) == ColumnNativeType.String]
        self._features_dict = {}
        for col in self._categorical_cols:
            self._features_dict[col] = self._get_col_features(data, col, self._settings.threshold,
                                                              self._settings.max_bin)
        return self

    def transform(self, data: pd.DataFrame, inplace: bool = False):
        """Transform data"""
        if self._features_dict is None:
            raise ValueError("Encoder not fitted yet")
        if data is None or data.empty:
            raise ValueError("Transformation data cannot be null or empty.")
        if not inplace:
            trans_data = data.copy()
        else:
            trans_data = data
        different_columns = [col for col in trans_data if
                             (get_column_native_type(trans_data, col) == ColumnNativeType.String and
                              col not in self._categorical_cols)]
        if different_columns:
            raise ValueError(
                f"These columns are not found in the train data or"
                f" their types were not categorical: {', '.join(different_columns)}.")

        generated_cols_per_category = {}
        for col in self._categorical_cols:
            features = self._features_dict[col]
            col_index = trans_data.columns.get_loc(col)
            data, generated_cols = self._append_binary_columns(trans_data, col, features, col_index)
            col_name = self._decide_combined_cat_name(trans_data, col)
            trans_data.insert(col_index + len(features), col_name, np.where(
                trans_data[col].isin(features), 0, 1).astype(np.uint8))
            del trans_data[col]
            generated_cols.append(col_name)
            generated_cols_per_category[col] = generated_cols
        self._columns_dict = generated_cols_per_category
        return trans_data

    @staticmethod
    def _get_col_features(data: pd.DataFrame, col: str, threshold: float, max_bin: int) -> List:
        col_params_df = data[col].value_counts(dropna=False)
        col_params_df = col_params_df.reset_index(level=0)
        col_params_df.columns = ["category", "value"]
        col_params_df["percentage"] = col_params_df["value"] / len(data)
        col_params_df["percentage"] = col_params_df["percentage"].cumsum(axis=0)
        number_of_features = OneHotEncodingService._calc_number_of_features(data, col_params_df, threshold, max_bin)
        return col_params_df.iloc[:number_of_features]["category"].to_list()

    @staticmethod
    def _calc_number_of_features(data: pd.DataFrame, col_params: pd.DataFrame, threshold: float, max_bin: int):
        if threshold == 1.0:
            return min(len(data), max_bin)
        if max_bin == INT_MAX:
            return col_params[col_params["percentage"] >= threshold].index[0] + 1
        return min(col_params[col_params["percentage"] >= threshold].index[0] + 1, max_bin)

    @staticmethod
    def _decide_combined_cat_name(data: pd.DataFrame, col: str) -> str:
        col_name = f"{col}_Other"
        col_name_prefix = col_name
        name_index = 2
        while col_name in data:
            col_name = f"{col_name_prefix}{name_index}"
            name_index += 1
        return col_name

    @staticmethod
    def _append_binary_columns(data: pd.DataFrame, col: str, features: List, col_index: int):
        generated_cols = []
        for index, feature in enumerate(features):
            if pd.isna(feature):
                transformed_col_name = col + "_" + "NULL"
                data.insert(col_index + index, transformed_col_name,
                            np.where(pd.isna(data[col]), 1, 0).astype(np.uint8))
            else:
                transformed_col_name = col + "_" + str(feature)
                data.insert(col_index + index, transformed_col_name,
                            np.where(data[col] == feature, 1, 0).astype(np.uint8))
            generated_cols.append(transformed_col_name)
        return data, generated_cols
