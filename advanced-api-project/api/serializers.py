from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# BookSerializer handles book serialization and includes custom validation for publication year

class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = ['title', 'publication_year', 'author']

  def validate_publication_year(self, value):
    if value > datetime.now().year:
      raise serializers.ValidationError(
    'Publication year cannot be in the future.'
  )
    return value

# AuthorSerializer includes a nested BookSerializer to serialize related books dynamically

class AuthorSerializer(serializers.ModelSerializer):
  books = BookSerializer(many=True, read_only=True)

  class Meta:
    model = Author
    fields = ['name', 'books']
