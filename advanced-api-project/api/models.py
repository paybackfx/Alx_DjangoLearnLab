"""
Models for the API application.

This module defines the data models for the book management system.
It establishes a one-to-many relationship between Author and Book models,
where one author can have multiple books.
"""

from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.
    
    Attributes:
        name (str): The full name of the author.
    
    Relationships:
        - Has a one-to-many relationship with Book model (one author can write many books).
        - Related books can be accessed via the 'books' reverse relation.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model representing a published book.
    
    Attributes:
        title (str): The title of the book.
        publication_year (int): The year the book was published.
        author (ForeignKey): Reference to the Author who wrote the book.
    
    Relationships:
        - Belongs to one Author (many-to-one relationship).
        - The author relationship uses CASCADE deletion, meaning if an author
          is deleted, all their books are also deleted.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.title
