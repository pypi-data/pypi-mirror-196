"""
This is the schema class for in network rates
"""

from ..pt_schema import Pt_schema
from .inr_header import Inr_header
from .inr_network import Inr_network
from .inr_provider import Inr_provider
from .in_coverage import In_coverage
from .in_rate import In_rate
from .in_provider import In_provider
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit
from pyspark.sql import functions as F


class In_network_rates(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'inr_header': Inr_header(self.mth, self.catalog_name, self.stage_db_name),
                              'inr_network': Inr_network(self.mth, self.catalog_name, self.stage_db_name),
                              'inr_provider': Inr_provider(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {'in_coverage': In_coverage(self.mth, self.catalog_name, self.stage_db_name),
                                'in_rate': In_rate(self.mth, self.catalog_name, self.stage_db_name),
                                'in_provider': In_provider(self.mth, self.catalog_name, self.stage_db_name)}

    @property
    def inr_header(self) -> DataFrame:
        return self.ingest_tables['inr_header'].df

    @property
    def inr_network(self) -> DataFrame:
        return self.ingest_tables['inr_network'].df

    @property
    def inr_provider(self) -> DataFrame:
        return self.ingest_tables['inr_provider'].df

    @property
    def in_coverage(self) -> DataFrame:
        return self.ingest_tables['in_coverage'].df

    @property
    def in_rate(self) -> DataFrame:
        return self.ingest_tables['in_rate'].df

    @property
    def in_provider(self) -> DataFrame:
        return self.ingest_tables['in_provider'].df

    def run_ingest(self):
        dbfs_path = f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self._mth}/schema={self.schema}/'
        file_df = self._spark.read.format("binaryFile") \
                      .option("pathGlobFilter", "*.json") \
                      .load(dbfs_path).select(col('path').alias('file_path'),
                                              F.element_at(F.split(col('path'), '/'), -1).alias('file_name')) \
                      .join(self._spark.table("pt_stage.inr_header"), "file_name", "left_anti")
        self.run_ingest_df(file_df)

    def run_analytic(self):
        pass

    def run_analytic_df(self, file_name_df: DataFrame):
        pass
