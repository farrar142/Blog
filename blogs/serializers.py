from typing import Optional, TypedDict
from django.http.request import HttpRequest
from rest_framework import serializers, exceptions, status
from rest_framework.request import Request
from blogs.models import Blog, Category, Article, Comment
from common_module.serializers import (
    BaseSerializer,
    ImageSerializer,
    ImageInjector,
    UserIdInjector,
)

from common_module.utils import Token, MockRequest


class BlogReadOnlySerializer(BaseSerializer):
    class Meta:
        model = Blog
        fields = ("user_id", "title", "description", "images")

    images = ImageSerializer(many=True)

    def create(self, validated_data):
        raise exceptions.NotAcceptable

    def update(self, instance, validated_data):
        raise exceptions.NotAcceptable


class BlogUpsertSerializer(BaseSerializer):
    class Meta:
        model = Blog
        fields = ("title", "description", "image")

    image = serializers.FileField(required=False)

    @ImageInjector
    @UserIdInjector
    def create(self, validated_data):
        return super().create(validated_data)

    @property
    def data(self):
        return BlogReadOnlySerializer(instance=self.instance, context=self.context).data
