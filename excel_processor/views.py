from django.urls import reverse
from file_upload.views import (
    FileUploadRegistryView,
    MontrekDownloadFileView,
    MontrekUploadFileView,
)
from mt_tools.excel_processor.pages import ExcelProcessorPage
from mt_tools.excel_processor.managers.excel_processor_managers import (
    ExcelProcessorManager,
    ExcelProcessorRegistryManager,
)


class ExcelProcessorUploadFileView(MontrekUploadFileView):
    file_upload_manager_class = ExcelProcessorManager
    accept = ".XLSX"
    page_class = ExcelProcessorPage
    tab = "tab_excel_processor_upload"

    def get_success_url(self):
        return reverse("excel_processor")


class ExcelProcessorRegistryListView(FileUploadRegistryView):
    manager_class = ExcelProcessorRegistryManager
    title = "Excel Processor Registry"
    page_class = ExcelProcessorPage


class ExcelProcessorDownloadFile(MontrekDownloadFileView):
    manager_class = ExcelProcessorRegistryManager
    title = "Excel Processor Registry Download"
