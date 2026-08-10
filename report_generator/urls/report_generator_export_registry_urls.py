from django.shortcuts import redirect
from django.urls import path

from mt_tools.report_generator.views.report_generator_export_registry_views import (
    ReportGeneratorExportDownloadView,
    ReportGeneratorExportFormView,
    ReportGeneratorExportRegistryListView,
)

urlpatterns = [
    path(
        "report_generator_export_registry",
        lambda _: redirect("report_generator_export_registry_list"),
        name="report_generator_export_registry",
    ),
    path(
        "report_generator_export_registry/list",
        ReportGeneratorExportRegistryListView.as_view(),
        name="report_generator_export_registry_list",
    ),
    path(
        "report_generator_export_registry/generate",
        ReportGeneratorExportFormView.as_view(),
        name="report_generator_export_form",
    ),
    path(
        "report_generator_export_registry/<int:pk>/download",
        ReportGeneratorExportDownloadView.as_view(),
        name="report_generator_export_download",
    ),
]
