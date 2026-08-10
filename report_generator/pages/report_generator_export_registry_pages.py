from django.urls import reverse

from baseclasses.dataclasses.view_classes import TabElement
from baseclasses.pages import MontrekPage


class ReportGeneratorExportRegistryPage(MontrekPage):
    page_title = "Report Generator Exports"

    def get_tabs(self):
        return (
            TabElement(
                name="Report Generator Exports",
                link=reverse("report_generator_export_registry_list"),
                html_id="tab_report_generator_export_registry_list",
                active="active",
            ),
        )
