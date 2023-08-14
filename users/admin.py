from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_teacher', 'is_school', 'is_staff', 'password', 'created_at', 'has_paid']
    search_fields = ['username', 'email']

    
admin.site.register(User, CustomUserAdmin)
