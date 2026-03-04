from django.urls import reverse
from baseclasses.dataclasses.view_classes import ActionElement, ListActionElement
from baseclasses import views
from mt_tools.notebook.managers.notebook_managers import NotebookTableManager
from mt_tools.notebook.managers.notebook_managers import NotebookDetailsManager
from mt_tools.notebook.pages.notebook_pages import NotebookPage
from mt_tools.notebook.pages.notebook_pages import NotebookDetailsPage
from mt_tools.notebook.forms.notebook_forms import NotebookCreateForm


class NotebookCreateView(views.MontrekCreateView):
    manager_class = NotebookTableManager
    page_class = NotebookPage
    tab = "tab_notebook_list"
    form_class = NotebookCreateForm
    success_url = "notebook_list"
    title = "Notebook Create"


class NotebookUpdateView(views.MontrekUpdateView):
    manager_class = NotebookTableManager
    page_class = NotebookPage
    tab = "tab_notebook_list"
    form_class = NotebookCreateForm
    success_url = "notebook_list"
    title = "Notebook Update"


class NotebookDeleteView(views.MontrekDeleteView):
    manager_class = NotebookTableManager
    page_class = NotebookPage
    tab = "tab_notebook_list"
    success_url = "notebook_list"
    title = "Notebook Delete"


class NotebookListView(views.MontrekListView):
    manager_class = NotebookTableManager
    page_class = NotebookPage
    tab = "tab_notebook_list"
    title = "Notebook List"

    @property
    def actions(self) -> tuple:
        action_new = ActionElement(
            icon="plus",
            link=reverse("notebook_create"),
            action_id="id_create_notebook",
            hover_text="Create new Notebook",
        )
        return (action_new,)

class NotebookDetailView(views.MontrekDetailView):
    manager_class = NotebookDetailsManager
    page_class = NotebookDetailsPage
    tab = "tab_notebook_details"
    title = "Notebook Details"

    @property
    def actions(self) -> tuple:
        action_back = ListActionElement("notebook_list")
        return (action_back,)


class NotebookHistoryView(views.MontrekHistoryListView):
    manager_class = NotebookTableManager
    page_class = NotebookDetailsPage
    tab = "tab_notebook_history"
    title = "Notebook History"

    @property
    def actions(self) -> tuple:
        action_back = ListActionElement("notebook_list")
        return (action_back,)