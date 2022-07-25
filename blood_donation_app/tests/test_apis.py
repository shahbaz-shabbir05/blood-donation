from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from blood_donation_app.models import Request
from blood_donation_app.tests.utils import create_test_user, TEST_PASSWORD


class TestProfileDetailAPI(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user('testuser', 'testuser@gmail.com')
        self.client.login(username=self.user.username, password=TEST_PASSWORD)
        data = {
            'username': self.user.username,
            'password': TEST_PASSWORD
        }
        response = self.client.post(reverse('token_obtain_pair'), data=data, format='json')
        token = response.data.get('access', None)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_profile_detail_status_code_200(self):
        url = reverse('profile-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_unauthorized_access(self):
        client = APIClient()
        url = reverse('profile-detail')
        response = client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_profile_detail_full_name(self):
        url = reverse('profile-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], self.user.full_name)


class TestUserDetailAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user('testuser', 'testuser@gmail.com')
        self.client.login(username=self.user.username, password=TEST_PASSWORD)
        data = {
            'username': self.user.username,
            'password': TEST_PASSWORD
        }
        response = self.client.post(reverse('token_obtain_pair'), data=data, format='json')
        token = response.data.get('access', None)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_user_detail_status_code_200(self):
        url = reverse('user-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_detail_unauthorized_access(self):
        client = APIClient()
        url = reverse('profile-detail')
        response = client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_user_detail_full_name(self):
        url = reverse('user-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], self.user.full_name)


class TestRequestAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user('testuser', 'testuser@gmail.com')
        self.client.login(username=self.user.username, password=TEST_PASSWORD)
        data = {
            'username': self.user.username,
            'password': TEST_PASSWORD
        }
        response = self.client.post(reverse('token_obtain_pair'), data=data, format='json')
        _token = response.data.get('access', None)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + _token)

    def test_request_get_status_code_200(self):
        url = reverse('requests-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_request_get(self):
        Request.objects.create(**{'requester': self.user, 'required_blood_group': 'A+', 'deadline': timezone.now()})
        url = reverse('requests-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_request_create(self):
        url = reverse('requests-list')
        data = {'required_blood_group': 'A+', 'deadline': timezone.now()}
        response = self.client.post(url, data=data)
        requests = Request.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(requests), 1)

    def test_request_detail(self):
        request = Request.objects.create(
            **{'requester': self.user, 'required_blood_group': 'A+', 'deadline': timezone.now()})
        url = reverse('requests-detail', kwargs={'pk': request.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['required_blood_group'], request.required_blood_group)

    def test_request_update(self):
        request_before = Request.objects.create(
            **{'requester': self.user, 'required_blood_group': 'A+', 'deadline': timezone.now()})
        url = reverse('requests-detail', kwargs={'pk': request_before.pk})
        response = self.client.patch(url, data={'required_blood_group': 'B+'})
        request_after = Request.objects.get(id=request_before.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['required_blood_group'], request_after.required_blood_group)
        self.assertNotEqual(request_before.required_blood_group, request_after.required_blood_group)

    def test_request_delete(self):
        request = Request.objects.create(
            **{'requester': self.user, 'required_blood_group': 'A+', 'deadline': timezone.now()})
        url = reverse('requests-detail', kwargs={'pk': request.pk})
        response = self.client.delete(url)
        requests = Request.objects.all()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(requests), 0)
