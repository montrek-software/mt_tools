from django.db import models

from baseclasses.models import MontrekSatelliteABC
from mt_tools.notebook.models.notebook_data_hub_models import NotebookDataHub


class NotebookDataSatellite(MontrekSatelliteABC):
    hub_entity = models.ForeignKey(NotebookDataHub, on_delete=models.CASCADE)

    data_row = models.JSONField(default=dict, blank=True)

    identifier_fields = ["hub_entity_id"]
