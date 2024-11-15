from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate, MontrekOneToOneLinkABC
from django.db import models
from file_upload.models import (
    FileUploadRegistryHubABC,
    FileUploadRegistryStaticSatelliteABC,
)


class ExcelProcessorFileUploadRegistryHub(FileUploadRegistryHubABC):
    link_file_upload_registry_file_upload_file = models.ManyToManyField(
        "file_upload.FileUploadFileHub",
        related_name="link_file_upload_file_excel_processor_registry",
        through="LinkExcelProcessorRegistryFile",
    )


class ExcelProcessorFileUploadRegistryHubValueDate(HubValueDate):
    hub = HubForeignKey(ExcelProcessorFileUploadRegistryHub)


class ExcelProcessorFileUploadRegistryStaticSatellite(
    FileUploadRegistryStaticSatelliteABC
):
    hub_entity = models.ForeignKey(
        ExcelProcessorFileUploadRegistryHub, on_delete=models.CASCADE
    )


class LinkExcelProcessorRegistryFile(MontrekOneToOneLinkABC):
    hub_in = models.ForeignKey(
        "ExcelProcessorFileUploadRegistryHub", on_delete=models.CASCADE
    )
    hub_out = models.ForeignKey(
        "file_upload.FileUploadFileHub", on_delete=models.CASCADE
    )
