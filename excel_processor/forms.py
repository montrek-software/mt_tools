import inspect

from django import forms
from file_upload.forms import UploadFileForm


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
        all_members = inspect.getmembers(
            self.excel_processor_functions_class,
            predicate=lambda f: inspect.isfunction(f) or inspect.ismethod(f),
        )
        marked = [
            f for f in all_members if getattr(f[1], "_is_processor_function", False)
        ]
        return [(f[0], f[0].replace("_", " ").title()) for f in marked]

    def _get_excel_processor_settings_choices(self) -> list[tuple[str, str]]:
        choices = self.excel_processor_functions_class.get_excel_processor_settings()
        return sorted([(ch.name, ch.name) for ch in choices])
