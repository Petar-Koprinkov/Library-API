from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from Library_Api.account.serializers import UserSerializer

UserModel = get_user_model()


class RegisterView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


