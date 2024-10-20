import pandas as pd


class ExcelProcessorBasisFunctions:
    @staticmethod
    def no_change(inpath: str) -> pd.DataFrame:
        return pd.read_excel(inpath)
