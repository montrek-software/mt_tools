from django.db import models

from file_export.models import FileExportRegistryStaticSatelliteABC
from mt_tools.report_generator.models.report_generator_export_registry_hub_models import (
    ReportGeneratorExportRegistryHub,
)


class ReportGeneratorExportRegistrySatellite(FileExportRegistryStaticSatelliteABC):
    hub_entity = models.ForeignKey(
        ReportGeneratorExportRegistryHub, on_delete=models.CASCADE
    )
