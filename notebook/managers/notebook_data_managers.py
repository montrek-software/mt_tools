from reporting.dataclasses import table_elements as te
from reporting.managers.montrek_table_manager import MontrekTableManager
from reporting.managers.montrek_details_manager import MontrekDetailsManager
from mt_tools.notebook.repositories.notebook_data_repositories import NotebookDataRepository

class CommonTableElementsMixin:
    @property
    def table_elements(self):
        return [
            te.LinkTableElement(
                name="Edit",
                url="notebook_data_update",
                icon="edit",
                kwargs={"pk": "id"},
                hover_text="Update Notebook Data",
            ),
            te.LinkTableElement(
                name="Delete",
                url="notebook_data_delete",
                icon="trash",
                kwargs={"pk": "id"},
                hover_text="Delete Notebook Data",
            ),
        ]

class NotebookDataTableManager(CommonTableElementsMixin, MontrekTableManager):
    repository_class = NotebookDataRepository

    @property
    def table_elements(self):
        table_elements = [
            te.LinkTextTableElement(
                name="Details",
                url="notebook_data_details",
                kwargs={"pk": "hub_id"},
                text="hub_entity_id",
                hover_text="View Notebook Data Details",
            ),
        ]
        table_elements += super().table_elements
        return table_elements


class NotebookDataDetailsManager(CommonTableElementsMixin, MontrekDetailsManager):
    repository_class = NotebookDataRepository

    @property
    def table_elements(self):
        table_elements = [
            te.StringTableElement(name="hub", attr="hub_entity_id"),
        ]
        table_elements += super().table_elements
        return table_elements