"""
Forms for the relationship_app application.

Security Features:
- All forms use Django's built-in validation (XSS/SQL injection prevention)
- User inputs are sanitized automatically
- Form data is validated before processing
"""

from django import forms
from .models import Book, Author


class BookForm(forms.ModelForm):
    """
    Form for creating and editing Book instances.
    Uses ModelForm for automatic field validation.
    """
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }


class ExampleForm(forms.Form):
    """
    Example form demonstrating secure input handling.
    All inputs are validated and sanitized by Django.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter message'})
    )
