# Delete Operation

Deleting a Book instance from the database.

## Command

```python
from bookshelf.models import Book

# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by trying to retrieve all books
all_books = Book.objects.all()
print(f"Remaining books: {all_books.count()}")
```

## Expected Output

```
Remaining books: 0
```

The book "Nineteen Eighty-Four" has been successfully deleted from the database.
