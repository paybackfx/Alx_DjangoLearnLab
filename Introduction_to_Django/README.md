# LibraryProject

A Django project for managing a library of books.

## Project Structure

- **LibraryProject/**: Django project settings and configuration
- **bookshelf/**: Django app containing the Book model

## Setup

1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install Django: `pip install django`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## Features

- Book model with title, author, and publication_year
- Django admin interface for managing books
- CRUD operations via Django ORM
