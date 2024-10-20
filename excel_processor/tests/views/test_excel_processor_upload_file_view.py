import inspect
import os

from django.test import TestCase
from django.test.client import WSGIRequest
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

    def _get_response_from_function(self, function_name: str) -> WSGIRequest:
        with open(self.test_file_path_a, "rb") as f:
            data = {"file": f, "function": function_name}
            return self.client.post(self.url, data, follow=True)

    def test_view_post_success__no_change(self):
        response = self._get_response_from_function("no_change")
        test_query = ExcelProcessorFileUploadRegistryRepository().std_queryset()
        self.assertEqual(test_query.count(), 1)
        self.assertEqual(
            response.get("Content-Disposition"),
            'attachment; filename="test_excel__no_change.xlsx"',
        )

    def test_view_post__catch_raised_error(self):
        response = self._get_response_from_function("raise_error")
        self.assertEqual(response.status_code, 200)
        test_query = ExcelProcessorFileUploadRegistryRepository().std_queryset()
        self.assertEqual(test_query.count(), 1)
        self.assertEqual(test_query.first().status, "Error")


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
