"""Excel flavour of the generic processor-functions layer.

The mechanics live in ``process_pipeline.functions.processor_functions``; this
module only pins the return types the Excel processor can build. Import the
generic names directly when writing a new processor.
"""

from enum import Enum

from process_pipeline.functions.processor_functions import (
    ProcessorFunctionsProtocol,
    ProcessorReturn,
    return_with_type,
)


class ExcelProcessorReturnType(Enum):
    XLSX = "xlsx"
    ZIP = "zip"


# Kept as aliases so existing imports and isinstance checks keep working.
ExcelProcessorReturn = ProcessorReturn
ExcelProcessorFunctionsProtocol = ProcessorFunctionsProtocol

return_excel = return_with_type(ExcelProcessorReturnType.XLSX)
return_zip = return_with_type(ExcelProcessorReturnType.ZIP)
