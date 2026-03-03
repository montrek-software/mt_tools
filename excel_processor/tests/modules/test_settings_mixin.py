from django.test import TestCase

from mt_tools.excel_processor.modules.settings_mixin import SettingsMixin


class MockExcelProcessorFunctions(SettingsMixin):
    has_settings = True


class TestSettingsMixin(TestCase):
    def test_get_setting__no_setting_passed(self):
        settings_mixin = SettingsMixin()
        with self.assertRaises(KeyError):
            settings_mixin.get_settings({})

    def test_get_setting_1(self):
        settings_mixin = MockExcelProcessorFunctions()
        settings = settings_mixin.get_settings({"settings": "settings_1"})
        expected_data = {
            "settings": {
                "sheet_name": "Sheet1",
                "header_row": 1,
                "skip_empty_rows": True,
            },
            "output": {"file_prefix": "processed_", "include_timestamp": True},
        }
        self.assertEqual(settings, expected_data)

    def test_get_setting_2(self):
        settings_mixin = MockExcelProcessorFunctions()
        settings = settings_mixin.get_settings({"settings": "settings_2"})
        expected_data = {
            "settings": {
                "sheet_name": "Data",
                "header_row": 2,
                "skip_empty_rows": False,
                "max_rows": 10000,
            },
            "output": {
                "file_prefix": "export_",
                "include_timestamp": False,
                "date_format": "%Y-%m-%d",
            },
            "filters": {
                "exclude_columns": ["internal_id", "debug_flag"],
                "required_columns": ["name", "value"],
            },
        }
        self.assertEqual(settings, expected_data)

    def test_get_setting__raise_setting_does_not_exist(self):
        settings_mixin = MockExcelProcessorFunctions()
        with self.assertRaises(FileNotFoundError):
            settings_mixin.get_settings({"settings": "settings_3"})
