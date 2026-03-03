from django.test import TestCase

from mt_tools.excel_processor.modules.settings_mixin import SettingsMixin


class MockExcelProcessorFunctions(SettingsMixin):
    has_settings = True


class TestSettingsMixin(TestCase):
    def test_get_setting__no_setting_passed(self):
        settings_mixin = SettingsMixin()
        with self.assertRaises(KeyError):
            settings_mixin.get_settings({})

    def test_get_setting(self):
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
