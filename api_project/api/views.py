"""
Views for the api application.

This module contains:
- BookList: ListAPIView for retrieving all books
- BookViewSet: ModelViewSet for full CRUD operations with authentication
"""

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to list all books.
    Uses ListAPIView for read-only access to book collection.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on Book model.
    
    Provides the following actions:
    - list: GET /books_all/ - List all books
    - create: POST /books_all/ - Create a new book
    - retrieve: GET /books_all/<id>/ - Retrieve a book by ID
    - update: PUT /books_all/<id>/ - Update a book
    - destroy: DELETE /books_all/<id>/ - Delete a book
    
    Authentication:
    - Requires authentication for all operations
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
