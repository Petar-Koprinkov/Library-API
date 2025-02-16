from django.contrib.auth import get_user_model, authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from Library_Api.account.serializers import UserSerializer, LoginRequestSerializer, LoginResponseSerializer

UserModel = get_user_model()


@extend_schema(
    tags=['Authentication'],
    summary="Register endpoint",
    description="Register yourself.",
    request=UserSerializer,
    responses={200: UserSerializer, 400: 'Invalid username, password or email.'},
)
class RegisterView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=['Authentication'],
    summary="Login endpoint",
    description="Authenticate a user and get back access and refresh tokens.",
    request=LoginRequestSerializer,
    responses={
        200: LoginResponseSerializer,
        401: "Invalid username or password"
    }
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response({
                "error": "Invalid username or password",
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Login successful",
        }, status=status.HTTP_200_OK)
