"""
Models for the relationship_app application.

This module defines:
- CustomUser: Extended User model with date_of_birth and profile_photo
- CustomUserManager: Custom manager for user creation
- Author, Book, Library, Librarian models with relationships
- Book model with custom permissions (can_view, can_create, can_edit, can_delete)
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


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


# ==================== AUTHOR MODEL ====================

class Author(models.Model):
    """Author model representing a book author."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ==================== BOOK MODEL ====================

class Book(models.Model):
    """
    Book model with ForeignKey to Author.
    Includes custom permissions for access control.
    
    Permissions:
    - can_view: Permission to view book entries
    - can_create: Permission to create book entries
    - can_edit: Permission to edit book entries
    - can_delete: Permission to delete book entries
    """
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title


# ==================== LIBRARY MODEL ====================

class Library(models.Model):
    """Library model with ManyToMany relationship to Book."""
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name


# ==================== LIBRARIAN MODEL ====================

class Librarian(models.Model):
    """Librarian model with OneToOne relationship to Library."""
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name


# ==================== USER PROFILE MODEL ====================

class UserProfile(models.Model):
    """
    UserProfile model extending CustomUser with role-based access.
    Roles: Admin, Librarian, Member
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ==================== SIGNALS ====================

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile for newly registered users."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved."""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
