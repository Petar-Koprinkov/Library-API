from django.urls import path
from Library_Api.account import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
]