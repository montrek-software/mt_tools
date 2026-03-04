from django.urls import reverse
from baseclasses.dataclasses.view_classes import ActionElement, ListActionElement
from baseclasses import views
from mt_tools.notebook.managers.notebook_data_managers import NotebookDataTableManager
from mt_tools.notebook.managers.notebook_data_managers import NotebookDataDetailsManager
from mt_tools.notebook.pages.notebook_data_pages import NotebookDataPage
from mt_tools.notebook.pages.notebook_data_pages import NotebookDataDetailsPage
from mt_tools.notebook.forms.notebook_data_forms import (
    NotebookDataCreateForm,
    NotebookDataUpdateForm,
)


class NotebookDataCreateView(views.MontrekCreateView):
    manager_class = NotebookDataTableManager
    page_class = NotebookDataPage
    tab = "tab_notebook_data_list"
    form_class = NotebookDataCreateForm
    success_url = "notebook_data_list"
    title = "Notebook Data Create"


class NotebookDataUpdateView(views.MontrekUpdateView):
    manager_class = NotebookDataTableManager
    page_class = NotebookDataPage
    tab = "tab_notebook_data_list"
    form_class = NotebookDataUpdateForm
    success_url = "notebook_data_list"
    title = "Notebook Data Update"


class NotebookDataDeleteView(views.MontrekDeleteView):
    manager_class = NotebookDataTableManager
    page_class = NotebookDataPage
    tab = "tab_notebook_data_list"
    success_url = "notebook_data_list"
    title = "Notebook Data Delete"


class NotebookDataListView(views.MontrekListView):
    manager_class = NotebookDataTableManager
    page_class = NotebookDataPage
    tab = "tab_notebook_data_list"
    title = "Notebook Data List"

    @property
    def actions(self) -> tuple:
        action_new = ActionElement(
            icon="plus",
            link=reverse("notebook_data_create"),
            action_id="id_create_notebook_data",
            hover_text="Create new Notebook Data",
        )
        return (action_new,)


class NotebookDataDetailView(views.MontrekDetailView):
    manager_class = NotebookDataDetailsManager
    page_class = NotebookDataDetailsPage
    tab = "tab_notebook_data_details"
    title = "Notebook Data Details"

    @property
    def actions(self) -> tuple:
        action_back = ListActionElement("notebook_data_list")
        return (action_back,)


class NotebookDataHistoryView(views.MontrekHistoryListView):
    manager_class = NotebookDataTableManager
    page_class = NotebookDataDetailsPage
    tab = "tab_notebook_data_history"
    title = "Notebook Data History"

    @property
    def actions(self) -> tuple:
        action_back = ListActionElement("notebook_data_list")
        return (action_back,)
