from mt_tools.notebook.models.notebook_hub_models import NotebookHub
from baseclasses.models import MontrekOneToManyLinkABC
from django.db import models
from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate, MontrekHubABC


class NotebookFieldsHub(MontrekHubABC):
    link_notebook_fields_notebook = models.ManyToManyField(
        to=NotebookHub,
    through="LinkNotebookFieldsNotebook",
    related_name="link_notebook_notebook_fields",
)

class NotebookFieldsHubValueDate(HubValueDate):
    hub = HubForeignKey(NotebookFieldsHub)

class LinkNotebookFieldsNotebook(MontrekOneToManyLinkABC):
    hub_in = models.ForeignKey(NotebookFieldsHub, on_delete=models.CASCADE)
    hub_out = models.ForeignKey(NotebookHub, on_delete=models.CASCADE)