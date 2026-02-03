# Advanced API Project

A Django REST Framework project demonstrating advanced API development concepts including custom serializers, generic views, filtering, searching, ordering, and comprehensive unit testing.

## Project Structure

```
advanced-api-project/
├── advanced_api_project/    # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/                     # API application
│   ├── models.py           # Author and Book models
│   ├── serializers.py      # Custom serializers with nested relationships
│   ├── views.py            # Generic views with filtering/searching/ordering
│   ├── urls.py             # URL patterns for Book API
│   └── test_views.py       # Comprehensive unit tests
├── manage.py
└── venv/                    # Virtual environment
```

## Setup Instructions

1. **Create and activate virtual environment:**
   ```bash
   cd advanced-api-project
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install django djangorestframework django-filter
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Models

### Author
- `name`: CharField - The author's name

### Book
- `title`: CharField - The book's title
- `publication_year`: IntegerField - Year of publication
- `author`: ForeignKey to Author - One-to-many relationship

## API Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/books/` | List all books | Public |
| GET | `/api/books/<id>/` | Retrieve a single book | Public |
| POST | `/api/books/create/` | Create a new book | Required |
| PUT/PATCH | `/api/books/<id>/update/` | Update a book | Required |
| DELETE | `/api/books/<id>/delete/` | Delete a book | Required |

## Filtering, Searching, and Ordering

### Filtering
Filter books by specific fields:
```
GET /api/books/?title=python
GET /api/books/?author=john
GET /api/books/?publication_year=2020
```

### Searching
Full-text search across title and author name:
```
GET /api/books/?search=django
```

### Ordering
Sort results by title or publication year:
```
GET /api/books/?ordering=title           # Ascending by title
GET /api/books/?ordering=-title          # Descending by title
GET /api/books/?ordering=publication_year
GET /api/books/?ordering=-publication_year
```

### Combined Queries
```
GET /api/books/?author=john&ordering=-publication_year&search=web
```

## Custom Serializers

### BookSerializer
- Serializes all Book model fields
- Includes custom validation to ensure `publication_year` is not in the future

### AuthorSerializer
- Includes nested BookSerializer for related books
- Demonstrates handling of one-to-many relationships in serialization

## Permissions

- **ListView & DetailView**: Allow read-only access to all users (authenticated or not)
- **CreateView, UpdateView, DeleteView**: Require authentication

## Running Tests

```bash
python manage.py test api

# For verbose output:
python manage.py test api -v 2
```

### Test Coverage

The test suite covers:
- CRUD operations (Create, Read, Update, Delete)
- Filtering by title, author, and publication_year
- Searching by title and author name
- Ordering by title and publication_year
- Permission enforcement (authenticated vs unauthenticated access)
- Data validation (future publication year)
- Model relationships (Author-Book)

## Views Documentation

### BookListView
- Lists all books with pagination
- Supports filtering, searching, and ordering
- Uses `DjangoFilterBackend`, `SearchFilter`, and `OrderingFilter`

### BookDetailView
- Retrieves a single book by ID
- Returns 404 if book not found

### BookCreateView
- Creates a new book
- Validates publication_year is not in the future
- Returns 201 on success, 400 on validation error

### BookUpdateView
- Supports both PUT (full update) and PATCH (partial update)
- Validates publication_year constraint

### BookDeleteView
- Removes a book from the database
- Returns 204 on success
