"""
Models for the bookshelf application.

This module defines:
- CustomUser: Extended User model with date_of_birth and profile_photo
- CustomUserManager: Custom manager for user creation
- Book: Model with custom permissions (can_view, can_create, can_edit, can_delete)
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# ==================== CUSTOM USER MANAGER ====================

class CustomUserManager(BaseUserManager):
    """
    Custom user manager for CustomUser model.
    Handles user creation with additional fields.
    """
    
    def create_user(self, username, email=None, password=None, date_of_birth=None, profile_photo=None, **extra_fields):
        """
        Create and save a regular user with the given username, email, and password.
        Handles date_of_birth and profile_photo fields.
        """
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email) if email else None
        user = self.model(
            username=username,
            email=email,
            date_of_birth=date_of_birth,
            **extra_fields
        )
        if profile_photo:
            user.profile_photo = profile_photo
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given username, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)


# ==================== CUSTOM USER MODEL ====================

class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Adds date_of_birth and profile_photo fields.
    """
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username


# ==================== BOOK MODEL ====================

class Book(models.Model):
    """
    Book model with custom permissions for access control.
    
    Permissions:
    - can_view: Permission to view book entries
    - can_create: Permission to create book entries
    - can_edit: Permission to edit book entries
    - can_delete: Permission to delete book entries
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title
