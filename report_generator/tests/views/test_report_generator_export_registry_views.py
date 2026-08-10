from unittest.mock import MagicMock

import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from process_pipeline.functions.selection import FunctionSelection, get_dotted_path
from testing.decorators.add_logged_in_user import add_logged_in_user
from testing.test_cases.view_test_cases import (
    MontrekDownloadViewTestCase,
    MontrekListViewTestCase,
)

from mt_tools.report_generator.managers.report_generator_export_processor import (
    ReportGeneratorFileExportProcessor,
)
from mt_tools.report_generator.modules.report_generator_basis_functions import (
    ReportGeneratorBasisFunctions,
)
from mt_tools.report_generator.repositories.report_generator_export_registry_repositories import (
    ReportGeneratorExportRegistryRepository,
)
from mt_tools.report_generator.tests.factories.report_generator_export_registry_sat_factories import (
    ReportGeneratorExportRegistrySatelliteFactory,
)
from mt_tools.report_generator.views.report_generator_export_registry_views import (
    ReportGeneratorExportDownloadView,
    ReportGeneratorExportRegistryListView,
)

CUSTOM_SETTINGS_TOML = b'[report]\ntitle = "Custom Report"\n'


def _make_processor(
    function_name: str,
    settings_name: str | None = "default",
    settings_file_name: str | None = None,
) -> ReportGeneratorFileExportProcessor:
    processor = ReportGeneratorFileExportProcessor(MagicMock(), {})
    processor.set_pipeline_data(
        FunctionSelection(
            functions_class_path=get_dotted_path(ReportGeneratorBasisFunctions),
            function_name=function_name,
            settings_name=settings_name,
            settings_file_name=settings_file_name,
        ).to_pipeline_data()
    )
    return processor


class TestReportGeneratorExportRegistryListView(MontrekListViewTestCase):
    viewname = "report_generator_export_registry_list"
    view_class = ReportGeneratorExportRegistryListView
    expected_no_of_rows = 3

    def build_factories(self):
        ReportGeneratorExportRegistrySatelliteFactory.create_batch(3)


class TestReportGeneratorExportDownloadView(MontrekDownloadViewTestCase):
    viewname = "report_generator_export_download"
    view_class = ReportGeneratorExportDownloadView

    def build_factories(self):
        self.registry_sat = ReportGeneratorExportRegistrySatelliteFactory(
            generate_export_file=True
        )

    def url_kwargs(self) -> dict:
        return {"pk": self.registry_sat.get_hub_value_date().pk}

    def expected_filename(self) -> str:
        # Django may append a uniqueness suffix; match any test_export*.csv
        return r"test_export.*\.csv"


class ReportGeneratorExportFormViewTestCaseMixin:
    @add_logged_in_user
    def setUp(self):
        self.url = reverse("report_generator_export_form")
        self.list_url = reverse("report_generator_export_registry_list")

    def get_registry(self):
        return ReportGeneratorExportRegistryRepository().receive().first()

    def read_report(self, registry) -> pd.DataFrame:
        export_file = ReportGeneratorExportRegistryRepository().get_export_file(
            registry.pk
        )
        return pd.read_excel(export_file)


class TestReportGeneratorExportFormViewGet(
    ReportGeneratorExportFormViewTestCaseMixin, TestCase
):
    def test_view_returns_correct_html(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "export_form.html")

    def test_form_offers_function_settings_and_upload(self):
        response = self.client.get(self.url)
        form = response.context["export_form"]
        self.assertEqual(sorted(form.fields), ["function", "settings", "settings_file"])

    def test_function_choices_come_from_the_functions_class(self):
        response = self.client.get(self.url)
        form = response.context["export_form"]
        self.assertEqual(
            form.fields["function"].choices,
            [
                ("raise_error", "Raise Error"),
                ("settings_overview", "Settings Overview"),
            ],
        )

    def test_settings_choices_come_from_the_settings_folder(self):
        response = self.client.get(self.url)
        form = response.context["export_form"]
        self.assertEqual(form.fields["settings"].choices, [("default", "default")])


class TestReportGeneratorExportFormViewPost(
    ReportGeneratorExportFormViewTestCaseMixin, TestCase
):
    def test_post_redirects_to_the_registry(self):
        response = self.client.post(
            self.url,
            data={"function": "settings_overview", "settings": "default"},
            follow=True,
        )
        self.assertRedirects(response, self.list_url)

    def test_post_writes_a_processed_registry_entry(self):
        self.client.post(
            self.url,
            data={"function": "settings_overview", "settings": "default"},
        )
        registry = self.get_registry()
        self.assertEqual(registry.export_status, "processed")
        self.assertEqual(registry.export_message, "Generated settings_overview!")

    def test_post_attaches_the_generated_report(self):
        self.client.post(
            self.url,
            data={"function": "settings_overview", "settings": "default"},
        )
        registry = self.get_registry()
        self.assertTrue(bool(registry.export_file))
        report = self.read_report(registry)
        self.assertIn("report.title", list(report["Setting"]))

    def test_uploaded_settings_file_wins_over_the_selected_one(self):
        settings_file = SimpleUploadedFile(
            name="custom.toml",
            content=CUSTOM_SETTINGS_TOML,
            content_type="application/toml",
        )
        self.client.post(
            self.url,
            data={
                "function": "settings_overview",
                "settings": "default",
                "settings_file": settings_file,
            },
        )
        registry = self.get_registry()
        self.assertEqual(registry.export_status, "processed")
        report = self.read_report(registry)
        self.assertEqual(list(report["Setting"]), ["report.title"])
        self.assertEqual(list(report["Value"]), ["Custom Report"])

    def test_non_toml_settings_file_is_rejected(self):
        settings_file = SimpleUploadedFile(
            name="custom.txt",
            content=CUSTOM_SETTINGS_TOML,
            content_type="text/plain",
        )
        response = self.client.post(
            self.url,
            data={
                "function": "settings_overview",
                "settings": "default",
                "settings_file": settings_file,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.get_registry())
        self.assertIn(
            "The settings file must be a .toml file.",
            response.context["export_form"].errors["settings_file"],
        )

    def test_failing_report_function_is_recorded_as_failed(self):
        self.client.post(
            self.url,
            data={"function": "raise_error", "settings": "default"},
        )
        registry = self.get_registry()
        self.assertEqual(registry.export_status, "failed")
        self.assertIn(
            "Error raised during report function raise_error", registry.export_message
        )


class TestReportGeneratorFileExportProcessor(TestCase):
    def test_pre_check_loads_the_selected_settings(self):
        processor = _make_processor("settings_overview")
        self.assertTrue(processor.pre_check())
        self.assertEqual(processor.settings["report"]["title"], "Report")

    def test_pre_check_reports_unknown_settings(self):
        processor = _make_processor("settings_overview", settings_name="nope")
        self.assertFalse(processor.pre_check())
        self.assertIn("Could not load the report settings", processor.message)

    def test_process_runs_the_selected_function(self):
        processor = _make_processor("settings_overview")
        processor.pre_check()
        self.assertTrue(processor.process())
        self.assertEqual(processor.message, "Generated settings_overview!")

    def test_process_reports_a_failing_function(self):
        processor = _make_processor("raise_error")
        processor.pre_check()
        self.assertFalse(processor.process())
        self.assertIn(
            "Error raised during report function raise_error", processor.message
        )

    def test_post_check_builds_the_result_file(self):
        processor = _make_processor("settings_overview")
        processor.pre_check()
        processor.process()
        self.assertTrue(processor.post_check())
        self.assertEqual(processor.result_file.name, "settings_overview.xlsx")

    def test_post_check_without_output_fails(self):
        processor = _make_processor("settings_overview")
        self.assertFalse(processor.post_check())
        self.assertIn("returned nothing", processor.message)
