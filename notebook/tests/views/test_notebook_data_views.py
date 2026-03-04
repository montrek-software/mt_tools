from mt_tools.notebook.tests.factories.notebook_fields_sat_factories import (
    NotebookFieldsSatelliteFactory,
)
from mt_tools.notebook.tests.factories.notebook_sat_factories import (
    NotebookSatelliteFactory,
)
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
        notebook = NotebookSatelliteFactory.create()
        NotebookFieldsSatelliteFactory(notebook=notebook, field_name="field_a")
        NotebookFieldsSatelliteFactory(notebook=notebook, field_name="field_b")
        self.sat_obj = NotebookDataSatelliteFactory(notebook=notebook)

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}

    def update_data(self):
        return {"field_a": "Hallo", "field_b": "Wallo"}

    def test_view_post_success(self):
        if not self._pre_test_view_post_success():
            return
        # Check added data
        created_object = self._get_object()
        data = self.update_data()
        self.assertEqual(created_object.data_row, data)


class TestNotebookDataListView(MontrekListViewTestCase):
    viewname = "notebook_data_list"
    view_class = NotebookDataListView
    expected_no_of_rows = 1

    def build_factories(self):
        notebook = NotebookSatelliteFactory.create()
        NotebookFieldsSatelliteFactory(notebook=notebook, field_name="field_a")
        NotebookFieldsSatelliteFactory(notebook=notebook, field_name="field_b")
        self.sat_obj = NotebookDataSatelliteFactory(notebook=notebook)


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
