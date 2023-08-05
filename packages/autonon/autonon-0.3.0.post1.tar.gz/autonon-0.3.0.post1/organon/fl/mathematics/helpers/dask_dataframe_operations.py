""" This module includes DaskDataFrameOperations class."""
from typing import List

from organon.fl.core.businessobjects.dataframe import DataFrame
from organon.fl.core.businessobjects.idataframe import IDataFrame
from organon.fl.mathematics.helpers.idataframe_operations import IDataFrameOperations


class DaskDataFrameOperations(IDataFrameOperations):
    """Class for Dask Dataframe Operations."""

    @staticmethod
    def get_column_stability(df_obj: IDataFrame):
        """:returns boolean df depends on whether a column is stable or not"""
        raise NotImplementedError

    @staticmethod
    def join(df1: DataFrame, df2: DataFrame):
        """:returns pandas join function equivalent for dask"""
        raise NotImplementedError

    @staticmethod
    def get_column_distinct_counts(df_obj: DataFrame, col_names: List[str] = None):
        """:returns number of unique values per column"""
        raise NotImplementedError
