from file_upload.forms import UploadFileForm
from process_pipeline.functions.forms import FunctionSelectionFormMixin


class ExcelProcessorUploadFileForm(FunctionSelectionFormMixin, UploadFileForm):
    def __init__(self, accept: str, *args, **kwargs):
        self.excel_processor_functions_class = kwargs.pop(
            "excel_processor_functions_class"
        )
        super().__init__(accept, *args, **kwargs)
        self.add_function_fields(self.excel_processor_functions_class)
