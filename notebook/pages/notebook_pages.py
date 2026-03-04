from django.urls import reverse
from baseclasses.dataclasses.view_classes import TabElement
from baseclasses.pages import MontrekDetailsPage, MontrekPage
from mt_tools.notebook.repositories.notebook_repositories import NotebookRepository

PAGE_TITLE="Notebook"
LIST_TAB_NAME="Notebook"
DETAILS_TAB_NAME="Notebook"

class NotebookPage(MontrekPage):
    page_title = PAGE_TITLE

    def get_tabs(self):
        return (
            TabElement(
                name=LIST_TAB_NAME,
                link=reverse("notebook_list"),
                html_id="tab_notebook_list",
                active="active",
            ),
        )


class NotebookDetailsPage(MontrekDetailsPage):
    repository_class = NotebookRepository
    title_field = "hub_entity_id"

    def get_tabs(self):
        return (
            TabElement(
                name=DETAILS_TAB_NAME,
                link=reverse("notebook_details", args=[self.obj.id]),
                html_id="tab_notebook_details",
                active="active",
            ),
            TabElement(
                name="History",
                link=reverse("notebook_history", args=[self.obj.id]),
                html_id="tab_notebook_history",
            ),
        )