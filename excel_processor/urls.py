from django.urls import path
from mt_tools.excel_processor import views

urlpatterns = [
    path(
        "upload", views.ExcelProcessorUploadFileView.as_view(), name="excel_processor"
    ),
    path(
        "excel_processor/registry",
        views.ExcelProcessorRegistryListView.as_view(),
        name="excel_processor_registry",
    ),
    path(
        "excel_processor_registry_download/<int:pk>",
        views.ExcelProcessorDownloadFile.as_view(),
        name="excel_processor_registry_download",
    ),
]
