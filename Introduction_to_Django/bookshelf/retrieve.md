# Retrieve Operation

Retrieving a Book instance from the database.

## Command

```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Display all attributes
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## Expected Output

```
Title: 1984
Author: George Orwell
Publication Year: 1949
```

The book details have been successfully retrieved from the database.
