from django.test import TestCase, SimpleTestCase

class HomePageTests(SimpleTestCase):
    def test_home_status_code(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)


