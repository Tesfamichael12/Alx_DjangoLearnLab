from django.contrib import admin

# Register your models here.

from .models import Author, Book

# Register Author and Book models in Django Admin
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'publication_year')  # Display publication_year in list
  fields = ('title', 'author', 'publication_year')  # Fields to be filled in admin form

admin.site.register(Author)
admin.site.register(Book)
