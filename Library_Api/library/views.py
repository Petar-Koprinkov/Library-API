from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Library_Api.library.models import Book
from Library_Api.library.serializers import BookSerializer


@extend_schema(
    tags=["Books"],
    summary="Books management",
    description="Can get and create books",
    request=BookSerializer,
    responses={200: BookSerializer, 400: BookSerializer},
)
class BooksApiView(APIView):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Book"],
    summary="Book management",
    description="Can get, edit, partially edit and delete current book",
    request=BookSerializer,
    responses={200: BookSerializer, 400: BookSerializer},
)
class BookListAPIViewSet(APIView):

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Book, pk=pk)

    @staticmethod
    def valid_serializer(serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk: int):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk: int):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)

        return self.valid_serializer(serializer)

    def patch(self, request, pk: int):
        book = self.get_object(pk)
        serializer = BookSerializer(book, request.data, partial=True)

        return self.valid_serializer(serializer)

    def delete(self, request, pk: int):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

