from django import forms
from process_pipeline.functions.forms import FunctionSelectionFormMixin

SETTINGS_FILE_ACCEPT = ".toml,.TOML"


class ReportGeneratorExportForm(FunctionSelectionFormMixin, forms.Form):
    """Pick a report, pick its settings, or upload settings of your own."""

    def __init__(self, *args, functions_class: type, **kwargs):
        super().__init__(*args, **kwargs)
        self.functions_class = functions_class
        self.add_function_fields(functions_class)
        self.fields["settings_file"] = forms.FileField(
            required=False,
            label="Settings file",
            help_text="Optional. Overrides the selected settings.",
            widget=forms.FileInput(
                attrs={
                    "id": "id_report__settings_file",
                    "class": "form-control mb-2",
                    "accept": SETTINGS_FILE_ACCEPT,
                }
            ),
        )

    def clean_settings_file(self):
        settings_file = self.cleaned_data.get("settings_file")
        if not settings_file:
            return None
        allowed = [
            file_type.lstrip(".").upper()
            for file_type in SETTINGS_FILE_ACCEPT.split(",")
        ]
        if settings_file.name.split(".")[-1].upper() not in allowed:
            raise forms.ValidationError("The settings file must be a .toml file.")
        return settings_file
