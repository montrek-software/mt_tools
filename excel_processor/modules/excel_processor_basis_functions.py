import pandas as pd


class ExcelProcessorBasisFunctions:
    @staticmethod
    def no_change(inpath: str) -> pd.DataFrame:
        """Returns the same dataframe as the input."""
        return pd.read_excel(inpath)

    @staticmethod
    def raise_error(inpath: str) -> pd.DataFrame:
        """Raises an error for testing purposes."""
        raise ValueError("Error")
