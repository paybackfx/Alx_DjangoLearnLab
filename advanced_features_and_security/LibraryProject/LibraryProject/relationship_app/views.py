"""
Views for the relationship_app application.

This module contains:
- Function-based views for listing books and handling authentication
- Class-based views for library details
- Role-based access views (Admin, Librarian, Member)
- Permission-protected views for book CRUD operations

Security Features:
- All views use parameterized queries via Django ORM (SQL injection prevention)
- User inputs are validated using Django forms
- Permission decorators enforce access control
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import LoginView, LogoutView

from .models import Book
from .models import Library
from .models import UserProfile
from .models import Author
from .forms import BookForm, ExampleForm


# ==================== BOOK LIST VIEW (Function-based) ====================

def list_books(request):
    """
    Function-based view to list all books.
    Displays all books with their titles and authors.
    Uses Django ORM for safe database queries (SQL injection prevention).
    """
    # Safe query using Django ORM - parameterized automatically
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# ==================== LIBRARY DETAIL VIEW (Class-based) ====================

class LibraryDetailView(DetailView):
    """
    Class-based view to display library details.
    Shows library information and all books available in the library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# ==================== AUTHENTICATION VIEWS ====================

class UserLoginView(LoginView):
    """Custom login view using Django's built-in LoginView."""
    template_name = 'relationship_app/login.html'


class UserLogoutView(LogoutView):
    """Custom logout view using Django's built-in LogoutView."""
    template_name = 'relationship_app/logout.html'


def register(request):
    """
    View for user registration.
    Uses Django's built-in UserCreationForm for input validation.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# ==================== ROLE CHECK FUNCTIONS ====================

def is_admin(user):
    """Check if user has Admin role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    """Check if user has Librarian role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    """Check if user has Member role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# ==================== ROLE-BASED VIEWS ====================

@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only to Admin users."""
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to Librarian users."""
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    """View accessible only to Member users."""
    return render(request, 'relationship_app/member_view.html')


# ==================== PERMISSION-PROTECTED VIEWS ====================

@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    """
    View for listing books.
    Requires 'can_view' permission.
    Uses Django ORM for safe database queries.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})


@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    """
    View for adding a new book.
    Requires 'can_create' permission.
    Uses Django forms for input validation (XSS/SQL injection prevention).
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})


@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    """
    View for editing an existing book.
    Requires 'can_edit' permission.
    Uses Django forms for input validation.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})


@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    """
    View for deleting a book.
    Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})


# ==================== SECURE FORM EXAMPLE VIEW ====================

def form_example(request):
    """
    Example view demonstrating secure form handling.
    - Uses Django forms for input validation
    - Template includes CSRF token
    - All inputs are sanitized
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the validated data safely
            pass
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
