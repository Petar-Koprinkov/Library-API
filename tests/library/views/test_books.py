from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from Library_Api.library.models import Book


class BooksApiViewTest(TestCase):
    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_user(username="petarkoprinkov", password="petarkoprinkovpassword")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.access_token}"}

        self.book1 = Book.objects.create(
            title="Under the Yoke",
            author="Ivan Vazov",
            publicationDate="1981-01-01",
            genre="Programming",
            isbn="123456789"
        )
        self.book2 = Book.objects.create(
            title="Under the Yoke 2",
            author="Ivan Vazov",
            publicationDate="1983-06-15",
            genre="Programming",
            isbn="123456789"
        )

        self.valid_payload = {
            "title": "New Book",
            "author": "Petar Koprinkov",
            "publicationDate": "2023-05-10",
            "genre": "Technology",
            "isbn": "123456789"
        }
        self.invalid_payload = {
            "title": "",
            "author": "Petar Koprinkov",
            "publicationDate": "2023-05-10",
            "genre": "Technology",
            "isbn": "123456789"
        }

    def test_unauthenticated_user_cannot_access_books(self):
        response = self.client.get(reverse("books-api"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_get_books(self):
        response = self.client.get(reverse("books-api"), **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_authenticated_user_can_create_book(self):
        response = self.client.post(reverse("books-api"), data=self.valid_payload, format="json", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "New Book")

    def test_authenticated_user_cannot_create_invalid_book(self):
        response = self.client.post(reverse("books-api"), data=self.invalid_payload, format="json", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 2)
