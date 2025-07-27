# Delete Operation
```python
from bookshelf.models import Book

book.delete()

# (1, {'bookshelf.Book': 1})

# Confirm Deletion

Book.objects.all()

<QuerySet []>
