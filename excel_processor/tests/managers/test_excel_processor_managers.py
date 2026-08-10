from unittest.mock import MagicMock

from django.test import TestCase
from process_pipeline.functions.selection import FunctionSelection, get_dotted_path

from mt_tools.excel_processor.managers.excel_processor_managers import ExcelProcessor
from mt_tools.excel_processor.modules.excel_processor_basis_functions import (
    ExcelProcessorBasisFunctions,
)
from mt_tools.excel_processor.modules.excel_processor_functions import (
    ExcelProcessorReturnType,
)

FUNCTIONS_CLASS_PATH = get_dotted_path(ExcelProcessorBasisFunctions)


def _make_processor(function_name: str) -> ExcelProcessor:
    processor = ExcelProcessor(
        file_upload_registry_hub=MagicMock(),
        session_data={},
    )
    processor.set_pipeline_data(
        FunctionSelection(
            functions_class_path=FUNCTIONS_CLASS_PATH,
            function_name=function_name,
        ).to_pipeline_data()
    )
    return processor


class TestExcelProcessorSelection(TestCase):
    def test_function_name_read_from_pipeline_data(self):
        processor = _make_processor("format_montrek")
        self.assertEqual(processor.processor_function_name, "format_montrek")

    def test_functions_class_read_from_pipeline_data(self):
        processor = _make_processor("format_montrek")
        self.assertIs(
            processor.excel_processor_functions_class, ExcelProcessorBasisFunctions
        )

    def test_unknown_function_name_is_rejected(self):
        processor = _make_processor("get_excel_processor_settings")
        self.assertFalse(processor.process("/some/path/report.xlsx"))
        self.assertIn("is not a processor function", processor.message)


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
