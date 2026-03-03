import inspect
from pathlib import Path

import tomllib
from baseclasses.typing import SessionDataType

from mt_tools.excel_processor.modules.excel_processor_functions import (
    SettingsData,
    get_excel_processor_settings,
)


class SettingsMixin:
    @classmethod
    def get_class_file(cls) -> Path:
        return Path(inspect.getfile(cls))

    def get_settings(self, session_data: SessionDataType):
        settings_name = session_data.get("settings")
        if settings_name is None:
            raise KeyError(
                "No settings parameter in session_data. Make sure ExcelProcessorFunctions has has_settings set to True."
            )
        settings_data = self.get_settings_data(settings_name)
        with open(settings_data.get_full_path(), "rb") as f:
            return tomllib.load(f)

    @classmethod
    def get_settings_data(cls, settings_name: str) -> SettingsData:
        settings = get_excel_processor_settings(cls)
        for setting in settings:
            if setting.name == settings_name:
                return setting
        raise ValueError(f"No file '{settings_name}' in settings_folder")
