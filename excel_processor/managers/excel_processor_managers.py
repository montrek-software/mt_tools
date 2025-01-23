import os
from typing import Any
from zipfile import ZipFile

from django.urls import resolve
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from file_upload.managers.file_upload_manager import FileUploadManagerABC
from file_upload.managers.file_upload_registry_manager import (
    FileUploadRegistryManagerABC,
)
from file_upload.models import FileUploadRegistryHubABC
from mt_tools.excel_processor.modules.excel_processor_formatter import (
    ExcelProcessorMontrekFormatter,
)
from mt_tools.excel_processor.modules.excel_processor_functions import (
    ExcelProcessorReturn,
    ExcelProcessorReturnType,
)
from mt_tools.excel_processor.repositories.excel_processor_repositories import (
    ExcelProcessorFileUploadRegistryRepository,
)


class ExcelProcessor:
    excel_processor_formatter = ExcelProcessorMontrekFormatter

    def __init__(
        self,
        file_upload_registry_hub: FileUploadRegistryHubABC,
        session_data: dict[str, Any],
        **kwargs,
    ):
        self.message = "Not processed!"
        self.session_data = session_data
        view_class = resolve(self.session_data["request_path"]).func.view_class
        self.excel_processor_functions_class = (
            view_class.excel_processor_functions_class
        )
        self.processor_function_name = self.session_data["function"][0]
        self.http_response = HttpResponse()

    def pre_check(self, file_path: str) -> bool:
        return True

    def process(self, file_path: str) -> bool:
        processor_function = getattr(
            self.excel_processor_functions_class,
            self.processor_function_name,
        )
        try:
            output = processor_function(file_path)
        except Exception as e:
            self.message = f"Error raised during Excel File Processing function {self.processor_function_name}: {e}"
            self.http_response = HttpResponseRedirect(self.session_data["http_referer"])
            return False
        if output.return_type == ExcelProcessorReturnType.XLSX:
            self.return_excel(output)
        elif output.return_type == ExcelProcessorReturnType.ZIP:
            self.return_zip(output)
        self._download(output, file_path)
        self.message = f"Processed and downloaded {self.processor_function_name}!"
        return True

    def post_check(self, file_path: str) -> bool:
        return True

    def return_excel(self, output: ExcelProcessorReturn) -> None:
        with pd.ExcelWriter(self.http_response, engine="openpyxl") as excel_writer:
            for sheet in output.data:
                output.data[sheet].to_excel(excel_writer, sheet_name=sheet, index=False)
                self.excel_processor_formatter.format_excel(
                    excel_writer, sheet_name=sheet
                )

    def return_zip(self, output: ExcelProcessorReturn) -> None:
        with ZipFile(self.http_response, "w") as zip_file:
            for file in output.data:
                zip_file.write(file, arcname=os.path.basename(file))

    def _get_filename(
        self, return_type: ExcelProcessorReturnType, file_path: str
    ) -> str:
        return f"{file_path.split('/')[-1].split('.')[0]}__{self.processor_function_name}.{return_type.value}"

    def _download(self, output: ExcelProcessorReturn, file_path: str) -> None:
        application_map = {
            ExcelProcessorReturnType.XLSX: "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ExcelProcessorReturnType.ZIP: "zip",
        }
        filename = self._get_filename(output.return_type, file_path)
        self.http_response["Content-Type"] = (
            f"application/{application_map[output.return_type]}"
        )
        self.http_response["Content-Disposition"] = f'attachment; filename="{filename}"'


class ExcelProcessorRegistryManager(FileUploadRegistryManagerABC):
    repository_class = ExcelProcessorFileUploadRegistryRepository
    download_url = "excel_processor_registry_download"


class ExcelProcessorManager(FileUploadManagerABC):
    file_upload_processor_class = ExcelProcessor
    file_registry_manager_class = ExcelProcessorRegistryManager
    do_process_file_async = False
