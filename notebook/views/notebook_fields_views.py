from baseclasses import views
from baseclasses.dataclasses.view_classes import ActionElement, ListActionElement
from django.urls import reverse

from mt_tools.notebook.forms.notebook_fields_forms import NotebookFieldsCreateForm
from mt_tools.notebook.managers.notebook_fields_managers import (
    NotebookFieldsDetailsManager,
    NotebookFieldsTableManager,
)
from mt_tools.notebook.pages.notebook_fields_pages import (
    NotebookFieldsDetailsPage,
    NotebookFieldsPage,
)


class NotebookFieldsCreateView(views.MontrekCreateView):
    manager_class = NotebookFieldsTableManager
    page_class = NotebookFieldsPage
    tab = "tab_notebook_fields_list"
    form_class = NotebookFieldsCreateForm
    success_url = "notebook_fields_list"
    title = "Notebook Fields Create"
    is_compact_form = True


class NotebookFieldsUpdateView(views.MontrekUpdateView):
    manager_class = NotebookFieldsTableManager
    page_class = NotebookFieldsPage
    tab = "tab_notebook_fields_list"
    form_class = NotebookFieldsCreateForm
    success_url = "notebook_fields_list"
    title = "Notebook Fields Update"
    is_compact_form = True


class NotebookFieldsDeleteView(views.MontrekDeleteView):
    manager_class = NotebookFieldsTableManager
    page_class = NotebookFieldsPage
    tab = "tab_notebook_fields_list"
    success_url = "notebook_fields_list"
    title = "Notebook Fields Delete"


class NotebookFieldsListView(views.MontrekListView):
    manager_class = NotebookFieldsTableManager
    page_class = NotebookFieldsPage
    tab = "tab_notebook_fields_list"
    title = "Notebook Fields List"

    @property
    def actions(self) -> tuple:
        action_new = ActionElement(
            icon="plus",
            link=reverse("notebook_fields_create"),
            action_id="id_create_notebook_fields",
            hover_text="Create new Notebook Fields",
        )
        return (action_new,)


class NotebookFieldsDetailView(views.MontrekDetailView):
    manager_class = NotebookFieldsDetailsManager
    page_class = NotebookFieldsDetailsPage
    tab = "tab_notebook_fields_details"
    title = "Notebook Fields Details"

    @property
    def actions(self) -> tuple:
        action_back = ListActionElement("notebook_fields_list")
        return (action_back,)


class NotebookFieldsHistoryView(views.MontrekHistoryListView):
    manager_class = NotebookFieldsTableManager
    page_class = NotebookFieldsDetailsPage
    tab = "tab_notebook_fields_history"
    title = "Notebook Fields History"

    @property
    def actions(self) -> tuple:
        action_back = ListActionElement("notebook_fields_list")
        return (action_back,)
