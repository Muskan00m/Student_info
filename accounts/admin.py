from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("username", "email", "first_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )
