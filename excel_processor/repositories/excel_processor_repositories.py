from mt_tools.excel_processor import models
from file_upload.repositories.file_upload_registry_repository import (
    FileUploadRegistryRepositoryABC,
)


class ExcelProcessorFileUploadRegistryRepository(FileUploadRegistryRepositoryABC):
    hub_class = models.ExcelProcessorFileUploadRegistryHub
    static_satellite_class = models.ExcelProcessorFileUploadRegistryStaticSatellite
    link_file_upload_registry_file_upload_file_class = (
        models.LinkExcelProcessorRegistryFile
    )
