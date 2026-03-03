import inspect

from django import forms
from file_upload.forms import UploadFileForm

from mt_tools.excel_processor.modules.excel_processor_functions import (
    get_excel_processor_settings,
)


class ExcelProcessorUploadFileForm(UploadFileForm):
    def __init__(self, accept: str, *args, **kwargs):
        self.excel_processor_functions_class = kwargs.pop(
            "excel_processor_functions_class"
        )
        super().__init__(accept, *args, **kwargs)
        self.fields["function"] = forms.ChoiceField(
            choices=self._get_function_choices(),
            widget=forms.Select(attrs={"class": "form-control"}),
        )
        if self.excel_processor_functions_class.has_settings:
            self.fields["settings"] = forms.ChoiceField(
                choices=self._get_excel_processor_settings_choices(),
                widget=forms.Select(attrs={"class": "form-control"}),
            )

    def _get_function_choices(self) -> list[tuple[str, str]]:
        list_functions = inspect.getmembers(
            self.excel_processor_functions_class, inspect.isfunction
        )
        return [(f[0], f[0].replace("_", " ").title()) for f in list_functions]

    def _get_excel_processor_settings_choices(self) -> list[tuple[str, str]]:
        choices = get_excel_processor_settings(self.excel_processor_functions_class)
        return sorted([(ch.name, ch.name) for ch in choices])
