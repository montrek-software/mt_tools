from django.test import TestCase
from django.urls import reverse
from testing.decorators import add_logged_in_user
import os
from mt_tools.excel_processor.repositories.excel_processor_repositories import (
    ExcelProcessorFileUploadRegistryRepository,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class TestExcelProcessorUploadFileView(TestCase):
    @add_logged_in_user
    def setUp(self):
        self.url = reverse("excel_processor")
        self.test_file_path_a = os.path.join(DATA_DIR, "test_excel.xlsx")

    def test_view_return_correct_html(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "upload_form.html")

    def test_view_post_success__no_change(self):
        with open(self.test_file_path_a, "rb") as f:
            data = {"file": f}
            response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response, reverse("excel_processor"))
        test_query = ExcelProcessorFileUploadRegistryRepository().std_queryset()
        self.assertEqual(test_query.count(), 1)
