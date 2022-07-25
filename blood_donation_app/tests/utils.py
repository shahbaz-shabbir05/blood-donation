from django.utils import timezone

from blood_donation_app.models import User, Request, Disease, UserDisease

TEST_PASSWORD = 'Pass1234!!'


def create_admin_user(username, email):
    return User.objects.create_superuser(username=username, email=email, password=TEST_PASSWORD)


def create_test_user(username, email):
    return User.objects.create_user(username=username, email=email, password=TEST_PASSWORD)


def create_request(requester, blood_group, deadline):
    return Request.objects.create(requester=requester, required_blood_group=blood_group, deadline=deadline)


def create_bulk_request(requests):
    return Request.objects.bulk_create(requests)


def create_disease(name):
    return Disease.objects.create(name=name)


def create_user_disease(user, disease):
    return UserDisease.objects.create(user=user, disease=disease, start_date=timezone.now(),
                                      end_date=(timezone.now() + timezone.timedelta(weeks=1)))
