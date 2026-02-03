"""
Sample queries demonstrating different relationship types in Django ORM.

This script contains functions for:
- Querying all books by a specific author (ForeignKey)
- Listing all books in a library (ManyToMany)
- Retrieving the librarian for a library (OneToOne)
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def get_books_by_author(author_name):
    """
    Query all books by a specific author.
    Demonstrates ForeignKey relationship.
    """
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []


def get_books_in_library(library_name):
    """
    List all books in a library.
    Demonstrates ManyToMany relationship.
    """
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\nBooks in {library_name} Library:")
        for book in books:
            print(f"  - {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []


def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    Demonstrates OneToOne relationship.
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"\nLibrarian for {library_name}: {librarian.name}")
        return librarian
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")
        return None


if __name__ == "__main__":
    # Example usage - these will work once data is added to the database
    print("=" * 50)
    print("Relationship App - Query Samples")
    print("=" * 50)
    
    # Uncomment and modify these lines after adding data:
    # get_books_by_author("J.K. Rowling")
    # get_books_in_library("City Library")
    # get_librarian_for_library("City Library")
    
    print("\nTo test these queries, first add some data via Django admin or shell.")
