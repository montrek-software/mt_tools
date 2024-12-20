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
        result = ExcelProcessorBasisFunctions.format_montrek(self.test_file_path).data
        test_df = pd.read_excel(self.test_file_path)
        pd.testing.assert_frame_equal(result["ExampleSheet"], test_df)

    def test_raise_error(self):
        with self.assertRaises(ValueError):
            ExcelProcessorBasisFunctions.raise_error(self.test_file_path)

    def test_to_markdown(self):
        results = ExcelProcessorBasisFunctions.to_markdown(self.test_file_path).data
        self.assertEqual(len(results), 2)
        expected_md = """|    |   A |   B |   C |
|---:|----:|----:|----:|
|  0 |   1 |   4 |   8 |
|  1 |   2 |   5 |   9 |
|  2 |   3 |   6 |  10 |"""
        with open(results[1]) as f:
            self.assertEqual(
                f.read(),
                expected_md,
            )
