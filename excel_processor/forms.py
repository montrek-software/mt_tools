from file_upload.forms import UploadFileForm
from django import forms


class ExcelProcessorUploadFileForm(UploadFileForm):
    def __init__(self, accept: str, *args, **kwargs):
        super().__init__(accept, *args, **kwargs)
        self.fields["function"] = forms.ChoiceField(
            choices=[("no_change", "No Change"), ("delete", "Delete")],
            widget=forms.Select(attrs={"class": "form-control"}),
        )
