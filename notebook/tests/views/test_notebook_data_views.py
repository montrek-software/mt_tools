from testing.test_cases.view_test_cases import (
    MontrekCreateViewTestCase,
    MontrekUpdateViewTestCase,
    MontrekViewTestCase,
    MontrekListViewTestCase,
    MontrekDeleteViewTestCase,
)
from mt_tools.notebook.tests.factories.notebook_data_hub_factories import (
    NotebookDataHubValueDateFactory,
)
from mt_tools.notebook.tests.factories.notebook_data_sat_factories import (
    NotebookDataSatelliteFactory,
)
from mt_tools.notebook.views.notebook_data_views import NotebookDataCreateView
from mt_tools.notebook.views.notebook_data_views import NotebookDataUpdateView
from mt_tools.notebook.views.notebook_data_views import NotebookDataListView
from mt_tools.notebook.views.notebook_data_views import NotebookDataDeleteView
from mt_tools.notebook.views.notebook_data_views import NotebookDataDetailView
from mt_tools.notebook.views.notebook_data_views import NotebookDataHistoryView


class TestNotebookDataCreateView(MontrekCreateViewTestCase):
    viewname = "notebook_data_create"
    view_class = NotebookDataCreateView

    def creation_data(self):
        return {}


class TestNotebookDataUpdateView(MontrekUpdateViewTestCase):
    viewname = "notebook_data_update"
    view_class = NotebookDataUpdateView

    def build_factories(self):
        self.sat_obj = NotebookDataSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}

    def update_data(self):
        return {}


class TestNotebookDataListView(MontrekListViewTestCase):
    viewname = "notebook_data_list"
    view_class = NotebookDataListView
    expected_no_of_rows = 1

    def build_factories(self):
        self.sat_obj = NotebookDataSatelliteFactory()


class TestNotebookDataDeleteView(MontrekDeleteViewTestCase):
    viewname = "notebook_data_delete"
    view_class = NotebookDataDeleteView

    def build_factories(self):
        self.sat_obj = NotebookDataSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}


class TestNotebookDataDetailView(MontrekViewTestCase):
    viewname = "notebook_data_details"
    view_class = NotebookDataDetailView

    def build_factories(self):
        self.hub_vd = NotebookDataHubValueDateFactory(value_date=None)
        NotebookDataSatelliteFactory(hub_entity=self.hub_vd.hub)

    def url_kwargs(self) -> dict:
        return {"pk": self.hub_vd.hub.id}


class TestNotebookDataHistoryView(MontrekViewTestCase):
    viewname = "notebook_data_history"
    view_class = NotebookDataHistoryView

    def build_factories(self):
        self.hub_vd = NotebookDataHubValueDateFactory(value_date=None)
        NotebookDataSatelliteFactory(hub_entity=self.hub_vd.hub)

    def url_kwargs(self) -> dict:
        return {"pk": self.hub_vd.id}
