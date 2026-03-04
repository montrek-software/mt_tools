from django.test import TestCase
from mt_tools.notebook.managers.notebook_managers import (
    NotebookNotebookDatasTableManager,
)
from mt_tools.notebook.tests.factories.notebook_data_sat_factories import (
    NotebookDataSatelliteFactory,
)
from mt_tools.notebook.tests.factories.notebook_fields_sat_factories import (
    NotebookFieldsSatelliteFactory,
)

from mt_tools.notebook.tests.factories.notebook_sat_factories import (
    NotebookSatelliteFactory,
)


class TestNotebookDataManager(TestCase):
    def test_json_separation(self):
        notebook = NotebookSatelliteFactory()
        field_a = NotebookFieldsSatelliteFactory(
            notebook=notebook, field_name="field_a"
        )
        field_b = NotebookFieldsSatelliteFactory(
            notebook=notebook, field_name="field_b"
        )
        data_table = NotebookNotebookDatasTableManager(
            {"pk": notebook.get_hub_value_date().pk}
        )
        NotebookDataSatelliteFactory(
            notebook=notebook, data_row={"field_a": "123", "field_b": "Hallo"}
        )
        NotebookDataSatelliteFactory(
            notebook=notebook, data_row={"unknown_field": "123"}
        )
        test_df = data_table.get_df()
        self.assertIn(field_a.field_name, test_df.columns)
        self.assertIn(field_b.field_name, test_df.columns)
        self.assertNotIn("unknown_field", test_df.columns)
        self.assertEqual(test_df.loc[0, "field_a"], "123")
        self.assertEqual(test_df.loc[0, "field_b"], "Hallo")
        self.assertIsNone(test_df.loc[1, "field_a"])
        self.assertIsNone(test_df.loc[1, "field_b"])
