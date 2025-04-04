from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import CustomUser, Server

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Server)
