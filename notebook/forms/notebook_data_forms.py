from django import forms
from baseclasses.forms import MontrekCreateForm
from mt_tools.notebook.repositories.notebook_repositories import NotebookRepository


class NotebookDataCreateForm(MontrekCreateForm):
    class Meta:
        exclude = ("data_row", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        notebooks_query = NotebookRepository(self.session_data).receive()
        if "pk" in self.session_data:
            fields = notebooks_query.get(
                hub_entity_id=self.session_data["pk"]
            ).field_name
            for field in fields.split(";"):
                self.fields[field] = forms.CharField(
                    required=False,
                    widget=forms.Textarea(
                        attrs={
                            "id": "id_value",
                            "class": "form-control",
                            "rows": 4,
                            "style": "resize: vertical;",
                        }
                    ),
                )
        self.add_link_choice_field(
            display_field="notebook_name",
            link_name="link_notebook_data_notebook",
            queryset=notebooks_query,
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        keys_to_extract = {"hub_entity_id", "link_notebook_data_notebook"}
        data_row = {
            k: cleaned_data.pop(k)
            for k in list(cleaned_data)
            if k not in keys_to_extract
        }
        cleaned_data["data_row"] = data_row
        return cleaned_data
