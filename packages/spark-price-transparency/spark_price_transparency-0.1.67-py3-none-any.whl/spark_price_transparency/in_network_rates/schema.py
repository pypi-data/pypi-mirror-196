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


class In_network_rates(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'inr_header': Inr_header(self.mth, self.catalog_name, self.stage_db_name),
                              'inr_network': Inr_network(self.mth, self.catalog_name, self.stage_db_name),
                              'inr_provider': Inr_provider(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {'in_coverage': In_coverage(self.mth, self.catalog_name, self.stage_db_name),
                                'in_rate': In_rate(self.mth, self.catalog_name, self.stage_db_name),
                                'in_provider': In_provider(self.mth, self.catalog_name, self.stage_db_name)}

    def run_file_analytic_merge(self, file_name):
        # TODO: Run analytic merges in parallel
        self.analytic_tables['in_provider'].run_file_analytic_merge(file_name)
        self.analytic_tables['in_coverage'].run_file_analytic_merge(file_name)
        self.analytic_tables['in_rate'].run_file_analytic_merge(file_name)
