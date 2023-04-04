from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'username', 'email', 'role', 'is_active')
#     list_editable = ('role',)


admin.site.register(User, UserAdmin)
