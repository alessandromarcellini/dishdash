from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'role', 'restaurant', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role', 'restaurant', 'kitchen')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'restaurant', 'kitchen', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(User, UserAdmin)
