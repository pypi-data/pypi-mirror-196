"""
This is the base table class that will include all common delta table operations
"""

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from delta.tables import DeltaTable
from pyspark.sql.types import DateType
from datetime import date
from pyspark.sql.functions import col, lit

class Pt_table:

    cat_name: str = 'hive_warehouse'
    wh_name: str = 'pt_stage'
    schema: str
    definition: [(str, DateType, bool, str)] = []

    def __init__(self, mth: int = None):
        self._spark = SparkSession.builder.getOrCreate()
        self._mth = int(date.today().strftime('%Y%m')) if mth is None else mth
        self.tbl_name = self.__class__.__name__.lower()
        self.wh_tbl_name = '.'.join([self.wh_name, self.tbl_name])

    @property
    def mth(self):
        return self._mth

    @mth.setter
    def mth(self, value):
        mth = int(value)
        self._mth = mth
        print(f'pt_stage.{self.schema.replace("-","_")}.mth set to {mth}.')

    @mth.deleter
    def mth(self):
        mth = int(date.today().strftime('%Y%m'))
        self._mth = mth
        print(f'pt_stage.{self.schema.replace("-","_")}.mth reset to {mth}')

    @property
    def df(self) -> DataFrame:
        return self._spark.table(self.wh_tbl_name).filter(col('mth') == lit(self._mth))

    @property
    def table(self) -> DeltaTable:
        return DeltaTable.forName(self._spark, self.wh_tbl_name)

    def create_table(self) -> None:
        dt = DeltaTable.createIfNotExists(self._spark).tableName(self.wh_tbl_name)
        dt.addColumn("mth", dataType="INT", nullable=False)
        for c in self.definition:
            dt.addColumn(*c[:-1], comment=c[-1])
        dt.partitionedBy("mth")
        dt.execute()

    def drop_table(self) -> None:
        self._spark.sql(f'DROP TABLE IF EXISTS {self.wh_tbl_name}')

    def create_view(self) -> None:
        self.df.createOrReplaceTempView(self.tbl_name)

    def purge_table(self) -> None:
        self._spark.sql(f'DELETE FROM {self.wh_tbl_name} WHERE 1=1')
        DeltaTable.forName(self._spark, self.wh_tbl_name).vacuum()
