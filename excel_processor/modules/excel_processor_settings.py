import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import tomllib
from baseclasses.typing import SessionDataType

from mt_tools.excel_processor.modules.excel_processor_functions import (
    ExcelProcessorFunctionsProtocol,
)


@dataclass
class SettingsData:
    name: str
    path: Path
    filetype: str = "toml"

    def get_full_path(self) -> Path:
        return self.path / f"{self.name}.{self.filetype}"


def get_excel_processor_settings(
    functions_class: type[ExcelProcessorFunctionsProtocol],
) -> list[SettingsData]:
    """Return all available TOML settings files for the given functions class.

    Settings files are expected in a ``settings/`` subfolder next to the
    module that defines *functions_class*.
    """
    if not functions_class.has_settings:
        return []
    class_file = Path(inspect.getfile(functions_class))
    settings_folder = class_file.parent / "settings"
    settings_folder.mkdir(exist_ok=True)
    toml_files = list(settings_folder.glob("*.toml"))
    if not toml_files:
        raise FileNotFoundError(
            f"No .toml settings files found in '{settings_folder}'. "
            "Either add .toml files to the settings folder, "
            f"or set `has_settings = False` on {functions_class.__name__}."
        )
    return [SettingsData(name=f.stem, path=f.parent) for f in toml_files]


def get_settings(
    functions_class: type[ExcelProcessorFunctionsProtocol],
    session_data: SessionDataType,
) -> dict:
    """Load the TOML settings file selected in *session_data* for *functions_class*."""
    settings_name = session_data.get("settings")
    if settings_name is None:
        raise KeyError(
            f"session_data must include a 'settings' key when the {functions_class.__name__} "
            "has has_settings = True; missing 'settings' entry in session_data."
        )
    if isinstance(settings_name, list) and len(settings_name) == 1:
        settings_name = settings_name[0]
    for setting in get_excel_processor_settings(functions_class):
        if setting.name == settings_name:
            with open(setting.get_full_path(), "rb") as f:
                return tomllib.load(f)
    raise FileNotFoundError(
        f"No settings file '{settings_name}' found for {functions_class.__name__}."
    )


class ExcelProcessorSettingsMixin:
    """Mixin that binds settings loading to the functions class.

    Inherit from this mixin when your functions class reads TOML settings.
    Set ``has_settings = True`` and use ``@classmethod`` for any processing
    function that needs to call ``cls.get_settings(session_data)``.

    Example::

        class MyFunctions(ExcelProcessorSettingsMixin):
            label: ClassVar[str] = "My Functions"
            description: ClassVar[str] = "..."
            has_settings: ClassVar[bool] = True

            @classmethod
            @return_excel
            def transform(cls, inpath: str, session_data: dict) -> dict[str, pd.DataFrame]:
                cfg = cls.get_settings(session_data)
                ...
    """

    has_settings: ClassVar[bool] = True

    @classmethod
    def get_settings(cls, session_data: SessionDataType) -> dict:
        return get_settings(cls, session_data)
