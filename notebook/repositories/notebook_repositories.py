from mt_tools.notebook.repositories.notebook_data_repositories import (
    NotebookDataRepository,
)
from mt_tools.notebook.models.notebook_hub_models import NotebookHubValueDate
from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_tools.notebook.models.notebook_sat_models import NotebookSatellite
from mt_tools.notebook.models.notebook_hub_models import NotebookHub


class NotebookRepository(MontrekRepository):
    hub_class = NotebookHub

    def set_annotations(self):
        self.add_satellite_fields_annotations(NotebookSatellite, ["notebook_name"])


class NotebookNotebookDatasRepository(NotebookDataRepository):
    def receive(self, apply_filter=True):
        notebook_hub = NotebookHubValueDate.objects.get(
            pk=self.session_data.get("pk")
        ).hub
        return super().receive(apply_filter).filter(notebook_id=notebook_hub.id)
