"""
Index reports is the analytic form for table of contents data
It is necessary since it will have all of the files that need to be ingested for any given payer
"""

from ..pt_analytic_table import AnalyticTable
from pyspark.sql.types import ArrayType, StructType, StructField, StringType


class Index_reports(AnalyticTable):

    reporting_plans = ArrayType(StructType([
                                StructField("plan_name", StringType(), True),
                                StructField("plan_id", StringType(), True),
                                StructField("plan_id_type", StringType(), True),
                                StructField("plan_market_type", StringType(), True)]))

    definition = \
        [("toc_file_name",         StringType(),    True, "Table of Contents file name"),
         ("reporting_entity_name", StringType(),    True, "Entity Name of the TOC reporting entity"),
         ("reporting_entity_type", StringType(),    True, "Entity Type of the TOC reporting entity"),
         ("file_type",             StringType(),    True, "File Type; 'in-network-rates' or 'allowed-amounts'"),
         ("location",              StringType(),    True, "URL of file"),
         ("reporting_plans",       reporting_plans, True, "Location file plans detail")]
