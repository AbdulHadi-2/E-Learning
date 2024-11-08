from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # The fields to be used in displaying the User model in the admin panel.
    # These override the definitions on the base UserAdmin class
    # that reference specific fields on auth.User.
    list_display = ('email', 'full_name', 'nick_name', 'phone', 'gender', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'gender')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('email',)
    filter_horizontal = ()

    # Fieldsets define the layout of the admin "edit" page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'nick_name', 'date_of_birth', 'phone', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined',)}),
        ('Additional Info', {'fields': ('reset_code',)}),
    )

    # Fields to be used when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'date_of_birth', 'phone', 'gender', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    # These attributes help manage users in the list view
    filter_horizontal = ()

# Register CustomUser with the customized CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
