"""
Serializers for the api application.

This module contains serializers to convert model instances to JSON format.
"""

from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Converts Book instances to JSON format and validates input data.
    """
    class Meta:
        model = Book
        fields = '__all__'
