from django.core.files import File
from file_upload.models import FileUploadFileStaticSatellite
from file_upload.repositories.file_upload_registry_repository import (
    FileUploadRegistryRepositoryABC,
)

from mt_tools.excel_processor import models


class ExcelProcessorFileUploadRegistryRepository(FileUploadRegistryRepositoryABC):
    hub_class = models.ExcelProcessorFileUploadRegistryHub
    static_satellite_class = models.ExcelProcessorFileUploadRegistryStaticSatellite
    link_file_upload_registry_file_upload_file_class = (
        models.LinkExcelProcessorRegistryFile
    )

    def set_annotations(self, **kwargs):
        super().set_annotations(**kwargs)

        self.add_linked_satellites_field_annotations(
            FileUploadFileStaticSatellite,
            models.LinkExcelProcessorRegistryProcessedFile,
            ["file"],
            rename_field_map={"file": "processed_file"},
        )

    def get_processed_file(self, file_log_registry_id: int, request) -> File | None:
        file_log_registry_path = (
            self.receive().get(hub__pk=file_log_registry_id).processed_file
        )

        return self._get_file_from_registry(file_log_registry_path, request)
