from django.test import Client, TestCase
from django.urls import reverse

from blood_donation_app.tests.utils import TEST_PASSWORD, create_admin_user


class TestUserProfileView(TestCase):
    def setUp(self):
        super(TestUserProfileView, self).setUp()
        self.admin_user = create_admin_user('testuser', 'testuser@gmail.com')
        self.client = Client()
        self.client.login(username=self.admin_user.username, password=TEST_PASSWORD)

    def tearDown(self):
        super(TestUserProfileView, self).tearDown()
        self.client.logout()

    def test_status_code_200(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_no_logged_in_user(self):
        client = Client()
        response = client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
