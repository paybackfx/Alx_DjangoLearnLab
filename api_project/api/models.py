"""
Models for the api application.
"""

from django.db import models


class Book(models.Model):
    """
    Book model for the API.
    Contains title and author fields.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title
