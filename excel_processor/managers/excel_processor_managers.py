from file_upload.managers.file_upload_manager import FileUploadManagerABC
from file_upload.models import FileUploadRegistryHubABC


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


class ExcelProcessorManager(FileUploadManagerABC):
    file_upload_processor_class = ExcelProcessor
