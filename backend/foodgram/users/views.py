from django.shortcuts import get_object_or_404

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate

from rest_framework import viewsets, status, mixins
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
    UserSerializer, SubscribeSerializer
)

from users.models import User, Subsribe

from .utils import generate_confirmation_code, send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('email', 'username',)
    lookup_field = 'id'
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'put']
    ALLOWED_HTTP_METHODS = ('get', 'post', 'put', 'delete')

    @action(
        methods=('post',),
        detail=False,
        url_path='set_password',
        permission_classes=(IsAuthenticated,)
    )
    def change_password(self, request):
        user = User.objects.get(username=request.user)
        if "current_password" in request.data and \
                user.check_password(request.data["current_password"]) and \
                "new_password" in request.data:
            user.set_password(request.data["new_password"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(
        methods=('put', 'delete',),
        detail=False,
        url_path='me/avatar',
        permission_classes=(IsAuthenticated,)
    )
    def avatar(self, request):
        user = request.user
        serializer = UserSerializer(
            user,
            partial=True,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        if self.request.method == 'DELETE':
            user.avatar.delete(save=True)
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer.save()
        return Response(
            {"avatar": request.build_absolute_uri(user.avatar.url)},
            status=status.HTTP_200_OK
        )

    @action(
        methods=('get', 'patch',),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(
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
        user = User.objects.get(email=request.data['email'])
        if serializer.is_valid():
            response = {
                "Неправильный email или пароль"
            }
            if User.objects.filter(email=request.data['email']).exists() and \
                    user.check_password(request.data["password"]):
                user = User.objects.get(email=request.data['email'])
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'auth_token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            username = serializer.data.get("username")
            email = serializer.data.get("email")
            first_name = serializer.data.get("first_name")
            last_name = serializer.data.get("last_name")
            user, created = User.objects.get_or_create(
                username=username, email=email,
                first_name=first_name, last_name=last_name,
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


class SubscribeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):

    queryset = Subsribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    # filter_backends = (filters.SearchFilter,)
    search_fields = ('subsribtion__username', 'user__username')

    def get_queryset(self):
        return self.request.user.subscriber.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)