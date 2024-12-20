import inspect
import io
import os
import zipfile

from django.test.client import WSGIRequest
from django.urls import reverse
from mt_tools.excel_processor.repositories.excel_processor_repositories import (
    ExcelProcessorFileUploadRegistryRepository,
)
from mt_tools.excel_processor.tests.factories.excel_processor_factories import (
    ExcelProcessorFileUploadRegistryStaticSatelliteFactory,
)
from mt_tools.excel_processor.views import (
    ExcelProcessorRegistryListView,
    ExcelProcessorUploadFileView,
)
from testing.decorators import add_logged_in_user
from testing.test_cases.view_test_cases import (
    MontrekListViewTestCase,
    MontrekViewTestCase,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class ExcelProcessorUploadFileTestCase(MontrekViewTestCase):
    @add_logged_in_user
    def setUp(self):
        super().setUp()
        self.test_file_path_a = os.path.join(DATA_DIR, "test_excel.xlsx")

    def _is_base_test_class(self) -> bool:
        # Django runs all tests within these base classes here individually. This is not wanted and hence we skip the tests if django attempts to do this.
        return self.__class__.__name__ == "ExcelProcessorUploadFileTestCase"

    def test_view_return_correct_html(self):
        if self._is_base_test_class():
            return
        super().test_view_return_correct_html()
        form = self.response.context[0]["form"]
        view = self.response.context[0]["view"]
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

    def _do_test_view_post_success(self, function_name: str):
        response = self._get_response_from_function(function_name)
        test_query = ExcelProcessorFileUploadRegistryRepository().receive()
        self.assertEqual(test_query.count(), 1)
        content_disposition = response.get("Content-Disposition")
        self.assertTrue(
            content_disposition.startswith('attachment; filename="test_excel'),
        )
        self.assertTrue(
            content_disposition.endswith(f'__{function_name}.xlsx"'),
        )


class TestExcelProcessorFileUploadView(ExcelProcessorUploadFileTestCase):
    viewname = "excel_processor"
    view_class = ExcelProcessorUploadFileView

    def test_view_post_success__format_montrek(self):
        self._do_test_view_post_success("format_montrek")

    def test_view_post_success__to_markdown(self):
        response = self._get_response_from_function("to_markdown")
        test_query = ExcelProcessorFileUploadRegistryRepository().receive()
        self.assertEqual(test_query.count(), 1)
        content_disposition = response.get("Content-Disposition")
        self.assertIsNotNone(content_disposition)
        self.assertEqual(
            content_disposition, 'attachment; filename="test_excel__to_markdown.zip"'
        )
        zip_file = io.BytesIO(response.content)
        # Open the ZIP file
        with zipfile.ZipFile(zip_file, "r") as zip:
            # Check the list of files in the ZIP archive
            files_in_zip = zip.namelist()
            expected_files = ["test_excel.xlsx", "test_excel.md"]
            # Assert all expected files are present
            for expected_file in expected_files:
                self.assertIn(expected_file, files_in_zip)

    def test_view_post__catch_raised_error(self):
        response = self._get_response_from_function("raise_error")
        self.assertEqual(response.status_code, 404)
        test_query = ExcelProcessorFileUploadRegistryRepository().receive()
        self.assertEqual(test_query.count(), 1)
        self.assertEqual(test_query.first().upload_status, "failed")
        self.assertEqual(
            test_query.first().upload_message,
            "Error raised during Excel File Processing function raise_error: Error",
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
