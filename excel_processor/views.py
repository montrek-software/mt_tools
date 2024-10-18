from django.urls import reverse
from baseclasses.dataclasses.view_classes import ActionElement
from file_upload.views import (
    FileUploadRegistryView,
    MontrekDownloadFileView,
    MontrekUploadFileView,
)
from mt_tools.excel_processor.forms import ExcelProcessorUploadFileForm
from mt_tools.excel_processor.managers.excel_processor_managers import (
    ExcelProcessorManager,
    ExcelProcessorRegistryManager,
)
from mt_tools.excel_processor.pages import ExcelProcessorPage
from mt_tools.excel_processor.modules.excel_processor_basis_functions import (
    ExcelProcessorBasisFunctions,
)


class ExcelProcessorUploadFileView(MontrekUploadFileView):
    file_upload_manager_class = ExcelProcessorManager
    accept = ".XLSX"
    page_class = ExcelProcessorPage
    tab = "tab_excel_processor_upload"
    upload_form_class = ExcelProcessorUploadFileForm
    excel_processor_functions_class = ExcelProcessorBasisFunctions

    def get_template_context(self, **kwargs):
        return {
            "form": self.upload_form_class(
                self.accept,
                excel_processor_functions_class=self.excel_processor_functions_class,
            )
        }

    @property
    def actions(self) -> tuple:
        action_registry = ActionElement(
            icon="inbox",
            link=reverse("excel_processor_registry"),
            action_id="id_excel_processor_registry",
            hover_text="Excel Processor Registry",
        )
        return (action_registry,)

    def get_success_url(self):
        return reverse("excel_processor")


class ExcelProcessorRegistryListView(FileUploadRegistryView):
    manager_class = ExcelProcessorRegistryManager
    title = "Excel Processor Registry"
    page_class = ExcelProcessorPage
    tab = "tab_excel_processor_upload"


class ExcelProcessorDownloadFile(MontrekDownloadFileView):
    manager_class = ExcelProcessorRegistryManager
    title = "Excel Processor Registry Download"
