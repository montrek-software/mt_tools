from dataclasses import dataclass
from enum import Enum
from typing import Any


class ExcelProcessorReturnType(Enum):
    XLSX = "xlsx"
    ZIP = "zip"


@dataclass
class ExcelProcessorReturn:
    data: Any
    return_type: ExcelProcessorReturnType


def return_excel(func):
    def wrapper(*args, **kwargs):
        return ExcelProcessorReturn(
            data=func(*args, **kwargs), return_type=ExcelProcessorReturnType.XLSX
        )

    return wrapper
