from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_tools.notebook.models.notebook_sat_models import NotebookSatellite
from mt_tools.notebook.models.notebook_hub_models import NotebookHub


class NotebookRepository(MontrekRepository):
    hub_class = NotebookHub

    def set_annotations(self):
        pass