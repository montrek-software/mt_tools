from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import Any, ClassVar, Protocol


class ExcelProcessorReturnType(Enum):
    XLSX = "xlsx"
    ZIP = "zip"


@dataclass
class ExcelProcessorReturn:
    data: Any
    return_type: ExcelProcessorReturnType


class ExcelProcessorFunctionsProtocol(Protocol):
    """Protocol for Excel Processor functions classes.

    Concrete implementations should:
    - Set ``label`` and ``description`` as class-level string attributes.
    - Expose processing logic as ``@staticmethod`` methods decorated with
      ``@return_excel`` or ``@return_zip``.  Each function must accept
      ``(inpath: str, session_data: dict)`` and implicitly return an
      ``ExcelProcessorReturn`` via the decorator.

    The ``label`` is shown to users when selecting a functions class;
    ``description`` can be used in tooltips or documentation pages.
    """

    label: ClassVar[str]
    description: ClassVar[str]
    has_settings: ClassVar[bool]


def return_with_type(return_type):
    """Decorator factory to return data with a specified type."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return ExcelProcessorReturn(
                data=func(*args, **kwargs), return_type=return_type
            )

        wrapper._is_processor_function = True
        return wrapper

    return decorator


# Create specific decorators using the factory
return_excel = return_with_type(ExcelProcessorReturnType.XLSX)
return_zip = return_with_type(ExcelProcessorReturnType.ZIP)
