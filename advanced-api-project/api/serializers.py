"""
Serializers for the API application.

This module provides serializers for converting model instances to JSON
and vice versa. It handles nested relationships between Author and Book models
and includes custom validation logic.
"""

from datetime import date
from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the serialization and deserialization of Book instances.
    It includes custom validation to ensure the publication_year is not in the future.
    
    Fields:
        - title: The title of the book
        - publication_year: The year the book was published (validated to not be in future)
        - author: Foreign key reference to the Author
    
    Validation:
        - publication_year must not exceed the current year
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        
        Args:
            value: The publication year to validate
            
        Returns:
            The validated publication year
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer handles the serialization of Author instances along with
    their related books. The relationship is handled dynamically using a
    nested BookSerializer.
    
    Fields:
        - name: The name of the author
        - books: A nested list of all books written by the author (read-only)
    
    Nested Relationships:
        The 'books' field uses a nested BookSerializer to serialize all books
        associated with the author. This creates a hierarchical JSON structure
        where each author includes an array of their books.
    
    Example Output:
        {
            "id": 1,
            "name": "Author Name",
            "books": [
                {"id": 1, "title": "Book 1", "publication_year": 2020, "author": 1},
                {"id": 2, "title": "Book 2", "publication_year": 2021, "author": 1}
            ]
        }
    """
    # Nested serializer to dynamically serialize related books
    # many=True indicates a one-to-many relationship
    # read_only=True prevents books from being created/updated through Author endpoint
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
