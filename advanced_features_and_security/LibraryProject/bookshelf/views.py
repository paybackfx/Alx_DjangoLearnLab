"""
Views for the bookshelf application.

Security Features:
- All views use parameterized queries via Django ORM (SQL injection prevention)
- User inputs are validated using Django forms
- Permission decorators enforce access control
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm
from .forms import ExampleForm


# ==================== BOOK LIST VIEW ====================

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View for listing books.
    Requires 'can_view' permission.
    Uses Django ORM for safe database queries.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


# ==================== PERMISSION-PROTECTED VIEWS ====================

@permission_required('bookshelf.can_create', raise_exception=True)
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
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)
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
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form, 'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """
    View for deleting a book.
    Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'bookshelf/delete_book.html', {'book': book})


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
