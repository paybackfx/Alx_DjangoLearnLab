# Update Operation

Updating a Book instance in the database.

## Command

```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Verify the update
print(f"Updated Title: {book.title}")
```

## Expected Output

```
Updated Title: Nineteen Eighty-Four
```

The book title has been successfully updated from "1984" to "Nineteen Eighty-Four".
