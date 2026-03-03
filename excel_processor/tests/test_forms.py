from typing import ClassVar

from django.test import TestCase

from mt_tools.excel_processor.forms import ExcelProcessorUploadFileForm


class MockExcelProcessorFunctionsClass:
    label: ClassVar[str] = "Test Functions"
    description: ClassVar[str] = "Mock functions for testing with settings."
    has_settings: ClassVar[bool] = True

    @staticmethod
    def format_montrek(_inpath: str, _session_data: dict) -> dict[str, str]:
        """Dummy function"""
        return {"dummy": ""}


class TestExcelProcessorForm(TestCase):
    def test_field_selections(self):
        test_form = ExcelProcessorUploadFileForm(
            "accept",
            **{"excel_processor_functions_class": MockExcelProcessorFunctionsClass},
        )
        self.assertEqual(
            test_form.fields["function"].choices, [("format_montrek", "Format Montrek")]
        )
        self.assertEqual(
            test_form.fields["settings"].choices,
            [(sett, sett) for sett in ["settings_1", "settings_2"]],
        )
