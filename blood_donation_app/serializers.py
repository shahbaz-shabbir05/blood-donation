from rest_framework import serializers

from blood_donation_app.models import User, Request


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'blood_group', 'is_donor']


class UserSerializer(serializers.ModelSerializer):
    diseases = serializers.SerializerMethodField()
    donations = serializers.SerializerMethodField()
    requests = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'blood_group', 'is_donor', 'diseases', 'donations', 'requests']

    def get_diseases(self, obj):
        # diseases = UserDisease.objects.select_related('user', 'disease').filter(user=instance)
        return [value.disease.name for value in obj.diseases.all().distinct()]

    def get_donations(self, obj):
        # donations = Request.objects.select_related('donor').filter(donor=instance)
        return obj.donations.all().values('required_blood_group', 'deadline', 'acknowledge_time')

    def get_requests(self, obj):
        # requests = Request.objects.select_related('requester').filter(requester=instance)
        return obj.donations.all().values('required_blood_group', 'deadline')


class RequestSerializer(serializers.ModelSerializer):
    requester = serializers.SerializerMethodField()
    donor = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = ['requester', 'required_blood_group', 'deadline', 'donor']

    def get_requester(self, obj):
        return obj.requester.full_name if obj.requester else ''

    def get_donor(self, obj):
        return obj.donor.full_name if obj.donor else ''
