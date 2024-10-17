import factory
from file_upload.tests.factories.file_upload_factories import (
    FileUploadRegistryStaticSatelliteFactory,
)


class ExcelProcessorFileUploadRegistryHubFactor(factory.django.DjangoModelFactory):
    class Meta:
        model = "excel_processor.ExcelProcessorFileUploadRegistryHub"


class ExcelProcessorFileUploadRegistryStaticSatelliteFactory(
    FileUploadRegistryStaticSatelliteFactory
):
    class Meta:
        model = "excel_processor.ExcelProcessorFileUploadRegistryStaticSatellite"

    hub_entity = factory.SubFactory(ExcelProcessorFileUploadRegistryHubFactor)
