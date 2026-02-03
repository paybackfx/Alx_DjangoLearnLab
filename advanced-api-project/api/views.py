"""
Views for the API application.

This module provides generic views for CRUD operations on the Book model.
It implements Django REST Framework's generic views with filtering, searching,
and ordering capabilities. Permission classes are applied to protect endpoints
based on user authentication status.
"""

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


class BookFilter(django_filters.FilterSet):
    """
    FilterSet for the Book model.
    
    Allows filtering books by:
        - title: exact or partial match (case-insensitive)
        - author: by author's name (case-insensitive)
        - publication_year: exact match
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    publication_year = django_filters.NumberFilter()
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    This view provides:
        - GET: List all books in the database
        
    Features:
        - Filtering: Filter books by title, author name, and publication_year
        - Searching: Full-text search on title and author name fields
        - Ordering: Sort results by title or publication_year
        
    Permissions:
        - Read access is allowed to all users (authenticated or not)
    
    Query Parameters:
        - title: Filter by book title (case-insensitive partial match)
        - author: Filter by author name (case-insensitive partial match)
        - publication_year: Filter by exact publication year
        - search: Search in title and author name fields
        - ordering: Sort by 'title' or 'publication_year' (prefix with '-' for descending)
    
    Example Usage:
        GET /api/books/?title=django
        GET /api/books/?author=john
        GET /api/books/?publication_year=2020
        GET /api/books/?search=python
        GET /api/books/?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Configure filter backends for filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Use the custom FilterSet for advanced filtering
    filterset_class = BookFilter
    
    # Fields that can be searched using the 'search' query parameter
    search_fields = ['title', 'author__name']
    
    # Fields that can be used for ordering results
    ordering_fields = ['title', 'publication_year']
    
    # Default ordering
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by its ID.
    
    This view provides:
        - GET: Retrieve a specific book's details
        
    Permissions:
        - Read access is allowed to all users (authenticated or not)
    
    URL Parameters:
        - pk: The primary key (ID) of the book to retrieve
    
    Example Usage:
        GET /api/books/1/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    
    This view provides:
        - POST: Create a new book in the database
        
    Permissions:
        - Only authenticated users can create books
        
    Request Body:
        - title (required): The title of the book
        - publication_year (required): The year of publication (cannot be in future)
        - author (required): The ID of the author
    
    Custom Behavior:
        - Validates that publication_year is not in the future (via serializer)
        - Returns the created book data with status 201 on success
    
    Example Usage:
        POST /api/books/
        {
            "title": "New Book",
            "publication_year": 2023,
            "author": 1
        }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    
    This view provides:
        - PUT: Full update of a book (all fields required)
        - PATCH: Partial update of a book (only changed fields required)
        
    Permissions:
        - Only authenticated users can update books
        
    URL Parameters:
        - pk: The primary key (ID) of the book to update
    
    Custom Behavior:
        - Validates that publication_year is not in the future (via serializer)
        - Handles both full and partial updates
    
    Example Usage:
        PUT /api/books/1/
        {
            "title": "Updated Book Title",
            "publication_year": 2023,
            "author": 1
        }
        
        PATCH /api/books/1/
        {
            "title": "Only Update Title"
        }
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    
    This view provides:
        - DELETE: Remove a book from the database
        
    Permissions:
        - Only authenticated users can delete books
        
    URL Parameters:
        - pk: The primary key (ID) of the book to delete
    
    Response:
        - Returns status 204 (No Content) on successful deletion
    
    Example Usage:
        DELETE /api/books/1/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
