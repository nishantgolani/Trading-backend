from django.contrib import admin
from .models import *


class UserModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number',  'otp_verified']


admin.site.register(UserModel, UserModelAdmin)

