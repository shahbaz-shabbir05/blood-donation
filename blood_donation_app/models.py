from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class BloodGroups(models.TextChoices):
        AB_POSITIVE = 'AB+', _('AB+')
        AB_NEGATIVE = 'AB-', _('AB-')
        A_POSITIVE = 'A+', _('A+')
        A_NEGATIVE = 'A-', _('A-')
        B_POSITIVE = 'B+', _('B+')
        B_NEGATIVE = 'B-', _('B-')
        O_POSITIVE = 'O+', _('O+')
        O_NEGATIVE = 'O-', _('O-')
        NOT_KNOWN = 'N', _('Not Known')

    is_donor = models.BooleanField(default=False)
    blood_group = models.CharField(max_length=5, choices=BloodGroups.choices)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Request(models.Model):
    requester = models.ForeignKey('User', on_delete=models.CASCADE, related_name='requesters')
    donor = models.ForeignKey('User', on_delete=models.PROTECT, blank=True, null=True, related_name='donors')
    required_blood_group = models.CharField(max_length=5)
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
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user')
    disease = models.ForeignKey('Disease', on_delete=models.PROTECT, related_name='diseases')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.pk)
