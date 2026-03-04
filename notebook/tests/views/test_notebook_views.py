from mt_tools.notebook.views.notebook_views import NotebookNotebookFieldssListView
from mt_tools.notebook.tests.factories.notebook_sat_factories import NotebookSatelliteFactory
from mt_tools.notebook.tests.factories.notebook_fields_sat_factories import NotebookFieldsSatelliteFactory
from testing.test_cases.view_test_cases import (
    MontrekCreateViewTestCase,
    MontrekDeleteViewTestCase,
    MontrekListViewTestCase,
    MontrekUpdateViewTestCase,
    MontrekViewTestCase,
)

from mt_tools.notebook.tests.factories.notebook_hub_factories import (
    NotebookHubValueDateFactory,
)
from mt_tools.notebook.tests.factories.notebook_sat_factories import (
    NotebookSatelliteFactory,
)
from mt_tools.notebook.views.notebook_views import (
    NotebookCreateView,
    NotebookDeleteView,
    NotebookDetailView,
    NotebookHistoryView,
    NotebookListView,
    NotebookUpdateView,
)


class TestNotebookCreateView(MontrekCreateViewTestCase):
    viewname = "notebook_create"
    view_class = NotebookCreateView

    def creation_data(self):
        return {"notebook_name": "Test Notebook"}


class TestNotebookUpdateView(MontrekUpdateViewTestCase):
    viewname = "notebook_update"
    view_class = NotebookUpdateView

    def build_factories(self):
        self.sat_obj = NotebookSatelliteFactory()

    def url_kwargs(self) -> dict:
        return {"pk": self.sat_obj.get_hub_value_date().id}

    def update_data(self):
        return {"notebook_name": "Test Notebook"}


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

class TestNotebookNotebookFieldssListView(MontrekListViewTestCase):
    viewname = "notebook_notebook_fieldss_list"
    view_class = NotebookNotebookFieldssListView
    expected_no_of_rows = 5

    def build_factories(self):
        self.notebook_factory = NotebookSatelliteFactory.create()
        NotebookFieldsSatelliteFactory.create_batch(
            5, notebook=self.notebook_factory
        )
        other_notebook_factory = NotebookSatelliteFactory.create()
        NotebookFieldsSatelliteFactory.create_batch(
            5, notebook=other_notebook_factory
        )

    def url_kwargs(self):
        return {"pk": self.notebook_factory.get_hub_value_date().pk}