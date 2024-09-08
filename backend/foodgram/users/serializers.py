import base64

from rest_framework import serializers

from django.core.files.base import ContentFile

from django.contrib.auth import get_user_model
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import MaxLengthValidator
from djoser.serializers import UserCreateSerializer

from subscribe.models import Subsribe


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


User = get_user_model()


class UserSerializer(UserCreateSerializer):
    username = serializers.CharField(
        validators=[ASCIIUsernameValidator(), MaxLengthValidator(150)]
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'username',
            'first_name',
            'last_name',
        )


class UserMeSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'avatar',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        if user.is_anonymous or user == obj:
            return False
        return Subsribe.objects.filter(user=user, subscription=obj).exists()


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ('avatar',)
