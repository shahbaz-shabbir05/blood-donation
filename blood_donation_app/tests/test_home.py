from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from blood_donation_app.models import Request
from blood_donation_app.tests.utils import TEST_PASSWORD, create_admin_user, create_request


class TestHomeView(TestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = create_admin_user('testuser', 'testuser@gmail.com')
        self.client = Client()
        self.client.login(username=self.admin_user.username, password=TEST_PASSWORD)

    def tearDown(self):
        super().tearDown()
        self.client.logout()

    def test_status_code_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_no_logged_in_user(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_no_requests_data(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        requests = Request.objects.all()
        self.assertQuerysetEqual(response.context['requests'], [])
        self.assertEqual(len(requests), 0)

    def test_requests_data(self):
        requests = [create_request(self.admin_user, 'A+', timezone.now()) for _ in range(10)]
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['requests']), 10)
        self.assertQuerysetEqual(
            response.context['requests'],
            requests,
        )
