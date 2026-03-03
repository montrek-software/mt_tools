from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

from django.test import TestCase

from mt_tools.excel_processor.modules.excel_processor_settings import (
    get_excel_processor_settings,
)


class MockExcelProcessorNoSettings:
    """Mock class with has_settings = False."""

    label: ClassVar[str] = "Mock No Settings"
    description: ClassVar[str] = "A mock class that has no settings."
    has_settings: ClassVar[bool] = False


class MockExcelProcessorWithSettings:
    """Mock class with has_settings = True."""

    label: ClassVar[str] = "Mock With Settings"
    description: ClassVar[str] = "A mock class that has settings."
    has_settings: ClassVar[bool] = True


class GetExcelProcessorSettingsTests(TestCase):
    def test_returns_empty_list_when_has_settings_is_false(self):
        result = get_excel_processor_settings(MockExcelProcessorNoSettings)
        self.assertEqual(result, [])

    def test_creates_settings_folder_if_not_exists(self):
        with (
            patch("inspect.getfile", return_value="/fake/path/module.py"),
            patch("pathlib.Path.mkdir") as mock_mkdir,
            patch("pathlib.Path.glob", return_value=[]),
        ):
            with self.assertRaises(FileNotFoundError):
                get_excel_processor_settings(MockExcelProcessorWithSettings)
            mock_mkdir.assert_called_once_with(exist_ok=True)

    def test_raises_error_when_settings_folder_is_empty(self):
        with (
            patch("inspect.getfile", return_value="/fake/path/module.py"),
            patch("pathlib.Path.mkdir"),
            patch("pathlib.Path.glob", return_value=[]),
        ):
            with self.assertRaises(FileNotFoundError) as ctx:
                get_excel_processor_settings(MockExcelProcessorWithSettings)
            self.assertIn("MockExcelProcessorWithSettings", str(ctx.exception))
            self.assertIn("has_settings = False", str(ctx.exception))

    def test_returns_toml_file_paths_as_strings(self):
        toml_files = [
            Path("/fake/path/settings/config.toml"),
            Path("/fake/path/settings/defaults.toml"),
        ]
        with (
            patch("inspect.getfile", return_value="/fake/path/module.py"),
            patch("pathlib.Path.mkdir"),
            patch("pathlib.Path.glob", return_value=toml_files),
        ):
            result = get_excel_processor_settings(MockExcelProcessorWithSettings)
        self.assertEqual([res.get_full_path() for res in result], toml_files)

    def test_returns_single_toml_file_as_list(self):
        toml_files = [Path("/fake/path/settings/only.toml")]
        with (
            patch("inspect.getfile", return_value="/fake/path/module.py"),
            patch("pathlib.Path.mkdir"),
            patch("pathlib.Path.glob", return_value=toml_files),
        ):
            result = get_excel_processor_settings(MockExcelProcessorWithSettings)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].filetype, "toml")
