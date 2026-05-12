from unittest.mock import MagicMock

from django.test import TestCase
from django.urls import reverse

from mt_tools.excel_processor.managers.excel_processor_managers import ExcelProcessor
from mt_tools.excel_processor.modules.excel_processor_functions import (
    ExcelProcessorReturnType,
)


def _make_processor(function_value: str | list) -> ExcelProcessor:
    session_data = {
        "function": function_value,
        "request_path": reverse("upload_excel_processor"),
    }
    return ExcelProcessor(
        file_upload_registry_hub=MagicMock(),
        session_data=session_data,
    )


class TestExcelProcessorFunctionName(TestCase):
    def test_function_as_list_takes_first_element(self):
        processor = _make_processor(["format_montrek"])
        self.assertEqual(processor.processor_function_name, "format_montrek")

    def test_function_as_string_used_directly(self):
        processor = _make_processor("format_montrek")
        self.assertEqual(processor.processor_function_name, "format_montrek")

    def test_function_as_list_with_multiple_entries_takes_first(self):
        processor = _make_processor(["format_montrek", "raise_error"])
        self.assertEqual(processor.processor_function_name, "format_montrek")


class TestExcelProcessorGetFilename(TestCase):
    def setUp(self):
        self.processor = _make_processor("format_montrek")
        self.processor.output = MagicMock()
        self.processor.output.return_type = ExcelProcessorReturnType.XLSX

    def test_with_file_path_uses_file_base_name(self):
        result = self.processor._get_filename("/some/path/report.xlsx")
        self.assertEqual(result, "report__format_montrek.xlsx")

    def test_with_none_file_path_uses_function_name_as_base(self):
        result = self.processor._get_filename(None)
        self.assertEqual(result, "format_montrek__format_montrek.xlsx")

    def test_with_empty_string_uses_function_name_as_base(self):
        result = self.processor._get_filename("")
        self.assertEqual(result, "format_montrek__format_montrek.xlsx")

    def test_filename_extension_matches_return_type(self):
        self.processor.output.return_type = ExcelProcessorReturnType.ZIP
        result = self.processor._get_filename(None)
        self.assertEqual(result, "format_montrek__format_montrek.zip")

    def test_file_path_with_multiple_dots_uses_first_segment(self):
        result = self.processor._get_filename("/path/to/my.report.file.xlsx")
        self.assertEqual(result, "my__format_montrek.xlsx")
