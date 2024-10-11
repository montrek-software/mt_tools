from django.urls import reverse
from file_upload.views import MontrekUploadFileView
from mt_tools.excel_processor.pages import ExcelProcessorPage


class ExcelProcessorUploadFileView(MontrekUploadFileView):
    # file_upload_manager_class = ExcelProcessorManager
    accept = ".XLSX"
    page_class = ExcelProcessorPage
    tab = "tab_excel_processor_upload"

    def get_success_url(self):
        return reverse("excel_processor")
