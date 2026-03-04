from testing.test_cases.view_test_cases import (
    MontrekCreateViewTestCase,
    MontrekUpdateViewTestCase,
    MontrekViewTestCase,
    MontrekListViewTestCase,
    MontrekDeleteViewTestCase,
)
from mt_tools.notebook.tests.factories.notebook_fields_hub_factories import NotebookFieldsHubValueDateFactory
from mt_tools.notebook.tests.factories.notebook_fields_sat_factories import NotebookFieldsSatelliteFactory
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsCreateView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsUpdateView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsListView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsDeleteView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsDetailView
from mt_tools.notebook.views.notebook_fields_views import NotebookFieldsHistoryView


class TestNotebookFieldsCreateView(MontrekCreateViewTestCase):
    viewname = "notebook_fields_create"
    view_class = NotebookFieldsCreateView

    def creation_data(self):
        return {}


class TestNotebookFieldsUpdateView(MontrekUpdateViewTestCase):
    viewname = "notebook_fields_update"
    view_class = NotebookFieldsUpdateView

    def build_factories(self):
        self.sat_obj = NotebookFieldsSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}

    def update_data(self):
        return {}


class TestNotebookFieldsListView(MontrekListViewTestCase):
    viewname = "notebook_fields_list"
    view_class = NotebookFieldsListView
    expected_no_of_rows = 1

    def build_factories(self):
        self.sat_obj = NotebookFieldsSatelliteFactory()


class TestNotebookFieldsDeleteView(MontrekDeleteViewTestCase):
    viewname = "notebook_fields_delete"
    view_class = NotebookFieldsDeleteView

    def build_factories(self):
        self.sat_obj = NotebookFieldsSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}



class TestNotebookFieldsDetailView(MontrekViewTestCase):
    viewname = "notebook_fields_details"
    view_class = NotebookFieldsDetailView

    def build_factories(self):
        self.hub_vd = NotebookFieldsHubValueDateFactory(value_date=None)
        NotebookFieldsSatelliteFactory(hub_entity=self.hub_vd.hub)

    def url_kwargs(self) -> dict:
        return {"pk": self.hub_vd.hub.id}


class TestNotebookFieldsHistoryView(MontrekViewTestCase):
    viewname = "notebook_fields_history"
    view_class = NotebookFieldsHistoryView

    def build_factories(self):
        self.hub_vd = NotebookFieldsHubValueDateFactory(value_date=None)
        NotebookFieldsSatelliteFactory(hub_entity=self.hub_vd.hub)

    def url_kwargs(self) -> dict:
        return {"pk": self.hub_vd.id}