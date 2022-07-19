from django.test import Client, TestCase
from django.urls import reverse

from blood_donation_app.models import UserDisease
from blood_donation_app.tests.utils import TEST_PASSWORD, create_admin_user, create_disease, \
    create_user_disease


class TestUserDiseaseView(TestCase):
    def setUp(self):
        super(TestUserDiseaseView, self).setUp()
        self.admin_user = create_admin_user('testuser', 'testuser@gmail.com')
        self.client = Client()
        self.client.login(username=self.admin_user.username, password=TEST_PASSWORD)

    def tearDown(self):
        super(TestUserDiseaseView, self).tearDown()
        self.client.logout()

    def test_no_user_diseases(self):
        response = self.client.get(reverse('user-disease-list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['diseases'], [])

    def test_get_user_diseases(self):
        disease = create_disease('Fever')
        user_disease = create_user_disease(self.admin_user, disease)
        response = self.client.get(reverse('user-disease-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['diseases']), 1)
        self.assertQuerysetEqual(
            response.context['diseases'],
            [user_disease]
        )

    def test_user_disease_create(self):
        disease = create_disease('Headache')
        data = {'disease': disease.id, 'start_date': '2022-02-04', 'end_date': '2022-05-10'}
        response = self.client.post(reverse('user-disease-create'), data=data)
        user_diseases = UserDisease.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(user_diseases), 1)

    def test_user_disease_detail(self):
        disease = create_disease('Fever')
        user_disease = create_user_disease(self.admin_user, disease)
        response = self.client.get(reverse('user-disease-detail', kwargs={'pk': user_disease.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['disease'],
            user_disease
        )

    def test_user_disease_update(self):
        disease = create_disease('Fever')
        obj = create_user_disease(self.admin_user, disease)
        disease_update = create_disease('Headache')
        data = {'disease': disease_update.id, 'start_date': '2022-02-04', 'end_date': '2022-05-10'}
        response = self.client.post(reverse('user-disease-update', kwargs={'pk': obj.id}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserDisease.objects.last().disease.name, 'Headache')

    def test_user_disease_delete(self):
        disease = create_disease('Fever')
        obj = create_user_disease(self.admin_user, disease)
        response = self.client.delete(reverse('user-disease-delete', kwargs={'pk': obj.id}))
        diseases = UserDisease.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(diseases), 0)
