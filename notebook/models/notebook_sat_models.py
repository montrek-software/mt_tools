from django.db import models

from baseclasses.models import MontrekSatelliteABC
from mt_tools.notebook.models.notebook_hub_models import NotebookHub


class NotebookSatellite(MontrekSatelliteABC):
    hub_entity = models.ForeignKey(NotebookHub, on_delete=models.CASCADE)