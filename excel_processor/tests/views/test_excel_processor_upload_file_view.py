import inspect
import os

from django.test import TestCase
from django.urls import reverse
from testing.test_cases.view_test_cases import MontrekListViewTestCase
from mt_tools.excel_processor.repositories.excel_processor_repositories import (
    ExcelProcessorFileUploadRegistryRepository,
)
from mt_tools.excel_processor.tests.factories.excel_processor_factories import (
    ExcelProcessorFileUploadRegistryStaticSatelliteFactory,
)
from mt_tools.excel_processor.views import (
    ExcelProcessorRegistryListView,
)
from mt_tools.excel_processor.modules.excel_processor_basis_functions import (
    ExcelProcessorBasisFunctions,
)

from testing.decorators import add_logged_in_user

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class TestExcelProcessorUploadFileView(TestCase):
    @add_logged_in_user
    def setUp(self):
        self.url = reverse("excel_processor")
        self.test_file_path_a = os.path.join(DATA_DIR, "test_excel.xlsx")

    def test_view_return_correct_html(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "upload_form.html")
        form = response.context[0]["form"]
        view = response.context[0]["view"]
        self.assertTrue("function" in form.fields)
        list_functions = inspect.getmembers(
            view.excel_processor_functions_class, inspect.isfunction
        )
        list_functions = [
            (f[0], f[0].replace("_", " ").title()) for f in list_functions
        ]
        self.assertEqual(form.fields["function"].choices, list_functions)

    def test_view_post_success__no_change(self):
        with open(self.test_file_path_a, "rb") as f:
            data = {"file": f, "function": "hallo"}
            response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse("excel_processor"))
        test_query = ExcelProcessorFileUploadRegistryRepository().std_queryset()
        self.assertEqual(test_query.count(), 1)
        self.assertEqual(
            response.get("Content-Disposition"), f"attachment; filename={f.name}"
        )


class TestExcelProcessorRegistryListView(MontrekListViewTestCase):
    viewname = "excel_processor_registry"
    view_class = ExcelProcessorRegistryListView
    expected_no_of_rows = 3

    def build_factories(self):
        ExcelProcessorFileUploadRegistryStaticSatelliteFactory.create_batch(
            self.expected_no_of_rows
        )

    def test_view_download_file(self):
        registry_factory = ExcelProcessorFileUploadRegistryStaticSatelliteFactory(
            generate_file_upload_file=True
        )
        response = self.client.get(
            reverse(
                "excel_processor_registry_download",
                kwargs={"pk": registry_factory.hub_entity.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "text/plain",
        )
        self.assertEqual(
            response["Content-Disposition"], 'attachment; filename="test_file.txt"'
        )
