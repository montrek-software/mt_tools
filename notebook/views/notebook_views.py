from mt_tools.notebook.managers.notebook_managers import (
    NotebookNotebookDatasTableManager,
)
from mt_tools.notebook.repositories.notebook_repositories import NotebookRepository
from mt_tools.notebook.views.notebook_data_views import NotebookDataCreateView
from baseclasses.dataclasses.view_classes import CreateActionElement
from baseclasses import views
from baseclasses.dataclasses.view_classes import (
    ActionElement,
    CreateActionElement,
    ListActionElement,
)
from django.urls import reverse

from mt_tools.notebook.forms.notebook_forms import NotebookCreateForm
from mt_tools.notebook.managers.notebook_managers import (
    NotebookDetailsManager,
    NotebookNotebookFieldssTableManager,
    NotebookTableManager,
)
from mt_tools.notebook.pages.notebook_pages import NotebookDetailsPage, NotebookPage
from mt_tools.notebook.repositories.notebook_repositories import NotebookRepository
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsCreateView


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


class NotebookNotebookFieldssListView(views.MontrekListView):
    manager_class = NotebookNotebookFieldssTableManager
    page_class = NotebookDetailsPage
    title = "Notebook Fields"
    tab = "tab_notebook_notebook_fieldss"

    @property
    def actions(self) -> tuple[ActionElement]:
        action_create = CreateActionElement(
            url_name="notebook_notebook_fields_create",
            kwargs={"pk": self.kwargs["pk"]},
            action_id="id_notebook_fields_notebook_create",
            hover_text="Create NotebookFields from Notebook",
        )
        return (action_create,)


class NotebookNotebookFieldsCreateView(NotebookFieldsCreateView):
    def get_success_url(self):
        return reverse(
            "notebook_notebook_fieldss_list", kwargs={"pk": self.kwargs["pk"]}
        )

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        hub = (
            NotebookRepository(self.session_data)
            .receive()
            .get(hub__pk=self.kwargs["pk"])
        )
        form["link_notebook_fields_notebook"].initial = hub
        return form


class NotebookNotebookDatasListView(views.MontrekListView):
    manager_class = NotebookNotebookDatasTableManager
    page_class = NotebookDetailsPage
    title = "Notebook Data"
    tab = "tab_notebook_notebook_datas"

    @property
    def actions(self) -> tuple[ActionElement]:
        action_create = CreateActionElement(
            url_name="notebook_notebook_data_create",
            kwargs={"pk": self.kwargs["pk"]},
            action_id="id_notebook_data_notebook_create",
            hover_text="Create NotebookData from Notebook",
        )
        return (action_create,)


class NotebookNotebookDataCreateView(NotebookDataCreateView):
    def get_success_url(self):
        return reverse("notebook_notebook_datas_list", kwargs={"pk": self.kwargs["pk"]})

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        hub = (
            NotebookRepository(self.session_data)
            .receive()
            .get(hub__pk=self.kwargs["pk"])
        )
        form["link_notebook_data_notebook"].initial = hub
        return form

