"""Excel flavour of the generic TOML settings layer.

The mechanics live in ``process_pipeline.functions.processor_settings``; this
module keeps the ``session_data``-driven API the Excel processor functions were
written against. New processors should use ``ProcessorSettingsMixin`` and
``resolve_settings`` directly, which take an explicit settings name instead of
digging through ``session_data``.
"""

from baseclasses.typing import SessionDataType
from process_pipeline.functions.processor_settings import (  # noqa: F401
    ProcessorSettingsMixin,
    SettingsData,
    load_settings_file,
)


class ExcelProcessorSettingsMixin(ProcessorSettingsMixin):
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

    @classmethod
    def get_excel_processor_settings(cls) -> list[SettingsData]:
        """Return all available TOML settings files for this functions class."""
        return cls.get_available_settings()

    @classmethod
    def get_settings(cls, session_data: SessionDataType) -> dict:
        """Load the TOML settings file selected in *session_data*."""
        settings_name = session_data.get("settings")
        if settings_name is None:
            raise KeyError(
                f"session_data must include a 'settings' key when the {cls.__name__} "
                "has has_settings = True; missing 'settings' entry in session_data."
            )
        if isinstance(settings_name, list) and len(settings_name) == 1:
            settings_name = settings_name[0]
        return cls.load_settings(settings_name)
