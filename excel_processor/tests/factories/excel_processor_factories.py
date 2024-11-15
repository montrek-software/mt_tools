import factory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubFactory,
)
from file_upload.tests.factories.file_upload_factories import (
    FileUploadRegistryStaticSatelliteFactory,
)


class ExcelProcessorFileUploadRegistryHubFactor(MontrekHubFactory):
    class Meta:
        model = "excel_processor.ExcelProcessorFileUploadRegistryHub"


class ExcelProcessorFileUploadRegistryStaticSatelliteFactory(
    FileUploadRegistryStaticSatelliteFactory
):
    class Meta:
        model = "excel_processor.ExcelProcessorFileUploadRegistryStaticSatellite"

    hub_entity = factory.SubFactory(ExcelProcessorFileUploadRegistryHubFactor)
