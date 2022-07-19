from django.test import Client, TestCase
from django.urls import reverse

from blood_donation_app.tests.utils import TEST_PASSWORD, create_admin_user


class TestNotificationView(TestCase):
    def setUp(self):
        super(TestNotificationView, self).setUp()
        self.admin_user = create_admin_user('testuser', 'testuser@gmail.com')
        self.client = Client()
        self.client.login(username=self.admin_user.username, password=TEST_PASSWORD)

    def tearDown(self):
        super(TestNotificationView, self).tearDown()
        self.client.logout()

    def test_status_code_200(self):
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
