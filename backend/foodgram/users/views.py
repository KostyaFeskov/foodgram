from django.shortcuts import get_object_or_404

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token


from users.permissions import IsAdmin
from users.serializers import (
    SignUpSerializer, TokenSerializer,
    UserSerializer, UserEditSerializer
)

from users.models import User

from .utils import generate_confirmation_code, send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('email', 'username',)
    lookup_field = 'id'
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    # @action(
    #     methods=('put', 'delete',),
    #     detail=False,
    #     url_path='me/avatar',
    #     permission_classes=(IsAuthenticated,)
    # )
    # def avatar(self, request):
    #     serializer = UserEditSerializer(
    #         request.user,
    #         partial=True,
    #         data=request.data
    #     )
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=('get', 'patch',),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserEditSerializer(
            request.user,
            partial=True,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        if self.request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    

class TokenView(APIView):
    def post(self, request, *args, **kargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "email": {
                    "detail": "Такого пользователя не существует!"
                }
            }
            if User.objects.filter(email=request.data['email']).exists():
                user = User.objects.get(email=request.data['email'])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'auth_token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):
    """Регистрирует пользователя и отправляет ему код подтверждения."""

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")
        password = serializer.validated_data.get("password")
        user, created = User.objects.get_or_create(
            username=username, email=email,
            first_name=first_name, last_name=last_name,
            password=password
        )

        return Response(
            {
                "email": user.email,
                "id": user.pk,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        auth_token = Token.objects.get(user=request.user)
        auth_token.delete()
        return Response({"detail": "До встречи!"}, status=status.HTTP_200_OK)