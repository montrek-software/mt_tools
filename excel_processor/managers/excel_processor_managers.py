import os
from typing import Any

from django.core.files.base import ContentFile
from file_upload.managers.file_upload_manager import (
    FileUploadManagerABC,
    FileUploadProcessorProtocol,
)
from file_upload.managers.file_upload_registry_manager import (
    FileUploadRegistryManagerABC,
)
from file_upload.models import FileUploadRegistryHubABC
from file_upload.repositories.file_upload_file_repository import (
    FileUploadFileRepository,
)
from process_pipeline.functions.result_files import build_excel_file, build_zip_file
from process_pipeline.functions.selection import FunctionSelection
from reporting.dataclasses.table_elements import LinkTableElement

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


class ExcelProcessor(FileUploadProcessorProtocol):
    excel_processor_formatter = ExcelProcessorMontrekFormatter

    def __init__(
        self,
        file_upload_registry_hub: FileUploadRegistryHubABC,
        session_data: dict[str, Any],
        **kwargs,
    ):
        self.set_message("Not processed!")
        self.session_data = session_data
        self.output: None | ExcelProcessorReturn = None
        self._selection: FunctionSelection | None = None

    @property
    def selection(self) -> FunctionSelection:
        """What the user picked in the upload form."""
        if self._selection is None:
            self._selection = FunctionSelection.from_pipeline_data(self.pipeline_data)
        return self._selection

    @property
    def excel_processor_functions_class(self) -> type:
        return self.selection.functions_class

    @property
    def processor_function_name(self) -> str:
        return self.selection.function_name

    def pre_check(self, file_path: str | None) -> bool:
        return True

    def process(self, file_path: str | None) -> bool:
        try:
            processor_function = self.selection.get_function()
            self.output = processor_function(file_path, self.session_data)
        except Exception as e:
            self.set_message(
                "Error raised during Excel File Processing function "
                f"{self.processor_function_name}: {e}"
            )
            return False
        self.set_message(f"Processed {self.processor_function_name}!")
        return True

    def post_check(self, file_path: str | None) -> bool:
        if self.output is None:
            return False
        if file_path is None:
            return False
        output_filename = self._get_filename(file_path=file_path)
        if self.output.return_type == ExcelProcessorReturnType.XLSX:
            file = self.return_excel(output_filename)
        elif self.output.return_type == ExcelProcessorReturnType.ZIP:
            file = self.return_zip(output_filename)
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
        return build_excel_file(
            self.output.data,
            file_name,
            formatter=self.excel_processor_formatter.format_excel,
        )

    def return_zip(self, zip_name: str) -> ContentFile:
        return build_zip_file(list(self.output.data), zip_name)

    def _get_filename(self, file_path: str | None) -> str:
        if file_path:
            safe_name = os.path.basename(file_path)
            base = safe_name.split(".")[0]
        else:
            base = self.processor_function_name
        return f"{base}__{self.processor_function_name}.{self.output.return_type.value}"


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
