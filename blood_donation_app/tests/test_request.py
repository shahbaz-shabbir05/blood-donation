from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from blood_donation_app.models import Request
from blood_donation_app.tests.utils import TEST_PASSWORD, create_admin_user, create_request


class TestRequestView(TestCase):
    def setUp(self):
        super(TestRequestView, self).setUp()
        self.admin_user = create_admin_user('testuser', 'testuser@gmail.com')
        self.client = Client()
        self.client.login(username=self.admin_user.username, password=TEST_PASSWORD)

    def tearDown(self):
        super(TestRequestView, self).tearDown()
        self.client.logout()

    def test_no_requests(self):
        response = self.client.get(reverse('request-list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['requests'], [])

    def test_get_requests(self):
        deadline = timezone.now() - timezone.timedelta(weeks=1)
        request = create_request(self.admin_user, 'A+', deadline)
        response = self.client.get(reverse('request-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['requests']), 1)
        self.assertQuerysetEqual(
            response.context['requests'],
            [request]
        )

    def test_request_create(self):
        data = {'requester': self.admin_user.id, 'required_blood_group': 'A+', 'deadline': timezone.now()}
        response = self.client.post(reverse('request-create'), data=data)
        requests = Request.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(requests), 1)
        self.assertEqual(Request.objects.last().required_blood_group, 'A+')

    def test_request_detail(self):
        request = create_request(self.admin_user, 'A+', timezone.now())
        response = self.client.get(reverse('request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['requests'],
            request
        )

    def test_request_update(self):
        obj = create_request(self.admin_user, 'A+', timezone.now())
        data = {'required_blood_group': 'B+', 'deadline': obj.deadline, 'requester': obj.requester.id}
        response = self.client.post(reverse('request-update', kwargs={'pk': obj.id}), data=data)
        request = Request.objects.get(id=obj.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.required_blood_group, 'B+')

    def test_request_delete(self):
        obj = create_request(self.admin_user, 'A+', timezone.now())
        response = self.client.delete(reverse('request-delete', kwargs={'pk': obj.id}))
        requests = Request.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(requests), 0)
