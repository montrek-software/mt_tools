from file_export.repositories.file_export_registry_repository import (
    FileExportRegistryRepositoryABC,
)
from mt_tools.report_generator.models.report_generator_export_registry_hub_models import (
    ReportGeneratorExportRegistryHub,
)
from mt_tools.report_generator.models.report_generator_export_registry_sat_models import (
    ReportGeneratorExportRegistrySatellite,
)


class ReportGeneratorExportRegistryRepository(FileExportRegistryRepositoryABC):
    hub_class = ReportGeneratorExportRegistryHub
    registry_satellite = ReportGeneratorExportRegistrySatellite
