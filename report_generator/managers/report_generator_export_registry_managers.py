from file_export.managers.file_export_registry_manager import (
    FileExportRegistryManagerABC,
)
from mt_tools.report_generator.repositories.report_generator_export_registry_repositories import (
    ReportGeneratorExportRegistryRepository,
)


class ReportGeneratorExportRegistryTableManager(FileExportRegistryManagerABC):
    repository_class = ReportGeneratorExportRegistryRepository
    document_name = "Report Generator Export Registry"
    download_url = "report_generator_export_download"
