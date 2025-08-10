from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author
from django.contrib.auth import get_user_model

# Custom user model
User = get_user_model()


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a user with a username, email, and password
        self.user = User.objects.create_user(
            username="testuser", 
            email="testuser@example.com", 
            password="testpass123"
        )
        self.author = Author.objects.create(name="Author 1")

        # Create some books
        self.book1 = Book.objects.create(
            title="Book 1", author=self.author, publication_year=2000
        )
        self.book2 = Book.objects.create(
            title="Book 2", author=self.author, publication_year=2020
        )

        # Authentication for creating and updating books
        self.client.login(username="testuser", password="testpass123")

    def test_get_all_books(self):
        url = reverse("book-list")  # Assuming 'book-list' is the URL name for the ListView
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book 1")

    def test_create_book(self):
        url = reverse("book-list")
        data = {"title": "Book 3", "author": self.author.id, "publication_year": 2021}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.id})
        data = {
            "title": "Updated Book 1",
            "author": self.author.id,
            "publication_year": 2001,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book 1")

    def test_delete_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # Testing filtering
    def test_filter_books_by_title(self):
        url = reverse("book-list") + "?title=Book 1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book 1")

    # Testing searching
    def test_search_books_by_title(self):
        url = reverse("book-list") + "?search=Book"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Testing ordering
    def test_order_books_by_publication_year(self):
        url = reverse("book-list") + "?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Book 1")  # Oldest book first
