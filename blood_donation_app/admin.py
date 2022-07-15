from django.contrib import admin

from blood_donation_app.models import User, Request, Disease, UserDisease

admin.site.register(User)
admin.site.register(Request)
admin.site.register(Disease)
admin.site.register(UserDisease)
