from mt_tools.notebook.models.notebook_hub_models import NotebookHub
from baseclasses.models import MontrekOneToManyLinkABC
from django.db import models
from baseclasses.fields import HubForeignKey
from baseclasses.models import HubValueDate, MontrekHubABC


class NotebookDataHub(MontrekHubABC):
    link_notebook_data_notebook = models.ManyToManyField(
        to=NotebookHub,
        through="LinkNotebookDataNotebook",
        related_name="link_notebook_notebook_data",
    )


class NotebookDataHubValueDate(HubValueDate):
    hub = HubForeignKey(NotebookDataHub)


class LinkNotebookDataNotebook(MontrekOneToManyLinkABC):
    hub_in = models.ForeignKey(NotebookDataHub, on_delete=models.CASCADE)
    hub_out = models.ForeignKey(NotebookHub, on_delete=models.CASCADE)

