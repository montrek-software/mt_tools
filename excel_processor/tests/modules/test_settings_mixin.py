from django.test import TestCase

from mt_tools.excel_processor.modules.settings_mixin import SettingsMixin


class TestSettingsMixin(TestCase):
    def test_get_setting__no_setting_passed(self):
        settings_mixin = SettingsMixin()
        with self.assertRaises(KeyError):
            settings_mixin.get_settings({})
