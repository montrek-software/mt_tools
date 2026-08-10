import factory

from baseclasses.tests.factories.baseclass_factories import ValueDateListFactory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubValueDateFactory,
)
from file_export.tests.factories.file_export_factories import (
    FileExportRegistryHubFactory,
)
from mt_tools.report_generator.models.report_generator_export_registry_hub_models import (
    ReportGeneratorExportRegistryHub,
)
from mt_tools.report_generator.models.report_generator_export_registry_hub_models import (
    ReportGeneratorExportRegistryHubValueDate,
)


class ReportGeneratorExportRegistryHubFactory(FileExportRegistryHubFactory):
    class Meta:
        model = ReportGeneratorExportRegistryHub


class ReportGeneratorExportRegistryHubValueDateFactory(MontrekHubValueDateFactory):
    class Meta:
        model = ReportGeneratorExportRegistryHubValueDate

    hub = factory.SubFactory(ReportGeneratorExportRegistryHubFactory)
    value_date_list = factory.SubFactory(ValueDateListFactory)
