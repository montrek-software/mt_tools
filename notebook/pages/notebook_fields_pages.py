from django.urls import reverse
from baseclasses.dataclasses.view_classes import TabElement
from baseclasses.pages import MontrekDetailsPage, MontrekPage
from mt_tools.notebook.repositories.notebook_fields_repositories import NotebookFieldsRepository

PAGE_TITLE="Notebook Fields"
LIST_TAB_NAME="Notebook Fields"
DETAILS_TAB_NAME="Notebook Fields"

class NotebookFieldsPage(MontrekPage):
    page_title = PAGE_TITLE

    def get_tabs(self):
        return (
            TabElement(
                name=LIST_TAB_NAME,
                link=reverse("notebook_fields_list"),
                html_id="tab_notebook_fields_list",
                active="active",
            ),
        )


class NotebookFieldsDetailsPage(MontrekDetailsPage):
    repository_class = NotebookFieldsRepository
    title_field = "hub_entity_id"

    def get_tabs(self):
        return (
            TabElement(
                name=DETAILS_TAB_NAME,
                link=reverse("notebook_fields_details", args=[self.obj.id]),
                html_id="tab_notebook_fields_details",
                active="active",
            ),
            TabElement(
                name="History",
                link=reverse("notebook_fields_history", args=[self.obj.id]),
                html_id="tab_notebook_fields_history",
            ),
        )