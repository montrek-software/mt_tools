from typing import Any, ClassVar

import pandas as pd
from process_pipeline.functions.processor_settings import ProcessorSettingsMixin

from mt_tools.report_generator.modules.report_generator_functions import return_xlsx


def _flatten(settings: dict[str, Any], prefix: str = "") -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    for key, value in settings.items():
        full_key = f"{prefix}{key}"
        if isinstance(value, dict):
            rows.extend(_flatten(value, prefix=f"{full_key}."))
        else:
            rows.append((full_key, value))
    return rows


class ReportGeneratorBasisFunctions(ProcessorSettingsMixin):
    """Reports that ship with the framework.

    Subclass this in your own app, add report functions decorated with
    ``@return_xlsx`` / ``@return_pdf`` / ``@return_zip``, and point your view's
    ``report_functions_class`` at the subclass. Every report function takes
    ``(session_data, settings)`` — the settings are resolved before the function
    runs, from either the settings file the user picked or the one they uploaded.
    """

    label: ClassVar[str] = "Basis Reports"
    description: ClassVar[str] = "Standard reports shipped with the framework."
    has_settings: ClassVar[bool] = True
    # Users may bring their own TOML instead of picking a packaged one.
    require_packaged_settings: ClassVar[bool] = False

    @staticmethod
    @return_xlsx
    def settings_overview(
        session_data: dict, settings: dict
    ) -> dict[str, pd.DataFrame]:
        """Tabulate the resolved settings — use it to check a settings file."""
        rows = _flatten(settings)
        return {
            "settings": pd.DataFrame(
                [{"Setting": key, "Value": str(value)} for key, value in rows],
                columns=["Setting", "Value"],
            )
        }

    @staticmethod
    @return_xlsx
    def raise_error(session_data: dict, settings: dict) -> dict[str, pd.DataFrame]:
        """Raise an error, for testing the failure path."""
        raise ValueError("Error")
