from django.core.files.uploadedfile import SimpleUploadedFile
import factory
from baseclasses.tests.factories.montrek_factory_schemas import (
    MontrekHubFactory,
)
from file_upload.tests.factories.file_upload_factories import (
    FileUploadFileStaticSatelliteFactory,
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

    @factory.post_generation
    def generate_file_processed_file(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.test_file = SimpleUploadedFile(
                name="test_processed_file.txt",
                content="test".encode("utf-8"),
                content_type="text/plain",
            )
            upload_file = FileUploadFileStaticSatelliteFactory.create(
                file=self.test_file
            )
            self.hub_entity.link_file_upload_registry_file_processed_file.add(
                upload_file.hub_entity
            )
