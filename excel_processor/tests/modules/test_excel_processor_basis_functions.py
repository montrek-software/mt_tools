import os

import pandas as pd
from django.test import TestCase
from mt_tools.excel_processor.modules.excel_processor_basis_functions import (
    ExcelProcessorBasisFunctions,
)


class TestExcelProcessorBasisFunctions(TestCase):
    def setUp(self):
        self.test_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "test_file.xlsx"
        )

    def test_format_montrek(self):
        result = ExcelProcessorBasisFunctions.format_montrek(self.test_file_path)
        test_df = pd.read_excel(self.test_file_path)
        pd.testing.assert_frame_equal(result["ExampleSheet"], test_df)

    def test_raise_error(self):
        with self.assertRaises(ValueError):
            ExcelProcessorBasisFunctions.raise_error(self.test_file_path)
