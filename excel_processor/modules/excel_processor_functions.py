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


def return_with_type(return_type):
    """Decorator factory to return data with a specified type."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            return ExcelProcessorReturn(
                data=func(*args, **kwargs), return_type=return_type
            )

        return wrapper

    return decorator


# Create specific decorators using the factory
return_excel = return_with_type(ExcelProcessorReturnType.XLSX)
return_zip = return_with_type(ExcelProcessorReturnType.ZIP)
