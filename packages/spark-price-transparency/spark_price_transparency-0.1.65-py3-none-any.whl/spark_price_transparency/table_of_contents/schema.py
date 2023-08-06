"""
This is the schema class for in table of contents
"""

from ..pt_schema import Pt_schema
from .toc_header import Toc_header
from .toc_reporting import Toc_reporting
from .index_reports import Index_reports
from pyspark.sql.functions import col


class Table_of_contents(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'toc_header': Toc_header(self.mth, self.catalog_name, self.stage_db_name),
                              'toc_reporting': Toc_reporting(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {'index_reports': Index_reports(self.mth, self.catalog_name, self.stage_db_name)}

    def run_ingest(self):
        dbfs_path = f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self._mth}/schema={self._schema}/'
        file_df = self._spark.read.format("binaryFile") \
                      .option("pathGlobFilter", "*.json") \
                      .load(dbfs_path).select(col('path').alias('file_path')) \
                      .join(self._spark.table("pt_stage.toc_header"), "file_name", "left_semi")
        self.run_ingest_df(file_df)

    def run_file_analytic_merge(self, file_name):
        self.analytic_tables['index_reports'].run_file_analytic_merge(file_name)
