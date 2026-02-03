# Create Operation

Creating a Book instance in Django shell.

## Command

```python
from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

print(book)
```

## Expected Output

```
1984
```

The book "1984" by George Orwell has been successfully created in the database.
