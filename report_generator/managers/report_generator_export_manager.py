from file_export.managers.file_export_manager import FileExportManagerABC
from file_export.repositories.file_export_registry_repository import (
    FileExportRegistryRepositoryABC,
)
from mt_tools.report_generator.managers.report_generator_export_processor import (
    ReportGeneratorFileExportProcessor,
)
from mt_tools.report_generator.repositories.report_generator_export_registry_repositories import (
    ReportGeneratorExportRegistryRepository,
)


class ReportGeneratorFileExportManager(FileExportManagerABC):
    processor_class = ReportGeneratorFileExportProcessor
    registry_repository_class: type[FileExportRegistryRepositoryABC] = (
        ReportGeneratorExportRegistryRepository
    )
