import factory

from file_export.tests.factories.file_export_factories import (
    FileExportRegistryStaticSatelliteFactory,
)
from mt_tools.report_generator.tests.factories.report_generator_export_registry_hub_factories import (
    ReportGeneratorExportRegistryHubFactory,
)
from mt_tools.report_generator.models.report_generator_export_registry_sat_models import (
    ReportGeneratorExportRegistrySatellite,
)


class ReportGeneratorExportRegistrySatelliteFactory(
    FileExportRegistryStaticSatelliteFactory
):
    class Meta:
        model = ReportGeneratorExportRegistrySatellite

    hub_entity = factory.SubFactory(ReportGeneratorExportRegistryHubFactory)
