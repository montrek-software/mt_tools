from django.urls import path
from mt_tools.excel_processor import views

urlpatterns = [
    path(
        "registry_list",
        views.ExcelProcessorRegistryListView.as_view(),
        name="excel_processor",
    ),
    path(
        "upload",
        views.ExcelProcessorUploadFileView.as_view(),
        name="upload_excel_processor",
    ),
    path(
        "registry_list",
        views.ExcelProcessorRegistryListView.as_view(),
        name="excel_processor_registry",
    ),
    path(
        "file_download/<int:pk>",
        views.ExcelProcessorDownloadFile.as_view(),
        name="excel_processor_registry_download",
    ),
    path(
        "download_processed_file/<int:pk>",
        views.ExcelProcessorDownloadProcessedFileView.as_view(),
        name="excel_processor_download_processed_file",
    ),
]
