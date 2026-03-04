from reporting.dataclasses import table_elements as te
from reporting.managers.montrek_table_manager import MontrekTableManager
from reporting.managers.montrek_details_manager import MontrekDetailsManager
from mt_tools.notebook.repositories.notebook_fields_repositories import NotebookFieldsRepository

class CommonTableElementsMixin:
    @property
    def table_elements(self):
        return [
            te.LinkTableElement(
                name="Edit",
                url="notebook_fields_update",
                icon="edit",
                kwargs={"pk": "id"},
                hover_text="Update Notebook Fields",
            ),
            te.LinkTableElement(
                name="Delete",
                url="notebook_fields_delete",
                icon="trash",
                kwargs={"pk": "id"},
                hover_text="Delete Notebook Fields",
            ),
        ]

class NotebookFieldsTableManager(CommonTableElementsMixin, MontrekTableManager):
    repository_class = NotebookFieldsRepository

    @property
    def table_elements(self):
        table_elements = [
            te.LinkTextTableElement(
                name="Details",
                url="notebook_fields_details",
                kwargs={"pk": "hub_id"},
                text="hub_entity_id",
                hover_text="View Notebook Fields Details",
            ),
        ]
        table_elements += super().table_elements
        return table_elements


class NotebookFieldsDetailsManager(CommonTableElementsMixin, MontrekDetailsManager):
    repository_class = NotebookFieldsRepository

    @property
    def table_elements(self):
        table_elements = [
            te.StringTableElement(name="hub", attr="hub_entity_id"),
        ]
        table_elements += super().table_elements
        return table_elements