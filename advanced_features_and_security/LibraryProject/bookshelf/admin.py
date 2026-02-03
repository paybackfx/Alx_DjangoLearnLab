"""
Admin configuration for the bookshelf application.

This module configures the Django admin interface for:
- CustomUser: Custom user model with date_of_birth and profile_photo
- Book: Book model with custom permissions
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book


# ==================== CUSTOM USER ADMIN ====================

class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser model.
    Includes date_of_birth and profile_photo fields.
    """
    model = CustomUser
    
    # Fields to display in list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    # Add custom fields to user edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    
    # Add custom fields to user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )


# ==================== BOOK ADMIN ====================

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model."""
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')


# Register CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
