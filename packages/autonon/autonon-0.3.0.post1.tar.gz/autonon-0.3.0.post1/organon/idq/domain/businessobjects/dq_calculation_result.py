"""todo"""
from typing import Optional

from organon.fl.core.businessobjects.dataframe import DataFrame
from organon.idq.domain.businessobjects.statistics.population_statistics import PopulationStatistics
from organon.idq.domain.businessobjects.statistics.sample_statistics import SampleStatistics
from organon.idq.domain.businessobjects.statistics.data_source_statistics import DataSourceStatistics


class DqCalculationResult:
    """todo"""

    def __init__(self):
        self.calculation_name: str = None
        self.data_source_stats: Optional[DataSourceStatistics] = None
        self.sample_stats: Optional[SampleStatistics] = None
        self.population_stats: Optional[PopulationStatistics] = None
        self.sample_data: Optional[DataFrame] = None
