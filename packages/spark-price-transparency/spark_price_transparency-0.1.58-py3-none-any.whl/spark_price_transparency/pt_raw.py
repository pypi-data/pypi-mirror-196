from pyspark.sql.session import SparkSession
import os
from datetime import date
from pyspark.sql.functions import col, lit
from pyspark.sql import functions as F
from pyspark.sql import DataFrame
from .pt_ingest_table import IngestTable
import subprocess
from os.path import exists as path_exists
from os.path import isfile as file_exists
from subprocess import check_output
import re

class PTRaw:
    name: str = "pt_raw"
    files: DataFrame
    toc_meta: DataFrame
    inr_meta: DataFrame
    pr_meta: DataFrame
    aa_meta: DataFrame
    stream_tgt: {str: IngestTable}

    def __init__(self, mth: int = None, location_uri=None, spark=None):
        """
        Meta is a class that consolidates all pt_raw metadata.
        Note: currently this class assumes hive_metastore is used
        """
        # TODO: move file_meta to guide
        self.spark = spark if spark is not None else SparkSession.builder.getOrCreate()
        self.mth = mth if mth is not None else int(date.today().strftime('%Y%m'))
        self.locationUri = location_uri if location_uri is not None else self.get_locationUri()
        if self.locationUri is not None:
            self.locationPath = self.locationUri.replace('dbfs:', '/dbfs')
            self.set_files()
            self.set_toc_meta()
            self.set_inr_meta()
            self.set_pr_meta()

    def get_locationUri(self):
        """
        We want to always get location Uri from the catalog so that we don't risk use of a custom location
        For now we will only accepts pt_raw as the raw database name
        """
        database = [d for d in self.spark.catalog.listDatabases() if d.name == "pt_raw"]
        if len(database) == 0:
            print(f'WARNING: {self.name} database does not exist. Run PTRaw.initialize_pt_raw().')
            location_uri = None
        else:
            location_uri = database[0].locationUri
        return location_uri

    def create_raw_database(self):
        # TODO: check if database already exists
        if self.locationUri is None:
            self.spark.sql(f'CREATE DATABASE IF NOT EXISTS {self.name}')
            self.locationUri = self.get_locationUri()
            print(f'Database {self.name} already exists.')
        else:
            self.spark.sql(f'CREATE DATABASE IF NOT EXISTS {self.name} LOCATION "{self.locationUri}"')
            print(f'Database {self.name} created.')
        self.locationUri = self.get_locationUri()
        self.locationPath = self.locationUri.replace('dbfs:', '/dbfs')

    def create_raw_directory(self):
        """
        The raw directory is required for a location to put raw files. Since it will not be a table,
        we will provide it with a _ prefix to avoid potential managed table conflicts
        Currently this path is not argumented.
        Currently this path generation is done only by local fs os operations to avoid dependency on dbutils.
        """
        path = self.locationUri.replace('dbfs:', '/dbfs') + '/_raw'
        if os.path.exists(path):
            print(f'{path} already exists.')
        else:
            os.mkdir(path)
            print(f'{path} created.')

    def create_raw_mth_directory(self):
        """
        This will simply create a new month with sub directories to put more files.
        This will eventually satisfy all schema, but for now, will only create partition for in_network_rates files
        """
        path = self.locationUri.replace('dbfs:', '/dbfs') + f'/_raw/mth={self.mth}'
        if os.path.exists(path):
            print(f'{path} already exists.')
        else:
            os.mkdir(path)
            print(f'{path} created.')
            os.mkdir(path + '/schema=in-network-rates')
            print(f'{path}/schema=in-network-rates created.')
        pass

    def initialize_pt_raw(self):
        self.create_raw_database()
        self.create_raw_directory()
        self.create_raw_mth_directory()
        self.set_files()
        self.set_toc_meta()
        self.set_inr_meta()
        self.set_pr_meta()

    def set_files(self):
        """
        Files will be real time definition of files in the raw directory.
        This is intended to help with the state of ingest.
        """
        files = self.spark.read.format("binaryFile") \
            .option("pathGlobFilter", "*.json") \
            .load(self.locationUri + '/_raw') \
            .drop('content')

        if 'mth' in files.columns:
            files = files.filter(col('mth') == lit(self.mth))
        else:
            files = files.withColumn("mth", lit(None)) \
                         .withColumn("schema", lit(None))

        self.files = files \
            .select(col('mth'),
                    col('schema'),
                    F.element_at(F.split(col('path'), '/'), -1).alias('file'),
                    col('path'),
                    col('length'),
                    col('modificationTime'))

    def set_toc_meta(self):
        """
        meta delta tables will be
        """
        # TODO: write condition for inr_header existing
        #  spark.catalog.tableExists("non_existing_table")
        toc_header = self.spark.table('pt_stage.toc_header') \
            .groupBy(col('file_name')) \
            .agg(F.first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name'))

        self.toc_meta = self.files.filter(col('schema') == lit("table-of-contents")).alias('files') \
            .join(toc_header.alias('header'),
                  col('file') == col('file_name'), 'left') \
            .select(col('files.*'),
                    F.when(col('header.file_name').isNotNull(), lit(True)).otherwise(lit(False)).alias('ingested'),
                    col('reporting_entity_name'))

    def set_inr_meta(self):
        """
        meta delta tables will be
        """
        # TODO: write condition for inr_header existing
        #  spark.catalog.tableExists("non_existing_table")
        inr_header = self.spark.table('pt_stage.inr_header') \
            .groupBy(col('file_name')) \
            .agg(F.first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name'),
                 F.first(col('last_updated_on'), ignorenulls=True).alias('last_updated_on'))

        self.inr_meta = self.files.filter(col('schema') == lit("in-network-rates")).alias('files') \
            .join(inr_header.alias('header'),
                  col('file') == col('file_name'), 'left') \
            .select(col('files.*'),
                    F.when(col('header.file_name').isNotNull(), lit(True)).otherwise(lit(False)).alias('ingested'),
                    col('reporting_entity_name'),
                    col('last_updated_on'))

    def set_pr_meta(self):
        pr_provider = self.spark.table('pt_stage.pr_provider').select('file_name')

        self.pr_meta = self.files.filter(col('schema') == lit("provider-reference")).alias('files') \
            .join(pr_provider.alias('provider'),
                  col('file') == col('file_name'), 'left') \
            .select(col('files.*'),
                    F.when(col('provider.file_name').isNotNull(), lit(True)).otherwise(lit(False)).alias('ingested'))

    def import_raw_file(self, url: str, meta: {} = None, compression_level=0):
        # TODO: convert join logic to os functions
        # TODO: write wrapper to run parallel distributed for array of files and concurrent argument
        # TODO: Once streaming gz works, update to default compression
        f_meta = self.get_file_meta(url.split('/')[-1]) if meta is None else meta
        # Make sure tgt path exists, create if doesn't
        if ~path_exists(f_meta['raw_tgt_folder']):
            sh(['mkdir', '-p', f_meta['raw_tgt_folder']])
        if compression_level == 0:
            # No compression for target file
            tgt = f_meta['raw_tgt_folder'] + '/' + f_meta['name'] + '.json'
            # Check if tgt already exists
            if file_exists(tgt):
                print(tgt + ' already exists.')
                return
            if f_meta['ext'] == 'json.gz':
                # Source file compressed
                with open(tgt, "w") as f:
                    wget_process = subprocess.Popen(('wget', '-O', '-', '-o', '/dev/null', url), stdout=subprocess.PIPE)
                    subprocess.call(('gunzip', '-c'), stdin=wget_process.stdout, stdout=f)
                    wget_process.wait()
            elif f_meta['ext'] == 'zip':
                # Source file(s) are zipped
                # Assumes single json within download & name matches except for extension
                # TODO: handle expected zip conventions (ie. multiple indexes)
                zip_tgt = f_meta['raw_tgt_folder'] + '/' + f_meta['name'] + '.zip'
                wget_process = subprocess.Popen(('wget', '-O', zip_tgt, url))
                wget_process.wait()
                unzip_process = subprocess.Popen(('unzip', zip_tgt))
                unzip_process.wait()
                # TODO: add extract validation
                rm_process = subprocess.Popen(('rm', '-rf', zip_tgt))
                rm_process.wait()
            else:
                wget_process = subprocess.Popen(('wget', '-O', tgt, url))
                wget_process.wait()
        elif 1 < compression_level <= 9:
            # TODO: write target compression logic
            pass
        else:
            # TODO: write download, no change logic
            pass

    def get_file_meta(self, file):
        """
        File parsing taken from https://github.com/CMSgov/price-transparency-guide#file-naming-convention
        """
        # TODO: add exception for mal formed file names
        # TODO: add allowed extensions check
        file_regex = r"((\d{4}-\d{2}(?:-\d{2})?)\_(.*)\_" + \
                     r"(in-network-rates|allowed-amounts|prescription-drugs|provider-reference|index)" + \
                     r"\_?([^\.]*))\.([^(?:\?|$)]*)(?:\??[^$]*)"
        file_name, dte, payer_plan, schema, index, ext = re.search(file_regex, file).groups()
        if schema == 'index':
            schema = 'table-of-contents'
        mth = int(dte[:4] + dte[5:7])
        raw_tgt_folder = '/'.join([self.locationPath, '_raw', 'mth=' + str(mth), 'schema=' + schema])
        indexed = index != ''
        return {'name': file_name, 'dte': dte, 'mth': mth, 'ext': ext,
                'indexed': indexed, 'index': int(index.split('_')[-1]) if indexed else 0,
                'schema': schema, 'payer_plan': payer_plan, 'raw_tgt_folder': raw_tgt_folder}

    def _remove_pt_raw(self):
        """
        Removes all components of pt_raw. Helpful to clean up env after evaluating
        """

def sh(args):
    return str(check_output(args)).split('\\n')
