from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate, MontrekHubABC


class NotebookFieldsHub(MontrekHubABC):
    pass


class NotebookFieldsHubValueDate(HubValueDate):
    hub = HubForeignKey(NotebookFieldsHub)