from django.test import TestCase
from Library_Api.library.models import Book


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Django for Beginners",
            author="William S. Vincent",
            publicationDate="2022-01-01",
            genre="Programming",
            isbn="978-1735467221"
        )

    def test_book_creation(self):
        book = Book.objects.get(title="Django for Beginners")
        self.assertEqual(book.author, "William S. Vincent")
        self.assertEqual(book.genre, "Programming")
        self.assertEqual(book.isbn, "978-1735467221")

    def test_title_max_length(self):
        max_length = self.book._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_author_max_length(self):
        max_length = self.book._meta.get_field("author").max_length
        self.assertEqual(max_length, 100)

    def test_genre_max_length(self):
        max_length = self.book._meta.get_field("genre").max_length
        self.assertEqual(max_length, 100)

    def test_isbn_max_length(self):
        max_length = self.book._meta.get_field("isbn").max_length
        self.assertEqual(max_length, 100)

