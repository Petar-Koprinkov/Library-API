from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from Library_Api.library.models import Book


class BookDetailApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="petarkoprinkov", password="petarkoprinkovpassword")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.access_token}"}

        self.book = Book.objects.create(
            title="Under the Yoke",
            author="Ivan Vazov",
            publicationDate="1893-01-01",
            genre="Historic novel",
            isbn="123546879"
        )

        self.valid_payload = {
            "title": "Updated Under the Yoke",
            "author": "Petar Koprinkov",
            "publicationDate": "2025-02-17",
            "genre": "Modern novel",
            "isbn": "123456786"
        }
        self.partial_payload = {"title": "Partially Updated Under the Yoke"}
        self.invalid_payload = {"title": ""}

    def test_unauthenticated_user_cannot_access_book(self):
        response = self.client.get(reverse("books-list", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_get_book(self):
        response = self.client.get(reverse("books-list", args=[self.book.id]), **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_authenticated_user_can_update_book(self):
        response = self.client.put(reverse("books-list", args=[self.book.id]), data=self.valid_payload, format="json",
                                   **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Under the Yoke")

    def test_authenticated_user_can_partially_update_book(self):
        response = self.client.patch(reverse("books-list", args=[self.book.id]), data=self.partial_payload,
                                     format="json", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Partially Updated Under the Yoke")

    def test_authenticated_user_cannot_update_book_with_invalid_data(self):
        response = self.client.put(reverse("books-list", args=[self.book.id]), data=self.invalid_payload, format="json",
                                   **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_can_delete_book(self):
        response = self.client.delete(reverse("books-list", args=[self.book.id]), **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
