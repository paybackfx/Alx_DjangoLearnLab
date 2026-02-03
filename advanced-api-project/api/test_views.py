"""
Unit Tests for the Book API endpoints.

This module contains comprehensive tests for the Book API, covering:
    - CRUD operations (Create, Read, Update, Delete)
    - Filtering, searching, and ordering functionality
    - Permission and authentication enforcement
    
Testing Strategy:
    - Each test case is isolated and uses a fresh database state
    - Tests cover both successful operations and error cases
    - Authentication tests verify proper access control
    
Running Tests:
    python manage.py test api
    
    Or for verbose output:
    python manage.py test api -v 2
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test cases for Book API endpoints.
    
    This test class covers all CRUD operations and ensures that:
        - Books can be created, retrieved, updated, and deleted
        - Proper status codes are returned
        - Data integrity is maintained
        - Permission controls are enforced
    """
    
    def setUp(self):
        """
        Set up test data before each test method.
        
        Creates:
            - A test user for authenticated requests
            - A test author
            - Sample books for testing
        """
        # Create a test user for authenticated requests
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test author
        self.author = Author.objects.create(name='Test Author')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Python Programming',
            publication_year=2020,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Django Web Development',
            publication_year=2021,
            author=self.author
        )
        
        # Create another author with a book for filtering tests
        self.author2 = Author.objects.create(name='Another Author')
        self.book3 = Book.objects.create(
            title='JavaScript Basics',
            publication_year=2019,
            author=self.author2
        )
        
        # Initialize API client
        self.client = APIClient()
    
    # ==================== LIST TESTS ====================
    
    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can list books."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_list_books_authenticated(self):
        """Test that authenticated users can list books."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    # ==================== DETAIL TESTS ====================
    
    def test_retrieve_book_unauthenticated(self):
        """Test that unauthenticated users can retrieve a single book."""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Python Programming')
        self.assertEqual(response.data['publication_year'], 2020)
    
    def test_retrieve_nonexistent_book(self):
        """Test that retrieving a non-existent book returns 404."""
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ==================== CREATE TESTS ====================
    
    def test_create_book_authenticated(self):
        """Test that authenticated users can create a book."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2022,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'New Book')
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create a book."""
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2022,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        
        # DRF returns 403 Forbidden for unauthenticated requests with session auth
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Book.objects.count(), 3)  # No new book created
    
    def test_create_book_future_year_validation(self):
        """Test that creating a book with future publication year fails."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 3000,  # Future year
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_missing_fields(self):
        """Test that creating a book with missing required fields fails."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {'title': 'Incomplete Book'}  # Missing required fields
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # ==================== UPDATE TESTS ====================
    
    def test_update_book_authenticated(self):
        """Test that authenticated users can update a book."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Python Programming',
            'publication_year': 2021,
            'author': self.author.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Python Programming')
        self.assertEqual(self.book1.publication_year, 2021)
    
    def test_partial_update_book_authenticated(self):
        """Test that authenticated users can partially update a book."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Partially Updated Title'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update a book."""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Unauthorized Update'}
        response = self.client.put(url, data, format='json')
        
        # DRF returns 403 Forbidden for unauthenticated requests with session auth
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_update_book_future_year_validation(self):
        """Test that updating a book with future year fails."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Book',
            'publication_year': 3000,
            'author': self.author.pk
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # ==================== DELETE TESTS ====================
    
    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete a book."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete a book."""
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        # DRF returns 403 Forbidden for unauthenticated requests with session auth
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Book.objects.count(), 3)  # Book still exists
    
    def test_delete_nonexistent_book(self):
        """Test that deleting a non-existent book returns 404."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete', kwargs={'pk': 9999})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ==================== FILTERING TESTS ====================
    
    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'Python'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Programming')
    
    def test_filter_books_by_author(self):
        """Test filtering books by author name."""
        url = reverse('book-list')
        response = self.client.get(url, {'author': 'Test Author'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 2020})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Programming')
    
    # ==================== SEARCH TESTS ====================
    
    def test_search_books_by_title(self):
        """Test searching books by title."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Django'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django Web Development')
    
    def test_search_books_by_author_name(self):
        """Test searching books by author name."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Another'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'JavaScript Basics')
    
    def test_search_no_results(self):
        """Test search with no matching results."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'NonexistentBook'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    # ==================== ORDERING TESTS ====================
    
    def test_order_books_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_title_descending(self):
        """Test ordering books by title in descending order."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_books_by_publication_year_ascending(self):
        """Test ordering books by publication year in ascending order."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
    
    def test_order_books_by_publication_year_descending(self):
        """Test ordering books by publication year in descending order."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))


class AuthorModelTestCase(TestCase):
    """Test cases for the Author model."""
    
    def test_author_creation(self):
        """Test that an author can be created."""
        author = Author.objects.create(name='New Author')
        self.assertEqual(author.name, 'New Author')
        self.assertEqual(str(author), 'New Author')
    
    def test_author_book_relationship(self):
        """Test the one-to-many relationship between Author and Book."""
        author = Author.objects.create(name='Prolific Author')
        book1 = Book.objects.create(
            title='Book One',
            publication_year=2020,
            author=author
        )
        book2 = Book.objects.create(
            title='Book Two',
            publication_year=2021,
            author=author
        )
        
        # Test reverse relationship
        self.assertEqual(author.books.count(), 2)
        self.assertIn(book1, author.books.all())
        self.assertIn(book2, author.books.all())


class BookModelTestCase(TestCase):
    """Test cases for the Book model."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name='Test Author')
    
    def test_book_creation(self):
        """Test that a book can be created."""
        book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=self.author
        )
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.publication_year, 2020)
        self.assertEqual(book.author, self.author)
        self.assertEqual(str(book), 'Test Book')
    
    def test_book_cascade_delete(self):
        """Test that deleting an author deletes their books."""
        book = Book.objects.create(
            title='Orphan Book',
            publication_year=2020,
            author=self.author
        )
        book_pk = book.pk
        
        self.author.delete()
        
        self.assertFalse(Book.objects.filter(pk=book_pk).exists())
