from mt_tools.notebook.models.notebook_sat_models import NotebookSatellite

from mt_tools.notebook.models.notebook_data_hub_models import LinkNotebookDataNotebook

from baseclasses.repositories.montrek_repository import MontrekRepository
from mt_tools.notebook.models.notebook_data_sat_models import NotebookDataSatellite
from mt_tools.notebook.models.notebook_data_hub_models import NotebookDataHub


class NotebookDataRepository(MontrekRepository):
    hub_class = NotebookDataHub

    def set_annotations(self):
        self.add_linked_satellites_field_annotations(
            NotebookSatellite,
            LinkNotebookDataNotebook,
            ["hub_entity_id", "notebook_name"],
            rename_field_map={"hub_entity_id": "notebook_id"},
        )
        self.add_satellite_fields_annotations(NotebookDataSatellite, ["data_row"])
