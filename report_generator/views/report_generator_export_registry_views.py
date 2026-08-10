import os
import uuid

from baseclasses.dataclasses.view_classes import ListActionElement, PlayActionElement
from django.core.files.storage import default_storage
from django.forms import Form
from django.urls import reverse
from django.utils.text import get_valid_filename
from file_export.views.file_export_views import (
    FileExportDownloadView,
    FileExportFormView,
    FileExportRegistryListView,
)
from process_pipeline.functions.selection import FunctionSelection

from mt_tools.report_generator.forms.report_generator_export_forms import (
    ReportGeneratorExportForm,
)
from mt_tools.report_generator.managers.report_generator_export_manager import (
    ReportGeneratorFileExportManager,
)
from mt_tools.report_generator.managers.report_generator_export_registry_managers import (
    ReportGeneratorExportRegistryTableManager,
)
from mt_tools.report_generator.modules.report_generator_basis_functions import (
    ReportGeneratorBasisFunctions,
)
from mt_tools.report_generator.pages.report_generator_export_registry_pages import (
    ReportGeneratorExportRegistryPage,
)

SETTINGS_UPLOAD_FOLDER = "report_generator_settings"


class ReportGeneratorExportRegistryListView(FileExportRegistryListView):
    manager_class = ReportGeneratorExportRegistryTableManager
    page_class = ReportGeneratorExportRegistryPage
    tab = "tab_report_generator_export_registry_list"
    title = "Report Generator Export Registry List"

    @property
    def actions(self) -> tuple:
        action_export = PlayActionElement(
            url_name="report_generator_export_form",
            hover_text="Generate a report",
        )
        return (action_export,)


class ReportGeneratorExportFormView(FileExportFormView):
    """Lets the user pick a report and the settings it should run with."""

    manager_class = ReportGeneratorFileExportManager
    export_form_class = ReportGeneratorExportForm
    report_functions_class: type = ReportGeneratorBasisFunctions
    page_class = ReportGeneratorExportRegistryPage
    tab = "tab_report_generator_export_registry_list"
    title = "Generate Report"
    submit_label = "Generate Report"

    @property
    def actions(self) -> tuple:
        return (ListActionElement("report_generator_export_registry_list"),)

    def get_form_kwargs(self) -> dict:
        return {"functions_class": self.report_functions_class}

    def get_pipeline_data(self, form: Form) -> dict:
        return FunctionSelection.from_cleaned_data(
            self.report_functions_class,
            form.cleaned_data,
            settings_file_name=self.store_settings_file(
                form.cleaned_data.get("settings_file")
            ),
        ).to_pipeline_data()

    def store_settings_file(self, settings_file) -> str | None:
        """Persist an uploaded settings file so the worker can read it back.

        Returns the name in the default storage rather than a filesystem path,
        so a worker on another host still reaches the file the web process saved.
        """
        if not settings_file:
            return None
        return default_storage.save(
            f"{SETTINGS_UPLOAD_FOLDER}/{self._get_storage_name(settings_file.name)}",
            settings_file,
        )

    @staticmethod
    def _get_storage_name(uploaded_name: str) -> str:
        """Turn a client-supplied file name into a safe, unique storage name.

        The name comes from the browser, so path segments and unsafe characters
        are stripped rather than trusted to the storage backend. The prefix keeps
        two users uploading ``settings.toml`` from landing on the same key.
        """
        safe_name = get_valid_filename(os.path.basename(uploaded_name))
        return f"{uuid.uuid4().hex}_{safe_name}"

    def get_success_url(self) -> str:
        return reverse("report_generator_export_registry_list")


class ReportGeneratorExportDownloadView(FileExportDownloadView):
    manager_class = ReportGeneratorExportRegistryTableManager
