from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate, MontrekHubABC


class NotebookHub(MontrekHubABC):
    pass


class NotebookHubValueDate(HubValueDate):
    hub = HubForeignKey(NotebookHub)