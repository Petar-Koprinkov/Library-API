from django.urls import path, include

from Library_Api.library import views

urlpatterns = [
    path('book_api/', include([
        path('', views.BooksApiView.as_view(), name='books-api'),
        path('<int:pk>/', views.BookListAPIViewSet.as_view(), name='books-list'),
    ])),
]