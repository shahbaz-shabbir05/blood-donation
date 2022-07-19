from django.test import Client, TestCase
from django.urls import reverse

from blood_donation_app.models import Disease
from blood_donation_app.tests.utils import TEST_PASSWORD, create_admin_user


class TestDiseaseView(TestCase):
    def setUp(self):
        super(TestDiseaseView, self).setUp()
        self.admin_user = create_admin_user('testuser', 'testuser@gmail.com')
        self.client = Client()
        self.client.login(username=self.admin_user.username, password=TEST_PASSWORD)

    def tearDown(self):
        super(TestDiseaseView, self).tearDown()
        self.client.logout()

    def test_disease_create(self):
        data = {'name': 'Headache'}
        response = self.client.post(reverse('disease-create'), data=data)
        diseases = Disease.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Disease.objects.last().name, 'Headache')
        self.assertEqual(len(diseases), 1)
