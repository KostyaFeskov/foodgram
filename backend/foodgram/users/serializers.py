import base64

from rest_framework import serializers, status

from django.core.files.base import ContentFile

from rest_framework.authtoken.models import Token

from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class SignUpSerializer(serializers.ModelSerializer):
    """Следит за уникальностью полей email и username,
       и не даёт создать юзера me"""
    email = serializers.EmailField(
        max_length=128, required=True)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=128
    )
    first_name = serializers.CharField(
        max_length=150,
        required=True
    )
    last_name = serializers.CharField(
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                "Имя 'me' для username запрещено."
            )
        return username

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        is_user_exists = User.objects.filter(username=username).exists()
        is_email_exists = User.objects.filter(email=email).exists()
        if is_user_exists:
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError(
                    {"detail": "Неверно указан email пользователя"},
                    status.HTTP_400_BAD_REQUEST,
                )
        if is_email_exists:
            user = User.objects.get(email=email)
            if user.username != username:
                raise serializers.ValidationError(
                    {"detail": "Пользователь с таким email уже существует"},
                    status.HTTP_400_BAD_REQUEST,
                )
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class TokenSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'password',
            'email',
        )
        

class UserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'avatar',)
        model = User



class AvatarEditSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('avatar',)


class ChangePasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField()
    current_password = serializers.CharField()
