import inspect
import os
from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

from django.test import TestCase

from mt_tools.excel_processor.modules.excel_processor_settings import (
    ExcelProcessorSettingsMixin,
)


class MockExcelProcessorWithSettings(ExcelProcessorSettingsMixin):
    """Mock class with has_settings = True."""

    label: ClassVar[str] = "Mock With Settings"
    description: ClassVar[str] = "A mock class that has settings."


class MockExcelProcessorWithSettingsPath(MockExcelProcessorWithSettings):
    @classmethod
    def get_settings_path(cls) -> Path:
        return Path(inspect.getfile(cls)).resolve().parent / "alt_settings"


class GetExcelProcessorSettingsTests(TestCase):
    def test_creates_settings_folder_if_not_exists(self):
        with (
            patch("inspect.getfile", return_value="/fake/path/module.py"),
            patch("pathlib.Path.mkdir") as mock_mkdir,
            patch("pathlib.Path.glob", return_value=[]),
        ):
            with self.assertRaises(FileNotFoundError):
                MockExcelProcessorWithSettings.get_excel_processor_settings()
            mock_mkdir.assert_called_once_with(exist_ok=True)

    def test_raises_error_when_settings_folder_is_empty(self):
        with (
            patch("inspect.getfile", return_value="/fake/path/module.py"),
            patch("pathlib.Path.mkdir"),
            patch("pathlib.Path.glob", return_value=[]),
        ):
            with self.assertRaises(FileNotFoundError) as ctx:
                MockExcelProcessorWithSettings.get_excel_processor_settings()
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
            result = MockExcelProcessorWithSettings.get_excel_processor_settings()
        self.assertEqual([res.get_full_path() for res in result], toml_files)

    def test_returns_single_toml_file_as_list(self):
        toml_files = [Path("/fake/path/settings/only.toml")]
        with (
            patch("inspect.getfile", return_value="/fake/path/module.py"),
            patch("pathlib.Path.mkdir"),
            patch("pathlib.Path.glob", return_value=toml_files),
        ):
            result = MockExcelProcessorWithSettings.get_excel_processor_settings()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].filetype, "toml")

    def test_returns_toml_file_paths_as_strings_no_default_settings_path(self):
        settings_path = Path(__file__).resolve().parent / "alt_settings"
        toml_files = os.listdir(settings_path)
        toml_files = sorted(
            [
                settings_path / toml_file
                for toml_file in toml_files
                if toml_file.endswith(".toml")
            ]
        )
        result = MockExcelProcessorWithSettingsPath.get_excel_processor_settings()
        self.assertEqual(sorted([res.get_full_path() for res in result]), toml_files)
