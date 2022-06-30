from django.contrib import admin

from blood_donation_app.models import Request, Disease, UserDisease

admin.site.regisyer(Request)
admin.site.regisyer(Disease)
admin.site.regisyer(UserDisease)
