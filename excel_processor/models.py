from django.db import models
from file_upload.models import (
    FileUploadRegistryHubABC,
    FileUploadRegistryStaticSatelliteABC,
)


class ExcelProcessorFileUploadRegistryHub(FileUploadRegistryHubABC):
    ...


class ExcelProcessorFileUploadRegistryStaticSatellite(
    FileUploadRegistryStaticSatelliteABC
):
    hub_entity = models.ForeignKey(
        ExcelProcessorFileUploadRegistryHub, on_delete=models.CASCADE
    )
