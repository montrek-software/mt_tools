from django import forms
from django.db.models import QuerySet
from baseclasses.forms import MontrekCreateForm
from mt_tools.notebook.repositories.notebook_data_repositories import (
    NotebookDataRepository,
)
from mt_tools.notebook.repositories.notebook_repositories import NotebookRepository


class NotebookDataBaseForm(MontrekCreateForm):
    class Meta:
        exclude = ("data_row", "comment")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        notebooks_query = NotebookRepository(self.session_data).receive()
        self.get_data_fields(notebooks_query)
        self.add_link_choice_field(
            display_field="notebook_name",
            link_name="link_notebook_data_notebook",
            queryset=notebooks_query,
        )

    def get_data_fields(self, notebooks_query: QuerySet) -> None: ...

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


class NotebookDataCreateForm(NotebookDataBaseForm):
    def get_data_fields(self, notebooks_query: QuerySet) -> None:
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


class NotebookDataUpdateForm(NotebookDataBaseForm):
    def get_data_fields(self, notebooks_query: QuerySet) -> None:
        notebook_data = (
            NotebookDataRepository(self.session_data)
            .receive()
            .get(pk=self.session_data["pk"])
        )

        fields = notebooks_query.get(hub_entity_id=notebook_data.notebook_id).field_name
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
