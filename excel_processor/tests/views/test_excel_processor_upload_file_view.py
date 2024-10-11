from django.test import TestCase
from django.urls import reverse
from testing.decorators import add_logged_in_user


class TestExcelProcessorUploadFileView(TestCase):
    @add_logged_in_user
    def setUp(self):
        self.url = reverse("excel_processor")

    def test_view_return_correct_html(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "upload_form.html")
