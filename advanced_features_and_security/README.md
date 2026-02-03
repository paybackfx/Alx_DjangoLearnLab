# Advanced Features and Security - LibraryProject

This Django project demonstrates advanced security features and custom user models.

## Project Structure

```
LibraryProject/
├── LibraryProject/           # Project settings
│   ├── settings.py           # Security configurations
│   ├── urls.py
│   └── wsgi.py
├── relationship_app/         # Main application
│   ├── models.py             # CustomUser, Book with permissions
│   ├── views.py              # Permission-protected views
│   ├── admin.py              # CustomUser admin
│   └── forms.py              # Secure forms
├── bookshelf/                # Bookshelf templates
│   └── templates/
└── manage.py
```

---

## Custom User Model

### Overview
The `CustomUser` model extends Django's `AbstractUser` with additional fields:
- `date_of_birth`: DateField for user's date of birth
- `profile_photo`: ImageField for user's profile photo

### Configuration
In `settings.py`:
```python
AUTH_USER_MODEL = 'relationship_app.CustomUser'
```

---

## Permissions and Groups

### Custom Permissions
The `Book` model includes the following custom permissions defined in `Meta.permissions`:
- `can_view`: Permission to view book entries
- `can_create`: Permission to create book entries
- `can_edit`: Permission to edit book entries
- `can_delete`: Permission to delete book entries

### Groups Setup
Create the following groups via Django Admin:

1. **Viewers**
   - Permissions: `can_view`
   
2. **Editors**
   - Permissions: `can_view`, `can_create`, `can_edit`
   
3. **Admins**
   - Permissions: `can_view`, `can_create`, `can_edit`, `can_delete`

### Permission Decorators
Views are protected using `@permission_required`:
```python
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    ...
```

---

## Security Best Practices

### Settings Configuration

#### HTTPS Settings
```python
SECURE_SSL_REDIRECT = True            # Redirect HTTP to HTTPS
SECURE_HSTS_SECONDS = 31536000        # HSTS for 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True # Include subdomains
SECURE_HSTS_PRELOAD = True            # Allow HSTS preloading
```

#### Cookie Security
```python
SESSION_COOKIE_SECURE = True          # Session cookies HTTPS only
CSRF_COOKIE_SECURE = True             # CSRF cookies HTTPS only
```

#### Browser Security Headers
```python
SECURE_BROWSER_XSS_FILTER = True      # XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True    # Prevent MIME-sniffing
X_FRAME_OPTIONS = 'DENY'              # Clickjacking protection
```

#### Content Security Policy (CSP)
```python
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
```

### CSRF Protection
All forms include CSRF tokens:
```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

### SQL Injection Prevention
All database queries use Django ORM:
```python
# Safe - parameterized query
books = Book.objects.filter(title__icontains=search_term)

# NEVER use raw SQL with string formatting
```

### XSS Prevention
Django templates auto-escape all output:
```html
<!-- Safe - automatically escaped -->
{{ user_input }}
```

---

## Testing Permissions

1. Create test users via Django Admin
2. Assign users to groups (Viewers, Editors, Admins)
3. Log in as each user
4. Verify:
   - Viewers can only view books
   - Editors can view, create, edit
   - Admins have full access

---

## Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set unique `SECRET_KEY`
- [ ] Enable HTTPS on web server
- [ ] Configure SSL certificates
- [ ] Run `python manage.py check --deploy`
