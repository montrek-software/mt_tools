from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate, MontrekHubABC


class NotebookDataHub(MontrekHubABC):
    pass


class NotebookDataHubValueDate(HubValueDate):
    hub = HubForeignKey(NotebookDataHub)