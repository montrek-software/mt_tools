from django import forms
from django.db.models import QuerySet
from baseclasses.forms import MontrekCreateForm
from mt_tools.notebook.repositories.notebook_data_repositories import (
    NotebookDataRepository,
)
from mt_tools.notebook.repositories.notebook_repositories import NotebookRepository


TEXTAREA_WIDGET = forms.Textarea(
    attrs={
        "class": "form-control",
        "rows": 4,
        "style": "resize: vertical;",
    }
)


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

    def _add_fields_from_field_names(self, field_names: str | None) -> None:
        if field_names is None:
            return
        for field in field_names.split(";"):
            self.fields[field] = forms.CharField(
                required=False,
                widget=TEXTAREA_WIDGET,
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


class NotebookDataCreateForm(NotebookDataBaseForm):
    def get_data_fields(self, notebooks_query: QuerySet) -> None:
        if "pk" in self.session_data:
            field_names = notebooks_query.get(
                hub_entity_id=self.session_data["pk"]
            ).field_name
            self._add_fields_from_field_names(field_names)


class NotebookDataUpdateForm(NotebookDataBaseForm):
    def get_data_fields(self, notebooks_query: QuerySet) -> None:
        notebook_data = (
            NotebookDataRepository(self.session_data)
            .receive()
            .get(pk=self.session_data["pk"])
        )
        field_names = notebooks_query.get(
            hub_entity_id=notebook_data.notebook_id
        ).field_name
        self._add_fields_from_field_names(field_names)
        self.initial.update(notebook_data.data_row)
