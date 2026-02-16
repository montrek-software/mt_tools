import inspect
import io
import os
import zipfile

from django.test.client import WSGIRequest
from django.urls import reverse
from testing.decorators import add_logged_in_user
from testing.test_cases.view_test_cases import (
    MontrekDownloadViewTestCase,
    MontrekListViewTestCase,
    MontrekViewTestCase,
)

from mt_tools.excel_processor.repositories.excel_processor_repositories import (
    ExcelProcessorFileUploadRegistryRepository,
)
from mt_tools.excel_processor.tests.factories.excel_processor_factories import (
    ExcelProcessorFileUploadRegistryStaticSatelliteFactory,
)
from mt_tools.excel_processor.views import (
    ExcelProcessorDownloadProcessedFileView,
    ExcelProcessorRegistryListView,
    ExcelProcessorUploadFileView,
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
        form = self.response.context[0]["upload_form"]
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
        self._get_response_from_function(function_name)
        test_query = ExcelProcessorFileUploadRegistryRepository().receive()
        self.assertEqual(test_query.count(), 1)
        test_registry = test_query.first()
        response = self.client.get(
            reverse(
                self.processed_file_download_url,
                kwargs={"pk": test_registry.pk},
            )
        )
        content_disposition = response.get("Content-Disposition")
        self.assertTrue(
            content_disposition.startswith('attachment; filename="test_excel'),
        )
        self.assertTrue(
            content_disposition.endswith(f'__{function_name}.xlsx"'),
        )


class TestExcelProcessorFileUploadView(ExcelProcessorUploadFileTestCase):
    viewname = "upload_excel_processor"
    view_class = ExcelProcessorUploadFileView
    processed_file_download_url = "excel_processor_download_processed_file"

    def test_view_post_success__format_montrek(self):
        self._do_test_view_post_success("format_montrek")

    def test_view_post_success__to_markdown(self):
        self._get_response_from_function("to_markdown")
        test_query = ExcelProcessorFileUploadRegistryRepository().receive()
        self.assertEqual(test_query.count(), 1)
        test_registry = test_query.first()
        response = self.client.get(
            reverse(
                self.processed_file_download_url,
                kwargs={"pk": test_registry.pk},
            )
        )
        content_disposition = response.get("Content-Disposition")
        self.assertIsNotNone(content_disposition)
        self.assertTrue(
            content_disposition.startswith('attachment; filename="test_excel')
        )
        self.assertTrue(content_disposition.endswith('__to_markdown.zip"'))
        content = b"".join(response.streaming_content)

        with zipfile.ZipFile(io.BytesIO(content), "r") as zip:
            files_in_zip = zip.namelist()
            expected_file_types = ["xlsx", "md"]

            for result_file in files_in_zip:
                self.assertTrue(result_file.startswith("test_excel"))
                file_appendix = result_file.split(".")[-1]
                self.assertIn(file_appendix, expected_file_types)

    def test_view_post__catch_raised_error(self):
        response = self._get_response_from_function("raise_error")
        self.assertEqual(response.status_code, 200)
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
            "text/csv",
        )
        self.assertEqual(
            response["Content-Disposition"],
            f'attachment; filename="{registry_factory.file_name}"',
        )


class TestExcelProcessorDownloadProcessedFileView(MontrekDownloadViewTestCase):
    viewname = "excel_processor_download_processed_file"
    view_class = ExcelProcessorDownloadProcessedFileView

    def expected_filename(self):
        return r"test_processed_file_[A-Za-z0-9]+\.txt"

    def build_factories(self):
        self.registry = ExcelProcessorFileUploadRegistryStaticSatelliteFactory(
            generate_file_processed_file=True
        )

    def url_kwargs(self):
        return {"pk": self.registry.get_hub_value_date().pk}
