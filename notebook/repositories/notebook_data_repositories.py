from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_tools.notebook.models.notebook_data_sat_models import NotebookDataSatellite
from mt_tools.notebook.models.notebook_data_hub_models import NotebookDataHub


class NotebookDataRepository(MontrekRepository):
    hub_class = NotebookDataHub

    def set_annotations(self):
        pass