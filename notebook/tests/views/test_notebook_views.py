from testing.test_cases.view_test_cases import (
    MontrekCreateViewTestCase,
    MontrekUpdateViewTestCase,
    MontrekViewTestCase,
    MontrekListViewTestCase,
    MontrekDeleteViewTestCase,
)
from mt_tools.notebook.tests.factories.notebook_hub_factories import NotebookHubValueDateFactory
from mt_tools.notebook.tests.factories.notebook_sat_factories import NotebookSatelliteFactory
from mt_tools.notebook.views.notebook_views import NotebookCreateView
from mt_tools.notebook.views.notebook_views import NotebookUpdateView
from mt_tools.notebook.views.notebook_views import NotebookListView
from mt_tools.notebook.views.notebook_views import NotebookDeleteView
from mt_tools.notebook.views.notebook_views import NotebookDetailView
from mt_tools.notebook.views.notebook_views import NotebookHistoryView


class TestNotebookCreateView(MontrekCreateViewTestCase):
    viewname = "notebook_create"
    view_class = NotebookCreateView

    def creation_data(self):
        return {}


class TestNotebookUpdateView(MontrekUpdateViewTestCase):
    viewname = "notebook_update"
    view_class = NotebookUpdateView

    def build_factories(self):
        self.sat_obj = NotebookSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}

    def update_data(self):
        return {}


class TestNotebookListView(MontrekListViewTestCase):
    viewname = "notebook_list"
    view_class = NotebookListView
    expected_no_of_rows = 1

    def build_factories(self):
        self.sat_obj = NotebookSatelliteFactory()


class TestNotebookDeleteView(MontrekDeleteViewTestCase):
    viewname = "notebook_delete"
    view_class = NotebookDeleteView

    def build_factories(self):
        self.sat_obj = NotebookSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}



class TestNotebookDetailView(MontrekViewTestCase):
    viewname = "notebook_details"
    view_class = NotebookDetailView

    def build_factories(self):
        self.hub_vd = NotebookHubValueDateFactory(value_date=None)
        NotebookSatelliteFactory(hub_entity=self.hub_vd.hub)

    def url_kwargs(self) -> dict:
        return {"pk": self.hub_vd.hub.id}


class TestNotebookHistoryView(MontrekViewTestCase):
    viewname = "notebook_history"
    view_class = NotebookHistoryView

    def build_factories(self):
        self.hub_vd = NotebookHubValueDateFactory(value_date=None)
        NotebookSatelliteFactory(hub_entity=self.hub_vd.hub)

    def url_kwargs(self) -> dict:
        return {"pk": self.hub_vd.id}