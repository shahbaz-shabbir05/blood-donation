import uuid

import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def test_password():
    return 'Pass1234!!'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_superuser(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_superuser(**kwargs)

    return make_user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def api_client(create_user, test_password):
    client = APIClient()
    user = create_user(username='testuser')
    data = {
        'username': user.username,
        'password': test_password
    }
    response = client.post(reverse('token_obtain_pair'), data=data, format='json')
    token = response.data.get('access', None)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    return client, user


@pytest.fixture
def api_client_with_user(create_user, test_password):
    def make_user_and_client(**kwargs):
        client = APIClient()
        user = create_user(**kwargs)
        data = {
            'username': user.username,
            'password': test_password
        }
        response = client.post(reverse('token_obtain_pair'), data=data, format='json')
        token = response.data.get('access', None)
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return client, user

    return make_user_and_client
