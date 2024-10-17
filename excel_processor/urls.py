from django.urls import path
from mt_tools.excel_processor import views

urlpatterns = [
    path(
        "upload", views.ExcelProcessorUploadFileView.as_view(), name="excel_processor"
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
]
