from baseclasses.dataclasses.view_classes import TabElement
from baseclasses.pages import MontrekPage
from django.urls import reverse


class ExcelProcessorPage(MontrekPage):
    page_title = "Excel Processor"

    def get_tabs(self):
        upload_tab = TabElement(
            name="Upload",
            link=reverse("excel_processor"),
            html_id="tab_excel_processor_upload",
        )
        return (upload_tab,)
