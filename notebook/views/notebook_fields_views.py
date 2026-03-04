from django.urls import reverse
from baseclasses.dataclasses.view_classes import ActionElement, ListActionElement
from baseclasses import views
from mt_tools.notebook.managers.notebook_fields_managers import NotebookFieldsTableManager
from mt_tools.notebook.managers.notebook_fields_managers import NotebookFieldsDetailsManager
from mt_tools.notebook.pages.notebook_fields_pages import NotebookFieldsPage
from mt_tools.notebook.pages.notebook_fields_pages import NotebookFieldsDetailsPage
from mt_tools.notebook.forms.notebook_fields_forms import NotebookFieldsCreateForm


class NotebookFieldsCreateView(views.MontrekCreateView):
    manager_class = NotebookFieldsTableManager
    page_class = NotebookFieldsPage
    tab = "tab_notebook_fields_list"
    form_class = NotebookFieldsCreateForm
    success_url = "notebook_fields_list"
    title = "Notebook Fields Create"


class NotebookFieldsUpdateView(views.MontrekUpdateView):
    manager_class = NotebookFieldsTableManager
    page_class = NotebookFieldsPage
    tab = "tab_notebook_fields_list"
    form_class = NotebookFieldsCreateForm
    success_url = "notebook_fields_list"
    title = "Notebook Fields Update"


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