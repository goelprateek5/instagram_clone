from django.contrib import admin
from authy.models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name']


admin.site.register(Profile, ProfileAdmin)