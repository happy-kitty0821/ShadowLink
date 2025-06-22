from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to be displayed in list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser', 'emails_verified')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    #fields to be used in the admin user detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture')}),
        (_('Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Verification'), {'fields': ('emails_verified',)}),
    )

    #fields when creating a new user in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_superuser',
            ),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
