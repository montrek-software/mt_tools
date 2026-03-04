from mt_tools.notebook.repositories.notebook_repositories import (
    NotebookNotebookDatasRepository,
)
from mt_tools.notebook.managers.notebook_data_managers import NotebookDataTableManager
from mt_tools.notebook.repositories.notebook_fields_repositories import (
    NotebookNotebookFieldssRepository,
)
from reporting.dataclasses import table_elements as te
from reporting.managers.montrek_details_manager import MontrekDetailsManager
from reporting.managers.montrek_table_manager import MontrekTableManager

from mt_tools.notebook.managers.notebook_fields_managers import (
    NotebookFieldsTableManager,
)
from mt_tools.notebook.repositories.notebook_repositories import (
    NotebookRepository,
)


class CommonTableElementsMixin:
    @property
    def table_elements(self):
        return [
            te.LinkTableElement(
                name="Edit",
                url="notebook_update",
                icon="edit",
                kwargs={"pk": "id"},
                hover_text="Update Notebook",
            ),
            te.LinkTableElement(
                name="Delete",
                url="notebook_delete",
                icon="trash",
                kwargs={"pk": "id"},
                hover_text="Delete Notebook",
            ),
        ]


class NotebookTableManager(CommonTableElementsMixin, MontrekTableManager):
    repository_class = NotebookRepository

    @property
    def table_elements(self):
        table_elements = [
            te.LinkTextTableElement(
                name="Details",
                url="notebook_details",
                kwargs={"pk": "hub_id"},
                text="notebook_name",
                hover_text="View Notebook Details",
            ),
        ]
        table_elements += super().table_elements
        return table_elements


class NotebookDetailsManager(CommonTableElementsMixin, MontrekDetailsManager):
    repository_class = NotebookRepository

    @property
    def table_elements(self):
        table_elements = [
            te.StringTableElement(name="Name", attr="notebook_name"),
        ]
        table_elements += super().table_elements
        return table_elements


class NotebookNotebookFieldssTableManager(NotebookFieldsTableManager):
    repository_class = NotebookNotebookFieldssRepository


class NotebookNotebookDatasTableManager(NotebookDataTableManager):
    repository_class = NotebookNotebookDatasRepository
