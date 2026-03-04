from mt_tools.notebook.models.notebook_hub_models import NotebookHubValueDate
from mt_tools.notebook.models.notebook_sat_models import NotebookSatellite

from mt_tools.notebook.models.notebook_fields_hub_models import (
    LinkNotebookFieldsNotebook,
)

from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_tools.notebook.models.notebook_fields_sat_models import NotebookFieldsSatellite
from mt_tools.notebook.models.notebook_fields_hub_models import NotebookFieldsHub


class NotebookFieldsRepository(MontrekRepository):
    hub_class = NotebookFieldsHub

    def set_annotations(self):
        self.add_linked_satellites_field_annotations(
            NotebookSatellite,
            LinkNotebookFieldsNotebook,
            ["hub_entity_id"],
            rename_field_map={"hub_entity_id": "notebook_id"},
        )
        self.add_satellite_fields_annotations(NotebookFieldsSatellite, ["field_name"])


class NotebookNotebookFieldssRepository(NotebookFieldsRepository):
    def receive(self, apply_filter=True):
        if not hasattr(self, "_notebook_hub_id"):
            self._notebook_hub_id = NotebookHubValueDate.objects.values_list(
                "hub_id", flat=True
            ).get(pk=self.session_data.get("pk"))
        return super().receive(apply_filter).filter(
            notebook_id=self._notebook_hub_id
        )
