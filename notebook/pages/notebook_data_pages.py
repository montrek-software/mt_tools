from django.urls import reverse
from baseclasses.dataclasses.view_classes import TabElement
from baseclasses.pages import MontrekDetailsPage, MontrekPage
from mt_tools.notebook.repositories.notebook_data_repositories import (
    NotebookDataRepository,
)

PAGE_TITLE = "Notebook Data"
LIST_TAB_NAME = "Notebook Data"
DETAILS_TAB_NAME = "Notebook Data"


class NotebookDataPage(MontrekPage):
    page_title = PAGE_TITLE

    def get_tabs(self):
        return (
            TabElement(
                name=LIST_TAB_NAME,
                link=reverse("notebook_data_list"),
                html_id="tab_notebook_data_list",
                active="active",
            ),
        )


class NotebookDataDetailsPage(MontrekDetailsPage):
    repository_class = NotebookDataRepository
    title_field = "hub_entity_id"

    def get_tabs(self):
        return (
            TabElement(
                name=DETAILS_TAB_NAME,
                link=reverse("notebook_data_details", args=[self.obj.id]),
                html_id="tab_notebook_data_details",
                active="active",
            ),
            TabElement(
                name="History",
                link=reverse("notebook_data_history", args=[self.obj.id]),
                html_id="tab_notebook_data_history",
            ),
        )
