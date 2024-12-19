import pandas as pd

from mt_tools.excel_processor.modules.excel_processor_functions import return_excel


class ExcelProcessorBasisFunctions:
    @staticmethod
    @return_excel
    def format_montrek(inpath: str) -> dict[str, pd.DataFrame]:
        """Returns the same dataframe as the input."""
        excel_file = pd.ExcelFile(inpath)
        primary_sheet = excel_file.sheet_names[0]
        return {str(primary_sheet): pd.read_excel(excel_file, sheet_name=primary_sheet)}

    @staticmethod
    @return_excel
    def raise_error(inpath: str) -> dict[str, pd.DataFrame]:
        """Raises an error for testing purposes."""
        raise ValueError("Error")
