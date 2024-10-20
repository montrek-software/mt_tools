import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from file_upload.managers.file_upload_manager import FileUploadManagerABC
from file_upload.managers.file_upload_registry_manager import (
    FileUploadRegistryManagerABC,
)
from file_upload.models import FileUploadRegistryHubABC
from mt_tools.excel_processor.forms import ExcelProcessorUploadFileForm
from mt_tools.excel_processor.repositories.excel_processor_repositories import (
    ExcelProcessorFileUploadRegistryRepository,
)


class ExcelProcessor:
    def __init__(
        self,
        file_upload_registry_hub: FileUploadRegistryHubABC,
        session_data: dict[str, ...],
        upload_form: ExcelProcessorUploadFileForm,
        request,
        **kwargs,
    ):
        self.message = "Not processed!"
        self.processor_function = upload_form.cleaned_data.get("function")
        self.excel_processor_functions_class = (
            upload_form.excel_processor_functions_class
        )
        self.request = request
        self.http_response = HttpResponse()

    def pre_check(self, file_path: str) -> bool:
        return True

    def process(self, file_path: str) -> bool:
        process_function = getattr(
            self.excel_processor_functions_class, self.processor_function
        )
        try:
            output_df = process_function(file_path)
        except Exception as e:
            self.message = f"Error raised during Excel File Processing function {self.processor_function}: {e}"
            self.http_response = HttpResponseRedirect(
                self.request.META.get("HTTP_REFERER")
            )
            return False
        with pd.ExcelWriter(self.http_response) as excel_writer:
            output_df.to_excel(excel_writer, index=False)
        filename = (
            f"{file_path.split('/')[-1].split('.')[0]}__{self.processor_function}.xlsx"
        )
        self.http_response[
            "Content-Type"
        ] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        self.http_response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return True

    def post_check(self, file_path: str) -> bool:
        return True


class ExcelProcessorRegistryManager(FileUploadRegistryManagerABC):
    repository_class = ExcelProcessorFileUploadRegistryRepository
    download_url = "excel_processor_registry_download"


class ExcelProcessorManager(FileUploadManagerABC):
    file_upload_processor_class = ExcelProcessor
    file_registry_manager_class = ExcelProcessorRegistryManager
