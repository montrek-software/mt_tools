from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate
from file_export.models import FileExportRegistryHubABC


class ReportGeneratorExportRegistryHub(FileExportRegistryHubABC):
    pass


class ReportGeneratorExportRegistryHubValueDate(HubValueDate):
    hub = HubForeignKey(ReportGeneratorExportRegistryHub)
