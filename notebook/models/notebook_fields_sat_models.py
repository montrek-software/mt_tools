from django.db import models

from baseclasses.models import MontrekSatelliteABC
from mt_tools.notebook.models.notebook_fields_hub_models import NotebookFieldsHub


class NotebookFieldsSatellite(MontrekSatelliteABC):
    hub_entity = models.ForeignKey(NotebookFieldsHub, on_delete=models.CASCADE)