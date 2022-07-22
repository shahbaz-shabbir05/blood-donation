import pytest
from django.urls import reverse
from django.utils import timezone

from blood_donation_app.models import Request

pytestmark = pytest.mark.django_db


class TestProfileDetailAPI:

    def test_profile_detail_status_code_200(self, api_client):
        client, _ = api_client
        url = reverse('profile-detail')
        response = client.get(url)
        assert response.status_code == 200

    def test_profile_detail_unauthorized_access(self, client):
        url = reverse('profile-detail')
        response = client.get(url)
        assert response.status_code == 401

    def test_profile_detail_full_name(self, api_client):
        client, user = api_client
        url = reverse('profile-detail')
        response = client.get(url)
        assert response.status_code == 200
        assert response.data['full_name'] == user.full_name


class TestUserDetailAPI:

    def test_user_detail_status_code_200(self, api_client):
        client, _ = api_client
        url = reverse('user-detail')
        response = client.get(url)
        assert response.status_code == 200

    def test_user_detail_unauthorized_access(self, client):
        url = reverse('profile-detail')
        response = client.get(url)
        assert response.status_code == 401

    def test_user_detail_full_name(self, api_client):
        client, user = api_client
        url = reverse('user-detail')
        response = client.get(url)
        assert response.status_code == 200
        assert response.data['full_name'] == user.full_name


class TestRequestAPI:

    def test_request_get_status_code_200(self, api_client):
        client, user = api_client
        url = reverse('requests-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_request_get(self, api_client):
        client, user = api_client
        Request.objects.create(**{'requester': user, 'required_blood_group': 'A+', 'deadline': timezone.now()})
        url = reverse('requests-list')
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_request_create(self, api_client):
        client, user = api_client
        url = reverse('requests-list')
        data = {'requester': user, 'required_blood_group': 'A+', 'deadline': timezone.now()}
        response = client.post(url, data=data)
        requests = Request.objects.all()
        assert response.status_code == 201
        assert len(requests) == 1

    def test_request_detail(self, api_client):
        client, user = api_client
        request = Request.objects.create(
            **{'requester': user, 'required_blood_group': 'A+', 'deadline': timezone.now()})
        url = reverse('requests-detail', kwargs={'pk': request.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert response.data['required_blood_group'] == request.required_blood_group

    def test_request_update(self, api_client):
        client, user = api_client
        request_before = Request.objects.create(
            **{'requester': user, 'required_blood_group': 'A+', 'deadline': timezone.now()})
        url = reverse('requests-detail', kwargs={'pk': request_before.pk})
        response = client.patch(url, data={'required_blood_group': 'B+'})
        request_after = Request.objects.get(id=request_before.id)
        assert response.status_code == 200
        assert response.data['required_blood_group'] == request_after.required_blood_group
        assert request_before.required_blood_group != request_after.required_blood_group

    def test_request_delete(self, api_client):
        client, user = api_client
        request = Request.objects.create(
            **{'requester': user, 'required_blood_group': 'A+', 'deadline': timezone.now()})
        url = reverse('requests-detail', kwargs={'pk': request.pk})
        response = client.delete(url)
        requests = Request.objects.all()
        assert response.status_code == 204
        assert len(requests) == 0
