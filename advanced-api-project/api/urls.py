"""
URL configuration for the API application.

This module defines URL patterns for the Book API endpoints.
Each URL is mapped to a specific generic view for handling CRUD operations.

URL Patterns:
    - /books/            - List all books (GET) 
    - /books/<int:pk>/   - Retrieve a specific book (GET)
    - /books/create/     - Create a new book (POST)
    - /books/<int:pk>/update/  - Update a book (PUT/PATCH)
    - /books/<int:pk>/delete/  - Delete a book (DELETE)
"""

from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    # List all books - accessible to all users
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve a single book by ID - accessible to all users
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book - requires authentication
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book - requires authentication
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book - requires authentication
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
