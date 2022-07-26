from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import UserCreateSerializer, LoginSerializer, UserSerializer, PasswordUpdateSerializer


class SingUpView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        login(self.request, user=serializer.user, backend="django.contrib.auth.backends.ModelBackend",)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, ** kwargs):
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user=user)
        user_serializer = UserSerializer(instance=user)
        return Response(user_serializer.data)


class ProfileView(RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @method_decorator(ensure_csrf_cookie)
    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(UpdateAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordUpdateSerializer

    def get_object(self):
        return self.request.user













