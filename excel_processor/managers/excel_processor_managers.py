from file_upload.managers.file_upload_manager import FileUploadManagerABC
from file_upload.models import FileUploadRegistryHubABC
from file_upload.managers.file_upload_registry_manager import (
    FileUploadRegistryManagerABC,
)
from mt_tools.excel_processor.repositories.excel_processor_repositories import (
    ExcelProcessorFileUploadRegistryRepository,
)


class ExcelProcessor:
    def __init__(
        self,
        file_upload_registry_hub: FileUploadRegistryHubABC,
        session_data: dict[str, ...],
        **kwargs,
    ):
        self.message = "Not processed!"

    def pre_check(self, file_path: str) -> bool:
        return True

    def process(self, file_path: str) -> bool:
        return True

    def post_check(self, file_path: str) -> bool:
        return True


class ExcelProcessorRegistryManager(FileUploadRegistryManagerABC):
    repository_class = ExcelProcessorFileUploadRegistryRepository


class ExcelProcessorManager(FileUploadManagerABC):
    file_upload_processor_class = ExcelProcessor
    file_registry_manager_class = ExcelProcessorRegistryManager
