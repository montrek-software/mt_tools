import inspect
from file_upload.forms import UploadFileForm
from django import forms


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

    def _get_function_choices(self) -> list[tuple[str, str]]:
        list_functions = inspect.getmembers(
            self.excel_processor_functions_class, inspect.isfunction
        )
        return [(f[0], f[0].replace("_", " ").title()) for f in list_functions]
