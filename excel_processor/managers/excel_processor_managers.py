from io import BytesIO
import os
from typing import IO, Any
from zipfile import ZipFile
from django.core.files.base import ContentFile

from django.urls import resolve
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from file_upload.managers.file_upload_manager import FileUploadManagerABC
from file_upload.managers.file_upload_registry_manager import (
    FileUploadRegistryManagerABC,
)
from file_upload.models import FileUploadRegistryHubABC
from file_upload.repositories.file_upload_file_repository import (
    FileUploadFileRepository,
)
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
from reporting.dataclasses.table_elements import LinkTableElement


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
        self.output: None | ExcelProcessorReturn = None

    def pre_check(self, file_path: str) -> bool:
        return True

    def process(self, file_path: str) -> bool:
        processor_function = getattr(
            self.excel_processor_functions_class,
            self.processor_function_name,
        )
        try:
            self.output = processor_function(file_path, self.session_data)
        except Exception as e:
            self.message = f"Error raised during Excel File Processing function {self.processor_function_name}: {e}"
            return False
        self.message = f"Processed {self.processor_function_name}!"
        return True

    def post_check(self, file_path: str) -> bool:
        output_filename = self._get_filename(file_path=file_path)
        if self.output.return_type == ExcelProcessorReturnType.XLSX:
            file = self.return_excel(output_filename)
        else:
            raise TypeError(f"Unknown return type {self.output.return_type}")
        processed_file_hub = FileUploadFileRepository(self.session_data).create_by_dict(
            {"file": file}
        )
        ExcelProcessorFileUploadRegistryRepository(self.session_data).create_by_dict(
            {
                "hub_entity_id": self.session_data["file_upload_registry_id"],
                "link_file_upload_registry_file_processed_file": processed_file_hub,
            }
        )
        return True

    def return_excel(self, file_name: str) -> ContentFile:
        buffer = BytesIO()

        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            for sheet in self.output.data:
                self.output.data[sheet].to_excel(writer, sheet_name=sheet, index=False)
                self.excel_processor_formatter.format_excel(writer, sheet_name=sheet)

        buffer.seek(0)
        return ContentFile(buffer.read(), name=file_name)

    def return_zip(self, output: ExcelProcessorReturn) -> None:
        with ZipFile(self.http_response, "w") as zip_file:
            for file in output.data:
                zip_file.write(file, arcname=os.path.basename(file))

    def _get_filename(self, file_path: str) -> str:
        safe_name = os.path.basename(file_path)
        return f"{safe_name.split('.')[0]}__{self.processor_function_name}.{self.output.return_type.value}"


class ExcelProcessorRegistryManager(FileUploadRegistryManagerABC):
    repository_class = ExcelProcessorFileUploadRegistryRepository
    download_url = "excel_processor_registry_download"

    @property
    def table_elements(self) -> tuple:
        table_elements = super().table_elements
        table_elements = list(table_elements)
        table_elements = [
            LinkTableElement(
                name="Processed File",
                url="excel_processor_download_processed_file",
                kwargs={"pk": "id"},
                icon="download",
                hover_text="Download Processed File",
            )
        ] + table_elements
        return tuple(table_elements)


class ExcelProcessorManager(FileUploadManagerABC):
    file_upload_processor_class = ExcelProcessor
    file_registry_manager_class = ExcelProcessorRegistryManager
    do_process_file_async = True
