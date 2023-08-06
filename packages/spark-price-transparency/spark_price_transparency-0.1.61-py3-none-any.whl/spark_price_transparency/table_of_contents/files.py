from ..pt_files import Pt_files

class Table_of_contents_files(Pt_files):

    schema = "table-of-contents"
    _meta_ingest_tbl = "pt_stage.toc_header"
