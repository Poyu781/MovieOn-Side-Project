from django.test import TestCase, SimpleTestCase
from .models import ErrorMsgRecord
class HomePageTests(SimpleTestCase):
    def test_home_status_code(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)


class ErrorMsgViewTests(TestCase):

    def setUp(self):
        ErrorMsgRecord.objects.create(user_id=38, error_feature='title_name_error',error_message='889495',update_date="2021-06-03")

    def tearDown(self):
        ErrorMsgRecord.objects.all().delete()
        
    def test_list_view(self):
        data = ErrorMsgRecord.objects.get(user_id=38)
        self.assertEqual(data.error_feature, 'title_name_error')