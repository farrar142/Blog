from typing import Optional, TypedDict
from django.http.request import HttpRequest
from rest_framework import serializers, exceptions, status
from rest_framework.request import Request
from blogs.models import Blog, Category, Article, Comment
from common_module.exceptions import ConflictException
from common_module.serializers import (
    BaseSerializer,
    ImageSerializer,
    ImageInjector,
    ResourceOwnerCheck,
    UpdateAvailableFields,
    UserIdInjector,
)

from common_module.utils import Token, MockRequest


class BlogReadOnlySerializer(BaseSerializer):
    class Meta:
        model = Blog
        fields = ("id", "user_id", "title", "description", "images")

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

    @UserIdInjector
    @ImageInjector
    def create(self, validated_data):
        return super().create(validated_data)

    @UserIdInjector
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    @property
    def data(self):
        return BlogReadOnlySerializer(instance=self.instance, context=self.context).data


class CategoryReadOnlySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ("id", "blog", "title", "order")


class CategoryUpsertSerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = ("blog", "title", "order")

    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())

    @ResourceOwnerCheck("blog")
    @UserIdInjector
    def create(self, validated_data):
        user = self.context["request"].user
        if not user:
            raise exceptions.NotAuthenticated
        blog: Blog = validated_data["blog"]
        if blog.user_id != user["user_id"]:
            raise ConflictException(detail={"blog": ["해당 블로그의 소유자가 아닙니다."]})
        return super().create(validated_data)

    @ResourceOwnerCheck("blog")
    @UpdateAvailableFields(fields=["title", "order"])
    def update(self, obj: Article, validated_data: dict):
        return super().update(obj, validated_data)

    @property
    def data(self):
        return CategoryReadOnlySerializer(
            instance=self.instance, context=self.context
        ).data


class ArticleReadOnlySerializer(BaseSerializer):
    class Meta:
        model = Article
        fields = ("id", "blog", "category", "title", "content", "is_saved")


class ArticleUpsertSerializer(BaseSerializer):
    class Meta:
        model = Article
        fields = ("blog", "category", "title", "content", "is_saved")

    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    @ResourceOwnerCheck("blog")
    @UserIdInjector
    def create(self, validated_data):
        return super().create(validated_data)

    @ResourceOwnerCheck("blog")
    @UpdateAvailableFields(fields=["title", "content", "is_saved"])
    def update(self, obj: Article, validated_data: dict):
        return super().update(obj, validated_data)

    @property
    def data(self):
        return ArticleReadOnlySerializer(
            instance=self.instance, context=self.context
        ).data
