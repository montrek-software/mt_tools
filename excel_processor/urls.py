from django.urls import path
from mt_tools.excel_processor import views

urlpatterns = [
    path(
        "upload", views.ExcelProcessorUploadFileView.as_view(), name="excel_processor"
    ),
]
