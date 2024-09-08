from rest_framework import serializers

from rest_framework.reverse import reverse

from urlshortener.models import LinkShortener


class UrlShortenerSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinkShortener
        fields = ('url_original',)
        write_only_fields = ('url_original',)

    def get_short_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('urlshortener:url_load', args=[obj.url_hash])
        )

    def create(self, validated_data):
        instance, _ = LinkShortener.objects.get_or_create(**validated_data)
        return instance

    def to_representation(self, instance):
        return {'short-link': self.get_short_link(instance)}
