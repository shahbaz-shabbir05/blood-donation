from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

AB_POSITIVE = 'AB+'
AB_NEGATIVE = 'AB-'
A_POSITIVE = 'A+'
A_NEGATIVE = 'A-'
B_POSITIVE = 'B+'
B_NEGATIVE = 'B-'
O_POSITIVE = 'O+'
O_NEGATIVE = 'O-'
NOT_KNOWN = 'N'
BLOOD_GROUPS_CHOICES = [
    (AB_POSITIVE, _('AB+')),
    (AB_NEGATIVE, _('AB-')),
    (A_POSITIVE, _('A+')),
    (A_NEGATIVE, _('A-')),
    (B_POSITIVE, _('B+')),
    (B_NEGATIVE, _('B-')),
    (O_POSITIVE, _('O+')),
    (O_NEGATIVE, _('O-')),
    (NOT_KNOWN, _('Not Known')),
]


class User(AbstractUser):
    is_donor = models.BooleanField(default=False)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS_CHOICES, default=NOT_KNOWN)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Request(models.Model):
    requester = models.ForeignKey('User', on_delete=models.CASCADE, related_name='requests')
    donor = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='donations')
    required_blood_group = models.CharField(max_length=5, choices=BLOOD_GROUPS_CHOICES, default=NOT_KNOWN)
    created = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField()
    acknowledge_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('request-detail', args=[self.pk])


class Disease(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserDisease(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='diseases')
    disease = models.ForeignKey('Disease', on_delete=models.PROTECT, related_name='user_diseases')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.pk)
