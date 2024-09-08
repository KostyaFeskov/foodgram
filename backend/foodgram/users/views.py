from rest_framework import status

from djoser.views import UserViewSet as DjUV
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.serializers import (
    UserMeSerializer,
    AvatarSerializer
)
from subscribe.serializers import (
    UserSubscriptionCreationSerializer,
    UserSubscriptionDeleteSerializer,
    UserSubscriptionSerializer
)

from subscribe.models import Subsribe


class UserViewSet(DjUV):

    def get_serializer_class(self):
        if self.action == 'subscriptions':
            return UserSubscriptionSerializer
        elif self.action == 'subscribe':
            return UserSubscriptionCreationSerializer
        elif self.action == 'delete_subscribe':
            return UserSubscriptionDeleteSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == 'subscriptions':
            queryset = self.request.user.subscriber.all()
            return [sub.subscription for sub in queryset]
        return super().get_queryset()

    @action(
        ['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        return super().list(request)

    @action(
        ['post'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path=r'(?P<id>\d+)/subscribe'
    )
    def subscribe(self, request, id):

        sub_user = self.get_object()
        serializer = self.get_serializer(
            instance=sub_user,
            data={'id': id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Subsribe.objects.create(
            user=request.user,
            subscription=sub_user
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):

        sub_user = self.get_object()
        serializer = self.get_serializer(
            instance=sub_user,
            data={'id': id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        Subsribe.objects.filter(
            user=request.user,
            subscription=sub_user
        ).delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=('get',),
        detail=False,
        pagination_class=None,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):

        serializer = UserMeSerializer(
            request.user,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=('put',),
        detail=False,
        url_path='me/avatar',
        permission_classes=(IsAuthenticated,),
    )
    def avatar_add(self, request):
        serializer = AvatarSerializer(
            instance=self.get_instance(), data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @avatar_add.mapping.delete
    def avatar_delete(self, request):
        user = self.get_instance()
        if user.avatar:
            user.avatar.delete()
            user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
