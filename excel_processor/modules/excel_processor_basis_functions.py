import pandas as pd

from mt_tools.excel_processor.modules.excel_processor_functions import (
    return_excel,
    return_zip,
)


class ExcelProcessorBasisFunctions:
    @staticmethod
    @return_excel
    def format_montrek(inpath: str, session_data: dict) -> dict[str, pd.DataFrame]:
        """Returns the same dataframe as the input."""
        excel_file = pd.ExcelFile(inpath)
        primary_sheet = excel_file.sheet_names[0]
        return {str(primary_sheet): pd.read_excel(excel_file, sheet_name=primary_sheet)}

    @staticmethod
    @return_excel
    def raise_error(inpath: str, session_data: dict) -> dict[str, pd.DataFrame]:
        """Raises an error for testing purposes."""
        raise ValueError("Error")

    @staticmethod
    @return_zip
    def to_markdown(inpath: str, session_data: dict) -> list[str]:
        """Converts the Excel to markdown and stores in zip"""
        data_frame = pd.read_excel(inpath)
        out_path = inpath.replace(".xlsx", ".md")
        data_frame.to_markdown(out_path)
        return [inpath, out_path]
