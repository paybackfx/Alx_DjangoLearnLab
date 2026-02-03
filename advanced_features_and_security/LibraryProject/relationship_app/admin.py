"""
Admin configuration for the relationship_app application.

This module configures the Django admin interface for:
- CustomUser: Custom user model with date_of_birth and profile_photo
- Author, Book, Library, Librarian models
- UserProfile for role-based access control
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Book, Library, Librarian, UserProfile


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
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')


# ==================== AUTHOR ADMIN ====================

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin configuration for Author model."""
    list_display = ('name',)
    search_fields = ('name',)


# ==================== LIBRARY ADMIN ====================

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    """Admin configuration for Library model."""
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('books',)


# ==================== LIBRARIAN ADMIN ====================

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    """Admin configuration for Librarian model."""
    list_display = ('name', 'library')
    search_fields = ('name', 'library__name')


# ==================== USER PROFILE ADMIN ====================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model."""
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)


# Register CustomUser with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
