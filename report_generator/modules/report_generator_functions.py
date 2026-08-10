"""Return types a report function can declare.

The mechanics live in ``process_pipeline.functions.processor_functions``; this
module only pins which kinds of file the report generator knows how to build.
Keep it in sync with
``ReportGeneratorFileExportProcessor.build_result_file``.
"""

from enum import Enum

from process_pipeline.functions.processor_functions import return_with_type


class ReportGeneratorReturnType(Enum):
    XLSX = "xlsx"
    PDF = "pdf"
    ZIP = "zip"


return_xlsx = return_with_type(ReportGeneratorReturnType.XLSX)
return_pdf = return_with_type(ReportGeneratorReturnType.PDF)
return_zip = return_with_type(ReportGeneratorReturnType.ZIP)
