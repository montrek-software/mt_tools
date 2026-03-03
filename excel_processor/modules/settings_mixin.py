from baseclasses.typing import SessionDataType


class SettingsMixin:
    def get_settings(self, session_data: SessionDataType):
        settings_name = session_data.get("settings")
        if settings_name is None:
            raise KeyError(
                "No settings parameter in session_data. Make sure ExcelProcessorFunctions has has_settings set to True."
            )
