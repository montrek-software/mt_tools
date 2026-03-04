from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_tools.notebook.models.notebook_fields_sat_models import NotebookFieldsSatellite
from mt_tools.notebook.models.notebook_fields_hub_models import NotebookFieldsHub


class NotebookFieldsRepository(MontrekRepository):
    hub_class = NotebookFieldsHub

    def set_annotations(self):
        pass